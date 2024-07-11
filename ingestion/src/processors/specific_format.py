import re
from .regex_based import RegexBasedProcessor
from models import Chunk

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