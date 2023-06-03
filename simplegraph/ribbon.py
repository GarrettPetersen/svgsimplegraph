from .base import BaseGraph
from .utils import human_readable_number
from .utils import get_adjusted_max
from .utils import get_adjusted_min
from .utils import get_color
from .utils import is_dark


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
        self.text_color = "#ffffff" if self.dark_mode else "#000000"

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
        assert self.num_series in [2, 3], "Two or three series are required"

        max_value = max(self.data[0] + self.data[1])

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

        adjusted_max_value_primary = get_adjusted_max(max_value)

        scale_primary = (
            self.height - self.y_top_padding - self.y_bottom_padding
        ) / adjusted_max_value_primary

        svg = ""
        svg_defs = f"""
<defs>
    <linearGradient id="legend_grad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:{self.colors[1]}" />
        <stop offset="100%" style="stop-color:{self.colors[0]}" />
    </linearGradient>
</defs>"""

        # Draw legend
        if self.show_legend:
            third_graph_width = (
                self.width - self.x_left_padding - self.x_right_padding
            ) / 3
            graph_height = self.height - self.y_top_padding - self.y_bottom_padding
            top_legend_x = self.x_left_padding + third_graph_width
            top_legend_y = (self.y_top_padding / 2) - (self.bar_width / 2)
            half_bar_width = self.bar_width / 2

            svg += f'<path d="M{top_legend_x} {top_legend_y} h{third_graph_width} l{half_bar_width} {half_bar_width} l-{half_bar_width} {half_bar_width} h-{third_graph_width} l{half_bar_width} -{half_bar_width}" fill="{self.colors[0]}" />'
            svg += f'<text x="{top_legend_x}" y="{top_legend_y + half_bar_width}" dy="0.35em" font-size="10" text-anchor="end" fill="{self.text_color}">{self.legend_labels[0]}</text>'
            svg += f'<text x="{top_legend_x+third_graph_width+half_bar_width+5}" y="{top_legend_y + half_bar_width}" dy="0.35em" font-size="10" text-anchor="start" fill="{self.text_color}">{self.legend_labels[1]}</text>'

            if color_series_present:
                right_legend_x = (
                    self.width - (self.x_right_padding / 2) - (self.bar_width / 2)
                )
                right_legend_y = self.y_top_padding
                right_legend_y_middle = right_legend_y + graph_height / 2

                svg += f'<rect x="{right_legend_x}" y="{right_legend_y}" width="{self.bar_width}" height="{graph_height}" fill="url(#legend_grad)" />'
                svg += f'<text x="{right_legend_x-5}" y="{right_legend_y_middle}" text-anchor="middle" font-size="10" transform="rotate(-90 {right_legend_x-5} {right_legend_y_middle})" fill="{self.text_color}">{self.legend_labels[2]}</text>'
                svg += f'<text x="{right_legend_x+self.bar_width+5}" y="{right_legend_y}" dy="0.35em" text-anchor="start" font-size="10" fill="{self.text_color}">{human_readable_number(max_color_range)}</text>'
                svg += f'<text x="{right_legend_x+self.bar_width+5}" y="{right_legend_y+graph_height}" dy="0.35em" text-anchor="start" font-size="10" fill="{self.text_color}">{human_readable_number(min_color_range)}</text>'

        # Draw ribbons
        num_ribbons = len(self.data[0])
        bar_spacing = (self.width - self.x_left_padding - self.x_right_padding) / (
            num_ribbons + 1 / 2
        )

        for index in range(num_ribbons):
            x = (index + 1 / 2) * bar_spacing + self.x_left_padding
            y1 = (
                self.height
                - self.y_bottom_padding
                - self.data[0][index] * scale_primary
            )
            y2 = (
                self.height
                - self.y_bottom_padding
                - self.data[1][index] * scale_primary
            )
            color = self.colors[0]
            if color_series_present:
                color_val = self.data[2][index]
                color_range = max_color_range - min_color_range
                color_percent = (color_val - min_color_range) / color_range
                color = get_color(color_percent, self.colors[0], self.colors[1])
            svg += self._draw_ribbon(x, y1, y2, self.bar_width, color)
            if self.print_values[0]:
                if y1 < y2:
                    svg += f'<text x="{x+self.bar_width/2}" y="{y1}" dy="0.35em" text-anchor="middle" font-size="10" fill="{self.text_color}">{human_readable_number(self.data[0][index])}</text>'
                else:
                    svg += f'<text x="{x+self.bar_width/2}" y="{y1}" dy="0.35em" text-anchor="middle" font-size="10" fill="{self.text_color}">{human_readable_number(self.data[0][index])}</text>'
            if self.print_values[1]:
                if y2 < y1:
                    svg += f'<text x="{x+self.bar_width/2}" y="{y2-self.bar_width/2-5}" dy="0.35em" text-anchor="middle" font-size="10" fill="{self.text_color}">{human_readable_number(self.data[1][index])}</text>'
                else:
                    svg += f'<text x="{x+self.bar_width/2}" y="{y2+self.bar_width/2+5}" dy="0.35em" text-anchor="middle" font-size="10" fill="{self.text_color}">{human_readable_number(self.data[1][index])}</text>'
            if color_series_present and self.print_values[2]:
                if y1 < y2:
                    y_adjustment = self.bar_width / 4
                else:
                    y_adjustment = -self.bar_width / 4
                if is_dark(color):
                    optional_fill = 'fill="white"'
                else:
                    optional_fill = ""
                svg += f'<text x="{x+self.bar_width/2}" y="{(y1+y2)/2 + y_adjustment}" dy="0.35em" text-anchor="middle" font-size="10" {optional_fill}>{human_readable_number(self.data[2][index])}</text>'

        # Draw axis
        svg += f'<line x1="{self.x_left_padding}" y1="{self.y_top_padding}" x2="{self.x_left_padding}" y2="{self.height - self.y_bottom_padding}" stroke="{self.text_color}" stroke-width="1" />'
        svg += f'<line x1="{self.x_left_padding}" y1="{self.height - self.y_bottom_padding}" x2="{self.width - self.x_right_padding}" y2="{self.height - self.y_bottom_padding}" stroke="{self.text_color}" stroke-width="1" />'

        # Draw x tick labels
        for index, label in enumerate(self.x_labels):
            x = (index + 1 / 2) * bar_spacing + self.x_left_padding + self.bar_width / 2
            y = self.height - self.y_bottom_padding + 5
            if label is not None and self.rotate_x_labels:
                svg += f'<text x="{x}" y="{y}" text-anchor="end" font-size="10" transform="rotate(-90 {x} {y})" fill="{self.text_color}">{label}</text>'
            elif label is not None and not self.rotate_x_labels:
                svg += f'<text x="{x}" y="{y+10}" text-anchor="middle" font-size="10" fill="{self.text_color}">{label}</text>'

        # Draw primary y-axis ticks and values
        for i in range(self.num_y_ticks + 1):
            tick_value = adjusted_max_value_primary * i / self.num_y_ticks
            tick_y = self.height - self.y_bottom_padding - tick_value * scale_primary
            tick_label = f"{human_readable_number(tick_value)}"

            svg += f'<text x="{self.x_left_padding - 5}" y="{tick_y + 3}" text-anchor="end" font-size="10" fill="{self.text_color}">{tick_label}</text>'
            svg += f'<line x1="{self.x_left_padding}" y1="{tick_y}" x2="{self.x_left_padding - 3}" y2="{tick_y}" stroke="{self.text_color}" stroke-width="1" />'

        # Draw axis labels
        if self.x_axis_label:
            x_label_x = (
                self.width - self.x_left_padding - self.x_right_padding
            ) / 2 + self.x_left_padding
            x_label_y = self.height - self.y_bottom_padding / 4
            svg += f'<text x="{x_label_x}" y="{x_label_y}" text-anchor="middle" font-size="12" fill="{self.text_color}">{self.x_axis_label}</text>'

        if self.primary_y_axis_label:
            y_label_x = self.x_left_padding / 4
            y_label_y = (
                self.height - self.y_top_padding - self.y_bottom_padding
            ) / 2 + self.y_top_padding
            svg += f'<text x="{y_label_x}" y="{y_label_y}" text-anchor="middle" font-size="12" transform="rotate(-90 {y_label_x} {y_label_y})" fill="{self.text_color}">{self.primary_y_axis_label}</text>'

        background_rect = ""
        if self.background_color:
            # Draw background with rounded corners
            background_rect = (
                f"<rect x='0' y='0' width='{self.width}' height='{self.height}' "
                + f"rx='10' ry='10' fill='{self.background_color}' />"
            )

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'
            + svg_defs
            + background_rect
            + svg
            + "</svg>"
        )
        return svg
