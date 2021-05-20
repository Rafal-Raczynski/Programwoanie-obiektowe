import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__init_view(width, height)
        self.__prepare_buttons()
        self.__prepare_chart_panel()

    def __prepare_chart_panel(self):
        fig = Figure(figsize=(5, 3), dpi=100)
        chart = FigureCanvasQTAgg(fig)
        self.__layout.addWidget(chart, 0, 0, 8, 3)

    def __init_view(self, width, height):
        self.setWindowTitle("Covid-21")

        self.__layout = QGridLayout()
        elems = QGroupBox()
        elems.setLayout(self.__layout)

        self.setGeometry(0, 0, width, height)
        self.setCentralWidget(elems)
        self.show()

    def __prepare_buttons(self):
        button = ButtonImport("csv")
        self.__layout.addWidget(button, 10, 10)


class ButtonImport(QPushButton):
    def __init__(self, accepted_formats):
        super().__init__("Import")
        self.__accepted_formats = accepted_formats
        self.clicked.connect(self.__handle_select_file)

    def __handle_select_file(self):
        self.__filepath = QFileDialog.getOpenFileName(self, "Select imgs dir")
        print(self.__filepath)

    def get_filename(self):
        return self.__filepath


class ReadData:
    def __init__(self, filepath, selected_countries):
        self.__filename = filepath
        self.__list_of_countries = list()
        self.__read_all_countries_data(filepath)
        self.selected_countries = selected_countries
        self.display_selected_data(filepath, selected_countries)

    def __read_all_countries_data(self, filename):
        i = 1
        with open(filename, "r") as f:
            for line in f:
                possible_region = line.split(",")[0]
                if i != 1 and possible_region == "":
                    country = line.split(",")[1]
                    self.__list_of_countries.append(country)

                i = i + 1

    def read_countries_data(self, filepath, countries):
        countries_data = dict()

        with open(filepath, "r") as f:
            for line in f:
                maybe_country = line.split(",")[1]

                if maybe_country in countries:
                    line = line.strip()
                    n_of_patients_in_time = self.get_patients_as_vector(line)

                    countries_data[maybe_country] = n_of_patients_in_time

        return countries_data

    def get_patients_as_vector(self, country_data_line):
        n_of_unimportant_column = 4
        n_of_patients_in_time = country_data_line.split(",")[n_of_unimportant_column:]
        n_of_patients_in_time = [int(val) for val in n_of_patients_in_time]

        return n_of_patients_in_time

    def get_list_of_all_countries(self):
        return self.__list_of_countries

    def display_data(self, n_of_patients_in_countries):

        for country, data in n_of_patients_in_countries.items():
            plt.semilogy(data, label=country)

        plt.xlabel("Days (subsequent data)")
        plt.ylabel("Total number of patients")
        plt.title("Covid-19 number of patients since 01.01.2020")
        plt.grid()
        plt.legend()
        plt.show()

    def display_selected_data(self, filepath, countries):
        countries_data = self.read_countries_data(filepath, countries)
        self.display_data(countries_data)


if __name__ == "__main__":
    app = QApplication([])

    # accepted_formats = (".jpg", ".png")
    img_browser = Covid(600, 300)
    # XD = ReadData("time_series_covid19_confirmed_global.csv", ["Poland","Russia"])
    # print(XD.get_list_of_all_countries())  # .keys())

    sys.exit(app.exec_())
