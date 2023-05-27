import math
import matplotlib


def get_color(val, min_color, max_color):
    # Normalize RGB values to the [0, 1] range
    min_rgb = matplotlib.colors.hex2color(min_color)
    max_rgb = matplotlib.colors.hex2color(max_color)

    # Compute the interpolated color's RGB values
    interpolated_rgb = [
        min_c + val * (max_c - min_c) for min_c, max_c in zip(min_rgb, max_rgb)
    ]

    # Convert the interpolated RGB values back to hexadecimal color format
    return matplotlib.colors.rgb2hex(interpolated_rgb)


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
        return f"{num:.0f}"
    elif num >= 1:
        return f"{num:.1f}"
    else:
        return f"{num:.2f}"


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
