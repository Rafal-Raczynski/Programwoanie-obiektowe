from PyQt5.QtWidgets import QPushButton, QGroupBox, QFormLayout, QScrollArea
from plot_and_data import Plot


class ScrollButtons(QScrollArea):
    def __init__(self, all_countries, plot: Plot):
        super().__init__()
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
        if name in self.__data.selected_countries:
            self.__data.remove_country(name)
        else:
            self.__data.add_country(name)
        self.__data.display_selected_data()
        self.__data.show()
