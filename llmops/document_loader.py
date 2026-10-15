from langchain_community.document_loaders import PyPDFLoader
from langchain_unstructured import UnstructuredLoader
import os
import glob
from abc import ABC, abstractmethod


# Abstract class structure
class ParsingMethod(ABC):
    """Strategy interface for reading a document into a list of pages."""

    @abstractmethod
    def read_document(self, file_path : str):
        """Read the document at ``file_path`` and return its pages."""
        pass


# Parsing Method 1 : PyPDFLoader
class PyPDFMethod(ParsingMethod):
    """Parse a PDF into pages using LangChain's ``PyPDFLoader``."""

    def read_document(self, file_path : str) -> list:
        loader = PyPDFLoader(file_path)
        
        pages = []
        for page in loader.lazy_load():
            pages.append(page)

        return pages


# Parsing Method 2 : UnstructuredLoader
class UnstructuredPDFMethod(ParsingMethod):
    """Parse a PDF into pages using ``UnstructuredLoader`` (hi_res strategy)."""

    def read_document(self, file_path : str) -> list:
        loader = UnstructuredLoader(
                                        file_path=file_path,
                                        strategy="hi_res",
                                        )
        
        pages = []
        for page in loader.lazy_load():
            pages.append(page)

        return pages
        

# Parsing Method 3 : To be implemented



# Parsing method interface
class DocumentLoader:
    """Context that delegates document reading to a chosen ``ParsingMethod``."""

    def __init__(self, parsing_method: ParsingMethod):
        self.parsing_method = parsing_method

    def get_document(self, file_path: str) -> list:
        """Read and return the pages of the document at ``file_path``."""
        return self.parsing_method.read_document(file_path)