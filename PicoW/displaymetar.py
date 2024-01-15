from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

try:
    from board import SCL, SDA
    import busio
    noDisplayLibraries = False
except ImportError:
    noDisplayLibraries = True

def startDisplay():
    if noDisplayLibraries:
        return None

    i2c = I2C(SCL, SDA)
    disp = SSD1306_I2C(128, 64, i2c)
    return disp

def shutdownDisplay(disp):
    if noDisplayLibraries:
        return

    disp.poweroff()

def clearScreen(disp):
    if noDisplayLibraries:
        return

    disp.fill(0)
    disp.show()

def outputMetar(disp, station, condition):
    if noDisplayLibraries:
        return

    width = disp.width
    height = disp.height
    padding = -2
    x = 0
    disp.fill(0)

    top = padding
    bottom = height - padding

    fontLarge = disp.load_font("freemono24")
    fontSmall = disp.load_font("freemono12")

    disp.text(station + "-" + condition["flightCategory"], x, top + 0, 1, font=fontLarge)
    disp.text(condition["obsTime"].strftime("%H:%MZ"), x + 90, top + 0, 1, font=fontSmall)

    disp.text(condition["windDir"] + "@" + str(condition["windSpeed"]) + ("G" + str(condition["windGustSpeed"]) if condition["windGust"] else ""), x, top + 15, 1, font=fontSmall)
    disp.text(str(condition["vis"]) + "SM " + condition["obs"], x + 64, top + 15, 1, font=fontSmall)
    disp.text(str(condition["tempC"]) + "C/" + str(condition["dewpointC"]) + "C", x, top + 25, 1, font=fontSmall)
    disp.text("A" + str(condition["altimHg"]) + "Hg", x + 64, top + 25, 1, font=fontSmall)

    yOff = 35
    xOff = 0
    NewLine = False

    for skyIter in condition["skyConditions"]:
        disp.text(skyIter["cover"] + ("@" + str(skyIter["cloudBaseFt"]) if skyIter["cloudBaseFt"] > 0 else ""), x + xOff, top + yOff, 1, font=fontSmall)
        if NewLine:
            yOff += 10
            xOff = 0
            NewLine = False
        else:
            xOff = 64
            NewLine = True

    disp.show()
