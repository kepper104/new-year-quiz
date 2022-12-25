import sys
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from threading import Thread
from os import getcwd
from os import path
import matplotlib.pyplot as plt
import pygame

# import playsound
team_count = 3

cur_team = 1
points = {}
for i in range(1, team_count + 1):
    points[i] = 0
print(points)

rubrics = ["История Нового Года", "Снеговики", "Новогодние Блюда",
           "Цитаты из фильмов", "Новый Год до Революции", "Dead Мороз", "Загадки", "Новый Год в Других Странах"]


if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(
        Qt.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

all_music = []


def playMusic(file_name):
    sound = SoundPlayer(file_name)
    all_music.append(Thread(target=sound.play_sound, args=()))
    all_music[-1].start()


def killAllMusic():
    for i in all_music:
        i.stop()


class SoundPlayer():
    def __init__(self, file_name):
        self.name = file_name

    def play_sound(self):

        cwd = getcwd()
        audio_file = path.join(cwd, "music", self.name)
        audio_file = audio_file.replace("\\", " /").replace(" ", "")

        pygame.mixer.music.load(audio_file)

        pygame.mixer.music.play(1)

        while True:
            pygame.time.Clock().tick(10)


class App(QMainWindow):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        super().__init__()

        # USEFUL STUFF
        # ------------------------------
        use_bg_image = False
        show_window_borders = True
        # ------------------------------

        # playsound("Ra-ta-ta.mp3")

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
        if id == 65:
            self.music_pause("alice_pause1.mp3")
        elif id == 42:
            self.music_pause("alice_pause2.mp3")
        elif id // 10 == 6:
            self.read_music(id)
        else:
            self.read_csv(id // 10, cost)

    def music_pause(self, music_name):
        x = self.geometry().x()
        y = self.geometry().y()
        self.window = QuestionWindow(self, pos=(
            x, y), isMusic=True, music_name=music_name)
        self.window.show()

    def read_csv(self, file_id, cost):
        playMusic("next.mp3")
        with open(f"{file_id}.csv", 'r', encoding='utf-8') as file:
            res = csv.reader(file, delimiter=';', quotechar='"')
            for i in res:
                if i[0] == cost:
                    x = self.geometry().x()
                    y = self.geometry().y()
                    # print(self.geometry())
                    self.window = QuestionWindow(
                        self, q=i[1], a=i[2], p=i[0], r=rubrics[file_id], pos=(x, y))
                    self.window.show()
                # print(i)
    # def read_music(self, file_id):


class QuestionWindow(QWidget):
    def __init__(self, *args, q="Музыкальная пауза", a='a-Error', p='', r="", pos=(0, 0), isMusic=False, music_name=''):
        super().__init__()
        uic.loadUi("question.ui", self)
        print(pos)
        self.setGeometry(pos[0], pos[1], 1513, 710)
        self.setWindowTitle('Вопрос')
        self.question = q
        self.answer = a
        self.price = p
        self.rubric = r
        self.shownAns = False
        self.showBorder = True
        self.isMusic = isMusic
        self.music_name = music_name
        print(p, r, q, a, pos, isMusic, music_name)

        if not self.showBorder:
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.setWindowFlag(Qt.FramelessWindowHint)

        self.label_3.setText(
            f"""<html><head/><body><p align="center"><span style=" font-size:26pt; color:#5e9ad7;">{q}</span></p></body></html>""")

        real_rubric = """<html><head/><body><p align="center"><span style=" font-size:28pt; color:#e88a2c;">""" + \
            r + " " + p + """</span></p></body></html>"""

        self.label_2.setText(real_rubric)

    def showAnswer(self):
        self.label_3.setText(
            f"""<html><head/><body><p align="center"><span style=" font-size:26pt; color:#5e9ad7;">{self.answer}</span></p></body></html>""")

    def keyPressEvent(self, event):
        global cur_team, points
        print(event.key())
        if event.key() == 16777220:
            if not self.shownAns:
                if self.isMusic:
                    playMusic(self.music_name)
                else:
                    self.showAnswer()
                self.shownAns = True

            else:
                self.close()
        elif event.key() == 89:
            points[cur_team + 1] += int(self.price)
            plot_histogram((cur_team + 1, self.price))
            cur_team += 1
            cur_team //= 3
        elif event.key() == 78:
            plot_histogram()
            cur_team += 1
            cur_team //= 3


# 89 Y
# 78 N

def plot_histogram(last_points=(0, 0)):
    teams = list(points.keys())
    team_points = list(points.values())

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    ax.set_ylabel("Очки", fontsize=16)
    ax.set_title("Результаты", fontsize=16)
    colors = [f"C{i}" for i in range(len(teams))]

    for i, team in enumerate(teams):
        ax.bar(team, team_points[i], color=colors[i])
        ax.text(team, team_points[i] - 20, team_points[i],
                ha="center", color="black", fontsize=14)

    if last_points != (0, 0):
        ax.text(last_points[0], team_points[last_points[0] - 1] + 5, "+" + str(last_points[1]), ha="center",
                color="black", fontsize=14)

    plt.xticks(teams, ["Команда {}".format(i) for i in teams], fontsize=13)

    plt.yticks(team_points, fontsize=14)
    print("before show")
    plt.show()
    print("shown")
    # plot_thread = Thread(target=plt.show, args=())
    # plot_thread.start()
    # plt.show()

    print(points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
