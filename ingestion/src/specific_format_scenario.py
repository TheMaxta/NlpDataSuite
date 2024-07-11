from document_ingestion_suite import DocumentIngestionSuite
from processors import SpecificFormatProcessor
from models import SequentialHierarchy

def run_specific_format_scenario(file_path: str):
    specific_processor = SpecificFormatProcessor()
    sequential_hierarchy = SequentialHierarchy()
    ingestion_suite = DocumentIngestionSuite(specific_processor, sequential_hierarchy)
    
    processed_hierarchy = ingestion_suite.ingest(file_path)

    print("Specific Format Scenario Results:")
    for i, chunk in enumerate(processed_hierarchy.get_chunks(), 1):
        print(f"Chunk {i}:")
        print(f"Content: {chunk.content}")
        print(f"Metadata: {chunk.metadata}")
        print("---")

if __name__ == "__main__":
    file_path = "path/to/your/specific/format/file.txt"  # Replace with actual file path
    run_specific_format_scenario(file_path)