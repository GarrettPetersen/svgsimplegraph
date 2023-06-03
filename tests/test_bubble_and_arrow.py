import pytest

from simplegraph.bubble_and_arrow import BubbleAndArrowGraph


def test_bubble_and_arrow_graph():
    graph = BubbleAndArrowGraph(
        width=600,
        height=600,
        background_color="#404040",
    )

    graph.add_bubble(100, None, "Bubble 0")
    graph.add_bubble(50, 25, "Bubble 1")
    graph.add_bubble(25, 12.5, "Bubble 2")

    graph.add_arrow(
        origin=0,
        destination=1,
        size=60,
    )
    graph.add_arrow(
        origin=0,
        destination=2,
        size=40,
    )
    graph.add_arrow(
        origin=1,
        destination=2,
        size=30,
    )
    graph.add_arrow(
        origin=2,
        destination=2,
        size=20,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"\n<img src='{svg_base64}' />")

    graph.add_bubble(12.5, 6.25, "Bubble 3", label="Bubble 3")
    graph.add_bubble(30, None, "Bubble 4")
    graph.add_bubble(3.125, 1.5625, "Bubble 5")
    graph.add_bubble(1.5625, 0.78125, "Bubble 6")

    graph.add_arrow(
        origin=2,
        destination="Bubble 3",
        size=10,
    )
    graph.add_arrow(
        origin="Bubble 3",
        destination=4,
        size=10,
    )
    graph.add_arrow(
        origin=4,
        destination=5,
        size=6,
    )
    graph.add_arrow(
        origin=4,
        destination=1,
        size=6,
    )
    graph.add_arrow(
        origin=4,
        destination=2,
        size=6,
    )
    graph.add_arrow(
        origin=4,
        destination=6,
        size=6,
    )
    graph.add_arrow(
        origin=5,
        destination=2,
        size=2,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    print(f"\n<img src='{svg_base64}' />")

    # Add a bunch of bubbles to test for overlapping text
    graph.add_bubble(1, None, "Bubble 7")
    graph.add_bubble(1, None, "Bubble 8")
    graph.add_bubble(1, None, "Bubble 9")
    graph.add_bubble(1, None, "Bubble 10")
    graph.add_bubble(1, None, "Bubble 11")
    graph.add_bubble(1, None, "Bubble 12")
    graph.add_bubble(1, None, "Bubble 13")
    graph.add_bubble(1, None, "Bubble 14")
    graph.add_bubble(1, None, "Bubble 15")
    graph.add_bubble(1, None, "Bubble 16")
    graph.add_bubble(1, None, "Bubble 17")
    graph.add_bubble(1, None, "Bubble 18")
    graph.add_bubble(1, None, "Bubble 19")
    graph.add_bubble(1, None, "Bubble 20")

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    print(f"\n<img src='{svg_base64}' />")
