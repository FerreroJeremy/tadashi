import svgwrite
from .mapDrawer import MapDrawer


class OutsideMapDrawer(MapDrawer):

    def draw_room_wall(self, handle):
        handle.add(handle.rect((70, 154), ("89px", "54px"), stroke_width = "2", stroke = "black", fill = "white"))
        return handle

    def draw_motion_sensor(self, handle):
        handle = self.draw_motion_icon(handle, 80, 175)
        return handle

    def draw_noise_sensor(self, handle):
        handle = self.draw_noise_icon(handle, 105, 175)
        return handle

    def draw_light_sensor(self, handle):
        handle = self.draw_light_icon(handle, 130, 175)
        return handle

    def draw_thermometer(self, handle):
        handle = self.draw_thermometer_icon(handle, 84, 193)
        return handle

    def draw_humidity(self, handle):
        handle = self.draw_drop_icon(handle, 107, 195)
        return handle

    def draw_smoke_detector(self, handle):
        handle = self.draw_smoke_icon(handle, 127, 195)
        return handle
