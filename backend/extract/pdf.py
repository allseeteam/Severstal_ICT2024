# from extract.pdf_camelot import parse_pdf_with_camelot
from extract.pdf_pdfplumber import parse_tables_with_pdfplumber


def get_tables_from_raw_pdf(path):
    # camelot_tables = parse_pdf_with_camelot(path)
    # if camelot_tables:
    #     return camelot_tables
    pdfplumber_tables = parse_tables_with_pdfplumber(path)
    if pdfplumber_tables:
        return pdfplumber_tables
