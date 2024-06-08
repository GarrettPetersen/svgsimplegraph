# svgsimplegraph

This is a simple little graphing package for making graphs and exporting them as raw or base64-encoded SVGs.

You can also upload the SVGs to your GitHub account as Gists, so they may be embedded in any website!

## Installing svgsimplegraph
Install svgsimplegraph by typing
```
pip install svgsimplegraph
```
in your terminal.

## Graph Types
### Categorical Graph

The categorical graph is for data that comes in distinct categories. It can generate a bar chart, a stacked bar chart, dots, or lines.

Here is an example of how to make a graph:

```
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

# You can use vertical or horizontal lines to mark specific values
graph.add_vertical_line(
    x=2.5,
    label="Vertical Line",
    label_x_position="right",
    label_y_position="top",
    rotate_label=True,
)

# Get the SVG string in base64 format
svg_base64 = graph.to_base64_src()

# Print the SVG string in an img tag so your browser can display it
print(f"\n<img src='{svg_base64}' />")

# Alternatively, you can get the raw SVG code with render()
raw_svg = graph.render()
print(raw_svg)
```
![Example categorical graph](https://github.com/GarrettPetersen/svgsimplegraph/blob/master/images/example_categorical.svg)

### Toggle Graph

You can combine multiple CategoricalGraphs into a ToggleGraph with interactive buttons.

```
from svgsimplegraph import ToggleGraph
from svgsimplegraph import CategoricalGraph

# Let's make some categorical graphs to put in our ToggleGraph
graph1 = CategoricalGraph(
    width=600,
    height=400,
    bar_width=30,
    title="Categorical Graph 1",
    watermark="<rect x='250' y='150' width='100' height='100' fill='rgba(255, 0, 0, 0.5)' />",
    primary_tick_prefix="$",
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

# You can't put this in the src of an image tag, because it implicitly contains
# JavaScript, which cannot execute from within an image. So we include it as the
# data within an object.
svg_base64 = toggle.to_base64_src()

print(f"\n<object type='image/svg+xml' data='{svg_base64}' />")

# Alternatively we can just print the SVG code
print(toggle.render())
```

<object type="image/svg+xml" data="https://github.com/GarrettPetersen/svgsimplegraph/blob/master/images/example_toggle_graph.svg" />

### Ribbon Graph

The ribbon graph is for comparing two numbers on the same scale and a third number on a different scale (represented through color).

The three series must be added in order, with the first representing the back of the ribbon, the second representing the point, and the (optional) third representing the color.

Here's an example:

```
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
```
![Example ribbon graph](https://github.com/GarrettPetersen/svgsimplegraph/blob/master/images/example_ribbon.svg)

### Bubble and Arrow Graph
The bubble and arrow graph is for displaying relationships between nodes in a network.

The user adds bubbles, which are displayed in clockwise order around a larger circle. Then the user can add arrows that exit from one bubble and enter another. Arrow width is scaled to show more important connections.

Here's an example:
```
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
```
![Example bubble and arrow graph](https://github.com/GarrettPetersen/svgsimplegraph/blob/master/images/example_bubble_and_arrow.svg)

## GitHub Gist integration

The `upload_to_github_gist` function allows you to render your graph and upload it to your GitHub account as a Gist.

To do this, you'll need an access token. Go to your github account and navigate to settings. Then click on Developer settings > Personal access tokens > Fine-grained tokens.

Click the Generate new token button in the top right of the screen. GitHub will prompt you to login. Set a token name (something like "gist-access-token") and an expiration.

Scroll down to Permissions and expand the Account permissions box. Then turn on read and write access for Gists only (you should not use this token for anything else). Finally, click the gree Generate token button at the bottom of the screen.

Now you should see a screen showing your token. This is the only time Github will show you this token, so save it somewhere safe.

Assuming you've done all that, you can use the token to turn your graphs into gists.

```
from svgsimplegraph import CategoricalGraph

GITHUB_ACCESS_TOKEN = "your_token_goes_here"

# Create an instance of a graph
graph = CategoricalGraph(
    width=600,
    height=400,
    bar_width=30,
    stacked=False,
    background_color="#404040",
)

graph.x_labels = ["A", "B", "C", "D", "E"]
graph.x_axis_label = "X Axis"
graph.primary_y_axis_label = "Primary Y Axis"

graph.add_series([10, 20, 30, 40, 50], legend_label="Series 1")

svg_url = graph.upload_to_github_gist(GITHUB_ACCESS_TOKEN, "my_categorical_graph")
```

The `svg_url` variable now contains a string with the url of your new SVG, ready to be embedded in any website!

## Watermarks

When you initialize a graph, you can use the watermark variable to add arbitrary svg code to the graph. It is recommended to make your watermark partially transparent, as it will be placed on top of your graph.