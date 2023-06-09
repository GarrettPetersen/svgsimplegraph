import base64
import urllib.request
import json
import time

from .utils import DEFAULT_COLOR_PALETTE
from .utils import is_dark


class BaseGraph:
    """
    This class contains the basic properties of all graphs. It is inherited by
    other classes.
    """

    def __init__(
        self,
        width=300,
        height=200,
        padding=20,
        x_padding=None,
        y_padding=None,
        y_top_padding=None,
        y_bottom_padding=None,
        x_left_padding=None,
        x_right_padding=None,
        colors=None,
        num_y_ticks=5,
        x_axis_label=None,
        primary_y_axis_label=None,
        secondary_y_axis_label=None,
        show_legend=True,
        rotate_x_labels=True,
        background_color=None,
        dark_mode=None,
    ):
        self.width = width
        self.height = height
        self.y_top_padding = y_top_padding or y_padding or padding
        self.y_bottom_padding = y_bottom_padding or y_padding or padding
        self.x_left_padding = x_left_padding or x_padding or padding
        self.x_right_padding = x_right_padding or x_padding or padding
        self.colors = (colors or DEFAULT_COLOR_PALETTE).copy()
        self.num_y_ticks = num_y_ticks
        self.x_axis_label = x_axis_label
        self.primary_y_axis_label = primary_y_axis_label
        self.secondary_y_axis_label = secondary_y_axis_label
        self.data = []
        self.legend_labels = []
        self.series_types = []
        self.secondary = []
        self.show_legend = show_legend
        self.rotate_x_labels = rotate_x_labels
        self.background_color = background_color
        self.dark_mode = dark_mode
        if dark_mode is None and background_color:
            self.dark_mode = is_dark(background_color)
        elif dark_mode is None:
            self.dark_mode = False
        self.defs = []
        self.svg_elements = []

        # Use dark colors last if in dark mode and using default color palette
        if self.colors == DEFAULT_COLOR_PALETTE and self.dark_mode:
            self.colors.sort(key=lambda x: is_dark(x))

    def _generate_svg(self):
        """
        Generate the SVG string from the styles and elements.
        """
        defs_str = ""
        if self.defs:
            defs_str = "<defs>" + "\n".join(self.defs) + "</defs>"
        svg_elements_str = "\n".join(self.svg_elements)
        svg = f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">
            {defs_str}
            {svg_elements_str}
        </svg>
        """
        return svg

    def render(self):
        # Implement the specific rendering for this subclass
        pass

    def to_base64_src(self):
        svg_str = self.render()
        svg_bytes = svg_str.encode("utf-8")
        encoded_svg = base64.b64encode(svg_bytes).decode("utf-8")
        return "data:image/svg+xml;base64," + encoded_svg

    def upload_to_github_gist(self, access_token, filename=None):
        token = access_token
        access_url = "https://api.github.com/gists"

        epoch_time = int(time.time())

        if not filename:
            filename = "simplegraph"
        filename = f"{filename}_{epoch_time}.svg"
        description = "test image"
        public = "true"

        raw_svg = self.render()
        json_svg = json.dumps(raw_svg)[
            1:-1
        ]  # escape the SVG content without adding extra quotes

        data = f"""{{
        "description": "{description}",
        "public": {public},
        "files": {{
            "{filename}": {{
            "content": "{json_svg}"
            }}
        }}
        }}"""

        req = urllib.request.Request(access_url)
        req.add_header("Authorization", f"token {token}")
        req.add_header("Content-Type", "application/json")

        try:
            response = urllib.request.urlopen(req, data=data.encode("utf-8"))
            response_dict = json.load(response)
            raw_url = response_dict["files"][filename]["raw_url"]
            return raw_url
        except urllib.error.HTTPError as e:
            raise Exception(
                f"An exception occurred while uploading to GitHub Gist: {e.read().decode()}"
            )
