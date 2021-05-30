import sys
from os import walk, path

from plot import Plot

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QGroupBox, QVBoxLayout, \
    QGridLayout, QLabel, QMainWindow, QFormLayout, QScrollArea, QMessageBox


class Covid(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__init_view(width, height)
        self.__prepare_import_button()

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
        while True:
            if button.handle_select_file() == 0:
                a = ReadData(button.get_filepath())
                scroll = ScrollButtons(a.get_list_of_all_countries(), button.get_filepath())
                break

        self.__layout.addWidget(scroll, 5, 10, 5, 2)
        self.__layout.addWidget(scroll.data, 0, 0, 8, 3)


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
    def __init__(self, all_countries, filepath):
        super().__init__()
        self.__all_countries = all_countries
        self.data = Plot(filepath)
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
        if name in self.data.selected_countries:
            self.data.remove_country(name)
        else:
            self.data.add_country(name)
        self.data.display_selected_data()
        self.data.show()


if __name__ == "__main__":
    app = QApplication([])

    img_browser = Covid(1000, 600)

    sys.exit(app.exec_())
