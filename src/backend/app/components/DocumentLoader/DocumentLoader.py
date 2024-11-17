from typing import List
import pandas as pd
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, Docx2txtLoader
from langchain_core.documents import Document

class DocumentLoaderComponent:
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        if file_path.endswith('.txt'):
            loader = TextLoader(file_path)
            return loader.load()
        elif file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            return loader.load()
        elif file_path.endswith('.csv'):
            loader = CSVLoader(file_path)
            return loader.load()
        elif file_path.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
            return loader.load()
        elif file_path.endswith('.xlsx'):
            documents = []
            xlsx = pd.ExcelFile(file_path)
            for sheet_name in xlsx.sheet_names:
                df = pd.read_excel(xlsx, sheet_name=sheet_name)
                full_text = df.to_string(index=False)
                documents.append(Document(page_content=full_text, metadata={"source": f"{file_path} - {sheet_name}"}))
            return documents
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
