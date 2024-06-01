import pytest

from svgsimplegraph.categorical import CategoricalGraph


def test_categorical_graph():
    graph = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph",
        watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
        primary_tick_prefix="$",
        secondary_tick_suffix="%",
    )

    graph.x_labels = ["A", "B", "C", "D", "E"]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"
    graph.secondary_y_axis_label = "Secondary Y Axis"

    graph.add_series([10, 20, -30, 40, 50])

    graph.add_horizontal_line(
        y=20, label="top left label", label_x_position="left", label_y_position="top"
    )
    graph.add_horizontal_line(
        y=20, label="top right label", label_x_position="right", label_y_position="top"
    )
    graph.add_horizontal_line(
        y=20,
        label="top center label",
        label_x_position="center",
        label_y_position="top",
    )
    graph.add_horizontal_line(
        y=20,
        label="bottom left label",
        label_x_position="left",
        label_y_position="bottom",
    )
    graph.add_horizontal_line(
        y=20,
        label="bottom right label",
        label_x_position="right",
        label_y_position="bottom",
    )
    graph.add_horizontal_line(
        y=20,
        label="bottom center label",
        label_x_position="center",
        label_y_position="bottom",
    )
    graph.add_vertical_line(
        x=3.5, label="top right label", label_x_position="right", label_y_position="top"
    )
    graph.add_vertical_line(
        x=3.5, label="top left label", label_x_position="left", label_y_position="top"
    )
    graph.add_vertical_line(
        x=3.5,
        label="bottom right label",
        label_x_position="right",
        label_y_position="bottom",
    )
    graph.add_vertical_line(
        x=3.5,
        label="bottom left label",
        label_x_position="left",
        label_y_position="bottom",
    )
    graph.add_vertical_line(
        x=3.5,
        label="center right label",
        label_x_position="right",
        label_y_position="center",
    )
    graph.add_vertical_line(
        x=3.5,
        label="center left label",
        label_x_position="left",
        label_y_position="center",
    )
    graph.add_vertical_line(
        x=1,
        label="top right label",
        label_x_position="right",
        label_y_position="top",
        rotate_label=True,
    )
    graph.add_vertical_line(
        x=1,
        label="top left label",
        label_x_position="left",
        label_y_position="top",
        rotate_label=True,
    )
    graph.add_vertical_line(
        x=1,
        label="bottom right label",
        label_x_position="right",
        label_y_position="bottom",
        rotate_label=True,
    )
    graph.add_vertical_line(
        x=1,
        label="bottom left label",
        label_x_position="left",
        label_y_position="bottom",
        rotate_label=True,
    )
    graph.add_vertical_line(
        x=1,
        label="center right label",
        label_x_position="right",
        label_y_position="center",
        rotate_label=True,
    )
    graph.add_vertical_line(
        x=1,
        label="center left label",
        label_x_position="left",
        label_y_position="center",
        rotate_label=True,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"\n<img src='{svg_base64}' />")

    graph.add_series([15, 0, -5, 44, 56], legend_label="Series 2")
    graph.add_series([5, 35, 10, 33, 40], legend_label="Series 3", series_type="line")
    graph.add_series(
        [0.35, 0.56, 0.25, 0.05, 0.44],
        legend_label="Series 4",
        series_type="dot",
        secondary=True,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"\n<img src='{svg_base64}' />")

    # Add a ton of series to test the two-column legend
    graph.add_series([5, 44, -10, 56, 15], legend_label="Series 5")
    graph.add_series([0.35, 6, 0.25, 0.05, 0.44], legend_label="Series 6")
    graph.add_series([5, 5, 10, 33, 40], legend_label="Series 7")
    graph.add_series([0.35, 0.56, 0.25, 0.05, 0.44], legend_label="Series 8")
    graph.add_series([5, 35, 10, 23, 40], legend_label="Series 9")
    graph.add_series([0.35, 0.56, 0.25, 0.05, 0.44], legend_label="Series 10")
    graph.add_series([5, 35, 10, 3, 40], legend_label="Series 11")
    graph.add_series([25, 0.56, 15, 0.05, 0.44], legend_label="Series 12")
    graph.add_series([5, 35, 11, 33, 90], legend_label="Series 13")
    graph.add_series([15, 6, 5, 5, 4], legend_label="Series 14")
    graph.add_series([5, 35, 10, 33, 4], legend_label="Series 15")
    graph.add_series([5, 5, 10, 33, 40], legend_label="Series 16")
    graph.add_series([5, 35, 1, 33, 40], legend_label="Series 17")
    graph.add_series([5, 35, 10, 3, 40], legend_label="Series 18")
    graph.add_series([5, 35, 10, 33, 4], legend_label="Series 19")
    graph.add_series([15, 15, 10, 11, 40], legend_label="Series 20")

    graph.height = 300

    graph.stacked = True

    stacked_base64 = graph.to_base64_src()
    print(f"\n<img src='{stacked_base64}' />")

    # Now try another legend position
    graph.legend_position = "top"

    stacked_base64 = graph.to_base64_src()
    print(f"\n<img src='{stacked_base64}' />")

    # Now try another legend position
    graph.legend_position = "left"

    stacked_base64 = graph.to_base64_src()
    print(f"\n<img src='{stacked_base64}' />")

    # Now try another legend position
    graph.legend_position = "bottom"

    stacked_base64 = graph.to_base64_src()
    print(f"\n<img src='{stacked_base64}' />")

    # New graph with a very long series
    graph = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph",
        primary_tick_prefix="$",
        line_curvature=0.5,
    )

    number_of_bars = 100

    graph.x_labels = [f"Label {i}" for i in range(number_of_bars)]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"
    graph.secondary_y_axis_label = "Secondary Y Axis"

    graph.add_series([abs(i - number_of_bars // 2) for i in range(number_of_bars)])
    graph.add_series(
        [(i**2) % number_of_bars for i in range(number_of_bars)], series_type="line"
    )

    large_base64 = graph.to_base64_src()
    print(f"\n<img src='{large_base64}' />")

    # New graph with stacked primary and line secondary
    graph = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        title="Categorical Graph",
        secondary_tick_suffix="%",
        stacked=True,
        line_curvature=0.5,
        legend_position="top",
    )

    graph.x_labels = [f"Label {i}" for i in range(5)]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"
    graph.secondary_y_axis_label = "Secondary Y Axis"

    graph.add_series([1, 2, 3, 4, 5, 1, 1, 1, 5, 6, 7, 8], legend_label="Primary Bar")
    graph.add_series(
        [50, 10, 35, 25, 10, 5, 30, 5, 10, 15, 20, 25],
        series_type="line",
        secondary=True,
        stroke_width=2,
        legend_label="Secondary Line",
    )
    graph.add_series(
        [50, None, 35, 25, 10, 5, None, None, 10, 15, None, 25],
        series_type="line",
        secondary=True,
        stroke_width=2,
        legend_label="Secondary Line 2",
    )
    graph.add_series([3, 4, 3, 2, 1, 1, 3, 4, 1, 2, 1, 3], legend_label="Primary Bar 2")

    stacked_base64 = graph.to_base64_src()
    svg_code = graph.render()

    print(f"\n<img src='{stacked_base64}' />")

    print(svg_code)
