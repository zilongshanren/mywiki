---
title: Interactive Graphs in the Browser - Alan Zucconi
url: https://www.alanzucconi.com/2015/11/01/interactive-graphs-in-the-browser/
author: Alan Zucconi
published: '2015-11-01'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Having worked both as a teacher and an artist, I know how important data visualisation is. This tutorial will teach you to create interactive network graphs with Python and JavaScript. **You can have a go by dragging the nodes of the graph below…**

- Step 1.
[The Graph](https://www.alanzucconi.com#step1) - Step 2.
[Interactive Graph](https://www.alanzucconi.com#step2) - Step 3.
[Customisation](https://www.alanzucconi.com#step3) [Conclusion](https://www.alanzucconi.com#conclusion)

You can find a high resolution version of the melancoil tree (2000x2000px, first 1000 numbers) here: [PNG](https://drive.google.com/file/d/0B4nCcaMlgxV2UWVEREdUYUV0SVk/view?usp=sharing), [SVG](https://drive.google.com/file/d/0B4nCcaMlgxV2SUxhakdWTU1lcmM/view?usp=sharing), [HTML](https://www.alanzucconi.com/extra/d3/melancoil_1000/).

There are many libraries in Python that can handle network graphs; for this tutorial I’ve chosen [NetworkX](https://networkx.github.io/), which is quite easy to use. The first step is to create the graph, which can be done by simply adding the edges; this will also automatically add all the nodes.

The code below is used to calculate the **Melancoil tree**, as discussed by [Matt Parker](https://twitter.com/standupmaths) in an episode of [Numberphile](https://www.youtube.com/watch?v=_DpzAvb3Vk4). The algorithm to generate them has been discussed in the tutorial Recreational Maths in Python.

import networkx as nx G = nx.DiGraph() for i in range(1,100): happy, tree = is_happy(i, []) # Skips happy numbers if happy: continue # Add the entire sequence to the tree for j in range(0,len(tree)-1): G.add_edge(tree[j], tree[j+1])

The result is a directed graph which represents how the non-happy numbers are connected.

The way the network graph is going to be transferred to JavaScript is via JSON. The module `json_graph`

allows to dump a NetworkX graph into a JSON file. Before doing that, you can add any additional parameter you want to the nodes or the edges. This can be very helpful to decide which colour to use, or which label to show on the graph.

import json from networkx.readwrite import json_graph for n in G: G.node[n]['name'] = n d = json_graph.node_link_data(G) json.dump(d, open('force/force.json','w'))

If you have a software which can read JSON network graphs, this is all you need. However, there are few interesting things you can still do. Following [one of the examples](https://github.com/networkx/networkx/tree/master/examples/javascript) on the NetworkX documentation (partially based on [Mike Bostock](http://bost.ocks.org/mike/)‘s work), you can launch a browser page with an interactive version of the graph:

import http_server http_server.load_url('force/force.html')

The Python script will keep running and serve as a local HTTP server on the port 8000. By visiting the address [localhost:8000/force/force.html](https://www.alanzucconi.com/8000/force/force.html), you’ll see something like this:

![d1](../../assets/ae17aeb8266da115.png)

The graph reacts to drag events and looks quite nice. Once the Python Script is closed, the HTTP server becomes unreachable; however you can simply copy the “force” folder onto your website and it will work just fine.

The network graph made However, there are no customisation options available from Python. If we want a fancier graph, we need to chance the JavaScript code that generates it. This is stored in the file [force.js](https://github.com/networkx/networkx/blob/master/examples/javascript/force/force.js).

#### Nodes with style

The styles of the nodes can be changed by chaining a call to `style`

while appending the nodes; this can be seen in **line 37**, which changes the node colours according to a property called `group`

:

.style("fill", function(d) { return fill(d.group); })

This function is evaluated for each node, which is called `d`

. Any property we previously added in Python is saved in the JSON, and can be recalled easily. For the network graph shown at the beginning of this page, these attributes and styles have been used:

.attr("r", function(d) { if (d.group == 0) return 20; return 15-d.group; }) .style("fill", function(d) { return d3.hsl(d.colour).brighter(d.group/3); }) .style("stroke-width", function(d) { if (d.group === 0) return 5; return 1; })

Both `colour`

and `group`

are properties that have been initialised by the Python script. The former indicates the base colour of the node, while the latter counts how far the node is from the melancoil loop.

Nodes with labels

The first change we need to do is to add labels to the nodes. In order to do this we have to create a container node which will host the circle and the text.

// Container var node = vis.selectAll(".node") .data(force.nodes()) .enter().append("g") .attr("class", "node") .call(force.drag); // Circle node.append("circle") .attr("class", "node") .attr("x", function(d) { return d.x; }) .attr("y", function(d) { return d.y; }) .attr("r", 5) .style("fill", function(d) { return fill(d.group); }); // Text node.append("text") .attr("x", -10) .style("font-size", "10") .text(function(d) { return d.name; });

We also have to make sure that the new containers move when the graph is rearranged. To do so, we need to add these two lines in the `force.on`

function:

node.attr("cx", function(d) { return d.x; }) .attr("cy", function(d) { return d.y; });

If you are interested in this topic, you might also find the following tutorials interesting:

## Leave a Reply Cancel reply