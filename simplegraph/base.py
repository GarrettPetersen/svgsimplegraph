import base64

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
        self.colors = colors or DEFAULT_COLOR_PALETTE
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

    def render(self):
        # Implement the specific rendering for this subclass
        pass

    def to_base64_src(self):
        svg_str = self.render()
        svg_bytes = svg_str.encode("utf-8")
        encoded_svg = base64.b64encode(svg_bytes).decode("utf-8")
        return "data:image/svg+xml;base64," + encoded_svg
