import tempfile
import os
from agno.knowledge.reader.pdf_reader import PDFReader

def process_pdf(pdf_bytes):
    """
    Processes a PDF from bytes, extracts text, and returns content string.
    Uses a temporary file to interface with Agno's PDFReader.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(pdf_bytes)
        tmp_path = tmp_pdf.name
    
    try:
        pdf_reader = PDFReader()
        pdf_docs = pdf_reader.read(tmp_path)
        text = "\n".join([d.content for d in pdf_docs if d.content])
        return text
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
