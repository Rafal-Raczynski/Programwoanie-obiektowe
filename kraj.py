import sys
from os import walk, path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout, QScrollArea
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
        self.__prepare_import_button()
        self.__prepare_chart_panel()

    # def __prepare_chart_panel(self):
    #     fig = Figure(figsize=(5, 3), dpi=100)
    #     chart = FigureCanvasQTAgg(fig)
    #     self.__layout.addWidget(chart, 0, 0, 8, 3)

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

    def __prepare_import_button(self):
        button = ButtonImport(".csv")
        self.__layout.addWidget(button, 10, 10)
        self.__filepath = button.get_filepath()
        while True:
            if button.handle_select_file() == 0:
                a = ReadData(button.get_filepath())
                scroll = ScrollButtons(a.get_list_of_all_countries())
                break
        # countries = a.get_list_of_all_countries()

        self.__layout.addWidget(scroll, 5, 10, 5, 2)


    # self.__layout.addWidget(scroll, 1, 10, 9, 1)

    # def __prepare_buttons2(self):
    #     a = ReadData("time_series_covid19_confirmed_global.csv", "Poland")
    #     scroll = ScrollButtons(a.get_list_of_all_countries())
    #     self.__layout.addWidget(scroll, 1, 10, 9, 1)
    # ebeebe


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
            print("Please choose file one more time")
            return 1
        return 0
        # Data = ReadData(self.__filepath, "Poland")
        # self.scroll = ScrollButtons(Data.get_list_of_all_countries())


class ReadData:
    def __init__(self, filepath):
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


class ScrollButtons(QScrollArea):
    def __init__(self, all_countries):
        super().__init__()
        self.__all_countries = all_countries
        self.__data = Plot("time_series_covid19_confirmed_global.csv")
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

    def handle_selected_countries(self, name):
        print("Clicked:", name)
        if name in self.__data.selected_countries:
            self.__data.remove_country(name)
        else:
            self.__data.add_country(name)
        self.__data.display_selected_data()
        self.__data.show()
    #
    # def remove(self, name):
    #     return lambda _: self.__data.add_country(name)

    # def add(self, name):
    #     return lambda _: self.__data.add_country(name)

    # def show(self):
    #     return lambda _: self.__data.display_selected_data()


if __name__ == "__main__":
    app = QApplication([])

    # accepted_formats = (".jpg", ".png")
    img_browser = Covid(1000, 600)
    # XD = ReadData("/mnt/c/Kodowanie2/projekcik/Programowanie-obiektowe/time_series_covid19_confirmed_global.csv",
    #               ["Poland", "Russia"])

    sys.exit(app.exec_())
