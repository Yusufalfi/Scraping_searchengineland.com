import os
from docx import Document
from config import OUTPUT_DIR

def create_word_doc(title: str, date_str: str, content_blocks: list, filename: str):
    """Membuat file .docx berisi judul, tanggal, paragraf, dan gambar."""
    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Published Date: {date_str}")
    doc.add_paragraph("-" * 40)

    for block in content_blocks:
        if block["type"] == "heading":
            doc.add_heading(block["text"], level=block.get("level", 2))
        elif block["type"] == "paragraph":
            doc.add_paragraph(block["text"])
        elif block["type"] == "list_item":
            doc.add_paragraph(block["text"], style='List Bullet')

    filepath = os.path.join(OUTPUT_DIR, filename)
    doc.save(filepath)
    print(f"Saved docx: {filepath}")