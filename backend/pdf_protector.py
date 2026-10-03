from pypdf import PdfReader, PdfWriter
from io import BytesIO


def protect_pdf(pdf_bytes, password):
    """
    Encrypts a PDF using the supplied password
    and returns the protected PDF as bytes.
    """

    input_pdf = BytesIO(pdf_bytes)
    output_pdf = BytesIO()

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)

    # Add password protection
    writer.encrypt(
        user_password=password,
        algorithm="AES-256"
    )

    # Write encrypted PDF
    writer.write(output_pdf)

    return output_pdf.getvalue()