import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QTabWidget

from buttons import *
from filtr import *
from pdf_generator import *
from plot_and_data import *
from sliders import *


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__width = width
        self.__height = height
        self.__init_view()
        self.__tabs = QTabWidget()
        self.__prepare_layout()

    def __init_view(self):
        self.setWindowTitle("Covid-21")
        self.__layout = QGridLayout()
        elems = QGroupBox()
        elems.setLayout(self.__layout)

        self.setGeometry(0, 0, self.__width, self.__height)
        self.setCentralWidget(elems)
        self.show()

    def __prepare_layout(self):
        import_data = Import(".csv")
        reset = QPushButton("Reset")
        reset.clicked.connect(self.__handle_reset)
        self.__layout.addWidget(reset, 10, 17)
        a = ReadData(import_data.get_filepath())
        plot = Plot(import_data.get_filepath())

        scroll = ScrollButtons(a.get_list_of_all_countries(),
                               plot)
        self.__layout.addWidget(scroll, 2, 15, 6, 3)

        filtr = Filtr(a.get_list_of_all_countries(), scroll)
        self.__layout.addWidget(filtr, 0, 15, 1, 3)
        self.__layout.addWidget(filtr.button, 1, 15, 1, 3)

        self.__layout.addWidget(plot, 0, 0, 8, 5)

        slider = Sliders(a.get_amount_of_days(), plot)
        self.__layout.addWidget(slider.get_low_slider(), 9, 1, 1, 4)
        self.__layout.addWidget(slider.get_high_slider(), 10, 1, 1, 4)
        self.__layout.addWidget(slider.get_low_slider_date_text(), 9, 0, 1, 1)
        self.__layout.addWidget(slider.get_high_slider_date_text(), 10, 0, 1, 1)

        pdf_button = PdfSaveButton("Export to PDF", plot, slider)
        self.__layout.addWidget(pdf_button, 10, 15)

    def __handle_reset(self):
        self.__init_view()
        self.__prepare_layout()


class ButtonReset(QPushButton):
    def __init__(self, covid: Covid):
        super().__init__("Reset")
        self.__covid = covid
        self.clicked.connect(covid.prepare_layout)


