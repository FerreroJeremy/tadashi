import svgwrite
from .mapDrawer import MapDrawer


class BedroomMapDrawer(MapDrawer):

    def draw_room_wall(self, handle):
        handle.add(handle.rect((168, 10), ("78px", "144px"), stroke_width = "2", stroke = "black", fill = "white"))
        return handle

    def draw_door_sensor(self, handle):
        handle = self.draw_door(handle, 168, 56, 168, 83)
        return handle

    def draw_shutter_sensor(self, handle):
        handle = self.draw_door(handle, 246, 48, 246, 76)
        return handle

    def draw_motion_sensor(self, handle):
        handle = self.draw_motion_icon(handle, 175, 110)
        return handle

    def draw_noise_sensor(self, handle):
        handle = self.draw_noise_icon(handle, 200, 110)
        return handle

    def draw_light_sensor(self, handle):
        handle = self.draw_light_icon(handle, 225, 110)
        return handle

    def draw_thermometer(self, handle):
        handle = self.draw_thermometer_icon(handle, 179, 128)
        return handle

    def draw_humidity(self, handle):
        handle = self.draw_drop_icon(handle, 202, 130)
        return handle

    def draw_smoke_detector(self, handle):
        handle = self.draw_smoke_icon(handle, 222, 130)
        return handle
