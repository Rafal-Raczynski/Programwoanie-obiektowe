import sys
from os import walk, path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout, QScrollArea, QLineEdit, QToolButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class Plot(FigureCanvasQTAgg):
    def __init__(self, filepath, width=4, height=4, dpi=100):
        self.__filepath = filepath
        self.selected_countries = list()
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.__fig)
        self.__axes = None

    def __read_countries_data(self):
        countries_data = dict()
        with open(self.__filepath, "r") as f:
            for line in f:
                maybe_country = line.split(",")[1]
                if maybe_country in self.selected_countries:
                    line = line.strip()
                    n_of_patients_in_time = self.__get_patients_as_vector(line)
                    countries_data[maybe_country] = n_of_patients_in_time
        return countries_data

    def __get_patients_as_vector(self, country_data_line):
        n_of_unimportant_column = 4
        n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
        n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]
        return n_of_patients_in_time

    def __display_data(self, n_of_patients_in_countries):
        if self.__axes is None:
            self.__axes = self.__fig.add_subplot(111)
        for country, data in n_of_patients_in_countries.items():
            self.__axes.semilogy(data, label=country)
        self.__axes.set_xlabel("Days (subsequent data)")
        self.__axes.set_ylabel("Total number of patients")
        self.__axes.set_title("Covid-19 number of patients since 01.01.2020")
        self.__axes.grid()
        self.__axes.legend()
        self.draw()
        self.__axes.clear()

    def display_selected_data(self):
        countries_data = self.__read_countries_data()
        self.__display_data(countries_data)

    def add_country(self, name):
        self.selected_countries.append(name)

    def remove_country(self, name):
        self.selected_countries.remove(name)


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__init_view(width, height)
        self.__prepare_buttons()

    def __prepare_chart_panel(self):
        fig = Plot("time_series_covid19_confirmed_global.csv")
        fig.add_country("Poland")
        fig.display_selected_data()
        self.__layout.addWidget(fig, 0, 0, 8, 3)

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
        self.__layout.addWidget(button, 10, 10)
        button.clicked.connect(button.handle_select_file)
        while True:
            if button.handle_select_file() == 0:
                break
        a = ReadData(button.get_filepath())
        plot = Plot(button.get_filepath())
        scroll = ScrollButtons(a.get_list_of_all_countries(), button.get_filepath(),
                               plot)
        self.__layout.addWidget(scroll, 5, 10, 5, 2)
        filtr = Filtr(a.get_list_of_all_countries(), button.get_filepath(), scroll)
        self.__layout.addWidget(filtr, 1, 10, 1, 2)
        self.__layout.addWidget(filtr.button, 2, 10, 1, 2)
        self.__layout.addWidget(scroll, 5, 10, 5, 2)
        self.__layout.addWidget(plot, 0, 0, 8, 3)


class ReadData:
    def __init__(self, filepath=None):
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
                    self.__list_of_countries.append(country)

                i = i + 1

    def get_list_of_all_countries(self):
        return self.__list_of_countries

    def set_filepath(self, file):
        self.__filepath = file


class ButtonImport(QPushButton):
    def __init__(self, accepted_formats):
        super().__init__("Import")
        self.__accepted_formats = accepted_formats
        self.__filepath = None
        self.clicked.connect(self.handle_select_file)

    def get_filepath(self):
        return self.__filepath

    def handle_select_file(self):
        self.__filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        file_extension = path.splitext(self.__filepath)[1].lower()
        if file_extension not in self.__accepted_formats:
            print("Please choose file one more time")
            return 1
        return 0


class ScrollButtons(QScrollArea):
    def __init__(self, all_countries, filepath, plot: Plot):
        super().__init__()
        self.__all_countries = all_countries
        self.__filepath = filepath
        self.__data = plot
        self.__init_view()

    def get_data(self):
        return self.__data

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

    def handle_selected_countries(self, name):
        print("Clicked:", name)
        if name in self.__data.selected_countries:
            self.__data.remove_country(name)
        else:
            self.__data.add_country(name)
        self.__data.display_selected_data()
        self.__data.show()

    def set_all_countries(self, countries):
        self.__all_countries = countries
        self.__init_view()


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
        print(self.__filtred_countries)


if __name__ == "__main__":
    app = QApplication([])

    img_browser = Covid(1000, 600)

    sys.exit(app.exec_())
