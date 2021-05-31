from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from io import BytesIO


class Plot(FigureCanvasQTAgg):
    __IMG_FORMAT = "png"

    def __init__(self, filepath, width=4, height=4, dpi=100):
        self.__filepath = filepath
        self.selected_countries = list()
        self.__fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.__fig)
        self.__axes = None
        self.__low = None
        self.__up = None

    def __read_countries_data(self):
        countries_data = dict()
        with open(self.__filepath, "r") as f:
            for line in f:
                if line.split(",")[0] == "":
                    maybe_country = line.split(",")[1]
                else:
                    maybe_country = line.split(",")[1] + ", " + line.split(",")[0]
                if maybe_country in self.selected_countries:
                    line = line.strip()
                    n_of_patients_in_time = self.__get_patients_as_vector(line)
                    countries_data[maybe_country] = n_of_patients_in_time
        return countries_data

    @staticmethod
    def __get_patients_as_vector(country_data_line):
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
        self.__axes.set_title("COVID-19 cases graph for countries")
        self.__axes.grid()
        self.__axes.legend()
        self.__axes.set_xlim(self.__low, self.__up)
        self.draw()
        self.__image = self.__get_img()
        self.__axes.clear()

    def clear_plot(self):
        self.__axes.clear()

    def set_x_lim(self, low, up):
        self.__low = low
        self.__up = up
        self.display_selected_data()

    def display_selected_data(self):
        countries_data = self.__read_countries_data()
        self.__display_data(countries_data)

    def add_country(self, name):
        self.selected_countries.append(name)

    def remove_country(self, name):
        self.selected_countries.remove(name)

    def __get_img(self):
        img_data = BytesIO()
        self.__fig.savefig(img_data, format=self.__IMG_FORMAT)

        seek_offset = 0
        img_data.seek(seek_offset)

        return img_data

    def get_plot(self):
        return self.__image
