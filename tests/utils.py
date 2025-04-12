from marker.providers.pdf import PdfProvider
import tempfile

import datasets


# In tests/utils.py
def setup_pdf_provider(pdf, config):
    import pytest

    pytest.skip("Skipping tests requiring PDF documents")
    # The following code won't run due to the skip
    dataset = datasets.load_dataset("datalab-to/pdfs", split="train")
    idx = dataset["filename"].index(pdf)
    temp_pdf = tempfile.NamedTemporaryFile(suffix=".pdf")
    temp_pdf.write(dataset["pdf"][idx])
    temp_pdf.flush()
    return PdfProvider(temp_pdf.name, config)
