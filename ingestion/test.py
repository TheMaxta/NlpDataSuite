from enum import Enum
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import re

class Chunk:
    def __init__(self, content: str):
        self.content = content
        self.metadata: Dict[str, Any] = {}
        self.linked_chunks: List['Chunk'] = []

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def link_chunk(self, chunk: 'Chunk'):
        self.linked_chunks.append(chunk)

class HierarchyOfChunks(ABC):
    def __init__(self):
        self.chunks: List[Chunk] = []

    @abstractmethod
    def add_chunk(self, chunk: Chunk):
        pass

    @abstractmethod
    def get_chunks(self) -> List[Chunk]:
        pass

class SequentialHierarchy(HierarchyOfChunks):
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    def get_chunks(self) -> List[Chunk]:
        return self.chunks

class NonOrderedHierarchy(HierarchyOfChunks):
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)

    def get_chunks(self) -> List[Chunk]:
        return self.chunks

    def link_chunks(self, chunk1: Chunk, chunk2: Chunk):
        chunk1.link_chunk(chunk2)
        chunk2.link_chunk(chunk1)

class DocumentProcessor(ABC):
    @abstractmethod
    def process_file(self, file_path: str, hierarchy: HierarchyOfChunks) -> HierarchyOfChunks:
        pass

class RegexBasedProcessor(DocumentProcessor):
    def __init__(self, chunk_separator: str, metadata_end_marker: Optional[str] = None):
        self.chunk_separator = chunk_separator
        self.metadata_end_marker = metadata_end_marker

    def process_file(self, file_path: str, hierarchy: HierarchyOfChunks) -> HierarchyOfChunks:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        chunks = re.split(self.chunk_separator, content)

        for chunk_content in chunks:
            if not chunk_content.strip():
                continue

            chunk = self.create_chunk(chunk_content)
            hierarchy.add_chunk(chunk)

        return hierarchy

    def create_chunk(self, chunk_content: str) -> Chunk:
        lines = chunk_content.split("\n")
        content_lines = []
        chunk = Chunk("")

        content_started = False
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if not content_started:
                if self.metadata_end_marker and line.startswith(self.metadata_end_marker):
                    content_started = True
                    continue
                if ':' in line:
                    key, value = line.split(":", 1)
                    chunk.add_metadata(key.strip(), value.strip())
                else:
                    content_started = True
                    content_lines.append(line)
            else:
                content_lines.append(line)

        chunk.content = "\n".join(content_lines).strip()
        return chunk

class ChopMethod(Enum):
    EXACT = 1
    SENTENCE = 2
    LINE_BREAK = 3
    WORD = 4

class TruncationBasedProcessor(DocumentProcessor):
    def __init__(self, truncation_length: int, chop_method: ChopMethod):
        self.truncation_length = truncation_length
        self.chop_method = chop_method

    def process_file(self, file_path: str, hierarchy: HierarchyOfChunks) -> HierarchyOfChunks:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        chunks = self.create_chunks(content)

        for chunk_content in chunks:
            chunk = Chunk(chunk_content)
            hierarchy.add_chunk(chunk)

        return hierarchy

    def create_chunks(self, content: str) -> List[str]:
        chunks = []
        current_position = 0

        while current_position < len(content):
            chunk_end = self.find_chunk_end(content, current_position)
            chunk = content[current_position:chunk_end].strip()
            if chunk:
                chunks.append(chunk)
            current_position = chunk_end

        return chunks

    def find_chunk_end(self, content: str, start: int) -> int:
        end = start + self.truncation_length

        if self.chop_method == ChopMethod.EXACT:
            return min(end, len(content))

        elif self.chop_method == ChopMethod.SENTENCE:
            sentence_end = content.find('.', end)
            return sentence_end + 1 if sentence_end != -1 else len(content)

        elif self.chop_method == ChopMethod.LINE_BREAK:
            line_break = content.find('\n', end)
            return line_break + 1 if line_break != -1 else len(content)

        elif self.chop_method == ChopMethod.WORD:
            word_end = re.search(r'\s', content[end:])
            return end + word_end.start() if word_end else len(content)

        return min(end, len(content))
    
class SpecificFormatProcessor(RegexBasedProcessor):
    def __init__(self):
        super().__init__(chunk_separator=r'(?=Comments:)', metadata_end_marker=None)

    def create_chunk(self, chunk_content: str) -> Chunk:
        chunk = super().create_chunk(chunk_content)
        
        # Rename 'Title' to 'Question' in metadata
        if "Title" in chunk.metadata:
            chunk.metadata["Question"] = chunk.metadata.pop("Title")
        
        # Remove the underscores at the beginning and end of the content
        chunk.content = re.sub(r'^_+|_+$', '', chunk.content).strip()
        
        return chunk

class DocumentIngestionSuite:
    def __init__(self, processor: DocumentProcessor, hierarchy: HierarchyOfChunks):
        self.processor = processor
        self.hierarchy = hierarchy

    def ingest(self, file_path: str) -> HierarchyOfChunks:
        return self.processor.process_file(file_path, self.hierarchy)

# Usage
specific_processor = SpecificFormatProcessor()
sequential_hierarchy = SequentialHierarchy()
ingestion_suite = DocumentIngestionSuite(specific_processor, sequential_hierarchy)
processed_hierarchy = ingestion_suite.ingest("C:\\Users\\964820\\desktop\\RFPproject\\data\\raw\\testFile.txt")

# Accessing the chunks
for chunk in processed_hierarchy.get_chunks():
    print(f"Content: {chunk.content}")
    print(f"Metadata: {chunk.metadata}")
    print("---")