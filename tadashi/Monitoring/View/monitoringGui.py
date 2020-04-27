import os
import glob
import ntpath
import cairosvg
import time
import fontawesome as fa

from PIL import Image as imag
from tkinter import *
from ...utils.helper import get_date_from_timestamp
from ..Model.monitoring import Monitoring
from ...Fibaro.Model.history import History


class MonitoringGui:
    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self._asset_path = self._absolute_path + "/assets"
        self._window = window
        self._window.title('Tadashi Monitoring')
        self.init_window()

    def init_window(self):
        for widget in self._window.winfo_children():
            widget.destroy()

        monitoring = self.load_metrology()

        main_panel = PanedWindow(self._window, orient=HORIZONTAL)
        main_panel.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        left_panel = PanedWindow(self._window, orient=VERTICAL)
        left_panel.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

        map_frame = self.draw_map_area(left_panel, monitoring)
        training_frame = self.draw_training_area(left_panel, monitoring)
        monitoring_frame = self.draw_monitoring_area(self._window, monitoring)
        alerting_frame = self.draw_alerting_area(self._window, monitoring)

        left_panel.add(map_frame)
        left_panel.add(training_frame)

        main_panel.add(left_panel)
        main_panel.add(monitoring_frame)
        main_panel.add(alerting_frame)

        self.draw_exit_button()
        self.draw_refresh_button()

    def draw_map_area(self, frame, monitoring):
        map_frame = LabelFrame(frame, text="Map state", font=12, borderwidth=3)
        map_frame.pack()

        map_filename = self.get_last_generated_map()
        image_path = self.convert_svg_to_png(map_filename)

        img = PhotoImage(file=image_path)
        map_canvas = Canvas(map_frame, width=256, height=256, bg='white')
        map_canvas.create_image(256/2, 256/2, image=img)
        map_canvas.image = img
        map_canvas.pack()

        map_filename = ntpath.basename(map_filename)
        timestamp = os.path.splitext(map_filename)[0]
        last_generated_map_date = get_date_from_timestamp(timestamp).replace(microsecond=0)

        label = Label(map_frame, text="last update: " + str(last_generated_map_date), padx=10, pady=10)
        label.pack(side=BOTTOM, fill=BOTH)

        return map_frame

    def draw_training_area(self, frame, monitoring):
        training_frame = LabelFrame(frame, text="Training model", font=12, borderwidth=3)
        training_frame.pack()

        image_path = self._asset_path + "/monitoring/training.png"

        im_temp = imag.open(image_path)
        im_temp = im_temp.resize((512, 384), imag.ANTIALIAS)
        im_temp.save(image_path, "png")

        img = PhotoImage(file=image_path)
        map_canvas = Canvas(training_frame, width=512, height=384, bg='white')
        map_canvas.create_image(512/2, 384/2, image=img)
        map_canvas.image = img
        map_canvas.pack(pady=5, padx=5)

        last_training_date = monitoring.last_training
        if last_training_date is not None:
            last_training_date = get_date_from_timestamp(last_training_date).replace(microsecond=0)
            label = Label(training_frame, text="last training: " + str(last_training_date))
            label.pack(side=TOP, fill=BOTH)

        model_size = monitoring.model_size
        if model_size is not None:
            label = Label(training_frame, text="model size: {:.2f}MB".format(model_size))
            label.pack(side=TOP, fill=BOTH)

        model_building_time = monitoring.model_building_time
        if model_building_time is not None:
            label = Label(training_frame, text="model builded in " + model_building_time)
            label.pack(side=TOP, fill=BOTH)

        return training_frame

    def draw_monitoring_area(self, frame, monitoring):
        monitoring_frame = LabelFrame(frame, text="Monitoring", font=12, borderwidth=3)
        monitoring_frame.pack(pady=5, padx=5)

        image_path = self._asset_path + "/monitoring/metrology.png"

        im_temp = imag.open(image_path)
        im_temp = im_temp.resize((512, 384), imag.ANTIALIAS)
        im_temp.save(image_path, "png")

        img = PhotoImage(file=image_path)
        map_canvas = Canvas(monitoring_frame, width=512, height=384, bg='white')
        map_canvas.create_image(512/2, 384/2, image=img)
        map_canvas.image = img
        map_canvas.pack(pady=5, padx=5)

        image_path = self._asset_path + "/monitoring/confusion_matrice.png"

        im_temp = imag.open(image_path)
        im_temp = im_temp.resize((512, 384), imag.ANTIALIAS)
        im_temp.save(image_path, "png")

        img = PhotoImage(file=image_path)
        map_canvas = Canvas(monitoring_frame, width=512, height=384, bg='white')
        map_canvas.create_image(512/2, 384/2, image=img)
        map_canvas.image = img
        map_canvas.pack(pady=5, padx=5)

        last_monitoring_update = monitoring.last_counter_update
        if last_monitoring_update is not None:
            last_monitoring_update = get_date_from_timestamp(last_monitoring_update).replace(microsecond=0)
            date_label = Label(monitoring_frame, text="last monitoring update: " + str(last_monitoring_update))
            date_label.pack(side=BOTTOM, fill=BOTH)

        current_date = get_date_from_timestamp(time.time()).replace(microsecond=0)
        date_label = Label(monitoring_frame, text="last window update: " + str(current_date))
        date_label.pack(side=BOTTOM, fill=BOTH)

        return monitoring_frame

    def draw_alerting_area(self, frame, monitoring):
        alerting_frame = LabelFrame(frame, text="Alerting", font=12, borderwidth=3)
        alerting_frame.pack(pady=5, padx=5)

        map_filename = self.get_last_generated_map()
        timestamp = os.path.splitext(ntpath.basename(map_filename))[0]
        path = self._asset_path + "/tmp/" + timestamp + "_f.json"
        devices = self.load_devices(path)

        for device in devices:
            if int(device.batteryLevel) >= 90:
                battery_level = 'battery-full'
                color = 'black'
            elif int(device.batteryLevel) >= 70:
                battery_level = 'battery-three-quarters'
                color = 'black'
            elif int(device.batteryLevel) > 45:
                battery_level = 'battery-half'
                color = 'black'
            elif int(device.batteryLevel) > 15:
                battery_level = 'battery-quarter'
                color = 'orange'
            else:
                battery_level = 'battery-empty'
                color = 'red'
            label = Label(alerting_frame, fg=color, text='room ' + str(device.roomID) + ' # ' + device.name + ' ' + fa.icons[battery_level] + ' ' + str(device.batteryLevel) + '%')
            label.pack(side=TOP)

        return alerting_frame

    def load_devices(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/tmp/fibaro_snapshot.json'
        devices = History()
        devices.load(path)
        return devices.logs

    def load_metrology(self):
        path = self._asset_path + "/monitoring/monitoring.json"
        monitoring = Monitoring()
        monitoring.load(path)
        return monitoring

    def draw_refresh_button(self):
        exit_button = Button(self._window, text="Force refresh (auto-refresh every 20 seconds)", pady=5, padx=5, command=self.refresh)
        exit_button.pack(side=BOTTOM, fill=BOTH)

    def refresh(self):
        self.init_window()

    def draw_exit_button(self):
        exit_button = Button(self._window, text="Exit", foreground="red", pady=5, padx=5, command=self._window.quit)
        exit_button.pack(side=BOTTOM, fill=BOTH)

    def get_last_generated_map(self):
        map_list = glob.glob(self._asset_path + "/map/*.svg")
        map_list = sorted(map_list, reverse=True)
        return map_list[0]

    @staticmethod
    def convert_svg_to_png(filename):
        svg_img_path = filename
        png_img_path = filename + '.png'
        cairosvg.svg2png(url=svg_img_path, write_to=png_img_path)
        return png_img_path


def clock():
    gui.refresh()
    window.after(20000, clock)  # run itself again after 20 seconds


window = Tk()
gui = MonitoringGui()
window.resizable(width=FALSE, height=FALSE)
clock()
window.mainloop()

