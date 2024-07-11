from document_ingestion_suite import DocumentIngestionSuite
from processors import TruncationBasedProcessor
from models import SequentialHierarchy
from utils import ChopMethod

def run_truncation_scenario(file_path: str, truncation_length: int, chop_method: ChopMethod):
    truncation_processor = TruncationBasedProcessor(truncation_length, chop_method)
    sequential_hierarchy = SequentialHierarchy()
    ingestion_suite = DocumentIngestionSuite(truncation_processor, sequential_hierarchy)
    
    processed_hierarchy = ingestion_suite.ingest(file_path)

    print(f"Truncation Scenario Results (Length: {truncation_length}, Method: {chop_method.name}):")
    for i, chunk in enumerate(processed_hierarchy.get_chunks(), 1):
        print(f"Chunk {i}:")
        print(f"Content: {chunk.content}")
        print("---")

if __name__ == "__main__":
    file_path = "C:\Users\964820\desktop\RFPproject\backend\ingestion\src\wiki.txt"  # Replace with actual file path
    truncation_length = 1000  # Adjust as needed
    chop_method = ChopMethod.SENTENCE  # Change to test different methods
    run_truncation_scenario(file_path, truncation_length, chop_method)