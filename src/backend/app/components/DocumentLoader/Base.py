class BaseDocumentLoader:
    def __init__(self):
        self.documents = None

    def load(self):
        raise NotImplementedError("You need to implement the load method.")
    
    def process_documents(self):
        raise NotImplementedError("You need to implement the process_documents method.")
    
    def get_documents(self):
        if self.documents is None:
            raise ValueError("Documents are not loaded yet. Call the load method first.")
        return self.documents
