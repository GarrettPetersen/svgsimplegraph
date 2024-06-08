from .categorical import CategoricalGraph
from .utils import estimate_text_dimensions
from .utils import to_snake_case
import uuid
import base64


class ToggleGraph:
    """
    The graphs generated by this class takes in CategoricalGraph objects and
    creates an interactive SVG with buttons that switch between them.
    """

    def __init__(self):
        self.graphs = []
        self.labels = []
        self.label_ids = []
        self.default = 0
        self.most_extreme_dimensions = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0,
        }
        self.defs = []
        self.svg_elements = []
        self.background_color = None
        self.element_spacing = None
        self.font_width_estimate_multiplier = None
        self.widest_label = 0
        self.tallest_label = 0
        self.colors = ["#73bed3", "#c7cfcc"]
        self.x_left_padding = 0
        self.x_right_padding = 0
        self.y_top_padding = 0
        self.y_bottom_padding = 0

    def add_graph(self, graph: CategoricalGraph, label: str, is_default: bool = False):
        # Enforce type hint
        if not isinstance(graph, CategoricalGraph):
            raise TypeError("Expected 'graph' to be an instance of CategoricalGraph.")

        self.graphs.append(graph)
        self.labels.append(label)
        self.label_ids.append(to_snake_case(f"{label}_{uuid.uuid4()}"))

        if is_default:
            self.default = len(graph) - 1

    def _reset_graph(self):
        self.most_extreme_dimensions = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0,
        }
        self.defs = set()
        self.svg_elements = []
        self.widest_label = 0

    def render(self):
        self._reset_graph()

        for index, graph in enumerate(self.graphs):
            # Render the graph to generate its SVG elements
            graph.render()
            self.defs.update(graph.defs)
            self.svg_elements.append(graph.svg_elements)

            # Track the biggest dimensions of all graphs
            self.most_extreme_dimensions["left"] = min(
                self.most_extreme_dimensions["left"],
                graph.most_extreme_dimensions["left"],
            )
            self.most_extreme_dimensions["right"] = max(
                self.most_extreme_dimensions["right"],
                graph.most_extreme_dimensions["right"],
                graph.width,
            )
            self.most_extreme_dimensions["top"] = min(
                self.most_extreme_dimensions["top"],
                graph.most_extreme_dimensions["top"],
            )
            self.most_extreme_dimensions["bottom"] = max(
                self.most_extreme_dimensions["bottom"],
                graph.most_extreme_dimensions["bottom"],
                graph.height,
            )

            if index == self.default:
                self.background_color = graph.background_color
                self.element_spacing = graph.element_spacing
                self.font_width_estimate_multiplier = (
                    graph.font_width_estimate_multiplier
                )
                self.x_left_padding = graph.x_left_padding
                self.x_right_padding = graph.x_right_padding
                self.y_top_padding = graph.y_top_padding
                self.y_bottom_padding = graph.y_bottom_padding

        for label in self.labels:
            # Track the widest label for button width
            estimated_x, estimated_y = estimate_text_dimensions(
                label, 10, self.font_width_estimate_multiplier
            )
            self.widest_label = max(
                estimated_x,
                self.widest_label,
            )
            self.tallest_label = max(estimated_y, self.tallest_label)

        defs_str = ""
        if self.defs:
            defs_str = "<defs>" + "\n".join(self.defs) + "</defs>"

        svg_elements_str = ""
        for index, this_svg_elements in enumerate(self.svg_elements):
            visibility = "visible" if self.default == index else "hidden"
            svg_elements_str += f"<g visibility ='{visibility}' >"
            svg_elements_str += "\n".join(this_svg_elements)
            label_ids_that_deactivate = ""
            for i, label_id in enumerate(self.label_ids):
                if index == i:
                    svg_elements_str += f"<set attributeName='visibility' to='visible' begin='{label_id}.click' />"
                else:
                    label_ids_that_deactivate += f"{label_id}.click;"
            svg_elements_str += f"<set attributeName='visibility' to='hidden' begin='{label_ids_that_deactivate}' /></g>"

        button_x_position = self.most_extreme_dimensions["right"] + self.element_spacing
        button_y_position = 0
        for index, (label, label_id) in enumerate(zip(self.labels, self.label_ids)):
            # Draw buttons
            svg_elements_str += f"<g id='{label_id}' transform='translate({button_x_position} {button_y_position})'>"
            width = 2 * self.element_spacing + self.widest_label
            height = self.element_spacing + self.tallest_label
            color = self.colors[0] if index == self.default else self.colors[1]
            label_ids_that_deactivate = ""
            for other_label_id in self.label_ids:
                if label_id != other_label_id:
                    label_ids_that_deactivate += f"{other_label_id}.click;"
            svg_elements_str += (
                f"<rect width='{width}' height='{height}' rx='{height/2}' ry='{height/2}' fill='{color}'>"
                + f"<set attributeName='fill' to='{self.colors[0]}' begin='{label_id}.click' />"
                + f"<set attributeName='fill' to='{self.colors[1]}' begin='{label_ids_that_deactivate}' /></rect>"
                + f"<text x='{width/2}' y='{height/2}' text-anchor='middle' dominant-baseline='middle' font-size='10'>{label}</text></g>"
            )

            button_y_position += self.tallest_label + 1.5 * self.element_spacing

        self.most_extreme_dimensions["right"] = (
            button_x_position + 2 * self.element_spacing + self.widest_label
        )
        self.most_extreme_dimensions["bottom"] = max(
            self.most_extreme_dimensions["bottom"],
            button_y_position - 0.5 * self.element_spacing,
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

        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{viewbox_width}' height='{viewbox_height}' {viewbox_param}>"
            + defs_str
            + background_rect
            + svg_elements_str
            + "</svg>"
        )
        return svg

    def to_base64_src(self):
        svg_str = self.render()
        svg_bytes = svg_str.encode("utf-8")
        encoded_svg = base64.b64encode(svg_bytes).decode("utf-8")
        return "data:image/svg+xml;base64," + encoded_svg
