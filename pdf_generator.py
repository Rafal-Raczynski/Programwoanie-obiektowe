from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from textwrap import wrap


class PdfReportGenerator:
    def __init__(self):
        self.__title = f"Report from 'COVID-21' app"
        dt = datetime.now()
        dt_string = dt.strftime("%d.%m.%Y %H:%M:%S")
        self.__subtitle = f"{dt_string})"

    def create_and_save_report(self, img, countries, timespan, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, countries, timespan, pagesize)
        pdf_template.setTitle(self.__title)
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, countries, timespan, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Helvetica", 20)
        title = self.__title
        subtitle = "(Generated: " + self.__subtitle
        title_magic_offset, subtitle_magic_offset, img_magic_offset = 70, 100, 650
        title_x, title_y = A4[0] / 2, A4[1] - title_magic_offset
        subtitle_x, subtitle_y = A4[0] / 2, A4[1] - subtitle_magic_offset
        img_x, img_y = 0, A4[1] - img_magic_offset

        canvas.drawCentredString(title_x, title_y, title)
        canvas.setFont("Helvetica", 12)
        canvas.drawCentredString(subtitle_x, subtitle_y, subtitle)
        canvas.drawImage(img, img_x, img_y, A4[0], A4[1] / 2)


        countries_wrap = "\n".join(wrap(countries, 70))
        countries_text = canvas.beginText(A4[0] - 450, A4[1] - 180)
        for line in countries_wrap.splitlines(False):
            countries_text.textLine(line.rstrip())
        canvas.drawText(countries_text)

        timespan_end = ' - '.join(timespan)
        timespan = "Timespan: " + timespan_end
        canvas.drawCentredString(A4[0] / 2, A4[1] - 150, timespan)

        return canvas
