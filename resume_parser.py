import PyPDF2

def extract_text_from_pdf(file):
    try:
        if file.name.endswith(".txt"):
            return str(file.read(), "utf-8")

        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        print("Error:", e)
        return ""