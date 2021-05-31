from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


class PdfReportGenerator:

    def __init__(self):
        self.__author = "Nobody"
        self.__title = f"Sin(x) report ({date.today()})"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setAuthor(self.__author)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman", 40)
        title = "Sin(x) -- report"
        title_magic_offset, img_magic_offset = 100, 600
        title_x, title_y = A4[0] / 2, A4[1] - title_magic_offset
        img_x, img_y = 0, A4[1] - img_magic_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawImage(img, img_x, img_y)

        return canvas
