---
title: Real-time server visualization with canvas and processing.js – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2010/04/real-time-server-visualization-with-canvas-and-processing-js/
author: Jay Patel
published: '2010-04-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![cloudkick_20100420](https://hacks.mozilla.org/wp-content/uploads/2010/04/cloudkick_20100420-250x142.png)

*This is a guest blog post by Logan Welliver, Chief Creative at Cloudkick. He is a graphic designer by training and a web designer in practice.*

Cloud management company Cloudkick has released a [real-time server monitoring visualization](https://www.cloudkick.com/viz/mozilla) based on canvas and processing.js, that was co-developed with [Alastair McDonald](http://alistairgmacdonald.com/) of processing.js fame. The product is designed to let users keep a finger on the pulse of their infrastructure, quickly identify problem nodes, and visualize aggregate performance with an easy-to-digest interface.

The tool uses canvas and processing.js to plot servers as stylized circles in 3 dimensions, with axes mapped to one of three performance metrics: CPU usage, memory usage, and ping latency. Each server’s radius is determined by it’s relative prowess (i.e. an EC2 extra large is bigger than 256mb Slice), and colors are customizable via the Cloudkick dashboard. Each server sparkles when the monitoring system returns data, and servers with problems identify themselves by flashing an angry red.

Canvas and processing.js take care of all the presentation, powered by a slew of back-end services that do everything from monitoring servers to pushing data in real-time back to the user.

Here’s a brief overview of the back-end architecture: instances of the [Cloudkick Agent](https://support.cloudkick.com/Main_Page#Cloudkick_Agent) (running on individual servers) report metrics to an endpoint, which talks to [Reconnoiter](https://labs.omniti.com/trac/reconnoiter), which then publishes messages to RabbitMQ. An internal service called Livedata consumes these messages, finds the ones applicable to an account, and publishes messages back to [RabbitMQ](http://www.rabbitmq.com/). [Orbited](http://orbited.org/) consumes these messages and sends them to the browser. From agent to browser, the round-trip time is less than a second.

Cloudkick has partnered with Mozilla to provide the visualization for their [addons.mozilla.org](http://addons.mozilla.org/) servers. You can see how they’re behaving in a live demo of the visualization here: [addons.mozilla.org infrastructure in Cloudkick Viz.](https://www.cloudkick.com/viz/mozilla/)

Get the visualization for your own servers. Cloudkick is offering [20% off for the first 100 Mozilla Hacks readers, using promo code “mozhacks01”.](https://www.cloudkick.com/pricing/mozhacks01)

## About Jay Patel

I strive to make the web better by making sure those that develop and drive it are happy campers.

## 4 comments

BrianApril 28th, 2010 at 08:01ChrisApril 28th, 2010 at 19:39MaxApril 29th, 2010 at 03:11b_i_dMay 12th, 2010 at 10:40