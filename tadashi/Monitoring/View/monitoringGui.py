from tkinter import *


class MonitoringGui:
    def __init__(self, window):
        window.title('Tadashi Monitoring')

        label = Label(window, text="Under development...")
        label.pack()

        exit_button = Button(window, text="Exit", command=window.quit)
        exit_button.pack()


gui = Tk()
MonitoringGui(gui)
gui.resizable(width=FALSE, height=FALSE)
gui.geometry("300x60")
gui.mainloop()
