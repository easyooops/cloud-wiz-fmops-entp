# /Retrievers/AzureSearchRetrieversComponent.py  
import logging  
from langchain_community.retrievers import AzureAISearchRetriever  
from langchain_core.output_parsers import StrOutputParser  
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.runnables import RunnablePassthrough  
from langchain_openai import ChatOpenAI

from app.components.Chat.Base import AbstractLLMComponent 
  
class AzureSearchRetrieversComponent(AbstractLLMComponent):  
    def __init__(self, index_name: str, model_id: str):  
        super().__init__()  
        self.index_name = index_name
        self.model_id = model_id
        self.retriever = None
  
    def build(self):  
        try:  
            # Initialize retriever  
            self.retriever = AzureAISearchRetriever(  
                content_key="content",  
                top_k=1,  
                index_name=self.index_name,  
            )  
  
            logging.info(f"Retriever for index {self.index_name} initialized successfully.")  
        except Exception as e:  
            logging.error(f"Failed to initialize retriever: {e}")  
  
    def run(self, input_text):  
        if self.retriever is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
        return self.retriever.invoke(input_text)  
  
    def use_within_chain(self, query: str):  
        try:  
            # Set up components for the chain  
            retriever = self.retriever  
            prompt = ChatPromptTemplate.from_template(  
                """Answer the question based only on the context provided.  
                Context: {context}  
                Question: {question}"""  
            )  
            llm = ChatOpenAI(model=self.model_id)  
  
            def format_docs(docs):  
                return "\n\n".join(doc.page_content for doc in docs)  
  
            chain = (  
                {"context": retriever | format_docs, "question": RunnablePassthrough()}  
                | prompt  
                | llm  
                | StrOutputParser()  
            )  
  
            # Run the chain with the provided query  
            return chain.invoke(query)  
        except Exception as e:  
            logging.error(f"Failed to use retriever within chain: {e}")  
            return None  