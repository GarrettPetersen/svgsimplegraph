import base64

from simplegraph.utils import DEFAULT_COLOR_PALETTE


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
        stacked=False,
        num_y_ticks=5,
        x_axis_label=None,
        primary_y_axis_label=None,
        secondary_y_axis_label=None,
        show_legend=True,
        rotate_x_labels=True,
    ):
        self.width = width
        self.height = height
        self.y_top_padding = y_top_padding or y_padding or padding
        self.y_bottom_padding = y_bottom_padding or y_padding or padding
        self.x_left_padding = x_left_padding or x_padding or padding
        self.x_right_padding = x_right_padding or x_padding or padding
        self.colors = colors or DEFAULT_COLOR_PALETTE
        self.stacked = stacked
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

    def render(self):
        # Implement the specific rendering for this subclass
        pass

    def to_base64_src(self):
        svg_str = self.render()
        svg_bytes = svg_str.encode("utf-8")
        encoded_svg = base64.b64encode(svg_bytes).decode("utf-8")
        return "data:image/svg+xml;base64," + encoded_svg
