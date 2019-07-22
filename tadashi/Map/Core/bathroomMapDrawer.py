from .mapDrawer import MapDrawer


class BathroomMapDrawer(MapDrawer):

    def draw_room_wall(self, handle):
        handle.add(handle.rect((80, 10), ("88px", "46px"), stroke_width="2", stroke="black", fill="white"))
        return handle

    def draw_door_sensor(self, handle):
        handle = self.draw_door(handle, 80, 15, 80, 38)
        return handle

    def draw_motion_sensor(self, handle):
        handle = self.draw_motion_icon(handle, 95, 28)
        return handle

    def draw_noise_sensor(self, handle):
        handle = self.draw_noise_icon(handle, 120, 28)
        return handle

    def draw_light_sensor(self, handle):
        handle = self.draw_light_icon(handle, 145, 28)
        return handle

    def draw_thermometer(self, handle):
        handle = self.draw_thermometer_icon(handle, 99, 46)
        return handle

    def draw_humidity(self, handle):
        handle = self.draw_drop_icon(handle, 122, 48)
        return handle

    def draw_smoke_detector(self, handle):
        handle = self.draw_smoke_icon(handle, 142, 48)
        return handle
