from math import e as exp
import cv2
import numpy as np
from config import Config
import matplotlib.pyplot as plt


class imageProc:
    def __init__(self,
                 name,
                 startImage=None,
                 runConfig=Config("./resources/config.example.yaml",
                                  "./config.yaml")):
        if (startImage is None):
            startImage = cv2.imread(runConfig.get_value("startImage"))
        self.limit = runConfig.get_value("limit")
        self.doLog = runConfig.get_value("doLog")
        self.runImage = startImage * (self.limit / 256.0)
        self.winName = name

        print("Created New Simulator: " + str(self.runImage.dtype))

        L = runConfig.get_value("L")
        T = runConfig.get_value("T")
        real_alpha = runConfig.get_value("real_alpha")
        real_vx = runConfig.get_value("real_vx")
        real_vy = runConfig.get_value("real_vy")

        alpha = real_alpha * T / (L * L)
        vx = real_vx * T / L
        vy = real_vy * T / L

        vxi = 1 + vx
        vxo = 1 - vx
        vyi = 1 + vy
        vyo = 1 - vy

        w2 = (alpha / 4) / (1 + exp)
        w1 = w2 * exp

        self.running = False
        self.kernel = np.array([[w2 * vxi * vyi, w1 * vyi, w2 * vxo * vyi],
                                [w1 * vxi, 1.0 - alpha, w1 * vxo],
                                [w2 * vxi * vyo, w1 * vyo, w2 * vxo * vyo]])
        cv2.imshow(self.winName, startImage)
        cv2.setMouseCallback(self.winName, self.__onShowClick)

        self.fig = plt.figure()
        self.axr = self.fig.add_subplot(3, 2, 1)
        self.axg = self.fig.add_subplot(3, 2, 3)
        self.axb = self.fig.add_subplot(3, 2, 5)
        self.ayr = self.fig.add_subplot(3, 2, 2)
        self.ayg = self.fig.add_subplot(3, 2, 4)
        self.ayb = self.fig.add_subplot(3, 2, 6)
        self.axr.set_title("Sliced Plot X")
        self.ayr.set_title("Sliced Plot Y")
        self.curx = 0
        self.cury = 0
        plt.show(block=False)

    def __onShowClick(self, event, cx, cy, f, p):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.curx = cx
            self.cury = cy
            self.updatePlot()

    def runLoop(self):
        while self.running and cv2.waitKey(1):
            self.runFrame()
            self.renderFrame()

    def runFrame(self):
        self.runImage = cv2.filter2D(self.runImage, -1, self.kernel)

    def renderFrame(self):
        renderImage = self.runImage / self.limit  # float display [0.0, 1.0]
        if self.doLog:
            renderImage = cv2.log(renderImage * (exp - 1.0) + 1.0)
        cv2.imshow(self.winName, renderImage)
        cv2.setMouseCallback(self.winName, self.__onShowClick)
        self.updatePlot()

    def updatePlot(self):
        self.axr.clear()
        self.axr.set_title("Sliced Plot X")
        self.axr.plot(range(self.runImage.shape[1]),
                      self.runImage[self.cury, :, 2])
        self.axg.clear()
        self.axg.plot(range(self.runImage.shape[1]),
                      self.runImage[self.cury, :, 1])
        self.axb.clear()
        self.axb.plot(range(self.runImage.shape[1]),
                      self.runImage[self.cury, :, 0])
        self.ayr.clear()
        self.ayr.set_title("Sliced Plot Y")
        self.ayr.plot(range(self.runImage.shape[0]),
                      self.runImage[:, self.curx, 2])
        self.ayg.clear()
        self.ayg.plot(range(self.runImage.shape[0]),
                      self.runImage[:, self.curx, 1])
        self.ayb.clear()
        self.ayb.plot(range(self.runImage.shape[0]),
                      self.runImage[:, self.curx, 0])
        plt.draw()
