from .mapDrawer import MapDrawer


class LoungeMapDrawer(MapDrawer):

    def draw_room_wall(self, handle):
        handle.add(handle.rect((10, 10), ("70px", "46px"), stroke_width="1", stroke="white", fill="white"))
        handle.add(handle.rect((10, 56), ("157px", "97px"), stroke_width="1", stroke="white", fill="white"))
        handle.add(handle.line((10, 10), (81, 10), stroke_width="2", stroke="black"))
        handle.add(handle.line((80, 10), (81, 56), stroke_width="2", stroke="black"))
        handle.add(handle.line((80, 56), (169, 56), stroke_width="2", stroke="black"))
        handle.add(handle.line((168, 56), (168, 155), stroke_width="2", stroke="black"))
        handle.add(handle.line((168, 154), (9, 154), stroke_width="2", stroke="black"))
        handle.add(handle.line((10, 154), (10, 9), stroke_width="2", stroke="black"))
        return handle

    def draw_door_sensor(self, handle):
        handle = self.draw_door(handle, 35, 10, 60, 10)
        return handle

    def draw_shutter_sensor(self, handle):
        handle = self.draw_door(handle, 71, 154, 135, 154)
        return handle

    def draw_motion_sensor(self, handle):
        handle = self.draw_motion_icon(handle, 75, 110)
        return handle

    def draw_noise_sensor(self, handle):
        handle = self.draw_noise_icon(handle, 100, 110)
        return handle

    def draw_light_sensor(self, handle):
        handle = self.draw_light_icon(handle, 125, 110)
        return handle

    def draw_thermometer(self, handle):
        handle = self.draw_thermometer_icon(handle, 79, 128)
        return handle

    def draw_humidity(self, handle):
        handle = self.draw_drop_icon(handle, 102, 130)
        return handle

    def draw_smoke_detector(self, handle):
        handle = self.draw_smoke_icon(handle, 122, 130)
        return handle

    def draw_vaccum_activity(self, handle):
        handle = self.draw_vaccum_icon(handle, 146, 130)
        return handle
