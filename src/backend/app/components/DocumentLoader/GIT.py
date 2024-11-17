from app.components.DocumentLoader.Base import BaseDocumentLoader
import git
from git import Repo
from langchain_community.document_loaders import GitLoader

class GitDocumentLoader(BaseDocumentLoader):
    def __init__(self, config: dict):
        super().__init__()
        self.git_loader = GitLoader(
            clone_url=config.get('git_clone_url', ''),
            branch=config.get('git_branch', 'main'),
            repo_path="./git/repo/"+config.get('git_repo_path', '/tmp/repo'),
            file_filter=None
            # file_filter=config.get('git_file_filter', lambda x: x.endswith('.md'))
        )

    def load(self):
        """Load documents from Git repository."""
        self.documents = self.git_loader.load()
        return self.documents

    def process_documents(self):
        """Process the documents if any additional processing is needed."""
        # Add any document processing steps here
        pass
