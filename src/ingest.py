import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.vectorstore import get_vectorstore
from src.config import CHROMA_DIR
from pathlib import Path

PDF_ROOT = Path("data/pdfs")
CHROMA_DIR = Path(CHROMA_DIR)


def load_all_pdfs(pdf_root:Path):
    """Load all PDFs recursively and return a list of LangChain Document objects."""
    pdf_files = sorted(pdf_root.glob("**/*.pdf"))
    print(f"Found {len(pdf_files)} PDFs")
    all_docs = []

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()

            for d in docs:
                d.metadata["source"] = pdf_file.name
                d.metadata["path"] = str(pdf_file)
                d.metadata["source_file"] = pdf_file.name     
                d.metadata["file_type"] = "pdf"

            all_docs.extend(docs)
            print(f"Loaded {len(docs)} pages")
        except Exception as e:
            print(f"Error loading {pdf_file.name}: {e}")

    print(f"\nTotal pages loaded: {len(all_docs)}")
    return all_docs


def main():
    if not PDF_ROOT.exists():
        raise FileNotFoundError(f"PDF_ROOT not found: {PDF_ROOT}")

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
        print(f"Deleted existing {CHROMA_DIR} (fresh rebuild)")

    docs = load_all_pdfs(PDF_ROOT)
    if not docs:
        raise FileNotFoundError(f"No PDF pages loaded from: {PDF_ROOT}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
    )
    chunks = splitter.split_documents(docs)
    print(f"\nTotal chunks created: {len(chunks)}")

    vs = get_vectorstore()

    BATCH_SIZE = 25
    total = len(chunks)

    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        vs.add_documents(batch)
        print(f"Embedded/stored {min(i + BATCH_SIZE, total)}/{total} chunks")

    print("\n✅ INGESTION COMPLETE")
    print("PDF files:", len(sorted(PDF_ROOT.glob('**/*.pdf'))))
    print("Loaded pages:", len(docs))
    print("Stored chunks:", len(chunks))


if __name__ == "__main__":
    main()
