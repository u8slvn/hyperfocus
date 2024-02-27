from __future__ import annotations

import re

from typing import Any
from typing import Match

import click

from hyperfocus.termui.exceptions import TermUIError


class Markup:
    """
    Manage console text style as markup.

    Example:
        bold and red text: "[bold red]my text[/]"

    Limitation: Markup cannot be nested.
    """

    _text_styles: list[str] = [
        "bold",
        "dim",
        "underline",
        "overline",
        "italic",
        "blink",
        "reverse",
        "strikethrough",
    ]
    # Sixteen first ones are write in plain text in order to be compatible
    # with colorama on Windows.
    _ansi_colors: dict[str, str | int] = {
        "black": "black",
        "red": "red",
        "green": "green",
        "yellow": "yellow",
        "blue": "blue",
        "magenta": "magenta",
        "cyan": "cyan",
        "white": "white",
        "bright_black": "bright_black",
        "bright_red": "bright_red",
        "bright_green": "bright_green",
        "bright_yellow": "bright_yellow",
        "bright_blue": "bright_blue",
        "bright_magenta": "bright_magenta",
        "bright_cyan": "bright_cyan",
        "bright_white": "bright_white",
        "grey0": 16,
        "navy_blue": 17,
        "dark_blue": 18,
        "blue3": 20,
        "blue1": 21,
        "dark_green": 22,
        "deep_sky_blue4": 25,
        "dodger_blue3": 26,
        "dodger_blue2": 27,
        "green4": 28,
        "spring_green4": 29,
        "turquoise4": 30,
        "deep_sky_blue3": 32,
        "dodger_blue1": 33,
        "green3": 40,
        "spring_green3": 41,
        "dark_cyan": 36,
        "light_sea_green": 37,
        "deep_sky_blue2": 38,
        "deep_sky_blue1": 39,
        "spring_green2": 47,
        "cyan3": 43,
        "dark_turquoise": 44,
        "turquoise2": 45,
        "green1": 46,
        "spring_green1": 48,
        "medium_spring_green": 49,
        "cyan2": 50,
        "cyan1": 51,
        "dark_red": 88,
        "deep_pink4": 125,
        "purple4": 55,
        "purple3": 56,
        "blue_violet": 57,
        "orange4": 94,
        "grey37": 59,
        "medium_purple4": 60,
        "slate_blue3": 62,
        "royal_blue1": 63,
        "chartreuse4": 64,
        "dark_sea_green4": 71,
        "pale_turquoise4": 66,
        "steel_blue": 67,
        "steel_blue3": 68,
        "cornflower_blue": 69,
        "chartreuse3": 76,
        "cadet_blue": 73,
        "sky_blue3": 74,
        "steel_blue1": 81,
        "pale_green3": 114,
        "sea_green3": 78,
        "aquamarine3": 79,
        "medium_turquoise": 80,
        "chartreuse2": 112,
        "sea_green2": 83,
        "sea_green1": 85,
        "aquamarine1": 122,
        "dark_slate_gray2": 87,
        "dark_magenta": 91,
        "dark_violet": 128,
        "purple": 129,
        "light_pink4": 95,
        "plum4": 96,
        "medium_purple3": 98,
        "slate_blue1": 99,
        "yellow4": 106,
        "wheat4": 101,
        "grey53": 102,
        "light_slate_grey": 103,
        "light_slate_gray": 103,
        "medium_purple": 104,
        "light_slate_blue": 105,
        "dark_olive_green3": 149,
        "dark_sea_green": 108,
        "light_sky_blue3": 110,
        "sky_blue2": 111,
        "dark_sea_green3": 150,
        "dark_slate_gray3": 116,
        "sky_blue1": 117,
        "chartreuse1": 118,
        "light_green": 120,
        "pale_green1": 156,
        "dark_slate_gray1": 123,
        "red3": 160,
        "medium_violet_red": 126,
        "magenta3": 164,
        "dark_orange3": 166,
        "indian_red": 167,
        "hot_pink3": 168,
        "medium_orchid3": 133,
        "medium_orchid": 134,
        "medium_purple2": 140,
        "dark_goldenrod": 136,
        "light_salmon3": 173,
        "rosy_brown": 138,
        "grey63": 139,
        "medium_purple1": 141,
        "gold3": 178,
        "dark_khaki": 143,
        "navajo_white3": 144,
        "grey69": 145,
        "light_steel_blue3": 146,
        "light_steel_blue": 147,
        "yellow3": 184,
        "dark_sea_green2": 157,
        "light_cyan3": 152,
        "light_sky_blue1": 153,
        "green_yellow": 154,
        "dark_olive_green2": 155,
        "dark_sea_green1": 193,
        "pale_turquoise1": 159,
        "deep_pink3": 162,
        "magenta2": 200,
        "hot_pink2": 169,
        "orchid": 170,
        "medium_orchid1": 207,
        "orange3": 172,
        "light_pink3": 174,
        "pink3": 175,
        "plum3": 176,
        "violet": 177,
        "light_goldenrod3": 179,
        "tan": 180,
        "misty_rose3": 181,
        "thistle3": 182,
        "plum2": 183,
        "khaki3": 185,
        "light_goldenrod2": 222,
        "light_yellow3": 187,
        "grey84": 188,
        "light_steel_blue1": 189,
        "yellow2": 190,
        "dark_olive_green1": 192,
        "honeydew2": 194,
        "light_cyan1": 195,
        "red1": 196,
        "deep_pink2": 197,
        "deep_pink1": 199,
        "magenta1": 201,
        "orange_red1": 202,
        "indian_red1": 204,
        "hot_pink": 206,
        "dark_orange": 208,
        "salmon1": 209,
        "light_coral": 210,
        "pale_violet_red1": 211,
        "orchid2": 212,
        "orchid1": 213,
        "orange1": 214,
        "sandy_brown": 215,
        "light_salmon1": 216,
        "light_pink1": 217,
        "pink1": 218,
        "plum1": 219,
        "gold1": 220,
        "navajo_white1": 223,
        "misty_rose1": 224,
        "thistle1": 225,
        "yellow1": 226,
        "light_goldenrod1": 227,
        "khaki1": 228,
        "wheat1": 229,
        "cornsilk1": 230,
        "grey100": 231,
        "grey3": 232,
        "grey7": 233,
        "grey11": 234,
        "grey15": 235,
        "grey19": 236,
        "grey23": 237,
        "grey27": 238,
        "grey30": 239,
        "grey35": 240,
        "grey39": 241,
        "grey42": 242,
        "grey46": 243,
        "grey50": 244,
        "grey54": 245,
        "grey58": 246,
        "grey62": 247,
        "grey66": 248,
        "grey70": 249,
        "grey74": 250,
        "grey78": 251,
        "grey82": 252,
        "grey85": 253,
        "grey89": 254,
        "grey93": 255,
    }
    _re_markup = re.compile(r"(\[(?P<style>[a-z][^[]*?)](?P<text>.[^[]*|.*)(\[/]))")

    def _resolve_style(self, style: str) -> Any:
        tags: dict[str, int | str | None] = {}

        for tag in style.split(" "):
            if tag in self._text_styles:
                tags.update({tag: True})
                continue

            try:
                tags.update({"fg": self._ansi_colors[tag]})
            except KeyError:
                raise TermUIError(f"Unknown markup tag {tag}.")

        return tags

    def _parse_markup(self, match: Match[str]) -> str:
        tags = self._resolve_style(match.group("style"))
        text = match.group("text")
        text = self.resolve(text)

        return click.style(text=text, **tags)

    def resolve(self, text: str) -> str:
        """
        Resolve markup in text with matching style.
        """
        return re.sub(self._re_markup, self._parse_markup, text)

    def _remove_markup(self, match: Match[str]) -> str:
        text = match.group("text")
        text = self.remove(text)

        return text

    def remove(self, text: str) -> str:
        """
        Remove markup from a text.
        """
        return re.sub(self._re_markup, self._remove_markup, text)


markup = Markup()
