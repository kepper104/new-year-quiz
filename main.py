import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        for i in self.buttonGroup.buttons():
            i.clicked.connect(self.bruh)

    def bruh(self):
        cost = self.sender().text()
        id = int(self.sender().objectName().split('_')[1])
        # print(id, cost)
        self.read_csv(id // 10, cost)

    def read_csv(self, file_id, cost):

        with open(f"{file_id}.csv", 'r', encoding='utf-8') as file:
            res = csv.reader(file, delimiter=';')
            for i in res:
                if i[0] == cost:
                    print(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
