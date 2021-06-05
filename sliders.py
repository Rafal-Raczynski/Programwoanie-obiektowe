from PyQt5.QtWidgets import QLabel, QSlider
from PyQt5 import QtCore
from plot_and_data import Plot
from datetime import datetime, timedelta


class Sliders(QSlider):
    def __init__(self, max_value, plot: Plot, min_value=1, min_width=150):
        super().__init__()
        self.__min_value = min_value
        self.__max_value = max_value
        self.__min_width = min_width
        self.__plot = plot
        self.__low_slider = self.__prepare_low_slider()
        self.__high_slider = self.__prepare_high_slider()
        self.__low_slider_date = QLabel()
        self.__high_slider_date = QLabel()
        self.__default_variables()

    def get_low_slider_date_text(self):
        return self.__low_slider_date

    def get_high_slider_date_text(self):
        return self.__high_slider_date

    def __prepare_slider(self, value):
        slider = QSlider(QtCore.Qt.Horizontal)
        slider.setMinimum(self.__min_value)
        slider.setMaximum(self.__max_value)
        slider.setMinimumWidth(self.__min_width)
        slider.setValue(value)
        return slider

    def __prepare_low_slider(self):
        slider = self.__prepare_slider(self.__min_value)
        slider.valueChanged.connect(lambda checked: self.__change_low())
        return slider

    def __prepare_high_slider(self):
        slider = self.__prepare_slider(self.__max_value)
        slider.valueChanged.connect(lambda checked: self.__change_high())
        return slider

    def __change_low(self):
        self.__plot.set_x_low_lim(self.__low_slider.value())
        new_value = self.__low_slider.value()
        high_value = self.__high_slider.value()
        if new_value >= high_value:
            self.__low_slider.setValue(high_value - 1)
        self.get_low_slider_date()

    def __change_high(self):
        self.__plot.set_x_high_lim(self.__high_slider.value())
        new_value = self.__high_slider.value()
        low_value = self.__low_slider.value()
        if new_value <= low_value:
            self.__high_slider.setValue(low_value + 1)
        self.get_high_slider_date()

    def __default_variables(self):
        start = "22-01-2020"
        start_date = "22-01-20"
        date = datetime.strptime(start_date, "%d-%m-%y")
        end_date = date + timedelta(days=self.__max_value - 1)
        end_date = end_date.strftime("%d-%m-%Y")
        self.__low_slider_date.setText(start)
        self.__high_slider_date.setText(end_date)

    def get_low_slider(self):
        return self.__low_slider

    def get_high_slider(self):
        return self.__high_slider

    def get_low_slider_date(self):
        start_date = "22-01-20"
        date = datetime.strptime(start_date, "%d-%m-%y")
        end_date = date + timedelta(days=self.__low_slider.value() - 1)
        end_date = end_date.strftime("%d-%m-%Y")
        self.__low_slider_date.setText(end_date)
        return end_date

    def get_high_slider_date(self):
        start_date = "22-01-20"
        date = datetime.strptime(start_date, "%d-%m-%y")
        end_date = date + timedelta(days=self.__high_slider.value() - 1)
        end_date = end_date.strftime("%d-%m-%Y")
        self.__high_slider_date.setText(end_date)
        return end_date
