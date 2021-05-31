import sys
from os import walk, path

from plot import Plot
from pdf_generator import PdfReportGenerator

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout, QScrollArea, QMessageBox, QLineEdit, QSlider
from reportlab.lib.utils import ImageReader


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__init_view(width, height)
        self.__prepare_buttons()
        self.__prepare_pdf_button()

    def __init_view(self, width, height):
        self.setWindowTitle("Covid-21")
        self.__layout = QGridLayout()
        elems = QGroupBox()
        elems.setLayout(self.__layout)

        self.setGeometry(0, 0, width, height)
        self.setCentralWidget(elems)
        self.show()

    def __prepare_buttons(self):
        button = ButtonImport(".csv")
        self.__layout.addWidget(button, 10, 17)
        button.clicked.connect(button.handle_select_file)
        while True:
            if button.handle_select_file() == 0:
                break
        a = ReadData(button.get_filepath())
        print(a.get_amount_of_days())
        plot = Plot(button.get_filepath())
        plot.set_x_lim(100, 200)
        scroll = ScrollButtons(a.get_list_of_all_countries(), button.get_filepath(),
                               plot)
        slider = Slider()
        self.__layout.addWidget(scroll, 2, 15, 6, 3)
        filtr = Filtr(a.get_list_of_all_countries(), button.get_filepath(), scroll)
        self.__layout.addWidget(filtr, 0, 15, 1, 3)
        self.__layout.addWidget(filtr.button, 1, 15, 1, 3)
        self.__layout.addWidget(plot, 0, 0, 8, 5)
        # self.__layout.addWidget(slider, 9, 0, 5, 1)

    def __prepare_pdf_button(self):
        name = "Export to PDF"
        graph = Plot("time_series_covid19_confirmed_global.csv")
        pdf_button = PdfSaveButton(name, graph)
        self.__layout.addWidget(pdf_button, 10, 15)


class ReadData:
    def __init__(self, filepath):
        self.__amount_of_days = None
        self.__filepath = filepath
        self.__list_of_countries = list()
        self.__read_all_countries_data()

    def __read_all_countries_data(self):
        i = 1
        with open(self.__filepath, "r") as f:
            for line in f:
                possible_region = line.split(",")[0]
                if i != 1 and possible_region == "":
                    country = line.split(",")[1]
                    if self.__amount_of_days is None:
                        self.__amount_of_days = len(line.split(",")[4:])
                    self.__list_of_countries.append(country)

                i = i + 1

    def get_amount_of_days(self):
        return self.__amount_of_days

    def get_list_of_all_countries(self):
        return self.__list_of_countries


class ButtonImport(QPushButton):
    def __init__(self, accepted_formats):
        super().__init__("Import")
        self.__accepted_formats = accepted_formats
        self.__filepath = None
        self.scroll = None
        self.clicked.connect(self.handle_select_file)

    def get_filepath(self):
        return self.__filepath

    def handle_select_file(self):
        self.__filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        file_extension = path.splitext(self.__filepath)[1].lower()
        if file_extension not in self.__accepted_formats:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong file!")
            msg.setInformativeText("Please choose file again")
            msg.setWindowTitle("Error")
            msg.exec_()
            print("Wrong file! Please choose file again")
            return 1
        return 0


class ScrollButtons(QScrollArea):
    def __init__(self, all_countries, filepath, plot: Plot):
        super().__init__()
        self.__filepath = filepath
        self.__all_countries = all_countries
        self.__data = plot
        self.__init_view()

    def __init_view(self):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for i in self.__all_countries:
            name = i
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, n=name: self.handle_selected_countries(n))
            btn_layout.addRow(btn)
        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)

    def set_all_countries(self, countries):
        self.__all_countries = countries
        self.__init_view()

    def handle_selected_countries(self, name):
        print("Clicked:", name)
        if name in self.__data.selected_countries:
            self.__data.remove_country(name)
        else:
            self.__data.add_country(name)
        self.__data.display_selected_data()
        self.__data.show()


class Filtr(QLineEdit):
    def __init__(self, all_countries, filepath, scroll: ScrollButtons):
        super().__init__()
        self.__filepath = filepath
        self.__all_countries = all_countries
        self.__filtred_countries = list()
        self.scroll = scroll
        self.button = QPushButton("Filtr")
        self.button.clicked.connect(self.__filtr_countries)

    def __filtr_countries(self):
        length = len(self.text())
        for country in self.__all_countries:
            if self.text().upper() == country[0:length].upper() and country not in self.__filtred_countries:
                self.__filtred_countries.append(country)
            elif self.text().upper() != country[0:length].upper() and country in self.__filtred_countries:
                self.__filtred_countries.remove(country)
        self.__update_buttons()

    def __update_buttons(self):
        self.scroll.set_all_countries(self.__filtred_countries)


class Slider(QSlider):
    def __init__(self):
        super().__init__()


class PdfSaveButton(QPushButton):
    def __init__(self, name, chart):
        super().__init__(name)
        self.__chart = chart
        self.__pdf_generator = PdfReportGenerator()

        self.clicked.connect(self.__save_btn_action)

    def __save_btn_action(self):
        img_data = self.__chart.display_selected_data()
        img = ImageReader(img_data)

        filename = self.__prepare_file_chooser()
        self.__pdf_generator.create_and_save_report(img, filename)

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="All Files (*)")
        return filename


if __name__ == "__main__":
    app = QApplication([])

    img_browser = Covid(1000, 600)

    sys.exit(app.exec_())
