import math

from .base import BaseGraph
from .utils import hex_to_rgba
from .utils import is_dark
from .utils import estimate_text_dimensions
from .utils import boxes_overlap
from .utils import polar_to_cartesian


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
        padding=10,
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
        viewbox=True,
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
            secondary_y_axis_label=secondary_y_axis_label,
            show_legend=show_legend,
            rotate_x_labels=rotate_x_labels,
            background_color=background_color,
            dark_mode=dark_mode,
        )
        self.bubbles = []
        self.arrows = []
        self.total_arrow_width_from_origin = {}
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.viewbox = viewbox
        self.most_extreme_dimensions = {
            "left": self.width,
            "right": 0,
            "top": self.height,
            "bottom": 0,
        }
        self.dot_labels = {}
        self.text_buffer = []
        self.inner_fill = (
            self.background_color or "#000000" if self.dark_mode else "#ffffff"
        )

    def add_bubble(
        self,
        size,
        inner_size=None,
        text=None,
        label=None,
    ):
        assert size >= 0, "size cannot be negative"
        assert inner_size is None or inner_size >= 0, "inner_size cannot be negative"
        self.bubbles.append((size, inner_size, text))
        if label:
            assert isinstance(label, str), "label must be a string"
            assert label not in self.dot_labels, "label must be unique"
            self.dot_labels[label] = len(self.bubbles) - 1

    def add_arrow(
        self,
        origin,
        destination,
        size,
    ):
        assert size >= 0, "size cannot be negative"
        if size > 0:
            self.arrows.append([origin, destination, size])

    def _draw_dot(self, x, y, fill, radius=5, inner_radius=None, text=None):
        text_width, _ = estimate_text_dimensions(text, 10) if text else 0
        if self.viewbox:
            self.most_extreme_dimensions["left"] = min(
                self.most_extreme_dimensions["left"], x - radius
            )
            self.most_extreme_dimensions["right"] = max(
                self.most_extreme_dimensions["right"], x + radius
            )
            self.most_extreme_dimensions["top"] = min(
                self.most_extreme_dimensions["top"], y - radius
            )
            self.most_extreme_dimensions["bottom"] = max(
                self.most_extreme_dimensions["bottom"], y + radius
            )
        dot = f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" />'
        if inner_radius:
            dot += f'<circle cx="{x}" cy="{y}" r="{inner_radius}" fill="{self.inner_fill}" />'
        if text:
            text_color = "black"
            if self.dark_mode:
                text_color = "white"
            if inner_radius and inner_radius > text_width:
                text_color = "white" if is_dark(self.inner_fill) else "black"
            elif radius > text_width and not inner_radius:
                text_color = "white" if is_dark(fill) else "black"
            self.text_buffer.append([x, y, text, text_color])
        return dot

    def _draw_arrow(self, x1, y1, x2, y2, cx, cy, backoff, width=1, start_offset=0):
        circular_arrow = x1 == x2 and y1 == y2

        arrow_head_length = max(10, width / 5)
        direction_in = math.atan2(y2 - cy, x2 - cx)
        direction_to_center = math.atan2(y1 - cy, x1 - cx)
        distance_to_center = math.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)
        ctrl_distance = distance_to_center
        interior_ctrl_distance = ctrl_distance - 2 * width

        if circular_arrow:
            # Self-pointing arrows emerge sideways
            direction_mid = direction_to_center - math.pi / 2
            direction_out = direction_to_center + 3 * math.pi / 4
            direction_in += math.pi / 4
        else:
            direction_out = direction_to_center
            direction_mid = math.atan2(y2 - y1, x2 - x1)

        perpendicular = direction_mid + math.pi / 2
        perpendicular_out = direction_out + math.pi / 2
        perpendicular_in = direction_in + math.pi / 2
        cx_offset, cy_offset = polar_to_cartesian(perpendicular, width / 2)
        x_out_offset, y_out_offset = polar_to_cartesian(perpendicular_out, width / 2)
        x_out_shift, y_out_shift = polar_to_cartesian(perpendicular_out, start_offset)
        x_in_offset, y_in_offset = polar_to_cartesian(perpendicular_in, width / 2)

        # Calculate backoff
        backoff_x, backoff_y = polar_to_cartesian(direction_in, backoff)

        # New position of x2, y2 after backoff
        x2_backoff = x2 - backoff_x
        y2_backoff = y2 - backoff_y

        # Arrow head with respect to the original x2, y2, but positioned at the backoff location
        x_arrow_head, y_arrow_head = polar_to_cartesian(
            direction_in, arrow_head_length, x2_backoff, y2_backoff
        )

        if circular_arrow:
            # Calculate positions of the control points along the direction_out and direction_in lines
            ctrl_x1, ctrl_y1 = polar_to_cartesian(direction_out, ctrl_distance, x1, y1)
            ctrl_x2, ctrl_y2 = polar_to_cartesian(direction_in, ctrl_distance, x2, y2)

            ctrl_x1_interior, ctrl_y1_interior = polar_to_cartesian(
                direction_out, interior_ctrl_distance, x1, y1
            )
            ctrl_x2_interior, ctrl_y2_interior = polar_to_cartesian(
                direction_in, interior_ctrl_distance, x2, y2
            )

            return (
                f"M {x1+x_out_offset},{y1+y_out_offset} "
                + f"C{ctrl_x1_interior},{ctrl_y1_interior} {ctrl_x2_interior},{ctrl_y2_interior} {x_arrow_head + x_in_offset},{y_arrow_head + y_in_offset} "
                + f"L{x_arrow_head + 1.3 * x_in_offset},{y_arrow_head + 1.3 * y_in_offset} "
                + f"L{x2_backoff},{y2_backoff} L{x_arrow_head - 1.3 * x_in_offset},{y_arrow_head - 1.3 * y_in_offset} "
                + f"L{x_arrow_head - x_in_offset},{y_arrow_head - y_in_offset} "
                + f"C{ctrl_x2},{ctrl_y2} {ctrl_x1},{ctrl_y1} {x1-x_out_offset},{y1-y_out_offset} z "
            )

        # Control points for each side of the arrow, adjusted by half the width in the direction perpendicular to the arrow
        ctrl_x1 = cx + cx_offset
        ctrl_y1 = cy + cy_offset
        ctrl_x2 = cx - cx_offset
        ctrl_y2 = cy - cy_offset

        return (
            f"M {x1-x_out_offset-x_out_shift},{y1-y_out_offset-y_out_shift} "
            + f"Q{ctrl_x1},{ctrl_y1} {x_arrow_head + x_in_offset},{y_arrow_head + y_in_offset} "
            + f"L{x_arrow_head + 1.3 * x_in_offset},{y_arrow_head + 1.3 * y_in_offset} "
            + f"L{x2_backoff},{y2_backoff} L{x_arrow_head - 1.3 * x_in_offset},{y_arrow_head - 1.3 * y_in_offset} "
            + f"L{x_arrow_head - x_in_offset},{y_arrow_head - y_in_offset}"
            + f"Q{ctrl_x2},{ctrl_y2} {x1+x_out_offset-x_out_shift},{y1+y_out_offset-y_out_shift} z "
        )

    def _draw_arrows(self, arrows, fill):
        path = ""
        for arrow in arrows:
            path += self._draw_arrow(*arrow)
        return f'<path d="{path}" fill="{hex_to_rgba(fill,0.5)}" />'

    def _draw_text(self, x, y, text, fill):
        text_width, text_height = estimate_text_dimensions(text, 10)
        half_width = text_width / 2
        half_height = text_height / 2
        if self.viewbox:
            self.most_extreme_dimensions["left"] = min(
                self.most_extreme_dimensions["left"], x - half_width
            )
            self.most_extreme_dimensions["right"] = max(
                self.most_extreme_dimensions["right"], x + half_width
            )
            self.most_extreme_dimensions["top"] = min(
                self.most_extreme_dimensions["top"], y - half_height
            )
            self.most_extreme_dimensions["bottom"] = max(
                self.most_extreme_dimensions["bottom"], y + half_height
            )
        return (
            f'<text x="{x}" y="{y}" text-anchor="middle" '
            + f'dominant-baseline="middle" fill="{fill}" '
            + f'font-size="10">{text}</text>'
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

        return positions

    def render(self):
        svg = ""
        svg_text = ""
        self.text_buffer = []
        self.total_arrow_width_from_origin = {}
        self.most_extreme_dimensions = {
            "left": self.width,
            "right": 0,
            "top": self.height,
            "bottom": 0,
        }

        positions = self._calculate_positions()

        for i, arrow in enumerate(self.arrows):
            if isinstance(arrow[0], str):
                self.arrows[i][0] = self.dot_labels[arrow[0]]
            if isinstance(arrow[1], str):
                self.arrows[i][1] = self.dot_labels[arrow[1]]

            if self.arrows[i][0] not in self.total_arrow_width_from_origin:
                self.total_arrow_width_from_origin[self.arrows[i][0]] = 0
            self.total_arrow_width_from_origin[self.arrows[i][0]] += arrow[2]

        self.arrows.sort(key=lambda x: (x[0], x[1] < x[0], x[1]))
        prev_origin = 0
        width_of_existing_arrows = 0
        arrows_from_origin = {}
        # Draw Arrows
        for arrow in self.arrows:
            origin = arrow[0]
            origin_position = positions[origin]
            if arrow[0] != prev_origin:
                width_of_existing_arrows = 0
                prev_origin = arrow[0]
            origin_bubble_diameter = 2 * origin_position[2]
            origin_bubble_size = self.bubbles[origin][0]
            size_all_arrows = self.total_arrow_width_from_origin[origin]
            width_all_arrows = min(
                origin_bubble_diameter * size_all_arrows / origin_bubble_size,
                origin_bubble_diameter,
            )
            size = arrow[2]
            width = width_all_arrows * size / size_all_arrows
            start_offset = (
                width_of_existing_arrows + (width / 2) - (width_all_arrows / 2)
            )
            width_of_existing_arrows += width
            destination_position = positions[arrow[1]]
            backoff = positions[arrow[1]][2]
            if origin not in arrows_from_origin:
                arrows_from_origin[origin] = []
            arrows_from_origin[origin].append(
                [
                    origin_position[0],
                    origin_position[1],
                    destination_position[0],
                    destination_position[1],
                    self.cx,
                    self.cy,
                    backoff,
                    width,
                    start_offset,
                ]
            )

        for origin, arrows in arrows_from_origin.items():
            svg += self._draw_arrows(arrows, self.colors[origin])

        # Draw Bubbles
        for i, bubble in enumerate(self.bubbles):
            position = positions[i]
            dot = self._draw_dot(
                position[0],
                position[1],
                self.colors[i],
                radius=position[2],
                inner_radius=position[3],
                text=bubble[2],
            )

            svg += dot

        # Shift labels to not overlap
        text_to_check = 0
        num_loops = 0
        max_loops = len(self.text_buffer) * 10
        while text_to_check < len(self.text_buffer) and num_loops < max_loops:
            first_text = self.text_buffer[text_to_check]
            any_change = False
            for i in [-2, -1, 1, 2]:
                other_index = (text_to_check + i) % len(self.text_buffer)
                other_text = self.text_buffer[other_index]
                first_text_width, first_text_height = estimate_text_dimensions(
                    first_text[2], 10
                )
                other_text_width, other_text_height = estimate_text_dimensions(
                    other_text[2], 10
                )
                vertical_overlap = boxes_overlap(
                    first_text[0],
                    first_text[1],
                    first_text_width,
                    first_text_height,
                    other_text[0],
                    other_text[1],
                    other_text_width,
                    other_text_height,
                )
                if vertical_overlap:
                    if first_text[1] < other_text[1]:
                        self.text_buffer[text_to_check][1] -= vertical_overlap
                    else:
                        self.text_buffer[text_to_check][1] += vertical_overlap

                    any_change = True
            if any_change:
                text_to_check = max(0, text_to_check - 3)
            else:
                text_to_check += 1
            num_loops += 1

        # Draw Text
        for text in self.text_buffer:
            svg_text += self._draw_text(*text)

        background_rect = ""
        if self.viewbox:
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

            viewbox_param = (
                f'viewBox="{self.most_extreme_dimensions["left"] - self.x_left_padding} '
                + f'{self.most_extreme_dimensions["top"] - self.y_top_padding} {viewbox_width} '
                + f'{viewbox_height}"'
            )

            self.width = viewbox_width + self.x_left_padding + self.x_right_padding
            self.height = viewbox_height + self.y_top_padding + self.y_bottom_padding
            if self.background_color:
                # Draw background with rounded corners
                background_rect = (
                    f"<rect x='{self.most_extreme_dimensions['left'] - self.x_left_padding}' "
                    + f"y='{self.most_extreme_dimensions['top'] - self.y_top_padding}' "
                    + f"width='{viewbox_width}' height='{viewbox_height}' "
                    + f"rx='10' ry='10' fill='{self.background_color}' />"
                )
        elif self.background_color:
            background_rect = (
                f"<rect x='0' y='0' width='{self.width}' height='{self.height}' "
                + f"rx='10' ry='10' fill='{self.background_color}' />"
            )

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            + f'height="{self.height}" {viewbox_param}>'
            + background_rect
            + svg
            + svg_text
            + "</svg>"
        )
        return svg
