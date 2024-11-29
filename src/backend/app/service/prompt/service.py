import asyncio
from decimal import Decimal
from sqlalchemy.orm import aliased
import os
from typing import Dict, List, Optional
import openai
from fastapi import HTTPException
from sqlmodel import Session, select
from uuid import UUID
import logging
from app.service.agent.model import Agent
from langchain.chains import RetrievalQA
from app.service.store.model import Store
from app.service.provider.model import Provider
from app.components.Chat.Bedrock import ChatBedrockComponent
from app.core.util.token import TokenUtilityService
from app.api.v1.schemas.chat import ChatResponse
from app.service.store.service import StoreService
from app.core.util.logging import LoggingConfigurator
from app.service.processing.model import Processing
from app.core.util.piimasking import PiiMaskingService
from app.core.util.textNormailization import TextNormalizationService
from app.service.credential.model import Credential
from app.service.embedding.service import EmbeddingService
from app.components.Chat.AzureOpenAI import ChatOpenAIComponent
from app.components.Chat.GoogleVertexAI import ChatVertexAIComponent
from app.components.Retrievers.AzureSearch import AzureSearchRetrieversComponent
from app.components.Retrievers.Bedrock import BedrockRetrieverComponent
from app.components.Retrievers.VertexAISearch import VertexAIRetrieversComponent

class PromptService:
    def __init__(self, session: Session):
        self.session = session
        self.embedding_service = EmbeddingService(session)

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

            # add context
            query = self._replace_question(_d_agent.template, query)

            # embedding
            if _d_agent.embedding_enabled:

                # check storage limit
                store_data = agent_data['Store']
                user_id = _d_agent.user_id

                # Limit Storage
                # if store_data:
                #     storage_limit_response = self._check_storage_limit(user_id, store_data)
                #     if storage_limit_response:
                #         return storage_limit_response
                        
                try:
                    documents = asyncio.run(self.embedding_service._run_embedding_main(agent_data))
                    # rag_response = asyncio.run(self._run_rag_retrieval(agent_data, query))
                    response = self._run_rag_retrieval(agent_data, query, documents)
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
                
            return ChatResponse(
                        answer=response,
                        tokens=tokens['token_counts'],
                        cost=tokens['total_cost']
                    )

        except Exception as e:    
            raise HTTPException(status_code=500, detail=str(e))

    def _get_agent_data(self, agent_id: UUID):
        statement = (
            select(
                Agent, Credential, Store
            )
            .join(Credential, Agent.fm_provider_id == Credential.credential_id)
            .outerjoin(Store, Agent.storage_object_id == Store.store_id)
        )
        statement = statement.where(Agent.agent_id == agent_id)

        result = self.session.execute(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Agent not found")

        agent_data, credential_data, store_data = result

        return {
            "Agent": agent_data,
            "Credential": credential_data,
            "Store": store_data
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

    def _replace_question(self, context: str, question: str) -> str:
        messages = [
            ("system", context),
            ("human", question)
        ]        
        return messages

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
        
    def _initialize_chat_component(self, csp_provider: str):  
        """  
        Initialize the chat component based on the chat provider type.  
    
        Args:  
            csp_provider (str): Type of chat provider (e.g., "azure" for OpenAI, "aws" for Bedrock, "gcp" for Google VertexAI).  
    
        Returns:  
            Any: The initialized chat component.  
    
        Raises:  
            ValueError: If required credentials are missing.  
        """  
    
        # Azure OpenAI Chat  
        if csp_provider == "azure":  
            azure_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")  
            openai_api_version = os.getenv("AZURE_OPENAI_API_CHAT_VERSION")  
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            model_id = os.getenv("AZURE_OPENAI_CHAT_MODEL_ID")
            if not all([openai_api_version, azure_endpoint, api_key, model_id]):  
                raise ValueError("Azure OpenAI credentials are not set in the environment variables.")  
            return ChatOpenAIComponent(openai_api_version, azure_endpoint, api_key, model_id)  
        
        # AWS Bedrock Chat  
        elif csp_provider == "aws":  
            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")  
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")  
            aws_region = os.getenv("AWS_REGION")  
            if not all([aws_access_key, aws_secret_access_key, aws_region]):  
                raise ValueError("AWS credentials or region are not set in the environment variables.")  
            return ChatBedrockComponent(aws_access_key, aws_secret_access_key, aws_region)  
        
        # Google VertexAI Chat  
        elif csp_provider == "gcp":  
            project_id = os.getenv("GCP_PROJECT_ID")  
            location = os.getenv("GCP_LOCATION")  
            credentials_path = os.getenv("GCP_CREDENTIALS_PATH")  
            if not all([project_id, location, credentials_path]):  
                raise ValueError("Google VertexAI credentials are not set in the environment variables.")  
            return ChatVertexAIComponent(project_id, location, credentials_path)  
        
        else:  
            raise ValueError(f"Unsupported chat type: {csp_provider}")  

    def _initialize_retrievers_component(self, csp_provider: str, index_name: str):  
        """  
        Initialize the retriever component based on the provider type.  
    
        Args:  
            csp_provider (str): Type of retriever provider (e.g., "azure" for Azure Search, "aws" for Bedrock, "gcp" for Google VertexAI).  
            resource_id (str): Resource identifier such as index name for Azure, knowledge base ID for AWS, or data store ID for Google VertexAI.  
    
        Returns:  
            Any: The initialized retriever component.  
    
        Raises:  
            ValueError: If required credentials are missing.  
        """  
        # Azure Search Retriever  
        if csp_provider == "azure":
            model_id = os.getenv("AZURE_OPENAI_CHAT_MODEL_ID")
            return AzureSearchRetrieversComponent(index_name, model_id)  
    
        # AWS Bedrock Retriever  
        elif csp_provider == "aws":  
            return BedrockRetrieverComponent(index_name)  
    
        # Google VertexAI Retriever  
        elif csp_provider == "gcp":  
            project_id = os.getenv("GCP_PROJECT_ID")  
            location_id = os.getenv("GCP_LOCATION")  
            search_engine_id = os.getenv("GCP_SEARCH_ENGINE_ID")  
            if not all([project_id, location_id]):  
                raise ValueError("Google VertexAI project ID and location ID must be set in the environment variables.")  
            return VertexAIRetrieversComponent(project_id, location_id, index_name, search_engine_id)  
    
        else:  
            raise ValueError(f"Unsupported retriever type: {csp_provider}")  
        
    async def _run_rag_retrieval(self, agent_data, query: str, documents):
        retriever_component = None
        agents_store = agent_data['Agent']        
        try:
            index_name = f"{agents_store.storage_object_id}_index" 
            csp_provider = os.getenv("CSP_PROVIDER")
            retriever_component = self._initialize_retrievers_component(csp_provider, index_name)
            retriever_component.build()
            retriever_component.run(query)

            return retriever_component.use_within_chain(query)
        
        except Exception as e:
            logging.error(f"Exception in _run_openai_model: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
    def _run_model(self, agent_data, query, history):
        component = None
        agents_store = agent_data['Agent']    
            
        try:
            csp_provider = os.getenv("CSP_PROVIDER")
            component = self._initialize_chat_component(csp_provider)
            component.build(
                temperature=agents_store.fm_temperature,
                top_p=agents_store.fm_top_p
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
            logging.warning('=== _get_token_counts()  =====================================')

            logging.warning(query)
            logging.warning(text)

            logging.warning('=== _get_token_counts()  =====================================')

            prompt_token_counts = 0
            completion_token_counts = 0
            prompt_cost = 0.0
            completion_cost = 0.0

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

        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION")

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