import PyPDF2

class PDFProcessor:
    @staticmethod
    def process_pdf(file_path):
        pdf_text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfFileReader(file)
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                pdf_text += page.extractText()
        return pdf_text