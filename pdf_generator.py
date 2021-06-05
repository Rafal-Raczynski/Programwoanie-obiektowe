from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from textwrap import wrap
from datetime import datetime
from PyQt5.QtWidgets import QPushButton, QMessageBox, QFileDialog
from plot_and_data import Plot
from sliders import Sliders


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


class PdfSaveButton(QPushButton):
    def __init__(self, name, plot: Plot, slider: Sliders):
        super().__init__(name)
        self.__plot = plot
        self.__slider = slider
        self.__pdf_generator = PdfReportGenerator()

        self.clicked.connect(self.__save_btn_action)

    def __save_btn_action(self):
        img_data = self.__plot.get_plot()
        countries = self.__plot.get_countries()
        img = ImageReader(img_data)

        filename = self.__prepare_file_chooser()
        timespan = [self.__slider.get_low_slider_date(), self.__slider.get_high_slider_date()]
        self.__pdf_generator.create_and_save_report(img, countries, timespan, filename)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Data exported to the file:")
        msg.setInformativeText(filename)
        msg.setWindowTitle("OK")
        msg.exec_()

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="*.pdf")
        return filename
