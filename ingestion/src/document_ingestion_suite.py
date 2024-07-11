from models import HierarchyOfChunks
from processors import DocumentProcessor

class DocumentIngestionSuite:
    def __init__(self, processor: DocumentProcessor, hierarchy: HierarchyOfChunks):
        self.processor = processor
        self.hierarchy = hierarchy

    def ingest(self, file_path: str) -> HierarchyOfChunks:
        return self.processor.process_file(file_path, self.hierarchy)