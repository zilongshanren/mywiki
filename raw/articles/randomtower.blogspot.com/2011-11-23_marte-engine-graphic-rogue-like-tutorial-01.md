---
title: Marte Engine Graphic Rogue Like Tutorial 01
url: https://randomtower.blogspot.com/2011/11/marte-engine-graphic-rouge-like.html
author: Pubblicato da Marte
published: '2011-11-23'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Project setup, HelloWorld, distribution**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from Trystan (

[http://trystans.blogspot.com/](http://trystans.blogspot.com/)) and follow the same organization, so let's start and setup the new project!

**Project setup**

You must install and download both

[Eclipse](http://www.eclipse.org/)(I'll assume you will use this IDE for your development) and

[Java](http://www.java.com/)to do this tutorial and create a new Java Project. New projects are empty, but you will fill it soon! First of all, add two new folders and call them lib and data. Not so surprising in lib data we will put library and in data all game assets (graphics, sounds and so on). Create a new folder inside lib folder and call it native, I'll explain his use later.

You need now to download MarteEngine from

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine), in this tutorial I'll refereer to version 0.3 of MarteEngine, download this version and be sure to be name it as marteEnginev03-dev.jar But what is MarteEngine? MarteEngine is a jar (a java library) a set of useful classes help brave developers in their duties, in this case build a rouge like. MarteEngine have also some dependencies:

[Slick](http://slick.cokeandcode.com/)and

[lwjgl](http://lwjgl.org/%20), you don't care for now about this libraries, so just download it from MarteEngine github site

You have also to download native libraries for lwjgl for your system: windows, mac or linux.

When you have done this, just add all three jars to your build path (select them and right click, then buil path then add to build path). Jars are now added as references libraries into your project and you can use classes. In order to setup your project correctly, you need to set native folder for lwjgl jar, so select into rerefernced libraries, right click, properties then native location and select a workspace location, yes, lib/native folder!

It's time to add also a package for your future classes, just add it and call it merlTut

It's also time to define resource file: it's used with MarteEngine to help you in loading and managing your game's assets, sounds, images and so on. So create inside data folder a resource.xml with this content:

**Hello World**

Now that project is setup, it's time to test it. Add a new class file, HelloWorld.java and copy/paste this code:

package merlTut; import it.marteEngine.ResourceManager; import it.marteEngine.World; import it.marteEngine.entity.TextEntity; import java.io.IOException; import org.newdawn.slick.AppGameContainer; import org.newdawn.slick.GameContainer; import org.newdawn.slick.SlickException; import org.newdawn.slick.state.StateBasedGame; import org.newdawn.slick.util.Log; public class HelloWorld extends StateBasedGame { private static boolean ressourcesInited; public HelloWorld(String title) { super(title); } @Override public void initStatesList(GameContainer container) throws SlickException { initResources(); World world = new World(0, container); world.add(new TextEntity(100, 100, null, "Hello World!")); addState(world); } public static void initResources() throws SlickException { if (ressourcesInited) return; try { ResourceManager.loadResources("data/resources.xml"); } catch (IOException e) { Log.error("failed to load ressource file 'data/resources.xml': " + e.getMessage()); throw new SlickException("Resource loading failed!"); } ressourcesInited = true; } public static void main(String[] argv) { try { AppGameContainer container = new AppGameContainer(new HelloWorld( "Hello World Marte Engine")); container.setDisplayMode(640, 480, false); container.setTargetFrameRate(60); container.start(); } catch (SlickException e) { e.printStackTrace(); } } }

Running this code an empty black window will open with no content inside: boring, yes? So just add a "Hello World" message, modifing initStatesList and adding this lines:

@Override public void initStatesList(GameContainer container) throws SlickException { initRessources(); World world = new World(0, container); world.add(new TextEntity(100, 100, null, "Hello World!")); addState(world); }

Now run your code a simple "Hello World", message will be rendered into your game's window

It's time to understand this basic example and then move on. Let's start with class definition: with this code we are subclassing a classes from slick that will help us to separate your game in different states: one for menu, one for game, one for achievements, but this are examples.

public class HelloWorld extends StateBasedGame { public static void initResources() throws SlickException { if (ressourcesInited) return; try { ResourceManager.loadResources("data/resources.xml"); } catch (IOException e) { Log.error("failed to load ressource file 'data/resources.xml': " + e.getMessage()); throw new SlickException("Resource loading failed!"); } ressourcesInited = true; }

with this code we are subclassing a classes from slick that will help us to separate your game in different states: one for menu, one for game, one for achievements, but this are examples.

initResources it's a utility method that load, using MarteEngine ResourceManager class, all your resources into memory, to be used after. For now we don't have resources, but soon we'll have something to put on screen, right?

World world = new World(0, container); world.add(new TextEntity(100, 100, null, "Hello World!")); addState(world);

with this code we are using a powerful mechanism from MarteEngine: Worlds and Entities. Worlds: are game states remember before? Game menu or game itsefl is a world. Worlds render and update all your entities, help you to remove when they are not so useful anymore and have many utilities methods. Entities: are your game objects. TextEntity is an example, but a monster, the hero, a wall are also entities. They can recieve input, be rendered on screen and updated. In this case, we are just defining an empty, general world and adding TextEntity (an entity that just show some text on screen), later we will use them for more complex duties.

**Distribution**

You have different ways to distribuite your game: as jar, applet or webstart. We decide to use webstart because is easy and fast to use for user and developer. For more information about webstart, take a look here:

[http://en.wikipedia.org/wiki/Java_Web_Start](http://en.wikipedia.org/wiki/Java_Web_Start)

First you need to build a script directory and create a manifest.txt file with this content:

Manifest-Version: 1.0

Created-By: MarteEngine

Main-Class: @package@.@class@

Class-Path: lib/slick.jar lib/lwjgl.jar lib/marteEnginev03-dev.jar

and create a template.jnpl file into script directory:

@title@ Gornova @description@

Using webstart as distribution platform ask you some stuff to: export your project as a jar, sign it using a valid certificate and build the jnpl file. I've developed an ant script to do this stuff for you:

You can select in Eclipse build.xml file and right click on run target: ant target take care to compile and run your code.

To build a webstart for your project just launch webstart target: your project will be compiled, archived as jar and signed. To be signed you must specify some information: in this example all be signed with "testtest" when and target ask to you, so be sure to change it when you will put on internet!

A target directory will be created with a webstart subdirectory into, with this content: - HelloWorld.jar, jar with your project classes - HelloWorld.jnpl, java webstart file, to be used as local file (see above) - marteEnginev03-dev.jar, marteEngine directory double click on your HelloWorld.jnpl file and see webstart in action!

This kind of webstart must be used only offile, just for tests: to put it online, you must marteEnginev03-dev.jar file online at some http address and then change HelloWorld.jnpl here:

you must change jar href values, where your jars are placed. Then upload also your jnpl file online and your game will be ready to be used from anyone on internet! Note: you can also specify website, company information, name of jnpl file, just change variable values into build.xml file.

**Conclusion**

In this first tutorial we have setup our project and show a simple Hello World, prepare all for webstart distribution!

You can

[download eclipse project from here](http://jpacman.googlecode.com/files/marteEngineRLtutorial01.zip), good coding!

Which methons do you use to find data for your fresh articles, which particular search engines do you regularly turn to?

ReplyDelete