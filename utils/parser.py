import fitz

def extract_text(pdf_path):
    """
    Extract text from all pages of a PDF.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page_number, page in enumerate(document):

        page_text = page.get_text()

        text += page_text + "\n"

    document.close()

    return text


if __name__ == "__main__":

    pdf_path = "DOC/docmindAI/uploads/Executive Summary.pdf"

    extracted_text = extract_text(pdf_path)

    print(extracted_text)