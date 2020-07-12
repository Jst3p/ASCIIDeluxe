import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider
from PIL import Image


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def binimgToStr(binImg):
    nrows = binImg.shape[0]
    ncols = binImg.shape[1]

    resStr = []
    for i in range(0, nrows - 4, 4):
        for j in range(0, ncols - 2, 2):
            segment = binImg[i:i + 4, j:j + 2]
            bitArr = np.array([*segment[0:3, 0], *segment[0:3, 1],
                               segment[3, 0], segment[3, 1]])
            bitStr = ''.join(np.flip(bitArr.astype(str)))
            val = int(bitStr, 2)
            resStr.append(chr(10240 + val))
        resStr.append('\n')

    resStr = ''.join(resStr)
    return resStr


def main():
    fname = input("Image file name:")
    dimStr = input("Desired dimentions (width height):")
    dimList = dimStr.split(" ")
    width = int(dimList[0])
    height = int(dimList[1])

    def update(val):
        thresh = binSlider.val
        threshImg = (img > thresh).astype(np.int)

        binPlot.set_data(threshImg)
        fig.canvas.draw_idle()

    img = Image.open(f"Images/{fname}")
    img = img.resize((width*2, height*4))
    img = np.asarray(img)
    img = img / 255
    img = rgb2gray(img)

    fig, ax = plt.subplots(1, 2)

    thresh = 0.5
    threshImg = (img > thresh).astype(np.int)
    originalPlot = ax[0].imshow(img, cmap="gray")
    binPlot = ax[1].imshow(threshImg, cmap="gray")

    ax[0].set_title("Original Image")
    ax[1].set_title("Binned Image")

    binAx = plt.axes([0.15, 0.02, 0.7, 0.04])
    binSlider = Slider(binAx, 'Threshold', 0.0, 1.0, valinit=thresh, valstep=0.01)
    binSlider.on_changed(update)

    print("Choose Threshold and exit window.")
    plt.show()

    thresh = binSlider.val
    threshImg = (img > thresh).astype(np.int)

    resStr = binimgToStr(threshImg)
    resFName = fname.split(".")[0]
    with open(f"Results/{resFName}.txt", "w", encoding="utf-8") as f:
        f.write(resStr)


if __name__ == '__main__':
    main()
