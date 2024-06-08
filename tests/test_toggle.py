import pytest

from svgsimplegraph.toggle import ToggleGraph
from svgsimplegraph.categorical import CategoricalGraph


def test_toggle_graph():
    graph1 = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph 1",
        watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
        primary_tick_prefix="$",
        background_color="#404040",
    )

    graph1.x_labels = ["A", "B", "C", "D", "E"]
    graph1.x_axis_label = "X Axis"
    graph1.primary_y_axis_label = "Primary Y Axis"

    graph1.add_series([10, 20, -30, 40, 50])

    graph2 = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph 2",
        watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
        primary_tick_prefix="$",
        background_color="#404040",
    )

    graph2.x_labels = ["A", "B", "C", "D", "E"]
    graph2.x_axis_label = "X Axis"
    graph2.primary_y_axis_label = "Primary Y Axis"

    graph2.add_series([20, 10, 30, 50, 10], legend_label="Legend Label")

    graph3 = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph 3",
        watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
        primary_tick_prefix="$",
        background_color="#404040",
    )

    graph3.x_labels = ["A", "B", "C", "D", "E"]
    graph3.x_axis_label = "X Axis"
    graph3.primary_y_axis_label = "Primary Y Axis"

    graph3.add_series([10, 25, 30, 40, 50])

    graph4 = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph 4",
        watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
        primary_tick_prefix="$",
        background_color="#404040",
    )

    graph4.x_labels = ["A", "B", "C", "D", "E"]
    graph4.x_axis_label = "X Axis"
    graph4.primary_y_axis_label = "Primary Y Axis"

    graph4.add_series([10, 10, 10, 50, 5])

    toggle = ToggleGraph()

    toggle.add_graph(graph1, label="Graph 1")
    toggle.add_graph(graph2, label="Graph 2")
    toggle.add_graph(graph3, label="Graph 3")
    toggle.add_graph(graph4, label="Graph 4")

    svg_base64 = toggle.to_base64_src()

    print(f"\n<object type='image/svg+xml' data='{svg_base64}' />")

    print(toggle.render())

    toggle2 = ToggleGraph(button_position="top", button_font_size=12)

    toggle2.add_graph(graph1, label="Graph 1")
    toggle2.add_graph(graph2, label="Graph 2")
    toggle2.add_graph(graph3, label="Graph 3")
    toggle2.add_graph(graph4, label="Graph 4")

    svg_base64 = toggle2.to_base64_src()

    print(f"\n<object type='image/svg+xml' data='{svg_base64}' />")

    print(toggle2.render())
