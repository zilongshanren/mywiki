---
title: MetricsGraphics.js – a lightweight graphics library based on D3 – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/12/metricsgraphics-js-a-lightweight-graphics-library-based-on-d3/
author: Ali Almossawi
published: '2014-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[MetricsGraphics.js](http://metricsgraphicsjs.org/) is a library built on top of [D3](http://d3js.org/) that is optimized for visualizing and laying out time-series data. It provides a simple way to produce common types of graphics in a principled and consistent way. The library supports line charts, scatterplots, histograms, barplots and data tables, as well as features like rug plots and basic linear regression.

The library elevates the layout and explanation of these graphics to the same level of priority as the graphics. The emergent philosophy is one of efficiency and practicality.

[Hamilton Ulmer](https://github.com/hamilton/) and I began building the library earlier this year, during which time we found ourselves copy-and-pasting bits of code in various projects. This led to errors and inconsistent features, and so we decided to develop a single library that provides common functionality and aesthetics to all of our internal projects.

Moreover, at the time, we were having limited success with our attempts to get casual programmers and non-programmers within the organization to use a library like D3 to create dashboards. The learning curve was proving a bit of an obstacle. So it seemed reasonable to create a level of indirection using well-established design patterns to try and bridge that chasm.

Our API is simple. All that’s needed to create a graphic is to specify a few default parameters and then, if desired, override one or more of the [optional parameters on offer](https://github.com/mozilla/metrics-graphics/wiki/List-of-Options). We don’t maintain state. To update a graphic, one would call *data_graphic* on the same target element.

The library is also data-source agnostic. While it provides a number of convenience functions and options that allow for graphics to better handle things like missing observations, it doesn’t care where the data comes from.

## A quick tutorial

Here’s a quick tutorial to get you started. Say that we have some data on a scholarly topic like [UFO sightings](http://geocommons.com/overlays/134594). We decide that we’re interested in creating a line chart of yearly sightings.

We create a JSON file called [data/ufo-sightings.json](http://metricsgraphicsjs.org/data/ufo-sightings.json) based on the original dataset, where we aggregate yearly sightings. The data doesn’t have to be JSON of course, but that will mean less work later on.

The next thing we do is load the data:

```
d3.json('data/ufo-sightings.json', function(data) {
})
```

*data_graphic* expects the data object to be an array of objects, which is already the case for us. That’s good. It also needs dates to be timestamps if they’re in a format like *yyyy-mm-dd*. We’ve got aggregated yearly data, so we don’t need to worry about that. So now, all we need to do is create the graphic and place it in the element specified in *target*.

```
d3.json('data/ufo-sightings.json', function(data) {
data_graphic({
title: "UFO Sightings",
description: "Yearly UFO sightings (1945 to 2010).",
data: data,
width: 650,
height: 150,
target: '#ufo-sightings',
x_accessor: 'year',
y_accessor: 'sightings',
markers: [{'year': 1964,
'label': '"The Creeping Terror" released'
}]
})
})
```

And this is what we end up with. In this example, we’re adding a marker to draw attention to a particular data point. This is optional of course.

![A line chart in MetricsGraphics.js](http://metricsgraphicsjs.org/images/metricsgraphics.png)


## A few final remarks

We follow a real-needs approach to development. Right now, we have mostly implemented features that have been important to us. Having said that, our work is available on [Github](https://github.com/mozilla/metrics-graphics), as are many of our discussions, and we take any and all pull requests and issues seriously.

There is still a lot of work to be done. We invite you to take the library out for a spin and file bugs! We’ve set up a sandbox that you can use to try things out without having to download anything: [http://metricsgraphicsjs.org](http://metricsgraphicsjs.org)

MetricsGraphics.js v1.1 is scheduled for release on December 1, 2014.

## About
[
Ali Almossawi ](http://almossawi.com)

Data visualization engineer at Mozilla almossawi.com

## 4 comments

alejandroDecember 3rd, 2014 at 01:42rgeDecember 5th, 2014 at 19:53ingeeDecember 12th, 2014 at 00:26Robert KaiserDecember 18th, 2014 at 08:15