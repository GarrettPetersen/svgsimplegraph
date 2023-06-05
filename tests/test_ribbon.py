import pytest

from simplegraph.ribbon import RibbonGraph


def test_ribbon_graph():
    graph = RibbonGraph(
        width=600,
        height=400,
        bar_width=30,
        x_left_padding=30,
        x_right_padding=60,
        y_top_padding=40,
        y_bottom_padding=30,
    )

    graph.x_labels = ["A", "B", "C", "D", "E"]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"

    graph.add_series([-10, 20, 30, 40, 50], legend_label="Series 1", print_values=True)
    graph.add_series([20, 30, 40, 30, 20], legend_label="Series 2", print_values=True)
    graph.add_series(
        [-10, -20, 30, 20, 10], legend_label="Color Series", print_values=True
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"\n<img src='{svg_base64}' />")

    graph.color_range = (0, 20)

    svg_base64 = graph.to_base64_src()

    print(f"\n<img src='{svg_base64}' />")
