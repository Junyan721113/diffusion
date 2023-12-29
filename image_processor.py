import cv2
import numpy as np
from config import Config
import matplotlib.pyplot as plt
from math import ceil, e as exp, factorial


class plotObserver:
    target = None

    def updatePlot(self):
        pass

    def changeCur(self, x, y):
        pass


class showRender:
    observers = []

    def __init__(self, winName, startImage, runConfig: Config):
        self.winName = winName
        self.limit = runConfig.get_value("limit")
        self.runImage = startImage * (self.limit / 256.0)

        self.doLog = runConfig.get_value("doLog")

        L = runConfig.get_value("L")
        T = runConfig.get_value("T")
        self.K = runConfig.get_value("K") / T / self.limit / self.limit
        real_alpha = runConfig.get_value("real_alpha")
        real_vx = runConfig.get_value("real_vx")
        real_vy = runConfig.get_value("real_vy")

        alpha = real_alpha * T / (L * L)
        vx = real_vx * T / L
        vy = real_vy * T / L

        sigma = 4 * alpha
        rd = ceil(3 * sigma)
        gx, gy = np.mgrid[-rd:rd+1:1, -rd:rd+1:1]
        z = 1 / (2 * np.pi * (sigma**2)) * np.exp(-(gx**2 + gy**2) / (2 * sigma**2))

        poix = [np.exp(-vx) * vx**i / factorial(i) for i in range(rd + 1)]
        poix[rd] = 0
        poix[rd] = 1.0 - np.sum(poix)
        poiy = [np.exp(-vy) * vy**i / factorial(i) for i in range(rd + 1)]
        poiy[rd] = 0
        poiy[rd] = 1.0 - np.sum(poiy)

        poi = np.outer(poiy, poix)
        # print(poi)

        self.movement = np.zeros((2 * rd + 1, 2 * rd + 1))
        self.movement[rd:, rd:] = poi
        # print(self.movement)

        self.diffusion = np.array(z)
        self.diffusion = self.diffusion / np.sum(self.diffusion)

        cv2.namedWindow(self.winName)
        self.renderFrame()

    def runFrame(self):
        # Chemical Reaction: R + G => B
        # Calculate the reaction velocity
        reactVelocity = self.runImage[:, :, 1] * self.runImage[:, :, 2] * self.K
        # Calculate the reaction
        self.runImage[:, :, 0] += reactVelocity
        self.runImage[:, :, 1] -= reactVelocity
        self.runImage[:, :, 2] -= reactVelocity
        # Limit the value
        self.runImage = np.clip(self.runImage, 0.0, self.limit)
        self.runImage = cv2.filter2D(self.runImage, -1, self.movement)
        self.runImage = cv2.filter2D(self.runImage, -1, self.diffusion)

    def renderFrame(self):
        renderImage = self.runImage / self.limit  # float display [0.0, 1.0]
        if self.doLog:
            renderImage = cv2.log(renderImage * (exp - 1.0) + 1.0)
        cv2.imshow(self.winName, renderImage)
        for observer in self.observers:
            observer.updatePlot()

    def attachObserver(self, observer: plotObserver):
        self.observers.append(observer)

    def getRunImage(self):
        return self.runImage


class plot2D(plotObserver):
    def __init__(self, rdr: showRender, fig, grid, gidx, rate):
        self.target = rdr
        self.rate = rate
        self.cnt = rate
        rdr.attachObserver(self)

        self.ax = fig.add_subplot(grid[0, gidx])
        self.ay = fig.add_subplot(grid[1, gidx])
        self.ax.set_title("Sliced Plot X")
        self.ay.set_title("Sliced Plot Y")
        self.curx = 0
        self.cury = 0

        plt.show(block=False)
        self.updatePlot()

    def changeCur(self, x, y):
        self.curx = x
        self.cury = y
        self.updatePlotForce()

    def updatePlotForce(self):
        self.cnt = self.rate
        self.updatePlot()

    def updatePlot(self):
        if self.cnt < self.rate:
            self.cnt += 1
            return
        self.cnt = 0

        rImg = self.target.getRunImage()
        self.ax.clear()
        self.ax.set_title("Sliced Plot X")
        self.ax.plot(range(rImg.shape[1]),
                     rImg[self.cury, :, 2],
                     color='red', alpha=0.5)
        self.ax.plot(range(rImg.shape[1]),
                     rImg[self.cury, :, 1],
                     color='green', alpha=0.5)
        self.ax.plot(range(rImg.shape[1]),
                     rImg[self.cury, :, 0],
                     color='blue', alpha=0.5)

        self.ay.clear()
        self.ay.set_title("Sliced Plot Y")
        self.ay.plot(range(rImg.shape[0]),
                     rImg[:, self.curx, 2],
                     color='red', alpha=0.5)
        self.ay.plot(range(rImg.shape[0]),
                     rImg[:, self.curx, 1],
                     color='green', alpha=0.5)
        self.ay.plot(range(rImg.shape[0]),
                     rImg[:, self.curx, 0],
                     color='blue', alpha=0.5)
        plt.draw()


class plot3D(plotObserver):
    def __init__(self, rdr: showRender, fig, grid, gidx, rate):
        self.target = rdr
        self.rate = rate
        self.cnt = rate
        rdr.attachObserver(self)

        self.a3d = fig.add_subplot(grid[:, gidx], projection='3d')
        self.a3d.set_title("3D Plot")

        plt.show(block=False)
        self.updatePlot()

    def changeCur(self, x, y):
        self.updatePlotForce()

    def updatePlotForce(self):
        self.cnt = self.rate
        self.updatePlot()

    def updatePlot(self):
        if self.cnt < self.rate:
            self.cnt += 1
            return
        self.cnt = 0

        self.a3d.clear()
        rImg = self.target.getRunImage()
        sampleX = round(rImg.shape[1] / 20)
        sampleY = round(rImg.shape[0] / 20)
        xx = np.arange(0, rImg.shape[1])
        yy = np.arange(0, rImg.shape[0])
        X, Y = np.meshgrid(xx, yy)
        self.a3d.plot_surface(X, Y, rImg[:, :, 2],
                              rstride=sampleX, cstride=sampleY,
                              cmap='Reds', alpha=0.5)
        self.a3d.plot_surface(X, Y, rImg[:, :, 1],
                              rstride=sampleX, cstride=sampleY,
                              cmap='Greens', alpha=0.5)
        self.a3d.plot_surface(X, Y, rImg[:, :, 0],
                              rstride=sampleX, cstride=sampleY,
                              cmap='Blues', alpha=0.5)
        plt.draw()


class plotManager:
    def __init__(self, rdr: showRender, runConfig: Config, gwidth=2):
        self.plots = []
        self.rdr = rdr
        self.fig = plt.figure()
        self.gwidth = gwidth
        self.grid = plt.GridSpec(2, gwidth, wspace=0.5, hspace=0.5)
        self.gidx = 0
        self.p2drate = runConfig.get_value("p2drate")
        self.p3drate = runConfig.get_value("p3drate")

    def createPlot(self, type):
        if self.gidx >= self.gwidth:
            return None
        if type == 0:
            plot = plot2D(self.rdr, self.fig, self.grid, self.gidx, self.p2drate)
        else:
            plot = plot3D(self.rdr, self.fig, self.grid, self.gidx, self.p3drate)
        self.gidx += 1
        self.plots.append(plot)
        return plot

    def changeCur(self, x, y):
        for plot in self.plots:
            plot.changeCur(x, y)

    def createDefaultPlot(self):
        self.createPlot(0)
        self.createPlot(1)

    def createDefaultPlotReverse(self):
        self.createPlot(1)
        self.createPlot(0)


class showPaint:
    def __init__(self, plt: plotManager, rdr: showRender, runConfig: Config):
        self.winName = rdr.winName
        self.plt = plt
        self.rdr = rdr
        self.limitInt = round(runConfig.get_value("limit"))
        self.size = 10
        self.color = [0, 0, 0]
        cv2.createTrackbar("Size", self.winName, 10, 1000, self.__onSizeChange)
        cv2.createTrackbar("Red", self.winName, 0, self.limitInt, self.__onColorChangeGenerator(2))
        cv2.createTrackbar("Green", self.winName, 0, self.limitInt, self.__onColorChangeGenerator(1))
        cv2.createTrackbar("Blue", self.winName, 0, self.limitInt, self.__onColorChangeGenerator(0))
        cv2.setMouseCallback(self.winName, self.__onShowClick)

    def __onSizeChange(self, x):
        self.size = x

    def __onColorChangeGenerator(self, y):
        def __onColorChange(x):
            self.color[y] = x
        return __onColorChange

    def __onShowClick(self, event, cx, cy, f, p):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.rdr.runImage, (cx, cy), self.size, self.color, -1)
            self.rdr.renderFrame()

        if event == cv2.EVENT_RBUTTONDOWN:
            self.plt.changeCur(cx, cy)

        if event == cv2.EVENT_MOUSEWHEEL:
            if f > 0:
                self.size += 10
            else:
                self.size -= 10
            self.size = max(1, self.size)
            self.size = min(1000, self.size)
            cv2.setTrackbarPos("Size", self.winName, self.size)


class imageProc:
    def __init__(self,
                 name,
                 startImage=None,
                 runConfig=Config("./resources/config.example.yaml",
                                  "./config.yaml")):
        if (startImage is None):
            startImage = runConfig.get_value("startImage")
        startImage = cv2.imread(startImage, cv2.IMREAD_COLOR)
        self.winName = name

        print("Created New Simulator: " + name)

        self.running = False

        self.showRdr = showRender(self.winName, startImage, runConfig)
        self.showPlt = plotManager(self.showRdr, runConfig)
        self.showPlt.createDefaultPlot()
        self.showPaint = showPaint(self.showPlt, self.showRdr, runConfig)

    def runLoop(self):
        while self.running and cv2.waitKey(1):
            self.showRdr.runFrame()
            self.showRdr.renderFrame()
