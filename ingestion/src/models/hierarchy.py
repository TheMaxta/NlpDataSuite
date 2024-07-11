from abc import ABC, abstractmethod
from typing import List
from .chunk import Chunk

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