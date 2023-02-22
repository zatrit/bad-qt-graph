import time
import cv2
import pyqtgraph as pg
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from collections import deque

vc = cv2.VideoCapture("bad_apple.mp4")
width = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = vc.get(cv2.CAP_PROP_FPS)
bounds = [[0, width, width, 0, 0], [0, 0, height, height, 0]]
plt = pg.plot(title="BadQtgraph")
media = QUrl.fromLocalFile("bad_apple.mp3")
content = QtMultimedia.QMediaContent(media)
player = QtMultimedia.QMediaPlayer()
player.setMedia(content)
player.setVolume(25)
player.play()
start_time = time.time()


def display_list(_list):
    plt.plot(*zip(*map(lambda a: a[0], _list[::2])))


while True:
    excepted_frames = int(fps * (time.time() - start_time))
    cur_frames = vc.get(cv2.CAP_PROP_POS_FRAMES)
    if excepted_frames > cur_frames:
        vc.set(cv2.CAP_PROP_POS_FRAMES, excepted_frames)
        cur_frames = excepted_frames
    edged = cv2.flip(cv2.threshold(vc.read()[1], 200, 255, cv2.THRESH_BINARY)[1], 0)
    edged = cv2.cvtColor(edged, cv2.COLOR_RGB2GRAY)
    contours = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    if contours != ():
        plt.clear()
        plt.plot(*bounds)
        [display_list(_list) for _list in contours]
        QApplication.processEvents()
    if cur_frames > excepted_frames:
        time.sleep(1 / fps)
