import asyncio
import datetime
from decimal import Decimal
import json
from langchain_core.documents import Document
from sqlalchemy.orm import aliased
import os
from typing import Dict, List, Optional
import openai
import tiktoken
from fastapi import HTTPException
from langchain_openai import OpenAIEmbeddings
from sqlmodel import Session, select
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from uuid import UUID
import logging
from app.components.Embedding.Bedrock import BedrockEmbeddingComponent
from app.components.Embedding.OpenAI import OpenAIEmbeddingComponent
from app.service.agent.model import Agent
from langchain.chains import RetrievalQA
from app.service.chat.service import ChatService
from app.service.model.model import Model
from app.service.store.model import Store
from app.service.provider.model import Provider
from app.components.LLM.OpenAI import OpenAILLMComponent
from app.components.Chat.OpenAI import ChatOpenAIComponent
from app.components.Chat.Bedrock import ChatBedrockComponent
from app.components.LLM.Bedrock import BedrockLLMComponent
from app.core.util.token import TokenUtilityService
from app.api.v1.schemas.chat import ChatResponse
from app.service.store.service import StoreService
from ddtrace.llmobs.decorators import workflow
from ddtrace.llmobs import LLMObs
from app.core.util.logging import LoggingConfigurator
from app.service.processing.model import Processing
from app.core.util.piimasking import PiiMaskingService
from app.core.util.textNormailization import TextNormalizationService
from app.service.credential.model import Credential
from app.components.VectorStore.Chroma import ChromaVectorStoreComponent
from app.components.VectorStore.Pinecone import PineconeVectorStoreComponent
from app.service.credential.service import CredentialService
from app.components.Chat.GoogleAI import ChatGoogleAIComponent
from app.components.LLM.GoogleAI import GoogleAILLMComponent
from app.components.Embedding.GoogleAI import GoogleEmbeddingComponent


class PromptService:
    def __init__(self, session: Session):
        self.session = session

    @workflow(name="cloudwiz-ai-fmops")
    @LoggingConfigurator.log_method
    def get_prompt(self, agent_id: UUID, query: Optional[str] = None) -> ChatResponse:

        response = []

        try:
            agent_data = self._get_agent_data(agent_id)
            _d_agent = agent_data['Agent']

            # check limit
            _d_credential = agent_data['Credential']
            limit_response = self._check_limit_token(_d_agent, _d_credential)
            if limit_response:
                return limit_response

            # verify                
            self._verify_query(agent_data)

            # get history
            history = self._get_history(agent_id)

            # pre-processing
            if _d_agent.processing_enabled:
                query = self._preprocess_query(agent_data, query)

            # template
            if _d_agent.template_enabled:
                query = self._replace_question(_d_agent.template, query)

            # embedding
            if _d_agent.embedding_enabled:

                # check storage limit
                store_data = agent_data['Store']
                user_id = _d_agent.user_id

                if store_data:
                    storage_limit_response = self._check_storage_limit(user_id, store_data)
                    if storage_limit_response:
                        return storage_limit_response
                        
                try:
                    documents = asyncio.run(self._run_embedding_main(agent_data))
                    rag_response = asyncio.run(self._run_rag_retrieval(agent_data, query, documents))
                    response = rag_response["llm_response"]
                except openai.PermissionDeniedError as e:
                    logging.error(f"Embedding generation permission denied: {str(e)}")
                    raise HTTPException(status_code=403, detail="Embedding generation permission denied")
            else:
                response = self._run_model(agent_data, query, history)

            # post-processing
            if _d_agent.processing_enabled:
                response = self._postprocess_response(agent_data, response)

            # set history
            history = self._set_history(agent_id)

            # tokens, cost
            tokens = self._get_token_counts(agent_id, query, response)

            LLMObs.annotate(
                span=None,
                input_data=query,
                output_data=response,
                tags={"agent_id":str(_d_agent.agent_id),"input_date": str(datetime.datetime),"user_id": str(_d_agent.user_id),"result": "success"}
            )
                
            return ChatResponse(
                        answer=response,
                        tokens=tokens['token_counts'],
                        cost=tokens['total_cost']
                    )

        except Exception as e:
            LLMObs.annotate(
                span=None,
                input_data=query,
                output_data=response,
                tags={"agent_id":str(_d_agent.agent_id),"input_date": str(datetime.datetime),"user_id": str(_d_agent.user_id),"result": "fail","error": e}
            )            
            raise HTTPException(status_code=500, detail=str(e))

    def _get_agent_data(self, agent_id: UUID):
        EmbeddingModel = aliased(Model)
        statement = (
            select(
                Agent, Model, Credential, Provider, Store,
                EmbeddingModel.model_name.label('embedding_model_name'),
                Provider.name.label('embedding_provider_name')
            )
            .join(Model, Agent.fm_model_id == Model.model_id)
            .join(Credential, Agent.fm_provider_id == Credential.credential_id)
            .join(Provider, Credential.provider_id == Provider.provider_id)
            .outerjoin(Store, Agent.storage_object_id == Store.store_id)
            .outerjoin(EmbeddingModel, Agent.embedding_model_id == EmbeddingModel.model_id)
        )
        statement = statement.where(Agent.agent_id == agent_id)

        result = self.session.execute(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Agent not found")

        agent_data, model_data, credential_data, provider_data, store_data, embedding_model_name, embedding_provider_name = result

        return {
            "Agent": agent_data,
            "Model": model_data,
            "Credential": credential_data,
            "Provider": provider_data,
            "Store": store_data,
            "EmbeddingModelName": embedding_model_name,
            "EmbeddingProviderName": embedding_provider_name
        }
    
    def _get_processing_data(self, processing_id: UUID):

        statement = select(Processing).where(Processing.processing_id == processing_id)
        result = self.session.execute(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Agent not found")

        return result
    
    def _check_limit_token(self, _d_agent, _d_credential) -> Optional[ChatResponse]:
        if _d_credential.inner_used:
            if _d_agent.expected_token_count > _d_credential.limit_cnt:
                return ChatResponse(
                        answer="Token usage limits. Please ask your system administrator.",
                        tokens=0,
                        cost=0
                    )
        return None
    
    def _check_storage_limit(self, user_id, store_data) -> Optional[ChatResponse]:

        directory_name = store_data.store_name
        credential_id = store_data.credential_id

        service = StoreService(self.session)
        storage_info = service.get_store_directory_info(user_id, directory_name, credential_id)
        total_size = storage_info.get('total_size', 0)

        credential = self.session.get(Credential, store_data.credential_id)
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found")
        
        if total_size > credential.limit_cnt:
            return ChatResponse(
                answer="Storage size limits exceeded. Please contact your system administrator.",
                tokens=0,
                cost=0
            )
        return None

    def _get_history(self, agent_id: UUID):
        # Logic to retrieve history
        return None

    def _set_history(self, agent_id: UUID):
        # Logic to retrieve history
        return None

    def _verify_query(self, agent_data):
        pass

    def _parse_options(self, data: str) -> Dict[str, bool]:
        options = data.split('|')
        return {option: True for option in options}

    def _convert_list(self, data: str) -> List[str]:
        return data.split('|')

    def _replace_question(self, template: str, question: str) -> str:
        return template.format(question=question)

    def _preprocess_query(self, agent_data, query: str):

        _d_agent = agent_data['Agent']
        pre_processing_id = _d_agent.pre_processing_id
        processing_data = self._get_processing_data(pre_processing_id)[0]

        # pii mask
        if processing_data.pii_masking:
            pii_options = self._parse_options(processing_data.pii_masking)
            pii_masking_service = PiiMaskingService()
            query = pii_masking_service.mask_pii(query, pii_options)

        # normalize text
        if processing_data.normalization:
            normalize_options = self._parse_options(processing_data.normalization)
            text_normalization_service = TextNormalizationService()
            query = text_normalization_service.normalize_text(query, normalize_options)

        # stopword removal
        if processing_data.stopword_removal:
            stopwords = set(self._convert_list(processing_data.stopword_removal))
            for stopword in stopwords:
                query = query.replace(stopword, '')

        return query

    def split_text_into_chunks(self, text, max_tokens, model_name='cl100k_base'):
        try:
            encoding = tiktoken.get_encoding(model_name)
        except KeyError:
            logging.warning(f"Warning: model {model_name} not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens = encoding.encode(text)

        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i + max_tokens]
            chunks.append(encoding.decode(chunk_tokens))
        return chunks

    async def _run_embedding_main(self, agent_data):
        agent = agent_data['Agent']

        store_service = StoreService(self.session)

        vector_store_type = store_service.get_provider_info(agent.vector_db_provider_id)
        if vector_store_type == "FS":
            return await self._run_embedding_faiss(agent_data)
        elif vector_store_type == "CM":
            return await self._run_embedding_chroma(agent_data)
        elif vector_store_type == "PC":
            return await self._run_embedding_pinecone(agent_data)
        else:
            return await self._run_embedding_faiss(agent_data)    
            
    async def _run_embedding_faiss(self, agent_data):
        """
        Run the embedding process using FAISS.
        
        Args:
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The FAISS engine or an error message.
        """
        store_service = StoreService(self.session)

        try:
            agents_store = agent_data['Agent']
            embedding_model_name = agent_data['EmbeddingModelName']

            # Load Object
            storage_store = agent_data['Store']
            files = None
            if storage_store:
                file_metadata_list = store_service.list_files(storage_store.user_id, storage_store.store_id)
                files = [file_metadata['Key'] for file_metadata in file_metadata_list]

            # Load Document
            documents = store_service.load_documents_v3(agents_store.storage_provider_id, files)

            # Make Chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            chunks = [chunk for chunk in text_splitter.split_documents(documents) if chunk.page_content]

            # Credential Type
            embedding_type = store_service.get_provider_info(agents_store.embedding_provider_id)
            embed_component = self._initialize_embedding_component(embedding_type, agent_data)

            embed_component.build(embedding_model_name)
            embeddings = await embed_component.run_embed_documents([chunk.page_content for chunk in chunks])

            logging.info(f"Number of chunks: {len(chunks)}")
            logging.info(f"Number of embeddings: {len(embeddings)}")
            logging.info(f"Sample chunk content: {chunks[0].page_content if chunks else 'No chunks'}")
            logging.info(f"Sample embedding: {embeddings[0] if embeddings else 'No embeddings'}")

            docs_with_embeddings = [
                Document(page_content=chunk.page_content, metadata={"embedding": embedding})
                for chunk, embedding in zip(chunks, embeddings)
            ]

            engine = await FAISS.afrom_documents(docs_with_embeddings, embed_component.model_instance)

            return engine
        
        except IndexError as e:
            logging.error(f"IndexError occurred during the FAISS embedding process: {e}")
            logging.error(f"Chunks: {len(chunks)}, Embeddings: {len(embeddings)}")
            return f"IndexError occurred: {e}"
        except Exception as e:
            logging.error(f"An unexpected error occurred during the FAISS embedding process: {e}")
            return f"An unexpected error occurred: {e}"

    async def _run_embedding_faiss_backup(self, agent_data):
        """
        Run the embedding process using FAISS.
        
        Args:
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The FAISS engine or an error message.
        """
        store_service = StoreService(self.session)

        try:
            agents_store = agent_data['Agent']
            embedding_model_name = agent_data['EmbeddingModelName']

            # Load Object
            storage_store = agent_data['Store']
            files = None
            if storage_store:
                file_metadata_list = store_service.list_files(storage_store.user_id, storage_store.store_id)
                files = [file_metadata['Key'] for file_metadata in file_metadata_list]

            # Load Document
            documents = store_service.load_documents_v3(agents_store.storage_provider_id, files)

            # Make Chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            chunks = text_splitter.split_documents(documents)

            # Credential Type
            embedding_type = store_service.get_provider_info(agents_store.embedding_provider_id)
            embed_component = self._initialize_embedding_component(embedding_type, agent_data)

            embed_component.build(embedding_model_name)
            embeddings = await embed_component.run_embed_documents([doc.page_content for doc in chunks])
            docs_with_embeddings = [
                Document(page_content=doc.page_content, metadata={"embedding": embedding})
                for doc, embedding in zip(documents, embeddings)
            ]
            engine = await FAISS.afrom_documents(docs_with_embeddings, embed_component.model_instance)

            return engine
        except Exception as e:
            logging.error(f"An error occurred during the FAISS embedding process: {e}")
            return f"An error occurred: {e}"
        
    async def _run_embedding_chroma(self, agent_data):
        """
        Load the Chroma engine for querying.
        
        Args:
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The Chroma engine or an error message.
        """    
        store_service = StoreService(self.session)
        credential_service = CredentialService(self.session)

        try:            
            agents_store = agent_data['Agent']
            embedding_model_name = agent_data['EmbeddingModelName']

            embedding_type = store_service.get_provider_info(agents_store.embedding_provider_id)
            embed_component = self._initialize_embedding_component(embedding_type, agent_data)
            embed_component.build(embedding_model_name)

            persist_directory = f"./chroma_db/{agents_store.storage_provider_id}"

            chroma_component = ChromaVectorStoreComponent()
            chroma_component.embedding_function = embed_component.model_instance

            chroma_component.load_index(persist_directory)

            if chroma_component.db:
                logging.warning("Database initialized successfully.")
            else:
                logging.warning("Database initialization failed.")

            return chroma_component.db
        except Exception as e:
            logging.error(f"An error occurred while loading the Chroma engine: {e}")
            return f"An error occurred: {e}"

    async def _run_embedding_pinecone(self, agent_data):
        """
        Load the Pinecone engine for querying.
        
        Args:
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The Pinecone engine or an error message.
        """
        store_service = StoreService(self.session)

        try:            
            agents_store = agent_data['Agent']
            embedding_model_name = agent_data['EmbeddingModelName']

            # Get embedding type and initialize embedding component
            embedding_type = store_service.get_provider_info(agents_store.embedding_provider_id)
            embed_component = self._initialize_embedding_component(embedding_type, agent_data)
            embed_component.build(embedding_model_name, 1536)

            # Pinecone initialization
            pinecone_api_key = store_service._get_credential_info(agents_store.vector_db_provider_id, "PINECONE_API_KEY")
            pinecone_environment = store_service._get_credential_info(agents_store.embedding_provider_id, "AWS_REGION")
            index_name = str(agents_store.storage_provider_id)
            pinecone_component = PineconeVectorStoreComponent(api_key=pinecone_api_key, environment=pinecone_environment, index_name=index_name)
            pinecone_component.load_index(embedding_function=embed_component.model_instance)

            if pinecone_component.db:
                logging.warning("Database initialized successfully.")
            else:
                logging.warning("Database initialization failed.")

            return pinecone_component.db
        except Exception as e:
            logging.error(f"An error occurred while loading the Pinecone engine: {e}")
            return f"An error occurred: {e}"
        
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
            openai_api_key = self._get_credential_info(agent_data, "OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the provider information.")
            return OpenAIEmbeddingComponent(openai_api_key)

        elif embedding_type == "BR":
            aws_access_key = self._get_credential_info(agent_data, "AWS_ACCESS_KEY_ID")
            aws_secret_access_key = self._get_credential_info(agent_data, "AWS_SECRET_ACCESS_KEY")
            aws_region = self._get_credential_info(agent_data, "AWS_REGION")
            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the provider information.")
            return BedrockEmbeddingComponent(aws_access_key, aws_secret_access_key, aws_region)
        
        elif embedding_type == "GN":
            google_api_key = self._get_credential_info(agent_data, "GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GoogleAI API key is not set in the provider information.")
            return GoogleEmbeddingComponent(google_api_key)
                
        else:
            raise ValueError(f"Unsupported embedding type: {embedding_type}")
        
    def _initialize_chat_component(self, model_type: str, agent_data):
        """
        Initialize the chat component based on the model type.
        
        Args:
            model_type (str): Type of chat provider (e.g., "OA" for OpenAI, "BR" for Bedrock, "GN" for Google).
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The initialized chat component.
        
        Raises:
            ValueError: If required credentials are missing.
        """
        if model_type == "OA":
            openai_api_key = self._get_credential_info(agent_data, "OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the provider information.")
            return ChatOpenAIComponent(openai_api_key)

        elif model_type == "BR":
            aws_access_key = self._get_credential_info(agent_data, "AWS_ACCESS_KEY_ID")
            aws_secret_access_key = self._get_credential_info(agent_data, "AWS_SECRET_ACCESS_KEY")
            aws_region = self._get_credential_info(agent_data, "AWS_REGION")
            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the provider information.")
            return ChatBedrockComponent(aws_access_key, aws_secret_access_key, aws_region)
        
        elif model_type == "GN":
            google_api_key = self._get_credential_info(agent_data, "GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("Google API key is not set in the provider information.")
            return ChatGoogleAIComponent(google_api_key)
                
        else:
            raise ValueError(f"Unsupported chat type: {model_type}")       

    def _initialize_llm_component(self, model_type: str, agent_data):
        """
        Initialize the llm component based on the model type.
        
        Args:
            model_type (str): Type of llm provider (e.g., "OA" for OpenAI, "BR" for Bedrock, "GN" for Google).
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.
        
        Returns:
            Any: The initialized llm component.
        
        Raises:
            ValueError: If required credentials are missing.
        """
        if model_type == "OA":
            openai_api_key = self._get_credential_info(agent_data, "OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the provider information.")
            return OpenAILLMComponent(openai_api_key)

        elif model_type == "BR":
            aws_access_key = self._get_credential_info(agent_data, "AWS_ACCESS_KEY_ID")
            aws_secret_access_key = self._get_credential_info(agent_data, "AWS_SECRET_ACCESS_KEY")
            aws_region = self._get_credential_info(agent_data, "AWS_REGION")
            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the provider information.")
            return BedrockLLMComponent(aws_access_key, aws_secret_access_key, aws_region)
        
        elif model_type == "GN":
            google_api_key = self._get_credential_info(agent_data, "GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("Google API key is not set in the provider information.")
            return GoogleAILLMComponent(google_api_key)
                
        else:
            raise ValueError(f"Unsupported llm type: {model_type}")


    async def _run_rag_retrieval(self, agent_data, query: str, db, top_k: int = 5):
        store_service = StoreService(self.session)
        try:
            agents_store = agent_data['Agent']
            models_store = agent_data['Model']
            
            matching_docs = db.similarity_search(query, k=top_k)

            retriever = db.as_retriever()

            model_type = store_service.get_provider_info(agents_store.fm_provider_id)

            if agents_store.fm_provider_type == "T":
                component = self._initialize_llm_component(model_type, agent_data)
            elif agents_store.fm_provider_type == "C":    
                component = self._initialize_chat_component(model_type, agent_data)
  
            component.build(
                model_id=models_store.model_name,
                temperature=agents_store.fm_temperature,
                top_p=agents_store.fm_top_p,
                max_tokens=agents_store.fm_response_token_limit
            )

            llm_instance = component.model_instance

            qa_chain = RetrievalQA.from_chain_type(llm=llm_instance, chain_type="stuff", retriever=retriever)
            inputs = {"query": query, "input_documents": matching_docs}
            try:
                answer = await asyncio.to_thread(qa_chain.invoke, inputs)
                result = answer['result'] if 'result' in answer else answer
                logging.info(f"Generated answer: {result}")
            except Exception as e:
                logging.error(f"Error generating response from QA chain: {str(e)}")
                result = "Error generating response from QA chain"

            return {
                "matching_documents": matching_docs,
                "llm_response": result
            }

        except Exception as e:
            logging.error(f"Exception in run_rag_openai: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def _run_model(self, agent_data, query, history):
        store_service = StoreService(self.session)
        try:
            component = None

            agents_store = agent_data['Agent']
            models_store = agent_data['Model']

            model_type = store_service.get_provider_info(agents_store.fm_provider_id)


            if agents_store.fm_provider_type == "T":
                component = self._initialize_llm_component(model_type, agent_data)
            elif agents_store.fm_provider_type == "C":    
                component = self._initialize_chat_component(model_type, agent_data)
  
            component.build(
                model_id=models_store.model_name,
                temperature=agents_store.fm_temperature,
                top_p=agents_store.fm_top_p,
                max_tokens=agents_store.fm_response_token_limit
            )

            return component.run(query)
        
        except Exception as e:
            logging.error(f"Exception in _run_openai_model: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def _postprocess_response(self, agent_data, response: str):

        _d_agent = agent_data['Agent']
        post_processing_id = _d_agent.post_processing_id
        processing_data = self._get_processing_data(post_processing_id)[0]

        # pii mask
        if processing_data.pii_masking:
            pii_options = self._parse_options(processing_data.pii_masking)
            pii_masking_service = PiiMaskingService()
            response = pii_masking_service.mask_pii(response, pii_options)

        # normalize text
        if processing_data.normalization:
            normalize_options = self._parse_options(processing_data.normalization)
            text_normalization_service = TextNormalizationService()
            response = text_normalization_service.normalize_text(response, normalize_options)

        # stopword removal
        if processing_data.stopword_removal:
            stopwords = set(self._convert_list(processing_data.stopword_removal))
            for stopword in stopwords:
                response = response.replace(stopword, '')

        return response

    def _get_token_counts(self, agent_id: UUID, query: Optional[str] = None, text: Optional[str] = None):
        try:

            agent_data = self._get_agent_data(agent_id)
            _d_agent = agent_data['Model']
            
            logging.warning('=== _get_token_counts()  =====================================')

            logging.warning(query)
            logging.warning(_d_agent.model_name)
            logging.warning(text)
            token_component = TokenUtilityService(None, None, None)
            prompt_token_counts = token_component.get_token_count(query, _d_agent.model_name)
            completion_token_counts = token_component.get_token_count(text, _d_agent.model_name)
            prompt_cost = token_component.get_prompt_cost(text, _d_agent.model_name)
            completion_cost = token_component.get_completion_cost(query, _d_agent.model_name)

            logging.warning(prompt_token_counts)
            logging.warning(completion_token_counts)
            logging.warning(prompt_cost)
            logging.warning(completion_cost)

            logging.warning('=== _get_token_counts()  =====================================')

            prompt_token_counts = prompt_token_counts or 0
            completion_token_counts = completion_token_counts or 0
            prompt_cost = prompt_cost or 0.0
            completion_cost = completion_cost or 0.0

            if isinstance(prompt_cost, Decimal):
                prompt_cost = float(prompt_cost)
            if isinstance(completion_cost, Decimal):
                completion_cost = float(completion_cost)

            total_token_counts = prompt_token_counts+completion_token_counts
            total_cost = prompt_cost+completion_cost

            self.update_agent_count(agent_id, total_token_counts, total_cost)

            result = {
                "token_counts": total_token_counts,
                "total_cost": total_cost
            }

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def _get_openai_token_counts(self, text: Optional[str] = None, model_name: Optional[str] = None):

        token_component = TokenUtilityService(None, None, None)
        return token_component.get_openai_token_count(
                text=text,
                model_id=model_name
            )

    def _get_bedrock_token_counts(self, text: Optional[str] = None, model_name: Optional[str] = None):

        aws_access_key = os.getenv("INNER_AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("INNER_AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("INNER_AWS_REGION")

        if not aws_access_key:
            return "aws_access_key is not set in the environment variables"
        if not aws_secret_access_key:
            return "aws_secret_access_key is not set in the environment variables"
        if not aws_region:
            return "aws_region is not set in the environment variables"

        token_component = TokenUtilityService(aws_access_key, aws_secret_access_key, aws_region)
        return token_component.get_bedrock_token_count(
                text=text,
                model_id=model_name
            )

    def update_agent_count(self, agent_id: UUID, token_count: int, total_cost: float):
        try:
            agent = self.session.get(Agent, agent_id)

            if agent:
                agent.expected_token_count += token_count
                agent.expected_request_count += 1
                agent.expected_cost += total_cost
                self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
    def _get_credential_info(self, agent_data, key):

        _d_credential = agent_data['Credential']

        if not _d_credential.inner_used:
            if key == "AWS_ACCESS_KEY_ID":
                return _d_credential.access_key
            elif key == "AWS_SECRET_ACCESS_KEY":
                return _d_credential.secret_key
            elif key == "AWS_REGION":
                return os.getenv(key)
            elif key == "OPENAI_API_KEY":
                return _d_credential.api_key
            elif key == "GOOGLE_API_KEY":
                return _d_credential.api_key
            elif key == "PINECONE_API_KEY":
                return _d_credential.api_key             
        else:
            return os.getenv(key)