from .base import BaseGraph
from .utils import human_readable_number
from .utils import get_adjusted_max


def max_stacked_bar_height(data, series_types, secondary):
    non_secondary_bars_to_use = [
        not secondary[index] and series_types[index][0] == "bar"
        for index in range(len(secondary))
    ]

    stacked_data = [
        sum(value for i, value in enumerate(column) if non_secondary_bars_to_use[i])
        for column in zip(*data)
    ]
    return max(stacked_data) if stacked_data else 0


def max_non_secondary_value(data, secondary):
    max_values = [(max(values), index) for index, values in enumerate(data)]
    non_secondary_values = [
        value for value, index in max_values if not secondary[index]
    ]
    return max(non_secondary_values) if non_secondary_values else 1


class CategoricalGraph(BaseGraph):
    """
    The graphs generated by this class should have a categorical x-axis (e.g.
    user accounts). They can have a primary and secondary y-axis with different
    scales. Each series can display as bars (stacked or side by side), a line,
    or dots.
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
        stacked=False,
        num_y_ticks=5,
        x_axis_label=None,
        primary_y_axis_label=None,
        secondary_y_axis_label=None,
        show_legend=True,
        rotate_x_labels=True,
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
            secondary_y_axis_label=secondary_y_axis_label,
            show_legend=show_legend,
            rotate_x_labels=rotate_x_labels,
        )
        self.stacked = stacked
        self.bar_width = bar_width
        self.x_labels = []
        self.series_types = []
        self.secondary = []

    def add_series(
        self,
        series,
        legend_label=None,
        series_type="bar",
        print_values=False,
        secondary=False,
    ):
        self.data.append(series)
        self.legend_labels.append(legend_label or "")
        self.series_types.append((series_type, print_values))
        self.secondary.append(secondary)

    def _draw_bar(self, x, y, width, height, fill):
        return (
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" />'
        )

    def _draw_dot(self, x, y, fill, radius=5, stroke="black", stroke_width="1"):
        return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'

    def _draw_line(self, x1, y1, x2, y2, stroke="black", stroke_width="1"):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" />'

    def render(self):
        if self.stacked:
            max_value_primary = max(
                max_stacked_bar_height(self.data, self.series_types, self.secondary),
                max_non_secondary_value(self.data, self.secondary),
            )

            max_value_secondary = max(
                max_stacked_bar_height(
                    self.data,
                    self.series_types,
                    [not sec for sec in self.secondary],
                ),
                max_non_secondary_value(
                    self.data,
                    [not sec for sec in self.secondary],
                ),
            )
        else:
            max_value_primary = max_non_secondary_value(self.data, self.secondary)
            max_value_secondary = max_non_secondary_value(
                self.data, [not sec for sec in self.secondary]
            )

        adjusted_max_value_primary = get_adjusted_max(max_value_primary)
        adjusted_max_value_secondary = get_adjusted_max(max_value_secondary)

        scale_primary = (
            self.height - self.y_top_padding - self.y_bottom_padding
        ) / adjusted_max_value_primary
        scale_secondary = (
            self.height - self.y_top_padding - self.y_bottom_padding
        ) / adjusted_max_value_secondary

        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'

        # Draw legend
        if self.show_legend:
            legend_x = self.x_left_padding
            legend_y = self.y_top_padding / 2
            legend_spacing = 5
            legend_rect_size = 10

            for index, label in enumerate(self.legend_labels):
                series_type, _ = self.series_types[index]
                if series_type == "dot":
                    svg += self._draw_dot(
                        legend_x + legend_rect_size / 2,
                        legend_y + legend_rect_size / 2,
                        radius=5,
                        fill=self.colors[index],
                    )
                elif series_type == "line":
                    svg += self._draw_line(
                        legend_x,
                        legend_y + legend_rect_size / 2,
                        legend_x + legend_rect_size,
                        legend_y + legend_rect_size / 2,
                        stroke=self.colors[index],
                    )
                else:  # series_type == "bar"
                    svg += f'<rect x="{legend_x}" y="{legend_y}" width="{legend_rect_size}" height="{legend_rect_size}" fill="{self.colors[index]}" />'
                svg += f'<text x="{legend_x + legend_rect_size + legend_spacing}" y="{legend_y + legend_rect_size}" font-size="10">{label}</text>'
                legend_x += (2 * legend_spacing) + legend_rect_size + len(label) * 6

        # Draw series
        bar_spacing = (self.width - self.x_left_padding - self.x_right_padding) / len(
            self.data[0]
        )
        bar_series_across = (
            1
            if self.stacked
            else len(
                [
                    series_type
                    for series_type, _ in self.series_types
                    if series_type == "bar"
                ]
            )
        )
        total_bars_width = bar_series_across * self.bar_width

        num_categories = len(self.data[0])
        num_series = len(self.data)
        bar_heights = [0] * num_categories

        for sub_index in range(num_categories):
            for index in range(num_series):
                value = self.data[index][sub_index]
                secondary_value = self.secondary[index]

                series_type, print_values = self.series_types[index]

                if series_type == "dot" or series_type == "line" or self.stacked:
                    x = (
                        self.x_left_padding
                        + sub_index * bar_spacing
                        + (bar_spacing - self.bar_width) / 2
                    )
                else:
                    x = (
                        self.x_left_padding
                        + sub_index * bar_spacing
                        + index * self.bar_width
                    )
                scale = scale_secondary if secondary_value else scale_primary
                y = self.height - self.y_bottom_padding - value * scale

                if series_type == "bar" and self.stacked:
                    bar_height = value * scale
                    x -= self.bar_width / 2
                    y -= bar_heights[sub_index]
                    svg += self._draw_bar(
                        x, y, self.bar_width, bar_height, self.colors[index]
                    )
                    bar_heights[sub_index] += bar_height
                elif series_type == "bar":
                    x += self.bar_width / 2
                    svg += self._draw_bar(
                        x,
                        y,
                        self.bar_width,
                        value * scale,
                        self.colors[index],
                    )
                elif series_type == "dot":
                    center_x = (
                        self.x_left_padding
                        + sub_index * bar_spacing
                        + (bar_spacing - total_bars_width) / 2
                        + self.bar_width * (bar_series_across - 1) / 2
                    )
                    svg += self._draw_dot(
                        center_x,
                        y,
                        radius=5,
                        fill=self.colors[index],
                    )
                elif series_type == "line" and sub_index > 0:
                    prev_y = (
                        self.height
                        - self.y_bottom_padding
                        - self.data[index][sub_index - 1] * scale
                    )
                    prev_x = (
                        self.x_left_padding
                        + (sub_index - 1) * bar_spacing
                        + (bar_spacing - self.bar_width) / 2
                    )
                    svg += self._draw_line(
                        prev_x,
                        prev_y,
                        x,
                        y,
                        stroke=self.colors[index],
                    )

                if print_values:
                    if series_type == "dot":
                        value_x = center_x
                    elif series_type == "line":
                        value_x = x
                    else:
                        value_x = x + self.bar_width / 2

                    value_y = y - 5 if series_type == "bar" else y - 10
                    svg += f'<text x="{value_x}" y="{value_y}" text-anchor="middle" font-size="10">{value}</text>'

        # Draw axis
        svg += f'<line x1="{self.x_left_padding}" y1="{self.y_top_padding}" x2="{self.x_left_padding}" y2="{self.height - self.y_bottom_padding}" stroke="black" stroke-width="1" />'
        svg += f'<line x1="{self.x_left_padding}" y1="{self.height - self.y_bottom_padding}" x2="{self.width - self.x_right_padding}" y2="{self.height - self.y_bottom_padding}" stroke="black" stroke-width="1" />'

        # Draw secondary y-axis if needed
        if any(self.secondary):
            svg += f'<line x1="{self.width - self.x_right_padding}" y1="{self.y_top_padding}" x2="{self.width - self.x_right_padding}" y2="{self.height - self.y_bottom_padding}" stroke="black" stroke-width="1" />'

        # Draw x tick labels
        for index, label in enumerate(self.x_labels):
            x = (
                self.x_left_padding
                + index * bar_spacing
                + (bar_spacing - total_bars_width) / 2
                + self.bar_width * (bar_series_across - 1) / 2
            )
            y = self.height - self.y_bottom_padding + 5
            if label is not None and self.rotate_x_labels:
                svg += f'<text x="{x}" y="{y}" text-anchor="end" font-size="10" transform="rotate(-90 {x} {y})">{label}</text>'
            elif label is not None and not self.rotate_x_labels:
                svg += f'<text x="{x}" y="{y+10}" text-anchor="middle" font-size="10">{label}</text>'

        # Draw primary y-axis ticks and values
        for i in range(self.num_y_ticks + 1):
            tick_value = adjusted_max_value_primary * i / self.num_y_ticks
            tick_y = self.height - self.y_bottom_padding - tick_value * scale_primary
            tick_label = f"{human_readable_number(tick_value)}"

            svg += f'<text x="{self.x_left_padding - 5}" y="{tick_y + 3}" text-anchor="end" font-size="10">{tick_label}</text>'
            svg += f'<line x1="{self.x_left_padding}" y1="{tick_y}" x2="{self.x_left_padding - 3}" y2="{tick_y}" stroke="black" stroke-width="1" />'

        # Draw secondary y-axis ticks and values if needed
        if any(self.secondary):
            for i in range(self.num_y_ticks + 1):
                tick_value = adjusted_max_value_secondary * i / self.num_y_ticks
                tick_y = (
                    self.height - self.y_bottom_padding - tick_value * scale_secondary
                )
                tick_label = f"{human_readable_number(tick_value)}"

                svg += f'<text x="{self.width - self.x_right_padding + 5}" y="{tick_y + 3}" text-anchor="start" font-size="10">{tick_label}</text>'
                svg += f'<line x1="{self.width - self.x_right_padding}" y1="{tick_y}" x2="{self.width - self.x_right_padding + 3}" y2="{tick_y}" stroke="black" stroke-width="1" />'

        # Draw axis labels
        if self.x_axis_label:
            x_label_x = (
                self.width - self.x_left_padding - self.x_right_padding
            ) / 2 + self.x_left_padding
            x_label_y = self.height - self.y_bottom_padding / 4
            svg += f'<text x="{x_label_x}" y="{x_label_y}" text-anchor="middle" font-size="12">{self.x_axis_label}</text>'

        if self.primary_y_axis_label:
            y_label_x = self.x_left_padding / 4
            y_label_y = (
                self.height - self.y_top_padding - self.y_bottom_padding
            ) / 2 + self.y_top_padding
            svg += f'<text x="{y_label_x}" y="{y_label_y}" text-anchor="middle" font-size="12" transform="rotate(-90 {y_label_x} {y_label_y})">{self.primary_y_axis_label}</text>'

        if any(self.secondary) and self.secondary_y_axis_label:
            sec_y_label_x = self.width - self.x_right_padding / 4
            sec_y_label_y = self.height / 2
            svg += f'<text x="{sec_y_label_x}" y="{sec_y_label_y}" text-anchor="middle" font-size="12" transform="rotate(-90 {sec_y_label_x} {sec_y_label_y})">{self.secondary_y_axis_label}</text>'

        svg += "</svg>"
        return svg