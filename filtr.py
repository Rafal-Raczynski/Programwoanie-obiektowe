from PyQt5.QtWidgets import QPushButton, QLineEdit
from buttons import ScrollButtons


class Filtr(QLineEdit):
    def __init__(self, all_countries, scroll: ScrollButtons):
        super().__init__()
        self.__all_countries = all_countries
        self.__filtred_countries = list()
        self.setPlaceholderText("Enter country name...")
        self.scroll = scroll
        self.button = QPushButton("Filter")
        self.button.clicked.connect(self.__filtr_countries)

    def __filtr_countries(self):
        for country in self.__all_countries:
            if self.text().upper() in country.upper() and country not in self.__filtred_countries:
                self.__filtred_countries.append(country)
            elif self.text().upper() not in country.upper() and country in self.__filtred_countries:
                self.__filtred_countries.remove(country)
        self.__update_buttons()
        
    def __update_buttons(self):
        self.scroll.set_all_countries(self.__filtred_countries)
