---
title: Flambe Provides Support For Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/03/flambe-provides-support-for-firefox-os/
published: '2014-03-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Flambe](https://github.com/aduros/flambe) is a performant cross-platform open source game engine based on the [Haxe](http://haxe.org/) programming language. Games are compiled to HTML5 or Flash and can be optimized for desktop or mobile browsers. The HTML5 Renderer uses [WebGL](https://developer.mozilla.org/en-US/docs/Web/WebGL), but provides fallback to the [Canvas](https://developer.mozilla.org/en-US/docs/HTML/Canvas) tag and functions nicely even on low-end phones. Flash Rendering uses [Stage 3D](http://www.adobe.com/devnet/flashplayer/stage3d.html) and native Android and iOS apps are packaged using [Adobe AIR](https://get.adobe.com/air/).

Flambe provides many other features, including:

- simple asset loading
- scene management
- touch support
- complete physics library
- accelerometer access

It has been used to create many of the Nickelodeon games available at [nick.com/games](http://nick.com/games) and [m.nick.com/games](http://m.nick.com/games). To see other game examples, and some of the other well-known brands making use of the engine, have a look at the [Flambe Showcase](https://github.com/aduros/flambe/wiki/Showcase).

In the last few weeks, the developers of the Flambe engine have been working to add support for [Firefox OS](https://developer.mozilla.org/en-US/Firefox_OS). With the 4.0.0 release of Flambe, it is now possible to take Flambe games and package them into publication-ready Firefox OS applications, complete with manifest.

## Firefox Marketplace Games

To get an idea of what is possible with the Flambe engine on the Firefox OS platform, take a look at two games that were submitted recently to the Firefox [Marketplace](https://marketplace.firefox.com/). The first — [The Firefly Game](https://marketplace.firefox.com/app/the-firefly) written by Mark Knol — features a firefly that must navigate through a flock of hungry birds. The game’s use of physics, sound and touch are very effective.

![firefly](../../assets/9384652c0b77aedb.png)


The second game, entitled [Shoot’em Down](https://marketplace.firefox.com/app/shootem-down), tests the player’s ability to dodge fire while shooting down as many enemy aircraft as possible. The game was written by Bruno Garcia, who is the main developer of the Flambe engine. The [source](https://github.com/aduros/flambe-demos/tree/master/shmup) for this game is available as one of the engine’s demo apps.

![shootemup](../../assets/4c0394d6f958262a.png)


## Building a Firefox OS App using Flambe

Before you can begin writing games using the Flambe engine, you will need to install and setup a few pieces of software:

- Haxe. Auto installers are available for OSX, Windows and Linux on the download page.
- Node.js for building projects. Version 0.8 or greater is required
- A Java runtime.

Once those prerequisites are met, you can run the following command to install Flambe:

```
# Linux and Mac may require sudo
npm install -g flambe
flambe update
```

This will install Flambe and you can begin writing apps with the engine.

### Create a Project

To create a new project, run the following command.

```
flambe new
```

This will create a directory named whatever you supplied for ProjectName. In this directory you will have several files and other directories for configuring and coding your project. By default the new command creates a very simple project that illustrates loading and animating an image.

A YAML (flambe.yaml) file within the project directory defines several characteristics of the project for build purposes. This file contains tags for developer, name and version of the app, and other project meta-data, such as description. In addition it contains the main class name that will be fired as the entry point to your application. This tag needs to be set to a fully qualified [Haxe Class](http://haxe.org/ref/oop) name. I.e., if you use a package name in your Haxe source file, you need to prepend the package name in this tag like this: packagename.Classname. (The default example uses urgame.Main.) You can also set the orientation for your app within the YAML file.

Of specific note for Firefox OS developers, a section of the YAML file contains a partial [manifest.webapp](https://developer.mozilla.org/en-US/Apps/Build/Manifest) that can be altered. This data is merged into a complete manifest.webapp when the project is built.

The main project folder also contains a directory for assets (images, sounds, animations, and particle effects files). The icons folder contains the icons that will be used with your app. The src folder contains the Haxe source code for your application.

### Build the Project

Flambe provides a build method to compile your code to the appropriate output. To build the app run:

```
flambe build
```

Where output is html, flash, android, ios, or firefox. Optionally you can add the –debug option to the build command, producing output more suitable for debugging. For Firefox OS this will produce non-minified JavaScript files. The build process will add a build directory to your application. Inside of the build directory a firefox directory will be created containing your Firefox OS app.

### Debug the Project

You can debug your application in the Firefox App Manager. See [Using the App Manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) for details on installing and debugging using the App Manager. Within the App Manager you can add the built app using the Add Packaged App button and selecting the ProjectName/build/firefox directory. Debugging for other platforms is described in the Flambe [documentation](https://github.com/aduros/flambe/wiki/Installation).

![appmanager](../../assets/2f2933ca4cacf235.png)


The -debug option can provide additional insight for debugging and performance tuning. In addition to being able to step through the generated JavaScript, Flambe creates a source map that allows you to look look through the original Haxe files while debugging.

![debugsession](../../assets/3dfbd04b859193fb.png)


To see the original Haxe files in the debugger, select the Debugger options icon in the far right corner of the debugger and choose Show Original Sources.

![sourcemap](../../assets/8f537f4f09012b0e.png)


Also, when using the -debug option you can use a shortcut key (Ctrl + O) to initiate a view of your app that illustrates overdraw — this measures the number of times a pixel is being drawn in a frame. The brighter the pixel the more times it is being drawn. By reducing the amount of overdraw, you should be able to improve the performance of your game.

![overdraw](../../assets/92f94deb0ec8eace.png)


## A Bit about Haxe and Flambe

Haxe is an object-oriented, class-based programing language that can be compiled to many other languages. In Flambe, your source code needs to be written using [Haxe-specific syntax](http://haxe.org/doc/features). Developers familiar with Java, C++ or JavaScript will find learning the language relatively straightforward. The Haxe website contains a [reference guide](http://haxe.org/ref) that nicely documents the language. For [editing](http://haxe.org/com/ide), there are many options available for working with Haxe. I am using Sublime with the Haxe plugin.

Flambe offers some additional classes that need to be used when building your app. To get a better understanding of these classes, let’s walk through the simple app that is created when you run the flambe new command. The Main.hx file created in the source directory contains the Haxe source code for the Main Class. It looks like this:

```
package urgame;
import flambe.Entity;
import flambe.System;
import flambe.asset.AssetPack;
import flambe.asset.Manifest;
import flambe.display.FillSprite;
import flambe.display.ImageSprite;
class Main
{
private static function main ()
{
// Wind up all platform-specific stuff
System.init();
// Load up the compiled pack in the assets directory named "bootstrap"
var manifest = Manifest.fromAssets("bootstrap");
var loader = System.loadAssetPack(manifest);
loader.get(onSuccess);
}
private static function onSuccess (pack :AssetPack)
{
// Add a solid color background
var background = new FillSprite(0x202020, System.stage.width, System.stage.height);
System.root.addChild(new Entity().add(background));
// Add a plane that moves along the screen
var plane = new ImageSprite(pack.getTexture("plane"));
plane.x._ = 30;
plane.y.animateTo(200, 6);
System.root.addChild(new Entity().add(plane));
}
}
```

### Haxe Packages and Classes

The `package`

keyword provides a way for classes and other Haxe data types to be grouped and addressed by other pieces of code, organized by directory. The `import`

keyword is used to include classes and other Haxe types within the file you are working with. For example, `import flambe.asset.Manifest`

will import the Manifest class, while `import flambe.asset.*`

will import all types defined in the asset package. If you try to use a class that you have not imported into your code and run the build command, you will receive an error message stating that the particular class could not be found. All of the Flambe packages are [documented](https://aduros.com/flambe/api/) on the Flambe website.

### Flambe Subsystem Setup and Entry point

The `main`

function is similar to other languages and acts as the entry point into your app. Flambe applications must have one main function and only one per application. In the main function the `System.init()`

function is called to setup all the subsystems that will be needed by your code and the Flambe engine.

### Flambe Asset Management

Flambe uses a dynamic asset management system that allows images, sound files, etc. to be loaded very simply. In this particular instance the `fromAssets`

function defined in the `Manifest`

class examines the bootstrap folder located in the assets directory to create a manifest of all the available files. The `loadAssetPack`

System function creates an instance of the `AssetPack`

based on this manifest. One of the functions of AssetPack is `get`

, which takes a function parameter to call when the asset pack is loaded into memory. In the default example, the only asset is an image named plane.png.

### Flambe Entities and Components

Flambe uses an abstract concept of Entities and Components to describe and manipulate game objects. An Entity is essentially just a game object with no defining characteristics. Components are characteristics that are attached to entities. For example an image component may be attached to an entity. Entities are also hierarchal and can be nested. For example, entity A can be created and an image could be attached to it. Entity B could then be created with a different image. Entity A could then be attached to the System root (top level Entity) and Entity B could then be attached to Entity A or the System root. The entity nest order is used for rendering order, which can be used to make sure smaller visible objects are not obscured by other game objects.

### Creating Entities and Components in the Sample App

The `onSuccess`

function in the default sample is called by the loader instance after the `AssetPack`

is loaded. The function first creates an instance of a `FillSprite`

Component, which is a rectangle defined by the size of the display viewport width and height. This rectangle is colored using the hex value defined in the first parameter. To actually have the `FillSprite`

show up on the screen you first have to create an `Entity`

and add the Component to it. The `new Entity().add(background)`

method first creates the `Entity`

and then adds the `FillSprite`

Component. The entire viewport hierarchy starts at the System.root, so the `addChild`

command adds this new Entity to the root. Note this is the first Entity added and it will be the first rendered. In this example this entity represents a dark background.

Next the plane image is created. This is done by passing the loaded plane image to the `ImageSprite`

Component constructor. Note that the AssetPack class’s `getTexture`

method is being used to retrieve the loaded plane image. The `AssetPack`

class contains methods for retrieving other types of Assets as well. For example, to retrieve and play a sound you would use `pack.getSound("bounce").play();`

.

### Flambe Animated Data Types

Flambe wraps many of the default Haxe [data types](http://haxe.org/manual/basic_types) in classes and introduces a few more. One of these is the `AnimatedFloat`

class. This class essentially wraps a float and provides some utility functions that allow the float to be altered in a specific way. For example, one of the functions of the `AnimatedFloat`

class is named `animateTo`

, which takes parameters to specify the final float value and the time in which the animation will occur. Many components within the Flambe system use AnimatedFloats for property values. The plane that is loaded in the default application is an instance of the `ImageSprite`

Component. Its x and y placement values are actually AnimatedFloats. `AnimatedFloat`

values can be set directly but special syntax has to be used `(value._)`

.

In the example, the x value for the `ImageSprite`

is set to 30 using this syntax: `plane.x._ = 30;`

. The y value for the `ImageSprite`

is then animated to 200 over a 6 second period. The x and y values for an `ImageSprite`

represent the upper left corner of the image when placed into the viewport. You can alter this using the `centerAnchor`

function of the `ImageSprite`

class. After this call, the x and y values will be in reference to the center of the image. While the default example does not do this, it could be done by calling `plane.centerAnchor();`

. The final line of code just creates a new Entity, adds the plane Component to the Entity and then adds the new Entity to the root. Note that this is the second Entity added to the root and it will render after the background is rendered.

### Flambe Event Model

Another area of Flambe that is important to understand is its event model. Flambe uses a signal system where the subsystems, Components and Entities have available signal properties that can be connected to in order to listen for a specific signal event. For example, resizing the screen fires a signal. This event can be hooked up using the following code.

```
System.stage.resize.connect(function onResize() {
//do something
});
```

This is a very nice feature when dealing with other components within apps. For example, to do something when a user either clicks on or touches an `ImageSprite`

within your app you would use the following code:

```
//ImageSprite Component has pointerDown signal property
myBasketBallEntity.get(ImageSprite).pointerDown.connect(function (event) {
bounceBall();
});
```

In this case the `pointerDown`

signal is fired when a user either uses a mouse down or touch gesture.

## Demo Apps

The Flambe repository also contains many [demo apps](https://github.com/aduros/flambe-demos) that can be used to further learn the mechanics and APIs for the engine. These demos have been tested on Firefox OS and perform very well. Pictured below are several screenshots taken on a Geeksphone Keon running Firefox OS.

![colla](../../assets/b99e2b95bfd38ae0.png)


Of particular note in the demos are the physics and particles demos. The physics demo uses the [Nape](http://napephys.com/index.html) Haxe library and allows for some very cool environments. The Nape website contains [documentation](http://napephys.com/docs/index.html) for all the packages available. To use this library you need to run the following command:

```
haxelib install nape
```

The particle demo illustrates using particle descriptions defined in a PEX file within a Flambe-based game. PEX files can be defined using a particle editor, like [Particle Designer](http://71squared.com/particledesigner).

## Wrapping Up

If you are a current Flambe game developer with one or more existing games, why not use the new version of the engine to compile and package them for Firefox OS? If you are a Firefox OS developer and are looking for a great way to develop new games for the platform, Flambe offers an excellent means for developing engaging, performant games for Firefox OS–and many other platforms besides!

And, if you are interested in contributing to Flambe, we’d love to hear from you as well.

## About
[
Bruno Garcia ](https://github.com/aduros)

Bruno is the lead developer of Flambe, and has been developing HTML5 games since 2010. He is also a member of the Haxe compiler team, contributes to the Flump open source project, and writes the occasional game on the side. His favorite color is #202020.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

jkeksMarch 18th, 2014 at 03:18geoMarch 19th, 2014 at 06:49MarcelMarch 19th, 2014 at 15:09YopSoloMarch 24th, 2014 at 14:39