from typing import Dict, Any, List

class Chunk:
    def __init__(self, content: str):
        self.content = content
        self.metadata: Dict[str, Any] = {}
        self.linked_chunks: List['Chunk'] = []

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def link_chunk(self, chunk: 'Chunk'):
        self.linked_chunks.append(chunk)