import pytest


def test_readme_categorical():
    from svgsimplegraph import CategoricalGraph

    graph = CategoricalGraph(
        width=600,
        height=400,
        bar_width=30,
        stacked=False,
        background_color="#404040",
        title="Categorical Graph",
    )

    graph.x_labels = ["A", "B", "C", "D", "E"]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"

    # Skip adding a legend_label to exclude a series from the legend
    graph.add_series([10, 20, 30, 40, 50], legend_label="Series 1")
    graph.add_series([15, 25, 5, 44, 56], legend_label="Series 2")
    graph.add_series([5, 35, 10, 33, 40], legend_label="Series 3", series_type="line")
    graph.add_series([35, 56, 25, 5, 44], legend_label="Series 4", series_type="dot")

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Print the SVG string in an img tag so your browser can display it
    print(f"\n<img src='{svg_base64}' />")

    # Alternatively, you can get the raw SVG code with render()
    raw_svg = graph.render()
    print(raw_svg)


def test_ribbon():
    from svgsimplegraph import RibbonGraph

    graph = RibbonGraph(
        width=600,
        height=400,
        bar_width=30,
        background_color="#404040",
        title="Ribbon Graph",
    )

    graph.x_labels = ["A", "B", "C", "D", "E"]
    graph.x_axis_label = "X Axis"
    graph.primary_y_axis_label = "Primary Y Axis"

    graph.add_series([10, 20, 30, 40, 50], legend_label="Series 1", print_values=True)
    graph.add_series([20, 30, 40, 30, 20], legend_label="Series 2", print_values=True)
    graph.add_series(
        [-10, -20, 30, 20, 10], legend_label="Color Series", print_values=True
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Print the SVG string in an img tag so your browser can display it
    print(f"\n<img src='{svg_base64}' />")

    # Alternatively, you can get the raw SVG code with render()
    raw_svg = graph.render()
    print(raw_svg)


def test_bubble_and_arrow():
    from svgsimplegraph import BubbleAndArrowGraph

    graph = BubbleAndArrowGraph(
        width=400,
        height=400,
        background_color="#ffffff",
        title="Bubble and Arrow Graph",
    )

    # Optional str label param can be referred to later when defining arrows
    graph.add_bubble(100, None, "Bubble 0", label="big_bubble")

    # Otherwise bubbles must be referred to by their index number
    graph.add_bubble(50, 25, "Bubble 1")
    graph.add_bubble(25, 12.5, "Bubble 2")

    graph.add_arrow(
        origin="big_bubble",
        destination=1,
        size=60,
    )
    graph.add_arrow(
        origin="big_bubble",
        destination=2,
        size=40,
    )
    graph.add_arrow(
        origin=1,
        destination=2,
        size=30,
    )

    # Arrows pointing to their origin will loop around
    graph.add_arrow(
        origin=2,
        destination=2,
        size=20,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Print the SVG string in an img tag so your browser can display it
    print(f"\n<img src='{svg_base64}' />")

    # Alternatively, you can get the raw SVG code with render()
    raw_svg = graph.render()
    print(raw_svg)
