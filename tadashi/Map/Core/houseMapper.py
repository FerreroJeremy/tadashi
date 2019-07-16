import os
import svgwrite
from ...Fibaro.Model.tadashiHistory import TadashiHistory
from ...Fibaro.Model.tadashiHistory import Context
from ...Fibaro.Model.room import Place
from .bathroomMapDrawer import BathroomMapDrawer
from .bedroomMapDrawer import BedroomMapDrawer
from .loungeMapDrawer import LoungeMapDrawer
from .outsideMapDrawer import OutsideMapDrawer


class HouseMapper:
    def __init__(self, city, history_manager):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self._city = city
        self._tadashi_history = TadashiHistory()
        self._logs = None
        self._context = None
        self._outside_map_drawer = None
        self._lounge_map_drawer = None
        self._bedroom_map_drawer = None
        self._bathroom_map_drawer = None

    def load_tadashi_history(self, input_path=None):
        if not input_path:
            input_path = self._absolute_path + '/../../assets/tmp/tadashi_history.json'
        self._tadashi_history.load(input_path)

    def parse(self):
        self._context = self._tadashi_history.context
        for room in self._tadashi_history.logs:
            if room.place == Place.OUTSIDE:
                self._outside_map_drawer = OutsideMapDrawer(self._city, room)
            elif room.place == Place.LOUNGE:
                self._lounge_map_drawer = LoungeMapDrawer(self._city, room)
            elif room.place == Place.BEDROOM:
                self._bedroom_map_drawer = BedroomMapDrawer(self._city, room)
            elif room.place == Place.BATHROOM:
                self._bathroom_map_drawer = BathroomMapDrawer(self._city, room)

    def draw(self, output_path=None):
        if not output_path:
            output_path = self._absolute_path + '/../../assets/map/test_svg.svg'
        handle = svgwrite.Drawing(output_path, size=("256px", "256px"))
        
        if self._outside_map_drawer is not None:
            handle = self._outside_map_drawer.draw(handle)
        
        if self._lounge_map_drawer is not None:
            handle = self._lounge_map_drawer.draw(handle)
            handle = self._lounge_map_drawer.draw_date(handle)
            if self._context is not None and self._context is not Context.UNKNOWN:
                handle = self._lounge_map_drawer.draw_context(handle, self._context.value)
        
        if self._bedroom_map_drawer is not None:
            handle = self._bedroom_map_drawer.draw(handle)
        
        if self._bathroom_map_drawer is not None:
            handle = self._bathroom_map_drawer.draw(handle)
        
        handle.save()

