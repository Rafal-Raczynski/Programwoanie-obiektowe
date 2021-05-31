from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


class PdfReportGenerator:
    def __init__(self):
        self.__title = f"Report from 'COVID-21' app"
        dt = datetime.now()
        dt_string = dt.strftime("%d.%m.%Y %H:%M:%S")
        self.__subtitle = f"({dt_string})"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Helvetica", 24)
        title = self.__title
        subtitle = self.__subtitle
        title_magic_offset, subtitle_magic_offset, img_magic_offset = 100, 130, 700
        title_x, title_y = A4[0] / 2, A4[1] - title_magic_offset
        subtitle_x, subtitle_y = A4[0] / 2, A4[1] - subtitle_magic_offset
        img_x, img_y = 0, A4[1] - img_magic_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.drawCentredString(subtitle_x, subtitle_y, subtitle)
        canvas.drawImage(img, img_x, img_y)

        return canvas
