import os
import requests
from bs4 import BeautifulSoup
import pdfkit
from PyPDF2 import PdfMerger
from urllib.parse import urljoin

BASE_URL = "https://docs.sqlalchemy.org/en/20/"
OUTPUT_DIR = "sqlalchemy_docs"
PDF_DIR = os.path.join(OUTPUT_DIR, "pdf")

os.makedirs(PDF_DIR, exist_ok=True)

def get_doc_links():
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") or href.startswith("#"):
            continue
        if href.startswith("http"):
            if "docs.sqlalchemy.org" in href:
                links.add(href)
        else:
            links.add(urljoin(BASE_URL, href))

    return sorted(links)

def convert_to_pdf(url, index):
    filename = os.path.join(PDF_DIR, f"{index}.pdf")
    pdfkit.from_url(url, filename)
    return filename

def merge_pdfs(pdf_files, output="sqlalchemy_full_docs.pdf"):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output)
    merger.close()

links = get_doc_links()

pdf_files = []
for i, link in enumerate(links):
    print("Converting:", link)
    pdf_files.append(convert_to_pdf(link, i))

merge_pdfs(pdf_files)

print("Done! SQLAlchemy documentation saved as sqlalchemy_full_docs.pdf")
