import random, time
import SUBSEAGUI, sys, threading
from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Pipe

from PyQt5.QtWidgets import QMainWindow



class Window(QMainWindow, SUBSEAGUI.Ui_MainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        threading.Thread(target=lambda: self.recieve_and_set_text(conn)).start()

    def recieve_and_set_text(self, conn):
        print("trying to take out of pipe")
        while True:
            data = conn.recv()
            self.dybde.setText(str(data))

def run(conn):
    app = QtWidgets.QApplication(sys.argv)
    win = Window(conn)
    win.show()
    sys.exit(app.exec())
    SUBSEAGUI.MainWindow = QtWidgets.QMainWindow()
    ui = SUBSEAGUI.Ui_MainWindow()
    ui.setupUi(SUBSEAGUI.MainWindow)


    SUBSEAGUI.MainWindow.show()

    while True:
        data = str(conn.recv())
        print(data)
        ui.dybde.setText(data)

        sys.exit(app.exec_())


def generate_data(conn):
    while True:
        time.sleep(0.5)
        print("tring to send on pipe")
        conn.send((random.randrange(65,97)))

if __name__ == "__main__":
    send_to_GUI, receive_from_GUI = Pipe()

    data_thread = threading.Thread(target=generate_data, args=(receive_from_GUI,))
    data_thread.start()

    run(send_to_GUI)


