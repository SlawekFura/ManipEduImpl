import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import SimpleKinematic as sk
import InverseKinematic as ik
from pynput import keyboard
from time import sleep
import multiprocessing

a0 = 0.3
f0 = 0.5
delta_f = 0.1
ind_x = 0
ind_y = 1
ind_z = 2
def plotManip(paramsRange, dhMatrix):

    axcolor = 'lightgoldenrodyellow'
    iter = 0
    axisOffset = 0.03

    sliders = {}
    for paramName, parRange in paramsRange.items():
        axVarName = plt.axes([0.1, 0.02 + axisOffset * iter, 0.35, 0.02], facecolor=axcolor)
        init_val = 0
        if dhMatrix.params[paramName[:-1]][paramName] != "var":
            init_val = dhMatrix.params[paramName[:-1]][paramName]
        sVarName = Slider(axVarName, paramName, min(parRange), max(parRange), valinit=init_val, valstep=0.1)
        sliders[paramName] = sVarName
        iter += 1

    ax = plt.axes(projection='3d')
    sct = None

    def update(var):


        ranges = {}
        for sliderName, slider in sliders.items():
            ranges[sliderName] = slider.val

        points = sk.genElemCoordForSingleParams(ranges, dhMatrix)  # lambda_range)

        xdata = [point[0] for point in points]
        ydata = [point[1] for point in points]
        zdata = [point[2] for point in points]

        # print("x", xdata)
        # print("y", ydata)
        # print("z", zdata)
        # print("dupa")
        global sct
        # if sct:
        #     sct.remove()
        ax.clear()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.plot(xdata, ydata, zdata)

        axes = plt.gca()
        axes.set_xlim([-1, 1])
        axes.set_ylim([-1, 1])
        axes.set_zlim([-0.5, 2])

        plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
        sct = ax.scatter3D(xdata, ydata, zdata, c=zdata)
        plt.show()


    for sliderName, slider in sliders.items():
        slider.on_changed(update)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    ax.figure.set_size_inches(5, 5)
    ax.plot([], [], [])
    ax.scatter3D([], [], [], cmap='Greens')
    plt.show()

def plotForConfigVariables(paramsRanges, dhMatrix):

    axcolor = 'lightgoldenrodyellow'
    axVarName = plt.axes([0.1, 0.02, 0.35, 0.02], facecolor=axcolor)
    print("keys: ", paramsRanges.keys())
    idxSlider = Slider(axVarName, "idx", 0, len(paramsRanges[list(paramsRanges.keys())[0]]) - 1, valinit=0, valstep=1)

    ax = plt.axes(projection='3d')
    path = {"x": [], "y" : [], "z" : []}

    genCoordinates = []
    ranges = {}
    paramsRangesLen = len(paramsRanges[list(paramsRanges.keys())[0]])

    for i in range(0, paramsRangesLen):
        for varName in paramsRanges.keys():
            ranges[varName] = paramsRanges[varName][i]
        points = sk.genElemCoordForSingleParams(ranges, dhMatrix)
        genCoordinates.append(points)

    xPoints = [pointsGroup[3][0] for pointsGroup in genCoordinates]
    yPoints = [pointsGroup[3][1] for pointsGroup in genCoordinates]
    zPoints = [pointsGroup[3][2] for pointsGroup in genCoordinates]

    global it
    it = 0

    def update(var):

        xdata = [point[0] for point in genCoordinates[idxSlider.val]]
        ydata = [point[1] for point in genCoordinates[idxSlider.val]]
        zdata = [point[2] for point in genCoordinates[idxSlider.val]]

        global it
        if idxSlider.val > len(path["x"]) -1:
            path["x"].append(xdata)
            path["y"].append(ydata)
            path["z"].append(zdata)
            it += 1

        ax.clear()

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.plot(xdata, ydata, zdata)

        axes = plt.gca()
        axes.set_xlim([-1, 1])
        axes.set_ylim([-1, 1])
        axes.set_zlim([-0.5, 2])

        plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
        ax.scatter3D(xdata, ydata, zdata, c=zdata)
        ax.scatter3D(xPoints[:idxSlider.val], yPoints[:idxSlider.val], zPoints[:idxSlider.val], s=0.5)
        plt.show()

    idxSlider.on_changed(update)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    ax.figure.set_size_inches(5, 5)
    ax.plot([], [], [])
    ax.scatter3D([], [], [], cmap='Greens')
    plt.show()

def on_press(key, q, prevConfVariables, invertJacobianMatrix, dhMatrix):
    if key not in [keyboard.Key.left, keyboard.Key.right, keyboard.Key.up, keyboard.Key.left.down]:
        return

    # print("prevConfVariables_1", hex(id(prevConfVariables)), prevConfVariables)
    prevPos = sk.genElemCoordForSingleParams(prevConfVariables, dhMatrix)[-1]
    expectedPos = list(prevPos)
    if key == keyboard.Key.left:
        expectedPos[ind_x] -= 0.02
    elif key == keyboard.Key.right:
        expectedPos[ind_x] += 0.02
    elif key == keyboard.Key.up:
        expectedPos[ind_y] += 0.02
    elif key == keyboard.Key.down:
        expectedPos[ind_y] -= 0.02
    else:
        return
    # print("prevPos", prevPos, "expectedPos", expectedPos)
    # print("in:", expectedPos)
    coord = ik.genConfigVariablesValues(prevConfVariables, prevPos, expectedPos, invertJacobianMatrix)
    q.put(coord)
    sleep(0.05)

def prepareKeyboardInput(q, prevConfVariables, invertJacobianMatrix, dhMatrix):
    with keyboard.Listener(
            on_press=lambda key: on_press(key, q, prevConfVariables, invertJacobianMatrix, dhMatrix)) as listener:
        listener.join()

def plotContinuous(prevConfVariables, invertJacobianMatrix, dhMatrix):
    ax = plt.axes(projection='3d')
    q = multiprocessing.Queue()

    manager = multiprocessing.Manager()
    prevConfVariables_ = manager.dict()
    prevConfVariables_.update(prevConfVariables)
    simulate=multiprocessing.Process(None, prepareKeyboardInput, args=(q, prevConfVariables_, invertJacobianMatrix, dhMatrix,))
    simulate.start()

    plt.subplots_adjust(left=0.4, right=0.9, top=0.9, bottom=0.20)
    ax.figure.set_size_inches(5, 5)
    ax.plot([], [], [])
    ax.scatter3D([], [], [], cmap='Greens')
    lastData = None
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.plot([1,2], [1,2], [1,2])
    plt.draw()
    plt.pause(0.1)

    while True:
        try:  # Try to check if there is data in the queue
            result = q.get_nowait()
            # result = q.get()
            if not lastData is result:
                # plt.ion()
                ax.clear()

                paramsRange = {"theta0" : result[0], "theta1" : result[1], "lambda2" : result[2]}
                # print("paramsRange_", paramsRange)
                prevConfVariables_.update(paramsRange)
                # print("prevConfVariables:", hex(id(keyboard.Key.left)), prevConfVariables)

                data = sk.genElemCoordForSingleParams(paramsRange, dhMatrix)

                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                xdata = [point[0] for point in data]
                ydata = [point[1] for point in data]
                zdata = [point[2] for point in data]
                # print("out", data[3])
                print("xdata", xdata, "ydata", ydata, "zdata", zdata)
                ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))
                # ax.scatter3D(xdata, ydata, zdata, c=zdata)
                # plt.show()
                plt.plot(xdata, ydata, zdata)
                plt.draw()
                plt.pause(0.1)
                lastData = data
        except:
            # print ("empty")
            sleep(0.1)


