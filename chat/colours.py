from functools import cache

from scipy.spatial import KDTree
from webcolors import (
    CSS3_HEX_TO_NAMES,
    CSS3_NAMES_TO_HEX,
    hex_to_rgb,
)


class ColourConverter:
    def __init__(self):
        self._names = []
        rgb_values = []
        for colour_hex, colour_name in CSS3_HEX_TO_NAMES.items():
            self._names.append(colour_name)
            rgb_values.append(hex_to_rgb(colour_hex))
        self.kdt_tree = KDTree(rgb_values)

    def get_closest_colour(self, rgb_tuple: tuple[int, int, int]) -> str:
        _, index = self.kdt_tree.query(rgb_tuple)
        return self._names[index]


colour_converter = ColourConverter()


@cache
def convert_rgb_to_colour(hex_code: str) -> str:
    rgb_tuple = hex_to_rgb(hex_code)
    return colour_converter.get_closest_colour(rgb_tuple)


def convert_colour_to_name(colour_name: str) -> str:
    return ",".join(map(str, hex_to_rgb(CSS3_NAMES_TO_HEX[colour_name])))
