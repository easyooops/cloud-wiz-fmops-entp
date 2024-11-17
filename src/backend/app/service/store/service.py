import logging
import tempfile

from aiohttp import ClientError
import boto3
import os
from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi import HTTPException, UploadFile
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from sqlmodel import Session, desc, select
from app.service.store.model import Store
from app.api.v1.schemas.store import StoreCreate, StoreUpdate, Vector
from app.core.provider.aws.s3 import S3Service
import pandas as pd
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, Docx2txtLoader
from langchain_core.documents import Document

from app.service.credential.model import Credential
from app.service.credential.service import CredentialService
from app.components.VectorStore.Chroma import ChromaVectorStoreComponent
from app.components.VectorStore.Faiss import FaissVectorStoreComponent
from app.components.VectorStore.Pinecone import PineconeVectorStoreComponent
from app.service.provider.model import Provider
from app.components.Embedding.Bedrock import BedrockEmbeddingComponent
from app.components.Embedding.OpenAI import OpenAIEmbeddingComponent
from app.service.model.model import Model
from app.components.DocumentLoader.Snowflake import SnowflakeDocumentLoader
from app.components.DocumentLoader.DocumentLoader import DocumentLoaderComponent
from app.components.Embedding.GoogleAI import GoogleEmbeddingComponent

class StoreService():
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.credential_service = CredentialService(session)
        self.document_loader_component = DocumentLoaderComponent()        
        self.store_bucket = os.getenv("AWS_S3_BUCKET_STORE_NAME")

    def get_all_stores(self, user_id: Optional[UUID] = None, store_id: Optional[UUID] = None):
        try:
            statement = select(Store)
            if user_id:
                statement = statement.where(Store.user_id == user_id)
            if store_id:
                statement = statement.where(Store.store_id == store_id)

            statement = statement.order_by(desc(Store.store_id))

            return self.session.execute(statement).scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error retrieving stores")

    def get_store_directory_info(self, user_id: UUID, directory_name: str, credential_id: UUID):
        try:
            full_directory_name = f"{user_id}/{directory_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=credential_id)
            if storage_service:
                return storage_service.get_directory_info(full_directory_name)
            else:
                print("Failed to initialize storage service")
                return {'total_size': 0, 'file_count': 0}
        except Exception as e:
            print(f"Error while retrieving directory info: {e}")
            return {'total_size': 0, 'file_count': 0}

    def create_store(self, store_data: StoreCreate, user_id: UUID):
        try:
            new_store = Store(**store_data.model_dump())
            self.session.add(new_store)
            self.session.commit()
            self.session.refresh(new_store)
            full_directory_name = f"{user_id}/{new_store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=new_store.credential_id)
            if storage_service:
                storage_service.retry(lambda: storage_service.create_directory(full_directory_name))
            else:
                print("Failed to initialize storage service")
            return new_store

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating store: {str(e)}")

    def update_store(self, store_id: UUID, store_update: StoreUpdate, user_id: UUID):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            for key, value in store_update.model_dump(exclude_unset=True).items():
                setattr(store, key, value)
            self.session.add(store)
            self.session.commit()
            self.session.refresh(store)
            return store
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating store: {str(e)}")

    def delete_store(self, store_id: UUID, user_id: UUID):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            self.session.delete(store)
            self.session.commit()
            full_directory_name = f"{user_id}/{store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = self.get_provider_info(store.credential_id)

            if provider_key == "AS":
                storage_service.delete_directory(full_directory_name)
            else:
                try:
                    store_folder_id = storage_service.get_folder_hierarchy_id(full_directory_name)
                    storage_service.delete_directory(store_folder_id)
                except FileNotFoundError:
                    logging.error(f"No folder found with the name: {full_directory_name}")
                    raise HTTPException(status_code=404, detail=f"No folder found with the name: {full_directory_name}")
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error deleting store: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting store: {str(e)}")

    def list_files(self, user_id: UUID, store_id: UUID) -> List[Dict[str, Any]]:
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            full_directory_name = f"{user_id}/{store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                return []

            provider_key = self.get_provider_info(store.credential_id)

            if provider_key == "AS":
                objects = storage_service.list_all_objects(full_directory_name)
            else:
                parts = full_directory_name.split('/')
                parent_id = None
                for part in parts:
                    try:
                        parent_id = storage_service.get_folder_id_by_name(part)
                    except FileNotFoundError:
                        parent_id = storage_service.create_directory(part, parent_id)['id']
                objects = storage_service.list_files_in_folder(parent_id)

            files = []
            if provider_key == "AS":
                for obj in objects:
                    file_info = {
                        "Key": obj["Key"],
                        "LastModified": obj["LastModified"],
                        "Size": obj["Size"],
                    }
                    files.append(file_info)
            else:
                for obj in objects:
                    file_info = {
                        "Key": obj["name"],
                        "LastModified": obj.get("modifiedTime", ""),
                        "Size": obj.get("size", 0),
                    }
                    files.append(file_info)

            logging.info(f"Files: {files}")
            return files
        except Exception as e:
            logging.error(f"Error listing files: {str(e)}")
            return []

    def upload_file_to_store(self, user_id: UUID, store_id: UUID, file: UploadFile):
        tmp_path = None
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            folder_name = f"{user_id}/{store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = self.get_provider_info(store.credential_id)

            if provider_key == "AS":
                file_location = f"{folder_name}/{file.filename}"
                storage_service.upload_file(file.file, file_location)
            else:
                parts = folder_name.split('/')
                parent_id = None
                for part in parts:
                    try:
                        parent_id = storage_service.get_folder_id_by_name(part)
                    except FileNotFoundError:
                        parent_id = storage_service.create_directory(part, parent_id)['id']

                storage_service.upload_file_to_folder(parent_id, file)
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def delete_file_from_store(self, user_id: UUID, store_id: UUID, file_name: str):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")

            full_directory_name = f"{user_id}/{store.store_name}"
            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = self.get_provider_info(store.credential_id)

            if provider_key == "AS":
                file_location = f"{full_directory_name}/{file_name}"
                storage_service.delete_file(file_location)
            else:
                parts = full_directory_name.split('/')
                parent_id = None
                for part in parts:
                    try:
                        parent_id = storage_service.get_folder_id_by_name(part)
                    except FileNotFoundError:
                        parent_id = storage_service.create_directory(part, parent_id)['id']
                try:
                    file_id = storage_service.get_file_id_by_name(parent_id, file_name)
                except FileNotFoundError:
                    logging.error(f"No file found with the name: {file_name} in folder: {full_directory_name}")
                    raise HTTPException(status_code=404, detail=f"No file found with the name: {file_name} in folder: {full_directory_name}")

                storage_service.delete_file(file_id)
        except Exception as e:
            logging.error(f"Error deleting file from store: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting file from store: {str(e)}")

    def load_documents(self, files: List[str]) -> List[Document]:
        try:
            if not files:
                logging.error("No files provided to load_documents.")
                raise HTTPException(status_code=400, detail="No files provided")

            documents = []
            s3_client = boto3.client('s3')
            bucket_name = os.getenv("AWS_S3_BUCKET_STORE_NAME")
            logging.info(f"Bucket name: {bucket_name}")

            for s3_file_key in files:
                local_file_path = f"/tmp/{s3_file_key.split('/')[-1]}"
                logging.info(f"Downloading file: {s3_file_key} to {local_file_path}")
                s3_client.download_file(bucket_name, s3_file_key, local_file_path)

                if local_file_path.endswith('.txt'):
                    loader = TextLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.pdf'):
                    loader = PyPDFLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.csv'):
                    loader = CSVLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.docx'):
                    loader = Docx2txtLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.xlsx'):
                    xlsx = pd.ExcelFile(local_file_path)
                    for sheet_name in xlsx.sheet_names:
                        df = pd.read_excel(xlsx, sheet_name=sheet_name)
                        full_text = df.to_string(index=False)
                        documents.append(Document(page_content=full_text, metadata={"source": f"{local_file_path} - {sheet_name}"}))
                else:
                    logging.error(f"Unsupported file format: {local_file_path}")
                    raise ValueError(f"Unsupported file format: {local_file_path}")
            logging.info(f"Loaded documents: {documents}")
            return documents
        except Exception as e:
            logging.error(f"Error in load_documents: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def load_documents_v2(self, credential_id: UUID, files: List[str]) -> List[Document]:
        try:
            if not files:
                logging.error("No files provided to load_documents.")
                raise HTTPException(status_code=400, detail="No files provided")

            storage_service = self.credential_service._set_storage_credential(credential_id=credential_id)

            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            documents = []
            for s3_file_key in files:
                local_file_path = f"/tmp/{s3_file_key.split('/')[-1]}"
                logging.info(f"Downloading file: {s3_file_key} to {local_file_path}")

                try:
                    storage_service.download_file(s3_file_key, local_file_path)
                except ClientError as e:
                    logging.error(f"Error downloading file from S3: {str(e)}")
                    raise HTTPException(status_code=500, detail=f"Error downloading file from S3: {str(e)}")

                if local_file_path.endswith('.txt'):
                    loader = TextLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.pdf'):
                    loader = PyPDFLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.csv'):
                    loader = CSVLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.docx'):
                    loader = Docx2txtLoader(local_file_path)
                    documents.extend(loader.load())
                elif local_file_path.endswith('.xlsx'):
                    xlsx = pd.ExcelFile(local_file_path)
                    for sheet_name in xlsx.sheet_names:
                        df = pd.read_excel(xlsx, sheet_name=sheet_name)
                        full_text = df.to_string(index=False)
                        documents.append(Document(page_content=full_text, metadata={"source": f"{local_file_path} - {sheet_name}"}))
                else:
                    logging.error(f"Unsupported file format: {local_file_path}")
                    raise ValueError(f"Unsupported file format: {local_file_path}")
            logging.info(f"Loaded documents: {documents}")
            return documents
        except Exception as e:
            logging.error(f"Error in load_documents: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def load_documents_v3(self, credential_id: UUID, files: List[str]) -> List[Document]:
        """
        로컬 파일 또는 Snowflake에서 문서를 로드하는 메서드.

        :param credential_id: 스토리지 서비스의 자격 증명 ID
        :param files: 로드할 파일의 리스트 (S3, Git, Google Drive 등)
        :param snowflake_query: Snowflake에서 데이터를 로드하기 위한 쿼리
        :return: 로드된 문서들의 리스트
        """
        try:
            documents = []

            credential_query = (
                select(Credential, Provider)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
            )
            result = self.session.execute(credential_query).first()

            if not result:
                raise ValueError(f"Credential with id {credential_id} and provider type 'S' not found")

            credential, provider = result

            if provider.type == "L":
                loader = self.credential_service._set_document_loader_credential(credential_id=credential_id)
                documents.extend(loader.load())

            elif provider.type == "S":
                storage_service = self.credential_service._set_storage_credential(credential_id=credential_id)

                if not storage_service:
                    logging.error("Failed to initialize storage service")
                    raise HTTPException(status_code=500, detail="Failed to initialize storage service")

                for s3_file_key in files:
                    local_file_path = f"/tmp/{s3_file_key.split('/')[-1]}"
                    logging.info(f"Downloading file: {s3_file_key} to {local_file_path}")

                    try:
                        storage_service.download_file(s3_file_key, local_file_path)
                    except ClientError as e:
                        logging.error(f"Error downloading file from S3: {str(e)}")
                        raise HTTPException(status_code=500, detail=f"Error downloading file from S3: {str(e)}")

                    documents.extend(self.document_loader_component.load_document(local_file_path))
            else:
                logging.error("No valid files or Snowflake query provided to load_documents.")
                raise HTTPException(status_code=400, detail="No valid files or Snowflake query provided")

            logging.info(f"Loaded documents: {documents}")
            return documents
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def create_indexing(self, agent_data: Vector):

        try:
            # 파일 목록을 가져옴
            file_keys = []
            if agent_data.storage_object_id:
                files = self.list_files(agent_data.user_id, agent_data.storage_object_id)
                file_keys = [file["Key"] for file in files]

            documents = self.load_documents_v3(agent_data.storage_provider_id, file_keys)

            # 문서를 1000 단위로 청킹
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            # chunked_docs = text_splitter.split_documents(documents)
            chunked_docs = [chunk for chunk in text_splitter.split_documents(documents) if chunk.page_content]

            # # 임베딩 생성
            # embedding_function = OpenAIEmbeddings()
            # embeddings = embedding_function.embed_documents([doc.page_content for doc in chunked_docs])

            # 벡터 스토어 초기화 및 인덱싱
            models = self.session.get(Model, agent_data.embedding_model_id)
            embedding_credential_type = self.get_provider_info(agent_data.embedding_provider_id)
            embed_component = self._initialize_embedding_component(embedding_credential_type, agent_data)

            vector_store_type = self.get_provider_info(agent_data.vector_db_provider_id)
            if vector_store_type == "FS":
                # vector_store = FaissVectorStoreComponent(storage_service=storage_service, embedding_function=embedding_function)
                # vector_store.initialize(dimension=1536)
                # vector_store.add_embeddings(embeddings, chunked_docs)  # 문서 추가
                # index_file_path = f"/tmp/faiss_index_{store_id}.index"
                # storage_location = f"{user_id}/faiss_indexes/faiss_index_{store_id}.index"
                # vector_store.save_index(index_file_path, storage_location)
                pass

            elif vector_store_type == "CM":

                embed_component.build(models.model_name)

                persist_directory = f"./chroma_db/{agent_data.storage_provider_id}"
                vector_store = ChromaVectorStoreComponent()
                vector_store.initialize(docs=chunked_docs, embedding_function=embed_component.model_instance, persist_directory=persist_directory, index_name=str(agent_data.storage_provider_id))
                # vector_store.save_index()

            elif vector_store_type == "PC":

                dimension = 1536
                if embedding_credential_type == "OA":
                    dimension = 1536
                elif embedding_credential_type == "BR" and models.model_name == "amazon.titan-embed-text-v2:0":
                    dimension = 1024
                elif embedding_credential_type == "GN":
                    dimension = 768

                embed_component.build(models.model_name, dimension)

                pinecone_api_key = self._get_credential_info(agent_data.vector_db_provider_id, "PINECONE_API_KEY")
                environment = self._get_credential_info(agent_data.embedding_provider_id, "AWS_REGION")
                vector_store = PineconeVectorStoreComponent(pinecone_api_key, environment, index_name=str(agent_data.storage_provider_id))
                vector_store.dimension = dimension
                vector_store.initialize(docs=chunked_docs, embedding_function=embed_component.model_instance)

            else:
                raise ValueError(f"Unsupported vector store type: {vector_store_type}")

            return {"status": "success", "message": "Indexing completed successfully."}

        except Exception as e:
            logging.error(f"Error creating indexing: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating indexing: {str(e)}")

    def get_provider_info(self, credential_id: UUID):
        try:
            statement = (
                select(Provider)
                .select_from(Credential)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
            )
            provider = self.session.execute(statement).one_or_none()

            if provider is None:
                raise HTTPException(status_code=404, detail="Store not found")

            return provider[0].pvd_key

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving store: {str(e)}")

    def get_provider(self, credential_id: UUID):
        try:
            statement = (
                select(Provider)
                .select_from(Credential)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
            )
            provider = self.session.execute(statement).one_or_none()

            if provider is None:
                raise HTTPException(status_code=404, detail="Store not found")

            return provider[0]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving store: {str(e)}")
        
    def _initialize_embedding_component(self, embedding_type: str, agent_data):
        """
        Initialize the embedding component based on the embedding type.

        Args:
            embedding_type (str): Type of embedding provider (e.g., "OA" for OpenAI, "BR" for Bedrock).
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.

        Returns:
            Any: The initialized embedding component.

        Raises:
            ValueError: If required credentials are missing.
        """
        if embedding_type == "OA":
            openai_api_key = self._get_credential_info(agent_data.embedding_provider_id, "OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the provider information.")
            return OpenAIEmbeddingComponent(openai_api_key)

        elif embedding_type == "BR":
            aws_access_key = self._get_credential_info(agent_data.embedding_provider_id, "AWS_ACCESS_KEY_ID")
            aws_secret_access_key = self._get_credential_info(agent_data.embedding_provider_id, "AWS_SECRET_ACCESS_KEY")
            aws_region = self._get_credential_info(agent_data.embedding_provider_id, "AWS_REGION")
            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the provider information.")
            return BedrockEmbeddingComponent(aws_access_key, aws_secret_access_key, aws_region)

        elif embedding_type == "GN":
            google_api_key = self._get_credential_info(agent_data.embedding_provider_id, "GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GoogleAI API key is not set in the provider information.")
            return GoogleEmbeddingComponent(google_api_key)
        
        else:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")

    def _get_credential_info(self, credentials_id, key):

        credentials = self.session.get(Credential, credentials_id)
        if not credentials:
            raise HTTPException(status_code=404, detail="Credentials not found")

        if not credentials.inner_used:
            if key == "AWS_ACCESS_KEY_ID":
                return credentials.access_key
            elif key == "AWS_SECRET_ACCESS_KEY":
                return credentials.secret_key
            elif key == "AWS_REGION":
                return os.getenv(key)
            elif key == "OPENAI_API_KEY":
                return credentials.api_key
            elif key == "GOOGLE_API_KEY":
                return credentials.api_key            
            elif key == "PINECONE_API_KEY":
                return credentials.api_key
        else:
            return os.getenv(key)