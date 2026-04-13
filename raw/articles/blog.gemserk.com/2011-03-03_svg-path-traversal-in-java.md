---
title: SVG Path Traversal in Java
url: https://blog.gemserk.com/2011/03/03/svg-path-traversal-in-java/
published: '2011-03-03'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Because [some people asked](http://slick.javaunlimited.net/viewtopic.php?p=18071#18071), in this post we are going to explain in some detail how we do the balls movement in Zombie Rockers. All this work could be useful for other kind of games using paths like, for example, a tower defense.

For Zombie Rockers (we have to change that name), we defined a Path as an ordered collection of points. Simplifying our [Path](https://github.com/gemserk/componentsengine/blob/a528379baadca8025cf1827624e02331f49b03ad/commons/src/main/java/com/gemserk/componentsengine/commons/components/Path.java) class, it could be something like this:

class Path { ArrayList<Vector2f> points; }

note: we are using Vector2f provided by [Slick2D](http://slick.cokeandcode.com/)

To easily traverse a path, we created the class [PathTraversal](https://github.com/gemserk/componentsengine/blob/f4aad6d676539608afac041b69837c6d75090907/commons/src/main/java/com/gemserk/componentsengine/commons/path/PathTraversal.java), which let us move forward or backward through the path. For example, we could start in the beginning of a path built by three points: (100,100), (200, 100) and (300, 100). Then, if we advance 50 units, then we are going to be on the coordinate (150, 100), between first and second point.

note: when we say units, could be anything you need, pixels, meters, etc, it is not important for the example.

The idea of the PathTraversal in the future is to support any kind of paths, for example, one made using [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) instead only a list of points.

This shows the API of the PathTraversal:

class PathTraversal { // the path we are traversing Path path; // the distance to the origin we are right now float getCurrentDistance(); // go back the specified distance void backward(float distance); // go forward the specified distance void forward(float distance); // returns a point based on the current distance Vector2f getPoint(); }

You can create the Path in the way you want, for Zombie Rockers we are using SVG files to store the paths for each level and we are loading it using [SVG Salamander](http://svgsalamander.java.net/) project. First we create a AWT Shape using the Path class provided by the SVG Salamander, then we use a PathIterator to build the points we need to create our Path.

public List<Vector2f> loadPointsFromSVG(URI fileUri) { ArrayList<Vector2f> points = new ArrayList<Vector2f>(); SVGDiagram diagram = SVGCache.getSVGUniverse().getDiagram(fileUri); SVGElement element = diagram.getElement(pathName); List vector = element.getPath(null); com.kitfox.svg.Path pathSVG = (com.kitfox.svg.Path) vector.get(1); // get the AWT Shape Shape shape = pathSVG.getShape(); // iterate over the shape using a path iterator discretizing with distance 0.001 units PathIterator pathIterator = shape.getPathIterator(null, 0.001d); float[] coords = new float[2]; while (!pathIterator.isDone()) { pathIterator.currentSegment(coords); points.add(new Vector2f(coords[0], coords[1])); pathIterator.next(); } }

To create the SVG path, you can use any program you want, in our case we are using mainly [Gimp](http://www.gimp.org/), we tried using [Inkscape](http://www.inkscape.org/) too but as we are creating the levels using Gimp it was easy to do all the work using the same application. So, open Gimp, create a path and then export it to a SVG file. Then, it should be ready to be loaded by SVG salamander inside your code.

A working example of this technique is shown in the next video of Zombie Rockers:

### Conclusion

This solution works well while you avoid making the angle of two consecutive segments too sharp. For example, right now when balls traverse between two segments where the angle is too sharp, they will change the render direction too quickly and doesn’t looks so good.

![The problem of SVG Path when the angle of two consecutive segments is too sharp.](../../assets/f248488c2ee7c2ae.png)


Figure 1: The problem of SVG Path when the angle of two consecutive segments is too sharp.

One solution to reduce this, is to increment the points of the path when making a discrete version of the path, so you will have more intermediate points, then less angle brusque changes.

Another solution is to use a smooth change for the rendering direction, so when you change the value of the render direction, it will change smoothly over time.

Hope it could be of help.

Update: Added figure for the problem of the angles between segments.

Update2: Added links to the current implementation of Path and PathTraversal classes.

Update3: Fixed the path example.