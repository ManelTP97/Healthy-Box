import tkinter

try:
    import Tkinter as tk
except:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import ttk
    import os.path
    import serial
    import time
    from threading import Thread
    #import RPi.GPIO as GPIO
    #import BME680
    #import SGP30
    #import SPS30

datei = None
mat = None

def getdoorSignal():
    pinhall = 17
    print('Hey')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pinhall, GPIO.IN)
    #GPIO.add_event_detected(pinhall, GPIO.RISING)

    #if GPIO.event_detected(pinhall):
        #print("Hey")

def getNC():
    sps30 = SPS30.SPS30()
    sps30.NC()

def getPM():
    sps30 = SPS30.SPS30()
    sps30.PM()

def geteCO2():
    sgp = SGP30.SGP30()
    sgp.geteCO2()

def getTVOC():
    sgp = SGP30.SGP30()
    sgp.getTVOC()

def getGas():
    bme = BME680.BME680()
    bme.getGas()

def getTemp():
    bme = BME680.BME680()
    bme.getTemps()

def venton():
    pinvent = 22
    print('Hey')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pinvent, GPIO.OUT)
    #GPIO.output(pinvent, 1)

def ventoff():
    pinvent = 22
    print('Hey')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pinvent, GPIO.OUT)
    #GPIO.output(pinvent, 0)

def dooropen():
    pindoor = 27
    print('Hey')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pindoor, GPIO.OUT)
    #GPIO.output(pindoor, 1)

def doorclose():
    pindoor = 27
    print('Hey')
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(pindoor, GPIO.OUT)
    #GPIO.output(pindoor, 0)


def hoch(ser):
    print('Hey')
    ser.write('G28')


def runter(ser):
    ser.write('G1 Z1')

def endprint():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.write('M0') #Vielleicht auch 410


def openData(self):
    encoding = None
    global datei
    global tail

    datei = filedialog.askopenfile(initialdir="/media/pi/", title="Select A File",
                                   filetypes=(("gcode", "*.gcode"), ("all files", "*.*")))

    if datei is not None:
        head, tail = os.path.split(datei.name)

    self.master.switch_frame(StartPage)


def goprint():
    incomming = ''
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

    time.sleep(5)

    for zeile in datei:
        # msg = bytes(zeile, 'utf-8')
        msgs = zeile.split(";")[0]
        msg = bytes(msgs + '\n', 'utf-8')
        # print(msgs)
        # print(type(msgs))
        # msg=zeile.encode()
        # time.sleep(0.3)
        ser.write(msg)

        while True:
            incomming = ser.readline()
            if incomming == bytes('', 'utf-8'):
                break
            print(str(incomming))
    time.sleep(5)
    ser.close()
    # datei=None

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        btn1 = tk.Button(self, text="Datei auswählen",
                  command=lambda: openData(self))
        btn1.pack()

        self.label = tk.Label(self, text="Keine Datei")
        self.label.pack()

        if datei is not None:
            self.label['text'] = str(tail)


        tk.Button(self, text="Material auswählen",
                  command=lambda: master.switch_frame(Material)).pack()
        self.label = tk.Label(self, text="Kein Material")
        self.label.pack()

        if mat is not None:
            if mat == 1:
                self.label['text'] = "PLA"
            elif mat == 2:
                self.label['text'] = "ABS"
            elif mat == 3:
                self.label['text'] = "PETG"
            elif mat == 4:
                self.label['text'] = "PA"
            elif mat == 5:
                self.label['text'] = "ASA"

        tk.Button(self, text="Drucken",
                  command=lambda: master.switch_frame(Print)).pack()

        tk.Button(self, text="Bedienung",
                  command=lambda: master.switch_frame(Bedienung)).pack()

class Material(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self)
        tk.Label(self, text="Materialien", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        material = tkinter.IntVar()
        tkinter.Radiobutton(self, text="PLA", variable=material, value=1, command=lambda: selMaterial(self)).pack(
            anchor=None)
        tkinter.Radiobutton(self, text="ABS", variable=material, value=2, command=lambda: selMaterial(self)).pack(
            anchor=None)
        tkinter.Radiobutton(self, text="PETG", variable=material, value=3, command=lambda: selMaterial(self)).pack(
            anchor=None)
        tkinter.Radiobutton(self, text="PA", variable=material, value=4, command=lambda: selMaterial(self)).pack(
            anchor=None)
        tkinter.Radiobutton(self, text="ASA", variable=material, value=5, command=lambda: selMaterial(self)).pack(
            anchor=None)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

        def selMaterial(self):
            global mat
            mat = material.get()


class Print(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='blue')
        tk.Label(self, text="Drucken", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)



        btn1 = tk.Button(self, text="Druck starten",
                  command=lambda: goprint())
        btn1.pack()

        if datei is None or mat is None:
            btn1['state'] = 'disabled'
        else:
            btn1['state'] = 'normal'

        tk.Button(self, text="Druck stoppen",
                  command=lambda: endprint()).pack()

        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class Bedienung(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='blue')
        tk.Label(self, text="Bedienung", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)

        #ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        ser = 1

        tk.Button(self, text="Hoch",
                  command=lambda: hoch(ser)).pack()

        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



