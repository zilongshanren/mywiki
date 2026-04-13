---
title: Gameleon and the map editor – a WebFWD project – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/gameleon-and-the-map-editor-a-webfwd-project/
author: Victor Popescu
published: '2013-03-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

More than 9 months ago, we were working on a web game, having all the nice HTML5 stuff like Canvas, WebSocket, CSS3. We were playing a lot with experimental code in NodeJS and Redis. We had all the nice scripts and plugins and quite a good architecture to make the game possible.

We lacked one thing though: a powerful editor. Since we had 8 years of nothing but web development experience, we were keen on making this web too. We didn’t like Flash though or anything which isn’t a web standard or open technology, because it was restricting us from using what we made on all the devices we had through the office, in the same way (tablets, phones, laptops, desktops).

## Creating an editor

So, we’ve started making [Gameleon](http://www.gameleon.co/) for Shay, our game architect. He did quite a lot of Dungeons and Dragons and played with many of the RPG editors out there. We thought that he was good just like that, without any programming knowledge, and we wanted to give him the means to make anything in our game, without coming to us.

The first thing we made was the map editor. One thing was sure about this: we didn’t want to have any kind of limitations, such as tiles. What we love doing is drawing the maps ourselves, in any way we see fit. The one thing you can never know about a random picture is where the obstacles are. For that, we made a polygon editing tool, which can define just that. It is like a mesh applied on top of the map, giving it the logic for collision detection later.

Probably this video demonstrating how a map is built will be of more help:

## Processing a map

In this article i’ll try to discuss a bit about how the map is processed and turned into a walkable, obstacle friendly surface.

When it comes to making a friendly way to define areas, using vectors is the way to go, as you probably saw in the above video.

A map is defined by vertices and points. They are sent to the server via WebSocket, in JSON format.

The struggle when having a good map is to have that good mixture between freedom to create as much content as you want, yet be able to determine what surface is an obstacle and have a very fast collision detection system and path finding.

The best mix of these two we’ve found to be in a grid. Using A* and QuadTree to determine the shortest route and the collisions between objects, no matter what size, became a lot simpler. By the way, all objects defined on a map, are treated as circles. When we determine if an object collides with another (in a combat situation for instance), we can make one of the objects move to the nearest empty area, while still being in range of the target.

So, this is why we are going to transform the vector map we’ve just received, into a grid, having a square of the size of 8 x 8 points. Experimentally, we’ve determined it is a small enough square to have a small number of collisions, and yet be effective when searching across long distances (for instance, searching for the shortest path between two points A and B on a map of 3200 x 2000 points).

### Determining the squares

To determine the squares a polygon is going to cover, we use a brute force technique. Yes, it may sound crude, but it is quite effective. First, we determine the rectangle covered by the polygon.

```
enhance.prototype._determineRectangle = function( points, poly )
{
var minX = null, minY = null, maxX = null, maxY = null;
for(var j=0;j
``` maxX )
{
maxX = currentPoint[0];
}
if( minY == null || currentPoint[ 1 ] < minY )
{
minY = currentPoint[1];
}
if( maxY == null || currentPoint[ 1 ] > maxY )
{
maxY = currentPoint[1];
}
}
return { minX: minX, minY: minY, maxX: maxX, maxY: maxY };
}

### Checking point positions

Once we have that, we start going through each point of that rectangle and check if the point is inside or outside the polygon. The theory behind this is to draw a horizontal line passing through that point and check the number of intersections with the polygon’s vertices. If the number of intersections is odd, then the point is outside. If the number is even, then it is inside.

```
enhance.prototype._pointInPolygon = function( x, y, poly, points )
{
var j = poly.coords.length - 1, oddNodes = false;
for(var i = 0;i < poly.coords.length; i++)
{
var pointI = poly.coords[i],
pointJ = poly.coords[j],
_pointIY = points[ pointI ][1],
_pointJY = points[ pointJ ][1],
_pointIX = points[ pointI ][0],
_pointJX = points[ pointJ ][0];
if(
_pointIX == x &&
_pointIY == y
)
{
return true;
}
if(
( _pointIY < y && _pointJY >= y ) ||
( _pointJY < y && _pointIY >= y )
)
{
if(
_pointIX + ( y - _pointIY ) / ( _pointJY - _pointIY ) * ( _pointJX - _pointIX ) < x
)
{
oddNodes = !oddNodes;
}
}
j = i;
}
return oddNodes;
}
```

This way, we mark the walkable and non-walkable areas of the map. However, there are those special situations when you want to mark an area as walkable or non-walkable dynamically.

Say you have some debris and you don't want that area to be walkable, but once the debris are destroyed, that area has to be changed. So, we keep in a separate vector, the actual points covered by each polygon.

### Setting names

In the map editor, you are being given the ability to name polygons, both for esthetic purposes - to notify the player that he is entering "The Killing Fields" for instance, and to lookup via scripting.

The scripting names are automatically given - ZP01, ZP02, etc. - to ensure their unique name.

In the script editor, you can use an action named setWalkableArea, and send as parameter the polygon name. When the action is executed, the server will broadcast to every member on the map, the points which are suppose to change their state, thus updating the map grid with ease. No additional processing will be done.

Say you attach this to the event of an object being destroyed, which was right on top of that area. This would create the illusion that the object itself was an obstacle and that it is now removed.

Neat, isn't it?

## Part of Gameleon

The code above is part of the editor and this coding standard can be found throughout the entire Gameleon code.

Hope you enjoyed this short intro into how we see maps and games being created. If you want to know more, have a look at [Gameleon](http://www.gameleon.co/) and [follow us on twitter: @gameleonMain](https://twitter.com/GameleonMain).

The complete [source code is available on GitHub](https://github.com/victoralex/gameleon).

## About
[
Victor Popescu ](http://www.gameleon.co)

Team lead & engine developer @ Gameleon Ask me anything about web software architecture, game-related algorithms, NodeJS, HTML5, noSQL or MySQL

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

MichaelMarch 28th, 2013 at 20:39Victor PopescuMarch 29th, 2013 at 12:50