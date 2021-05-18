import math
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import UI
import matplotlib.pyplot as plt
import json

class MyWindow(QtWidgets.QMainWindow, UI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Build.clicked.connect(self.show_graph)
        self.pushButton.clicked.connect(self.approximate)
        self.pushButton_2.clicked.connect(self.aproximate_file)

    def aproximate_file(self):
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    x = data['x']
                    y = data['y']
                self.textBrowser.append('Ожидание...')
                self.textBrowser.repaint()

                first_index = 0
                second_index = 0
                third_index = 0

                for i in range(len(y)):
                    if y[i] > 0.2:
                        first_index = i
                        break
                for i in range(first_index, len(y)):
                    if y[i] > 0.5:
                        second_index = i
                        break
                for i in range(second_index, len(y)):
                    if y[i] > 0.8:
                        third_index = i
                        break

                array = func(x[first_index], y[first_index], x[second_index], y[second_index],
                             x[third_index], y[third_index])


                self.textBrowser.append(f'T={array[0]}')
                self.textBrowser.append(f't03={array[1]}')
                self.textBrowser.append(f'm={array[2]}')
                self.textBrowser.repaint()
            except:
                self.textBrowser.append('Ошибка')
                self.textBrowser.repaint()



    def approximate(self):
        self.textBrowser.append('Ожидание...')
        self.textBrowser.repaint()
        try:
            self.textBrowser.clear()
            self.textBrowser.repaint()
            Hi = float(self.Hi.toPlainText())
            Ti = float(self.Ti.toPlainText())
            Hj = float(self.Hj.toPlainText())
            Tj = float(self.Tj.toPlainText())
            Ha = float(self.Ha.toPlainText())
            Ta = float(self.Ta.toPlainText())

            model_time = int(self.model_time.toPlainText())

            array = func(Ta, Ha, Ti, Hi, Tj, Hj)

            self.textBrowser.append(f'T={array[0]}')
            self.textBrowser.append(f't03={array[1]}')
            self.textBrowser.append(f'm={array[2]}')
            self.textBrowser.repaint()
        except:
            self.textBrowser.append('Ошибка')
            self.textBrowser.repaint()

    def show_graph(self):

        try:
            model_time = int(self.model_time.toPlainText())
            T = float(self.T.toPlainText())
            m = int(self.m.toPlainText())
            t0 = float(self.t0.toPlainText())
            arr = plot(T, m, t0, model_time)
            fig, ax = plt.subplots()
            ax.plot(arr[1], arr[0])
            with open('data.json', 'w') as f:
                json.dump({'x': arr[1], 'y': arr[0]}, f)

            plt.show()

        except:
            self.textBrowser.append('Ошибка')
            self.textBrowser.repaint()


def calc_m(Ta, Ha, Ti, Hi, Tj, Hj):

    delta_to = []
    for i in range(1, 9):
        Ta_ = count_alpha(i, Ha)
        Ti_ = count_alpha(i, Hi)
        Tj_ = count_alpha(i, Hj)


        t023 = Ta_ * ((Ti_ / Ta_) * Ti - Ta) / (Ti_ - Ta_)
        to13 = Ta_ * ((Tj_ / Ta_) * Tj - Ta) / (Tj_ - Ta_)
        delta_to.append((i, math.fabs(to13 - t023), to13))

    delta_to.sort(key=lambda x: x[1])
    return delta_to[0]

def plot(T, m, t0, model_time):

    h_arr = []
    t_arr = []
    t = 0
    while t < model_time:
        temp = 0

        for a in range(1, int(m+1)):
            temp += (a / math.factorial(a)) * (t ** (a - 1)) / (T ** (a - 1))
        if t == 0:
            h = 0
            h_arr.append(h)
            t_arr.append(t+t0)
            t += 0.5
            continue

        h = 1 - (2.72 ** (-t / T)) * temp
        h_arr.append(h)
        t_arr.append(t+t0)
        t += 0.25
    arr = [h_arr, t_arr]
    return arr

def func(Ta, Ha, Ti, Hi, Tj, Hj):
    delta = calc_m(Ta, Ha, Ti, Hi, Tj, Hj)
    m = delta[0]
    to13 = delta[2]

    T = (count_alpha(m, Ha)*(Ta-to13), to13, m)
    return T


def count_alpha(m, a):

    step = 0.00001
    i = 0.00001

    while i <= 20:
        second_func = 0
        first_func = (1-a)*2.72**i
        for n in range(m+1):
            n_fact = math.factorial(n)
            second_func += (n/n_fact)*(i**(n-1))

        if math.fabs(first_func-second_func) < 0.01:
            return 1/i
        if (m > 4) and math.fabs(first_func-second_func) < 0.05:
            return 1/i
        if (m > 7) and math.fabs(first_func - second_func) < 0.1:
            return 1/i
        if (m > 9) and math.fabs(first_func - second_func) < 0.4:
            return 1/i
        if (m > 12) and i > 5 and math.fabs(first_func - second_func) < 3.5:
            return 1/i
        i += step



app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())

