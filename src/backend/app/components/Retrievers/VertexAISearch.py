import logging  
from langchain_google_community import VertexAISearchRetriever  
from langchain_core.output_parsers import StrOutputParser  
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.runnables import RunnablePassthrough  
from langchain_openai import ChatOpenAI  
from app.components.Chat.Base import AbstractLLMComponent  
  
class VertexAIRetrieversComponent(AbstractLLMComponent):  
    def __init__(self, project_id: str, location_id: str, data_store_id: str, search_engine_id: str = None):  
        super().__init__()  
        self.project_id = project_id  
        self.location_id = location_id  
        self.data_store_id = data_store_id  
        self.search_engine_id = search_engine_id  
        self.retriever = None  
  
    def build(self):  
        try:  
            # Initialize retriever  
            self.retriever = VertexAISearchRetriever(  
                project_id=self.project_id,  
                location_id=self.location_id,  
                data_store_id=self.data_store_id,  
                search_engine_id=self.search_engine_id,  
                max_documents=3  # You can adjust this value based on your needs  
            )  
            logging.info(f"Retriever for project {self.project_id} initialized successfully.")  
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
            llm = ChatOpenAI(model=self.model)  
  
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