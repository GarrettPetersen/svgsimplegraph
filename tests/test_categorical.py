import pytest

from simplegraph.categorical import CategoricalGraph


def test_categorical_graph():
    graph = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        x_padding=10,
        y_top_padding=20,
        y_bottom_padding=30,
    )

    graph.x_labels = ["A", "B", "C", "D", "E"]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"

    graph.add_series([10, 20, 30, 40, 50], legend_label="Series 1")

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"<img src='{svg_base64}' />")
