from .base import BaseGraph
from .utils import human_readable_number
from .utils import get_adjusted_max
from .utils import get_adjusted_min
from .utils import get_color
from .utils import is_dark
from .utils import calculate_ticks


class RibbonGraph(BaseGraph):
    """
    This graph is for comparing two series with the same scale, while a third
    series with a different scale is represented by a heatmap.
    """

    def __init__(
        self,
        width=300,
        height=200,
        bar_width=30,
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
        show_legend=True,
        rotate_x_labels=True,
        color_range=None,
        background_color=None,
        dark_mode=None,
    ):
        super().__init__(
            width=width,
            height=height,
            padding=padding,
            x_padding=x_padding,
            y_padding=y_padding,
            y_top_padding=y_top_padding,
            y_bottom_padding=y_bottom_padding,
            x_left_padding=x_left_padding,
            x_right_padding=x_right_padding,
            colors=colors,
            num_y_ticks=num_y_ticks,
            x_axis_label=x_axis_label,
            primary_y_axis_label=primary_y_axis_label,
            show_legend=show_legend,
            rotate_x_labels=rotate_x_labels,
            background_color=background_color,
            dark_mode=dark_mode,
        )
        self.bar_width = bar_width
        self.x_labels = []
        self.print_values = []
        self.num_series = 0
        self.color_range = color_range

    def add_series(
        self,
        series,
        legend_label=None,
        print_values=False,
    ):
        self.data.append(series)
        self.legend_labels.append(legend_label or "")
        self.print_values.append(print_values)
        assert self.num_series < 3, "Only three series are allowed"
        self.num_series += 1

    def _draw_ribbon(self, x, y1, y2, width, fill):
        half_width = width / 2
        if y1 < y2:
            diff = y2 - y1
            return (
                f'<path d="M{x} {y1} v{diff} l{half_width} {half_width} '
                + f"l{half_width} -{half_width} v-{diff} l-{half_width} "
                + f'{half_width}" fill="{fill}" />'
            )
        else:
            diff = y1 - y2
            return (
                f'<path d="M{x} {y2} v{diff} l{half_width} -{half_width} '
                + f"l{half_width} {half_width} v-{diff} l-{half_width} "
                + f'-{half_width}" fill="{fill}" />'
            )

    def render(self):
        self._reset_graph()
        self.defs = []
        self.svg_elements = []
        assert self.num_series in [2, 3], "Two or three series are required"

        max_value = max(self.data[0] + self.data[1])
        min_value = min(self.data[0] + self.data[1])

        color_series_present = True if self.num_series == 3 else False

        if color_series_present and self.color_range:
            max_color_range = self.color_range[1]
            min_color_range = self.color_range[0]
        elif color_series_present:
            max_range = max(self.data[2])
            min_range = min(self.data[2])
            # Adjust max and min range to be round numbers
            if max_range >= 0:
                max_color_range = get_adjusted_max(max_range)
            else:
                max_color_range = -get_adjusted_min(-max_range)
            if min_range >= 0:
                min_color_range = get_adjusted_min(min_range)
            else:
                min_color_range = -get_adjusted_max(-min_range)

        primary_ticks = calculate_ticks(
            min_value,
            max_value,
            include_zero=True,
            target_tick_count=self.num_y_ticks,
        )

        adjusted_max_value = primary_ticks[-1]
        adjusted_min_value = primary_ticks[0]

        scale_primary = (self.height) / (adjusted_max_value - adjusted_min_value)

        self.defs.append(
            "<linearGradient id='legend_grad' x1='0%' y1='0%' x2='0%' y2='100%'>"
            + f"<stop offset='0%' style='stop-color:{self.colors[1]}' />"
            + f"<stop offset='100%' style='stop-color:{self.colors[0]}' /></linearGradient>"
        )

        # Draw legend
        if self.show_legend:
            third_graph_width = (self.width) / 3
            graph_height = self.height
            top_legend_x = third_graph_width
            top_legend_y = -(self.bar_width / 2)
            half_bar_width = self.bar_width / 2

            self.svg_elements.append(
                f'<path d="M{top_legend_x} {top_legend_y} h{third_graph_width} l{half_bar_width} {half_bar_width} l-{half_bar_width} {half_bar_width} h-{third_graph_width} l{half_bar_width} -{half_bar_width}" fill="{self.colors[0]}" />'
            )
            self.svg_elements.append(
                self._generate_text(
                    self.legend_labels[0],
                    top_legend_x,
                    top_legend_y + half_bar_width,
                    fill=self.text_color,
                    anchor="end",
                )
            )
            self.svg_elements.append(
                self._generate_text(
                    self.legend_labels[1],
                    top_legend_x + third_graph_width + half_bar_width + 5,
                    top_legend_y + half_bar_width,
                    fill=self.text_color,
                    anchor="start",
                )
            )

            if color_series_present:
                right_legend_x = self.width + 10 - (self.bar_width / 2)
                right_legend_y = 0
                right_legend_y_middle = right_legend_y + graph_height / 2

                self.svg_elements.append(
                    f'<rect x="{right_legend_x}" y="{right_legend_y}" width="{self.bar_width}" height="{graph_height}" fill="url(#legend_grad)" />'
                )
                self.svg_elements.append(
                    self._generate_text(
                        self.legend_labels[2],
                        right_legend_x - 5,
                        right_legend_y_middle,
                        fill=self.text_color,
                        anchor="middle",
                        rotation=-90,
                    )
                )
                self.svg_elements.append(
                    self._generate_text(
                        human_readable_number(max_color_range),
                        right_legend_x + self.bar_width + 5,
                        right_legend_y,
                        fill=self.text_color,
                        anchor="start",
                    )
                )
                self.svg_elements.append(
                    self._generate_text(
                        human_readable_number(min_color_range),
                        right_legend_x + self.bar_width + 5,
                        right_legend_y + graph_height,
                        fill=self.text_color,
                        anchor="start",
                    )
                )

        # Draw ribbons
        num_ribbons = len(self.data[0])
        bar_spacing = (self.width) / (num_ribbons + 1 / 2)

        for index in range(num_ribbons):
            x = (index + 1 / 2) * bar_spacing
            y1 = (
                self.height - (self.data[0][index] - adjusted_min_value) * scale_primary
            )
            y2 = (
                self.height - (self.data[1][index] - adjusted_min_value) * scale_primary
            )
            color = self.colors[0]
            if color_series_present:
                color_val = self.data[2][index]
                color_range = max_color_range - min_color_range
                color_percent = (color_val - min_color_range) / color_range
                color = get_color(color_percent, self.colors[0], self.colors[1])
            self.svg_elements.append(
                self._draw_ribbon(x, y1, y2, self.bar_width, color)
            )
            if self.print_values[0]:
                if y1 < y2:
                    self.svg_elements.append(
                        self._generate_text(
                            human_readable_number(self.data[0][index]),
                            x + self.bar_width / 2,
                            y1,
                            fill=self.text_color,
                            anchor="middle",
                        )
                    )
                else:
                    self.svg_elements.append(
                        self._generate_text(
                            human_readable_number(self.data[0][index]),
                            x + self.bar_width / 2,
                            y1,
                            fill=self.text_color,
                            anchor="middle",
                        )
                    )
            if self.print_values[1]:
                if y2 < y1:
                    self.svg_elements.append(
                        self._generate_text(
                            human_readable_number(self.data[1][index]),
                            x + self.bar_width / 2,
                            y2 - self.bar_width / 2 - 7,
                            fill=self.text_color,
                            anchor="middle",
                        )
                    )
                else:
                    self.svg_elements.append(
                        self._generate_text(
                            human_readable_number(self.data[1][index]),
                            x + self.bar_width / 2,
                            y2 + self.bar_width / 2 + 5,
                            fill=self.text_color,
                            anchor="middle",
                        )
                    )
            if color_series_present and self.print_values[2]:
                if y1 < y2:
                    y_adjustment = self.bar_width / 4
                else:
                    y_adjustment = -self.bar_width / 4
                text_color = "#ffffff" if is_dark(color) else "#000000"
                self.svg_elements.append(
                    self._generate_text(
                        human_readable_number(self.data[2][index]),
                        x + self.bar_width / 2,
                        (y1 + y2) / 2 + y_adjustment,
                        fill=text_color,
                        anchor="middle",
                    )
                )

        # Draw axis
        self.svg_elements.append(
            f'<line x1="0" y1="0" x2="0" y2="{self.height}" stroke="{self.text_color}" stroke-width="1" />'
        )
        if adjusted_min_value < 0 and adjusted_max_value > 0:
            zero_line = self.height - (0 - adjusted_min_value) * scale_primary
            self.svg_elements.append(
                f'<line x1="0" y1="{zero_line}" x2="{self.width}" y2="{zero_line}" stroke="{self.text_color}" stroke-width="1" />'
            )
        else:
            self.svg_elements.append(
                f'<line x1="0" y1="{self.height}" x2="{self.width}" y2="{self.height}" stroke="{self.text_color}" stroke-width="1" />'
            )

        # Draw x tick labels
        for index, label in enumerate(self.x_labels):
            x = (index + 1 / 2) * bar_spacing + self.bar_width / 2
            y = self.height + 5
            if label is not None and self.rotate_x_labels:
                self.svg_elements.append(
                    self._generate_text(
                        label, x, y, fill=self.text_color, anchor="end", rotation=-90
                    )
                )
            elif label is not None and not self.rotate_x_labels:
                self.svg_elements.append(
                    self._generate_text(
                        label, x, y + 10, fill=self.text_color, anchor="middle"
                    )
                )

        # Draw primary y-axis ticks and values
        for tick_value in primary_ticks:
            tick_y = self.height - (tick_value - adjusted_min_value) * scale_primary
            tick_label = f"{human_readable_number(tick_value)}"

            self.svg_elements.append(
                self._generate_text(
                    tick_label,
                    -5,
                    tick_y + 3,
                    fill=self.text_color,
                    anchor="end",
                )
            )
            self.svg_elements.append(
                f'<line x1="0" y1="{tick_y}" x2="-3" y2="{tick_y}" stroke="{self.text_color}" stroke-width="1" />'
            )

        # Draw axis labels
        if self.x_axis_label:
            x_label_x = (self.width) / 2
            x_label_y = self.height + 5
            self.svg_elements.append(
                self._generate_text(
                    self.x_axis_label,
                    x_label_x,
                    x_label_y,
                    font_size=12,
                    fill=self.text_color,
                    anchor="middle",
                )
            )

        if self.primary_y_axis_label:
            y_label_x = -5
            y_label_y = (self.height) / 2
            self.svg_elements.append(
                self._generate_text(
                    self.primary_y_axis_label,
                    y_label_x,
                    y_label_y,
                    font_size=12,
                    fill=self.text_color,
                    anchor="middle",
                    rotation=-90,
                )
            )

        return self._generate_svg()
