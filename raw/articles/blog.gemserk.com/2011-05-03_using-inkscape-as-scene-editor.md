---
title: Using Inkscape as Scene Editor
url: https://blog.gemserk.com/2011/05/03/using-inkscape-as-scene-editor/
published: '2011-05-03'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

On a previous blog post</a>, I wrote about how are we using [Inkscape](http://inkscape.org/) as a Scene Editor for Archer Vs Zombies. Now, I want to talk a bit more about it. The post was going to be a dev log about Archer Vs Zombies but since it is about general Inkscape stuff for games, the original name lost its meaning.

First, I want to share a video showing how changes made in Inkscape are being reflected when the game loads.

note: some of the rocks were moved.

### Creating Physics Object

As I probably said before, we are using [Box2D](http://www.box2d.org/) to do physics behavior on our games. Box2D provides a way to define bodies based on [circle or polygon shapes](http://www.box2d.org/manual.html#_Toc258082970). Circle shapes are defined by a center and a radius and polygon shapes are defined by a list of vertices with some restrictions explained in [Box2D manual](http://www.box2d.org/manual.html).

On the other hand, SVG specification provides a way to specify [paths](http://www.w3.org/TR/SVG/paths.html) which are used to describe straight lines or curves.

Then, I am creating SVG paths, when building the scene, in a separated Inkscape layer (named Physics) which could be parsed later inside the game to create Box2D polygon shapes. Having a separated layer for those shapes simplify the scene load process and, when working on Inkscape, provides a way to hide or show shapes definitions layer to easily work on the others.

![](../../assets/24d2f1254d8ea987.png)


### Using XML Data to define Physics Bodies properties

One thing we could need in the future is to define more stuff about physics bodies like if they are [static or dynamic, their mass, density and others](http://www.box2d.org/manual.html#_Toc258082973). As said on the previous post</a>, we could add custom XML data to XML nodes of the SVG file and process it when parsing the SVG inside the game to define those properties. For now, I am treating all SVG paths from the Physics layer as static bodies with no properties.

### Parsing the SVG - Second part

I wanted to give a second chance to both SVG Salamander and Batik but the main reason to discard them is because both libraries depends on AWT classes and that doesn’t work on Android.

In the end, I am using my [own and incomplete parser implementation](https://github.com/gemserk/commons-gdx/tree/master/commons-gdx-core/src/main/java/com/gemserk/commons/svg/inkscape) based on Slick2D SVG Parser classes with a lot of modifications because I am not using Slick2D Vector2f and Transform classes and because its doesn’t handle SVG images.

### Conclusion

After all that work, I feel comfortable working with Inkscape as a Scene Editor and I don’t feel the need to implement our own for now. Also, in my opinion, it is similar to Aquaria Scene Editor</a> as you can add sprites, rotate and scale them, move from one layer to another, etc, with limitations like you cannot test the scene until you load it in your game, between others.

Thats all for now, hope you like it.