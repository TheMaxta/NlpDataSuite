from abc import ABC, abstractmethod
from models import HierarchyOfChunks

class DocumentProcessor(ABC):
    @abstractmethod
    def process_file(self, file_path: str, hierarchy: HierarchyOfChunks) -> HierarchyOfChunks:
        pass