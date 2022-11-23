import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.setWindowTitle("Новый Год 2023")
        self.setGeometry(300, 300, 1513, 710)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)

        for i in self.buttonGroup.buttons():
            i.clicked.connect(self.bruh)
        # self.pushButton.clicked.connect(self.open_question_window)

    def bruh(self):

        cost = self.sender().text()
        print(cost)

        id = int(self.sender().objectName().split('_')[1])
        # print(id, cost)
        self.read_csv(id // 10, cost)

    def read_csv(self, file_id, cost):
        with open(f"{file_id}.csv", 'r', encoding='utf-8') as file:
            res = csv.reader(file, delimiter=';')
            for i in res:
                if i[0] == cost:
                    self.open_question_window(i[1], i[2])
                    # print(i)

    def open_question_window(self, question, answer):
        self.window = QuestionWindow(self, q=question, a=answer)
        self.window.show()


class QuestionWindow(QWidget):
    def __init__(self, *args, q="q-Error", a='a-Error'):
        print(args[0])
        super().__init__()
        self.initUI(q, a)

    def initUI(self, q, a):
        self.setGeometry(300, 300, 1513, 710)
        self.setWindowTitle('Вопрос')

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.bg_label = QLabel(self)
        self.bg_label.setText("lol")
        self.bg_label.move(0, 0)
        self.bg_label.setFixedSize(1513, 710)
        self.bg_label.setPixmap(QPixmap("bg.png"))

        self.q_label = QLabel(self)
        self.q_label.setText(q)
        self.q_label.setWordWrap(True)
        self.q_label.move(370, 320)
        self.q_label.setFixedSize(500, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
