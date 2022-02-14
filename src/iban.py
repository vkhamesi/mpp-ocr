from tika import parser
from PIL import Image
import pytesseract
import io
import re
from schwifty import BIC


def getTextFromImage(image):
    
    text = pytesseract.image_to_string(image)
    text = text.replace("\n", "").replace(" ", "").upper()

    return text


def getTextFromPdf(file):

    content = file.read()

    raw = parser.from_buffer(content)
    text = raw["content"]
    text = text.replace("\n", "").replace(" ", "").upper()

    return text


def getImageFromPdf(file):

    for page_index in range(len(file)):
        page = file[page_index]
        images = []
        for _, img in enumerate(page.getImageList(), start=1):
            xref = img[0]
            base_image = file.extractImage(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    image = images[-1]

    return image


def getText(file):

    try:
        # If PDF
        if file.filename[-3:] == "pdf":
            # Try to retrieve text from PDF
            try:
                return getTextFromPdf(file)
            # If the PDF contains images
            except Exception:
                image = getImageFromPdf(file)
                return getTextFromImage(image)
        # If different type than PDF (image)
        else:
            image = Image.open(file)
            return getTextFromImage(image)
    except Exception:
        return None


def getIban(text):

    try:
        regex = "FR[a-zA-Z0-9]{2}\s?([0-9]{4}\s?){2}([0-9]{2})([a-zA-Z0-9]{2}\s?)([a-zA-Z0-9]{4}\s?){2}([a-zA-Z0-9]{1})([0-9]{2})\s?"
        iban = re.search(regex, text).group(0)
        return iban

    except Exception:
        return None


def checkIban(iban):

    try:

        _RIB_MAP = {
            'A':'1', 'B':'2', 'C':'3', 'D':'4', 'E':'5', 'F':'6', 'G':'7', 'H':'8', 'I':'9',
            'J':'1', 'K':'2', 'L':'3', 'M':'4', 'N':'5', 'O':'6', 'P':'7', 'Q':'8', 'R':'9',
            'S':'2', 'T':'3', 'U':'4', 'V':'5', 'W':'6', 'X':'7', 'Y':'8', 'Z':'9',
        }

        values = "".join(_RIB_MAP.get(char.upper(), char) for char in iban[4:])

        return int(values) % 97 == 0
    
    except:

        return False


def getBic(iban):

    try:
        bic = BIC.from_bank_code('FR', iban[4:9])
        return bic.compact
    
    except Exception:
        return None


def guess(file):

    text = getText(file)
    iban = getIban(text)

    if text is None:
        return None

    elif iban is None:
        return None

    else:
        bic = getBic(iban)
        return {"iban": iban, "bic": bic}