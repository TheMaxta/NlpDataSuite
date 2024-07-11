import re
from typing import List
from .base import DocumentProcessor
from models import HierarchyOfChunks, Chunk
from utils.enums import ChopMethod

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