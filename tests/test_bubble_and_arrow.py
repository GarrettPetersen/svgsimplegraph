import pytest

from simplegraph.bubble_and_arrow import BubbleAndArrowGraph


def test_bubble_and_arrow_graph():
    graph = BubbleAndArrowGraph(
        width=600,
        height=600,
    )

    graph.add_bubble(100, 50, "Bubble 1")
    graph.add_bubble(50, 25, "Bubble 2")
    graph.add_bubble(25, 12.5, "Bubble 3")

    graph.add_arrow(
        origin=0,
        destination=1,
        size=90,
    )
    graph.add_arrow(
        origin=1,
        destination=2,
        size=30,
    )

    # Get the SVG string in base64 format
    svg_base64 = graph.to_base64_src()

    # Check that the result starts with the correct prefix
    assert svg_base64.startswith("data:image/svg+xml;base64,")

    # Check that the result is long enough to be a non-trivial SVG
    assert len(svg_base64) > 100

    print(f"\n<img src='{svg_base64}' />")
