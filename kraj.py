import sys
from os import walk, path

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__init_view(width, height)
        self.__prepare_import_button()
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

    def __prepare_import_button(self):
        button = ButtonImport(".csv")
        while (button.get_filepath() == None):
            button.handle_select_file()
        self.__layout.addWidget(button, 10, 10)
        self.__filepath = button.get_filepath()
        print(self.__filepath)
        a = ReadData(button.get_filepath(), "Poland")
        scroll = ScrollButtons(a.get_list_of_all_countries())
        # countries = a.get_list_of_all_countries()

        self.__layout.addWidget(scroll, 5, 10, 5, 2)

    # self.__layout.addWidget(scroll, 1, 10, 9, 1)

    # def __prepare_buttons2(self):
    #     a = ReadData("time_series_covid19_confirmed_global.csv", "Poland")
    #     scroll = ScrollButtons(a.get_list_of_all_countries())
    #     self.__layout.addWidget(scroll, 1, 10, 9, 1)


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
        # Data = ReadData(self.__filepath, "Poland")
        # self.scroll = ScrollButtons(Data.get_list_of_all_countries())


class ReadData:
    def __init__(self, filepath, selected_countries):
        self.__filepath = filepath
        self.__list_of_countries = list()
        self.__read_all_countries_data()
        self.__selected_countries = selected_countries

    def __read_all_countries_data(self):
        i = 1
        with open(self.__filepath, "r") as f:
            for line in f:
                possible_region = line.split(",")[0]
                if i != 1 and possible_region == "":
                    country = line.split(",")[1]
                    self.__list_of_countries.append(country)

                i = i + 1

    def read_countries_data(self):
        countries_data = dict()

        with open(self.__filepath, "r") as f:
            for line in f:
                maybe_country = line.split(",")[1]

                if maybe_country in self.__selected_countries:
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

    def display_selected_data(self):
        countries_data = self.read_countries_data()
        self.display_data(countries_data)


class ScrollButtons(QScrollArea):
    def __init__(self, all_countries):
        super().__init__()
        self.__all_countries = all_countries
        self.__init_view()

    def __init_view(self):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        for i in self.__all_countries:
            name = i
            btn = QPushButton(name)
            # btn.clicked.connect((lambda name_to_show: lambda _: print(name_to_show))(name))
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)


if __name__ == "__main__":
    app = QApplication([])

    # accepted_formats = (".jpg", ".png")
    img_browser = Covid(600, 300)
    # XD = ReadData("/mnt/c/Kodowanie2/projekcik/Programowanie-obiektowe/time_series_covid19_confirmed_global.csv",
    #               ["Poland", "Russia"])

    sys.exit(app.exec_())
