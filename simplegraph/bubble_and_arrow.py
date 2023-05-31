import math

from .base import BaseGraph
from .utils import hex_to_rgba
from .utils import is_dark


class BubbleAndArrowGraph(BaseGraph):
    """
    The graphs generated by this class feature bubbles and arrows. The bubbles
    and arrows are sized based on the data provided. The bubbles are colored
    based on the legend labels provided. The arrows are colored based on the
    data provided.
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
        self.bubbles = []
        self.arrows = []
        self.total_arrow_width_from_origin = {}
        self.cx = self.width / 2
        self.cy = self.height / 2

    def add_bubble(
        self,
        size,
        inner_size=None,
        text=None,
    ):
        self.bubbles.append((size, inner_size, text))

    def add_arrow(
        self,
        origin,
        destination,
        size,
    ):
        if size > 0 and origin != destination:
            self.arrows.append((origin, destination, size))
            if origin not in self.total_arrow_width_from_origin:
                self.total_arrow_width_from_origin[origin] = 0
            self.total_arrow_width_from_origin[origin] += size

    def _draw_dot(self, x, y, fill, radius=5, inner_radius=None, text=None):
        dot = f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" />'
        if inner_radius:
            dot += f'<circle cx="{x}" cy="{y}" r="{inner_radius}" fill="white" />'
        if text:
            text_color = "white" if is_dark(fill) and not inner_radius else "black"
            dot += (
                f'<text x="{x}" y="{y}" text-anchor="middle" '
                + f'dominant-baseline="middle" fill="{text_color}">{text}</text>'
            )
        return dot

    def _draw_arrow(
        self, x1, y1, x2, y2, cx, cy, backoff, fill="black", width=1, start_offset=0
    ):
        arrow_head_length = max(10, width / 5)
        direction_in = math.atan2(y2 - cy, x2 - cx)
        direction_mid = math.atan2(y2 - y1, x2 - x1)
        direction_out = math.atan2(y1 - cy, x1 - cx)
        perpendicular = direction_mid + math.pi / 2
        perpendicular_out = direction_out + math.pi / 2
        perpendicular_in = direction_in + math.pi / 2
        cx_offset = math.cos(perpendicular) * width / 2
        cy_offset = math.sin(perpendicular) * width / 2
        x_out_offset = math.cos(perpendicular_out) * width / 2
        y_out_offset = math.sin(perpendicular_out) * width / 2
        x_out_shift = math.cos(perpendicular_out) * start_offset
        y_out_shift = math.sin(perpendicular_out) * start_offset
        x_in_offset = math.cos(perpendicular_in) * width / 2
        y_in_offset = math.sin(perpendicular_in) * width / 2

        # Calculate backoff
        backoff_x = math.cos(direction_in) * backoff
        backoff_y = math.sin(direction_in) * backoff

        # New position of x2, y2 after backoff
        x2_backoff = x2 - backoff_x
        y2_backoff = y2 - backoff_y

        # Arrow head with respect to the original x2, y2, but positioned at the backoff location
        x_arrow_head = x2_backoff - math.cos(direction_in) * arrow_head_length
        y_arrow_head = y2_backoff - math.sin(direction_in) * arrow_head_length

        # Control points for each side of the arrow, adjusted by half the width in the direction perpendicular to the arrow
        ctrl_x1 = cx + cx_offset
        ctrl_y1 = cy + cy_offset
        ctrl_x2 = cx - cx_offset
        ctrl_y2 = cy - cy_offset

        return (
            f'<path d="M {x1-x_out_offset-x_out_shift},{y1-y_out_offset-y_out_shift} '
            + f"Q{ctrl_x1},{ctrl_y1} {x_arrow_head + x_in_offset},{y_arrow_head + y_in_offset} "
            + f"L{x_arrow_head + 1.3 * x_in_offset},{y_arrow_head + 1.3 * y_in_offset} "
            + f"L{x2_backoff},{y2_backoff} L{x_arrow_head - 1.3 * x_in_offset},{y_arrow_head - 1.3 * y_in_offset} "
            + f"L{x_arrow_head - x_in_offset},{y_arrow_head - y_in_offset}"
            + f'Q{ctrl_x2},{ctrl_y2} {x1+x_out_offset-x_out_shift},{y1+y_out_offset-x_out_shift} z" '  # Z closes the path
            + f'fill="{hex_to_rgba(fill,0.5)}" />'
        )

    def _calculate_positions(self):
        inter_bubble_space = 0.1  # Proportional gap between bubbles

        # Calculate radii for all bubbles without scaling
        unscaled_bubbles = [
            (
                math.sqrt(bubble[0] / math.pi),
                math.sqrt(bubble[1] / math.pi) if bubble[1] else None,
                bubble[2],
            )
            for bubble in self.bubbles
        ]

        # Distribute bubbles evenly around a circle
        num_bubbles = len(unscaled_bubbles)

        # Compute the minimum circle radius to avoid any overlap between bubbles
        min_circle_radius = (
            sum((1 + inter_bubble_space) * bubble[0] for bubble in unscaled_bubbles)
            / num_bubbles
            / math.sin(math.pi / num_bubbles)
        )
        largest_radii = sorted(bubble[0] for bubble in unscaled_bubbles)[-2:]
        min_circle_radius = max(
            min_circle_radius, sum(largest_radii) * (1 + inter_bubble_space)
        )

        # With this circle radius, determine the diameter and add some inter-bubble space
        min_diameter = 2 * (
            min_circle_radius + largest_radii[-1] * (1 + inter_bubble_space)
        )

        # Now compute the scaling factor to fit this minimum circle within the canvas
        scaling_factor = min(self.width, self.height) / min_diameter

        # Apply the scaling factor to the bubbles
        scaled_bubbles = [
            (
                bubble[0] * scaling_factor,
                bubble[1] * scaling_factor if bubble[1] else None,
                bubble[2],
            )
            for bubble in unscaled_bubbles
        ]

        # Also scale the circle radius
        circle_radius = min_circle_radius * scaling_factor

        positions = []
        total_size = sum(
            bubble[0] for bubble in scaled_bubbles
        )  # Total size of all bubbles

        angle_accumulator = (
            0  # This will accumulate the angles as we move around the circle
        )

        for i, bubble in enumerate(scaled_bubbles):
            bubble_size = bubble[0]  # Size of the current bubble
            proportion = (
                bubble_size / total_size
            )  # Proportion of total size that this bubble represents

            angle_accumulator += proportion / 2  # Move to the middle of the bubble

            angle = (
                2 * math.pi * angle_accumulator
            )  # Angle around circle (adjusted by the angle_accumulator)
            bx = self.cx + circle_radius * math.cos(angle)  # Bubble x position
            by = self.cy + circle_radius * math.sin(angle)  # Bubble y position

            positions.append(
                (bx, by, bubble_size, bubble[1])
            )  # Append bubble center coordinates and radius

            angle_accumulator += (
                proportion / 2
            )  # Increase the accumulator by the proportion that this bubble represents

        return positions, scaling_factor

    def render(self):
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}">'

        positions, scaling_factor = self._calculate_positions()

        self.arrows.sort(key=lambda x: (x[0], x[1] > x[0], x[1]))
        prev_origin = 0
        width_of_existing_arrows = 0
        # Draw Arrows
        for arrow in self.arrows:
            origin = positions[arrow[0]]
            if arrow[0] != prev_origin:
                width_of_existing_arrows = 0
                prev_origin = arrow[0]
            origin_bubble_diameter = 2 * origin[2]
            origin_bubble_size = self.bubbles[arrow[0]][0]
            size_all_arrows = self.total_arrow_width_from_origin[arrow[0]]
            width_all_arrows = (
                origin_bubble_diameter * size_all_arrows / origin_bubble_size
            )
            size = arrow[2]
            width = width_all_arrows * size / size_all_arrows
            start_offset = (
                width_of_existing_arrows + (width / 2) - (width_all_arrows / 2)
            )
            width_of_existing_arrows += width
            destination = positions[arrow[1]]
            backoff = positions[arrow[1]][2]
            svg += self._draw_arrow(
                origin[0],
                origin[1],
                destination[0],
                destination[1],
                self.cx,
                self.cy,
                backoff,
                width=width,
                fill=self.colors[arrow[0]],
                start_offset=start_offset,
            )

        # Draw Bubbles
        for i, bubble in enumerate(self.bubbles):
            position = positions[i]
            svg += self._draw_dot(
                position[0],
                position[1],
                self.colors[i],
                radius=position[2],
                inner_radius=position[3],
                text=bubble[2],
            )

        svg += "</svg>"
        return svg
