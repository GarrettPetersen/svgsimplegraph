import base64
import urllib.request
import json
import time
import math

from .utils import DEFAULT_COLOR_PALETTE
from .utils import is_dark
from .utils import estimate_text_dimensions


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
        title=None,
        title_font_size=None,
        element_spacing=None,
        watermark=None,
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
        self.title = title
        self.title_font_size = title_font_size or 16
        self.defs = []
        self.svg_elements = []
        self.element_spacing = element_spacing or 10
        self.watermark = watermark

        # Use dark colors last if in dark mode and using default color palette
        if self.colors == DEFAULT_COLOR_PALETTE and self.dark_mode:
            self.colors.sort(key=lambda x: is_dark(x))

        self.text_color = "#ffffff" if self.dark_mode else "#000000"

        self.most_extreme_dimensions = {
            "left": self.width,
            "right": 0,
            "top": self.height,
            "bottom": 0,
        }

    def _generate_text(
        self,
        text,
        x,
        y,
        font_size=10,
        fill=None,
        anchor="middle",
        dominant_baseline="middle",
        rotation=None,
        additional_attributes=None,
    ):
        if not fill:
            fill = self.text_color
        # Start building the SVG text element
        text_element = f'<text x="{x}" y="{y}" font-size="{font_size}" fill="{fill}"'

        # Add optional attributes
        if anchor:
            text_element += f' text-anchor="{anchor}"'
        if dominant_baseline:
            text_element += f' dominant-baseline="{dominant_baseline}"'
        if rotation:
            text_element += f' transform="rotate({rotation} {x} {y})"'
        if additional_attributes:
            text_element += " " + " ".join(
                [f'{k}="{v}"' for k, v in additional_attributes.items()]
            )

        # Close the opening tag and add the text content
        text_element += f">{text}</text>"

        # Estimate the text dimensions
        text_width, text_height = estimate_text_dimensions(text, font_size)

        # Adjust the bounding box coordinates according to the anchor and dominant-baseline
        if anchor == "end":
            left = x - text_width
        elif anchor == "start":
            left = x
        else:  # Default to middle
            left = x - text_width / 2

        right = left + text_width

        if dominant_baseline in ["auto", "text-bottom", "alphabetic", "ideographic"]:
            top = y - text_height
        elif dominant_baseline in ["text-top", "hanging"]:
            top = y
        else:  # Default to middle
            top = y - text_height / 2

        bottom = top + text_height

        if rotation:
            # Rotate each corner of the bounding box
            corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
            rotation_radians = math.radians(rotation)
            rotated_corners = [
                (
                    x
                    + (cx - x) * math.cos(rotation_radians)
                    - (cy - y) * math.sin(rotation_radians),
                    y
                    + (cx - x) * math.sin(rotation_radians)
                    + (cy - y) * math.cos(rotation_radians),
                )
                for cx, cy in corners
            ]

            # Recalculate the bounding box from the rotated corners
            xs, ys = zip(*rotated_corners)
            left, right = min(xs), max(xs)
            top, bottom = min(ys), max(ys)

        # Update the most extreme dimensions
        self.most_extreme_dimensions["left"] = min(
            self.most_extreme_dimensions["left"], left
        )
        self.most_extreme_dimensions["right"] = max(
            self.most_extreme_dimensions["right"], right
        )
        self.most_extreme_dimensions["top"] = min(
            self.most_extreme_dimensions["top"], top
        )
        self.most_extreme_dimensions["bottom"] = max(
            self.most_extreme_dimensions["bottom"], bottom
        )

        return text_element

    def _reset_graph(self):
        self.most_extreme_dimensions = {
            "left": self.width,
            "right": 0,
            "top": self.height,
            "bottom": 0,
        }
        self.defs = []
        self.svg_elements = []

    def _generate_svg(self):
        """
        Generate the SVG string from the styles and elements.
        """
        if self.title:
            title_x_position = self.width / 2
            title_y_position = (
                min(0, self.most_extreme_dimensions["top"]) - self.element_spacing
            )
            self.svg_elements.append(
                self._generate_text(
                    self.title,
                    title_x_position,
                    title_y_position,
                    font_size=self.title_font_size,
                    fill=self.text_color,
                    anchor="middle",
                    dominant_baseline="text-top",
                )
            )

        viewbox_width = (
            self.most_extreme_dimensions["right"]
            - self.most_extreme_dimensions["left"]
            + self.x_left_padding
            + self.x_right_padding
        )

        viewbox_height = (
            self.most_extreme_dimensions["bottom"]
            - self.most_extreme_dimensions["top"]
            + self.y_top_padding
            + self.y_bottom_padding
        )

        viewbox_left = self.most_extreme_dimensions["left"] - self.x_left_padding
        viewbox_top = self.most_extreme_dimensions["top"] - self.y_top_padding

        viewbox_param = (
            f'viewBox="{viewbox_left} {viewbox_top} {viewbox_width} {viewbox_height}"'
        )

        background_rect = ""
        if self.background_color:
            background_rect = (
                f"<rect x='{viewbox_left}' y='{viewbox_top}' width='{viewbox_width}' height='{viewbox_height}' "
                + f"rx='10' ry='10' fill='{self.background_color}' />"
            )

        if self.watermark:
            self.svg_elements.append(self.watermark)

        defs_str = ""
        if self.defs:
            defs_str = "<defs>" + "\n".join(self.defs) + "</defs>"
        svg_elements_str = "\n".join(self.svg_elements)
        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{viewbox_width}' height='{viewbox_height}' {viewbox_param}>"
            + defs_str
            + background_rect
            + svg_elements_str
            + "</svg>"
        )
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
