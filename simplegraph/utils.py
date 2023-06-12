import math
import matplotlib
import numpy as np


def polar_to_cartesian(angle, radius, x=0, y=0):
    x = x + radius * math.cos(angle)
    y = y + radius * math.sin(angle)
    return x, y


def estimate_text_dimensions(text, font_size):
    # Split the text into lines
    lines = text.splitlines()

    # Find the line with the most characters
    max_chars = max(len(line) for line in lines)

    # Assume each character is about 0.6 times the font size (this is a rough approximation)
    estimated_width = max_chars * font_size * 0.6

    # The height of a single line of text is roughly equal to the font size.
    # For multiple lines, multiply by the number of lines.
    # Include line spacing by multiplying the font size by a factor (e.g., 1.2).
    estimated_height = len(lines) * font_size * 1.2

    return estimated_width, estimated_height


def boxes_overlap(x1, y1, width1, height1, x2, y2, width2, height2):
    # Calculate the corners of the boxes
    left1, right1 = x1 - width1 / 2, x1 + width1 / 2
    top1, bottom1 = y1 - height1 / 2, y1 + height1 / 2
    left2, right2 = x2 - width2 / 2, x2 + width2 / 2
    top2, bottom2 = y2 - height2 / 2, y2 + height2 / 2

    # Check if the boxes overlap horizontally
    if right1 < left2:
        return False
    if right2 < left1:
        return False

    # Check if the boxes overlap vertically
    if bottom1 < top2:
        return False
    if bottom2 < top1:
        return False

    # Return the amount of vertical overlap
    if y1 < y2:
        return bottom1 - top2
    else:
        return bottom2 - top1


def get_color(val, colors):
    # Convert hex colors to RGB
    rgbs = [np.array(matplotlib.colors.hex2color(color)) for color in colors]

    # Assign values to color ranges
    ranges = np.linspace(0, 1, len(colors))

    # If value is outside the defined range, use the edge colors.
    if val <= 0:
        return colors[0]
    elif val >= 1:
        return colors[-1]

    # Find the two colors between which the value lies.
    for i in range(len(ranges) - 1):
        # Adjust the ranges to match the colors properly
        low_range = ranges[i]
        high_range = ranges[i + 1]
        # Perform interpolation if val falls within the adjusted ranges
        if low_range <= val < high_range:
            t = (val - low_range) / (high_range - low_range)
            color = rgbs[i] * (1 - t) + rgbs[i + 1] * t
            break
    else:
        color = rgbs[0]  # default to the first color if no range found

    return matplotlib.colors.rgb2hex(color)


def hex_to_rgba(hex_color, alpha=1.0):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def calculate_ticks(min_val, max_val, include_zero=True, target_tick_count=7):
    if include_zero:
        min_val = min(0, min_val)
        max_val = max(0, max_val)

    # Calculate the initial range of the data
    data_range = max_val - min_val

    # If all values are zero, avoid dividing by zero by returning some reasonable defaults
    if data_range == 0:
        if include_zero:
            return [0, 1]
        else:
            return [min_val, min_val + 1]

    # Calculate approximately how many steps we want to have
    rough_step = data_range / target_tick_count

    # Calculate the magnitude of the step size (e.g., 10, 100, 0.1, etc)
    magnitude = 10 ** (math.floor(math.log10(rough_step)))

    # Calculate the most significant digit of the step size
    msd = rough_step / magnitude

    # If the most significant digit is in the range 2-5, we use a step size of 2, 2.5, or 5 by multiplying the magnitude by 2 or 2.5.
    # If the most significant digit is higher than 5, we can just use the magnitude as the step size.
    # If the most significant digit is lower than 2, we can use the magnitude divided by 2 as the step size.
    if msd >= 5:
        step_size = 5 * magnitude
    elif msd >= 2.5:
        step_size = 2.5 * magnitude
    elif msd >= 2:
        step_size = 2 * magnitude
    else:
        step_size = magnitude

    # Calculate the new min and max values for the y-axis
    if include_zero:
        axis_min = 0
        # If min_val is below zero, ensure we capture the negative range.
        if min_val < 0:
            axis_min = -math.ceil(abs(min_val) / step_size) * step_size
    else:
        axis_min = step_size * math.floor(min_val / step_size)

    axis_max = step_size * math.ceil(max_val / step_size)

    # Generate the list of ticks
    ticks = list(np.arange(axis_min, axis_max + step_size, step_size))

    if include_zero:
        assert 0 in ticks, "Zero should be included in the ticks."

    return ticks


def match_ticks(ticks1, ticks2):
    # Find zero position in both lists
    zero_index1 = [i for i, v in enumerate(ticks1) if v == 0]
    zero_index2 = [i for i, v in enumerate(ticks2) if v == 0]

    # If zero is not present in any of the lists, raise an error
    if not zero_index1 or not zero_index2:
        raise ValueError("Both tick lists must contain zero.")

    # Find the difference between the zero indices
    zero_index_diff = zero_index1[0] - zero_index2[0]

    # If the first list has more ticks below zero, add ticks to the second list
    if zero_index_diff > 0:
        ticks2 = [
            ticks2[0] - (zero_index_diff - i) * (ticks2[1] - ticks2[0])
            for i in range(zero_index_diff)
        ] + ticks2
    # If the second list has more ticks below zero, add ticks to the first list
    elif zero_index_diff < 0:
        ticks1 = [
            ticks1[0] - (-zero_index_diff - i) * (ticks1[1] - ticks1[0])
            for i in range(-zero_index_diff)
        ] + ticks1

    # Make the lengths of the tick lists match by adding ticks above the highest value
    len_diff = len(ticks1) - len(ticks2)
    if len_diff > 0:
        ticks2 += [
            ticks2[-1] + (i + 1) * (ticks2[1] - ticks2[0]) for i in range(len_diff)
        ]
    elif len_diff < 0:
        ticks1 += [
            ticks1[-1] + (i + 1) * (ticks1[1] - ticks1[0]) for i in range(-len_diff)
        ]

    assert len(ticks1) == len(
        ticks2
    ), f"Tick lists must be the same length: {ticks1}, {ticks2}"
    assert all(
        ticks1[i] <= ticks1[i + 1] for i in range(len(ticks1) - 1)
    ), f"ticks1 is not in ascending order: {ticks1}"
    assert all(
        ticks2[i] <= ticks2[i + 1] for i in range(len(ticks2) - 1)
    ), f"ticks2 is not in ascending order: {ticks2}"
    assert all([(t1 == 0) == (t2 == 0) for t1, t2 in zip(ticks1, ticks2)]), (
        "Tick lists must have zero at the same index.\n"
        + f"ticks1: {ticks1}, ticks2: {ticks2}"
    )
    return ticks1, ticks2


def get_adjusted_max(value):
    if value == 0:
        return 0
    exponent = math.floor(math.log10(abs(value)))
    base_value = 10**exponent
    rounding_factors = [1, 1.2, 1.5, 2, 2.5, 5]

    adjusted_value = float("inf")
    for factor in rounding_factors:
        candidate_value = math.ceil(value / (base_value * factor)) * (
            base_value * factor
        )
        if candidate_value >= value * 1.05 and candidate_value < adjusted_value:
            adjusted_value = candidate_value

    return adjusted_value


def get_adjusted_min(value):
    if value == 0:
        return 0

    sign = 1 if value >= 0 else -1
    abs_value = abs(value)

    exponent = math.floor(math.log10(abs_value))
    base_value = 10**exponent
    rounding_factors = [1, 1.2, 1.5, 2, 2.5, 5]

    adjusted_value = float("inf")
    for factor in rounding_factors:
        candidate_value = math.floor(abs_value / (base_value * factor)) * (
            base_value * factor
        )
        if candidate_value <= abs_value * 0.95 and candidate_value < adjusted_value:
            adjusted_value = candidate_value

    return sign * adjusted_value


def human_readable_number(num):
    if num < 0:
        return f"-{human_readable_number(-num)}"
    if num >= 1000000000:
        value = num / 1000000000.0
        return f"{value:.1f}B" if value != int(value) else f"{int(value)}B"
    elif num >= 1000000:
        value = num / 1000000.0
        return f"{value:.1f}M" if value != int(value) else f"{int(value)}M"
    elif num >= 1000:
        value = num / 1000.0
        return f"{value:.1f}K" if value != int(value) else f"{int(value)}K"
    elif num >= 10:
        return f"{num:.1f}" if num != int(num) else f"{int(num)}"
    else:
        return f"{num:.2f}" if num != int(num) else f"{int(num)}"


def is_dark(color):
    if color[0] == "#":
        color = color[1:]

    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    return brightness < 128  # return True if the color is dark


DEFAULT_COLOR_PALETTE = [
    "#253a5e",
    "#e8c170",
    "#a53030",
    "#75a743",
    "#73bed3",
    "#7a367b",
    "#3c5e8b",
    "#4f8fba",
    "#a4dddb",
    "#25562e",
    "#468232",
    "#a8ca58",
    "#d0da91",
    "#7a4841",
    "#ad7757",
    "#c09473",
    "#d7b594",
    "#e7d5b3",
    "#602c2c",
    "#884b2b",
    "#be772b",
    "#de9e41",
    "#411d31",
    "#752438",
    "#cf573c",
    "#da863e",
    "#402751",
    "#a23e8c",
    "#c65197",
    "#df84a5",
    "#10141f",
    "#151d28",
    "#202e37",
    "#394a50",
    "#577277",
    "#172038",
    "#19332d",
    "#4d2b32",
    "#341c27",
    "#241527",
    "#1e1d39",
    "#090a14",
    "#819796",
    "#a8b5b2",
    "#c7cfcc",
    "#ebede9",
]
