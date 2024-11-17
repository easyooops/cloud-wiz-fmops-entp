import asyncio
import json
import boto3
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain.docstore.document import Document
from typing import List
from langchain_community.embeddings import BedrockEmbeddings
from app.core.factories import get_database
from app.service.chat.service import ChatService
from app.service.embedding.service import EmbeddingService
from app.components.Embedding.OpenAI import OpenAIEmbeddingComponent
from app.api.v1.schemas.embedding import EmbeddingMultipleResponse
from app.service.store.service import StoreService
from app.service.auth.service import AuthService, get_current_user

router = APIRouter()
load_dotenv()


@router.post("/initialize-faiss")
async def initialize_faiss_store(
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    embedding_service = EmbeddingService(session)

    openai_api_key = AuthService.get_openai_key()
    
    embedding_component = OpenAIEmbeddingComponent(openai_api_key)
    embedding_component.build(model_id="text-embedding-ada-002")
    await embedding_service.initialize_faiss_store(embedding_component, dimension=2056)
    return {"status": "Faiss store initialized"}


@router.post("/add-to-faiss", response_model=EmbeddingMultipleResponse)
async def add_to_faiss_store(
    texts: List[str],
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    embedding_service = EmbeddingService(session)
    embeddings = await embedding_service.add_to_faiss_store(texts)
    return EmbeddingMultipleResponse(embeddings=embeddings)


@router.post("/rag-open-ai")
async def rag_open_ai(
    query: str,
    store_name: str,
    top_k: int = 5,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        store_service = StoreService(session)
        chat_service = ChatService(session)

        file_metadata_list = store_service.list_files(store_name)
        files = [file_metadata['Key'] for file_metadata in file_metadata_list]

        documents = store_service.load_documents(files)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        if not docs:
            raise ValueError("No documents were split into chunks")

        openai_api_key = AuthService.get_openai_key()

        if not openai_api_key:
            raise ValueError("OpenAI API key is not set in the environment")
        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        db = await FAISS.afrom_documents(docs, embeddings)
        matching_docs = await db.asimilarity_search(query, k=top_k)

        if not matching_docs:
            raise ValueError("No matching documents found")

        retriever = db.as_retriever()
        llm_instance = await chat_service.get_llm_openai_instance(query=query, model_id="gpt-3.5-turbo", max_tokens=600, temperature=0.1)
        qa_chain = RetrievalQA.from_chain_type(llm=llm_instance, chain_type="stuff", retriever=retriever)

        inputs = {"query": query, "input_documents": matching_docs}
        try:
            answer = await asyncio.to_thread(qa_chain.invoke, inputs)
            result = answer['result'] if 'result' in answer else answer
        except Exception as e:
            result = "Error generating response from QA chain"
        return {"response": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag-bedrock")
async def rag_bedrock(
    query: str,
    store_name: str,
    model_id: str,
    top_k: int = 5,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        store_service = StoreService(session)
        chat_service = ChatService(session)

        file_metadata_list = store_service.list_files(store_name)
        files = [file_metadata['Key'] for file_metadata in file_metadata_list]
        documents = store_service.load_documents(files)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(documents)

        if not split_docs:
            raise ValueError("No documents were split into chunks")

        if isinstance(split_docs[0], str):
            docs = [Document(page_content=doc) for doc in split_docs]
        else:
            docs = [Document(page_content=doc.page_content) for doc in split_docs]

        aws = AuthService.get_aws_key()
        aws_access_key = aws['aws_access_key']
        aws_secret_access_key = aws['aws_secret_access_key']
        aws_region = aws['aws_region']

        if not all([aws_access_key, aws_secret_access_key, aws_region]):
            raise ValueError("AWS credentials or region are not set in the environment variables")

        boto3_session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        embeddings = BedrockEmbeddings(
            model_id=model_id,
            client=boto3_session.client('bedrock-runtime')
        )
        db = await FAISS.afrom_documents(docs, embeddings)
        matching_docs = await db.asimilarity_search(query, k=top_k)

        if not matching_docs:
            raise ValueError("No matching documents found")

        retriever = db.as_retriever()
        llm_instance = chat_service.get_llm_bedrock_instance(model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=500, temperature=0.1)
        qa_chain = RetrievalQA.from_chain_type(llm=llm_instance, chain_type="stuff", retriever=retriever)

        inputs = {"query": query, "input_documents": matching_docs}
        try:
            answer = await asyncio.to_thread(qa_chain.invoke, inputs)
            result = answer['result'] if 'result' in answer else answer
        except Exception as e:
            result = "Error generating response from QA chain"
        return {"response": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))