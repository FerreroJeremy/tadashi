import fontawesome as fa
import datetime
import pytz
from astral import Astral
from ...Fibaro.Model.room import OpeningState
from ...Fibaro.Model.room import MonoxideState
from ...utils.helper import get_season
from ...utils.helper import get_day_of_week


class MapDrawer:
    def __init__(self, city, log=None):
        self._astral = Astral()
        self._astral.solar_depression = 'civil'
        self._city = city
        self._astral = self._astral[self._city]
        self._room_info = log

    def draw(self, handle):
        handle = self.draw_room_wall(handle)
        handle = self.draw_sensors(handle)
        return handle

    def draw_sensors(self, handle):
        handle = self.draw_motion_sensor(handle)
        handle = self.draw_noise_sensor(handle)
        handle = self.draw_light_sensor(handle)
        handle = self.draw_thermometer(handle)
        handle = self.draw_humidity(handle)
        handle = self.draw_vaccum_activity(handle)
        handle = self.draw_smoke_detector(handle)
        handle = self.draw_openings(handle)
        return handle

    def draw_openings(self, handle):
        if self._room_info.door == OpeningState.OPEN:
            handle = self.draw_door_sensor(handle)
        if self._room_info.shutter == OpeningState.OPEN:
            handle = self.draw_shutter_sensor(handle)
        return handle

    def draw_date(self, handle, x=90, y=246, size='15', color='black'):
        hour = datetime.datetime.now().strftime('%H:%M:%S')
        day_of_week = get_day_of_week()
        season = get_season()

        season_icon = fa.icons["snowflake"]
        if season == 'spring':
            season_icon = fa.icons["yelp"]
        elif season == 'summer':
            season_icon = fa.icons["sun"]
        elif season == 'fall':
            season_icon = fa.icons["envira"]

        utc = pytz.UTC
        sun = self._astral.sun(date=datetime.datetime.now(), local=True)
        sun_icon = fa.icons["moon"]
        if sun['sunrise'].replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc) < sun['sunset'].replace(tzinfo=utc):
            sun_icon = fa.icons["sun"]

        text = day_of_week + '  ' + hour + '  ' + sun_icon + '  ' + season_icon
        handle = self.draw_text(handle, text, x, y, size, color)
        return handle

    def draw_door_sensor(self, handle):
        return handle

    def draw_shutter_sensor(self, handle):
        return handle

    def draw_vaccum_activity(self, handle):
        return handle

    def draw_light_icon(self, handle, x, y, size='15', color='yellow'):
        if self._room_info.light:
            handle = self.draw_icon(handle, 'lightbulb', x, y, size, color)
        return handle

    def draw_motion_icon(self, handle, x, y, size='15', color='black'):
        if self._room_info.motion:
            handle = self.draw_icon(handle, 'eye', x, y, size, color)
        return handle

    def draw_noise_icon(self, handle, x, y, size='15', color='black'):
        if self._room_info.noise:
            handle = self.draw_icon(handle, 'volume-up', x, y, size, color)
        return handle

    def draw_vaccum_icon(self, handle, x, y, size='15', color='black'):
        if self._room_info.vaccum:
            handle = self.draw_icon(handle, 'codiepie', x, y, size, color)
        return handle

    def draw_drop_icon(self, handle, x, y, size='15', color='blue'):
        if self._room_info.humidity:
            handle = self.draw_icon(handle, 'tint', x, y, size, color)
        return handle

    def draw_smoke_icon(self, handle, x, y, size='15', color='lightgray'):
        if self._room_info.gaz == MonoxideState.MODERATE:
            handle = self.draw_icon(handle, 'cloud', x, y, size, color)
        elif self._room_info.gaz == MonoxideState.DANGEROUS:
            handle = self.draw_icon(handle, 'cloud', x, y, size, 'grey')
        else:
            handle = self.draw_icon(handle, 'cloud', x, y, size, 'white')
        return handle

    def draw_thermometer_icon(self, handle, x, y, size='15'):
        if self._room_info.temperature is not None:
            temperature = int(self._room_info.temperature)
            if temperature < 4:
                color = 'cyan'
                icon = 'snowflake'
                x -= 4
            elif temperature < 18:
                color = 'blue'
                icon = 'thermometer-empty'
            elif temperature < 21:
                color = 'orange'
                icon = 'thermometer-half'
            else:
                color = 'red'
                icon = 'thermometer-full'
            handle = self.draw_icon(handle, icon, x, y, size, color)
        return handle

    def draw_pet_icon(self, handle, x, y, size='15', color='black'):
        handle = self.draw_icon(handle, 'paw', x, y, size, color)
        return handle

    def draw_context(self, handle, icon, x=10, y=246, size='30', color='black'):
        handle = self.draw_icon(handle, icon, x, y, size, color)
        return handle

    def draw_icon(self, handle, icon, x, y, size='15', color='black'):
        handle.add(handle.text(fa.icons[icon], insert=(x, y), fill=color, font_size=size+'px'))
        return handle

    def draw_text(self, handle, text, x, y, size='15', color='black'):
        handle.add(handle.text(text, insert=(x, y), fill=color, font_size=size+'px'))
        return handle

    def draw_door(self, handle, x1, y1, x2, y2, width="2", color="white"):
        handle.add(handle.line((x1, y1), (x2, y2), stroke_width=width, stroke=color))
        return handle

    def print_all_fontawesome(self):
        for icon in fa.icons:
            print(icon + '    ' + fa.icons[icon])
