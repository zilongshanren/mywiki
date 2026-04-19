---
title: Brachiograph plotter
url: https://www.4rknova.com/blog/2022/05/02/brachiograph
author: Nikolaos Papadopoulos
published: '2022-05-02'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

A while back I stumbled across a very interesting electronics project that I was really keen to try myself.

BrachioGraph is a 2D plotter that is based on the raspberry pi computer and is extremely simple and cheap to build. I followed the original design with a few small modifications to build my own. More specifically:

- I replaced the Tower SG90 servos in the articulated segments with metal gear MG995 ones to increase stability and reduce jerkiness during drawing.
- I added two metal brackets to hold the MG995s to further improve stability.
- I’ve soldered together a rundimentary circuit that allows servos to share the ground (GND) pin on the raspberry pi.

The plotter can draw any image by simply vectorizing it and then breaking the vector shapes down to very short line segments. This is done because activating the motor to move from point A to point B will produce a curved line rather than a straight one, so the idesired straight line is approximated with smaller line segments that accommodate for the associated error.

The mathematical background of how the plotter draws a line is very simple. It uses basic trigonometry to calculate the angles for each segment and interpolate between two positions. A detailed explanation is available at this page: [BrachioGraph, The mathematics](https://www.brachiograph.art/explanation/mathematics/)

Below you can see the plotter in action.