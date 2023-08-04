from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from io import BytesIO
from base64 import b64encode


ISSUE_NAME = "/Issue by"
ISSUE_DATA = "Server A"
SIGNATURE_METADATA_NAME = "/Signature"


def _normalize_pdf(bytes_data):
    tmp = PdfReader(BytesIO(bytes_data))
    out = PdfWriter()

    [out.add_page(p) for p in tmp.pages]

    out.add_metadata({ISSUE_NAME: ISSUE_DATA})
    with BytesIO() as stream:
        out.write(stream)
        stream.seek(0)
        tmp = stream.read()
    out.close()
    return tmp


def add_sign(bytes_data, sign):
    bytes_data = _normalize_pdf(bytes_data)
    rd = PdfReader(BytesIO(bytes_data))
    wt = PdfWriter()

    [wt.add_page(p) for p in rd.pages]

    wt.add_metadata({ISSUE_NAME: ISSUE_DATA, SIGNATURE_METADATA_NAME: b64encode(sign)})
    ret = ""
    with BytesIO() as stream:
        wt.write(stream)
        stream.seek(0)
        ret = stream.read()
    wt.close()
    return ret


def get_sign(bytes_data):
    rd = PdfReader(BytesIO(bytes_data))
    try:
        return rd.metadata.pop(SIGNATURE_METADATA_NAME)
    except:
        return None
