import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from playsound import playsound
from threading import Thread
rubrics = ["История Нового Года", "Снеговики", "Новогодние Блюда",
           "Цитаты из фильмов", "Новый Год до Революции", "Dead Мороз", "Загадки", "Новый Год в Других Странах"]


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(
        Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # playsound("Ra-ta-ta.mp3")

        use_bg_image = False
        show_window_borders = True
        if use_bg_image:
            self.bg_label = QLabel(self)
            self.bg_label.setPixmap(QPixmap("bg-main.png"))
            self.bg_label.setFixedSize(1513, 710)
            self.bg_label.move(0, 0)

        uic.loadUi('design.ui', self)
        self.setWindowTitle("Новый Год 2023")
        # self.setGeometry(300, 300, 1513, 710)

        if not show_window_borders:
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.setWindowFlag(Qt.FramelessWindowHint)

        for i in self.buttonGroup.buttons():
            i.clicked.connect(self.bruh)
        # self.pushButton.clicked.connect(self.open_question_window)

    def bruh(self):

        cost = self.sender().text()
        print(cost)
        # self.sender().setParent(None)
        self.sender().setText("")
        # self.sender().setStyle()
        self.sender().setEnabled(False)

        id = int(self.sender().objectName().split('_')[1])
        # print(id, cost)
        if id // 10 == 6:
            self.read_music(id)
        else:
            self.read_csv(id // 10, cost)

    def read_csv(self, file_id, cost):
        with open(f"{file_id}.csv", 'r', encoding='utf-8') as file:
            res = csv.reader(file, delimiter=';', quotechar='"')
            for i in res:
                if i[0] == cost:
                    self.window = QuestionWindow(
                        self, q=i[1], a=i[2], p=i[0], r=rubrics[file_id])
                    self.window.show()
                    # print(i)
    def read_music(self, file_id):
        print(file_id)

class QuestionWindow(QWidget):
    def __init__(self, *args, q="q-Error", a='a-Error', p='Error', r="Error"):
        super().__init__()
        uic.loadUi("question.ui", self)
        self.setGeometry(300, 300, 1513, 710)
        self.setWindowTitle('Вопрос')
        self.question = q
        self.answer = a
        self.price = p
        self.rubric = r
        self.shownAns = False
        print(p, r, q, a)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.label_3.setText(
            f"""<html><head/><body><p align="center"><span style=" font-size:26pt; color:#5e9ad7;">{q}</span></p></body></html>""")

        real_rubric = """<html><head/><body><p align="center"><span style=" font-size:28pt; color:#e88a2c;">""" + \
            r + " " + p + """</span></p></body></html>"""

        self.label_2.setText(real_rubric)

        # self.pushButton.clicked.connect(self.close)
    def showAnswer(self):
        self.label_3.setText(
            f"""<html><head/><body><p align="center"><span style=" font-size:26pt; color:#5e9ad7;">{self.answer}</span></p></body></html>""")
        # self.close()
    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777220:
            if not self.shownAns:
                print("showing")
                self.shownAns = True
                self.showAnswer()
            else:
                self.close()

    # def load_answer(self):

        # class AnswerWindow(QWidget):
        #     def __init__(self, *args, q="q-Error", a='a-Error', p='Error', r="Error"):
        #         super().__init__()
        #         uic.loadUi("question.ui", self)
        #         self.setGeometry(300, 300, 1513, 710)
        #         self.setWindowTitle('Вопрос')
        #         print(p, r, q, a)
        #         self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #         self.setWindowFlag(Qt.FramelessWindowHint)

        #         self.label_3.setText(
        #             f"""<html><head/><body><p align="center"><span style=" font-size:26pt; color:#5e9ad7;">{q}</span></p></body></html>""")

        #         real_rubric = """<html><head/><body><p align="center"><span style=" font-size:28pt; color:#e88a2c;">""" + \
        #             r + " " + p + """</span></p></body></html>"""

        #         self.label_2.setText(real_rubric)

        #         self.pushButton.clicked.connect(self.close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
