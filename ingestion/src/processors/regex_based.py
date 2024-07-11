import re
from typing import Optional
from .base import DocumentProcessor
from models import HierarchyOfChunks, Chunk

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