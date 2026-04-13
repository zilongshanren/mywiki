---
title: Artemis and niftyGui
url: https://randomtower.blogspot.com/2012/09/artemis-and-niftygui.html
author: Pubblicato da Marte
published: '2012-09-19'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

Artemis is a good Entity System Framework library that helps coding your games. Core concept here is "Entity", that is only a container for Components, that hold data. Adding Systems to the game, you can draw stuff on screen, move it and so on.

More info on

[Artemis web site](http://gamadu.com/artemis/)!

Nifty gui solves an old problem for Java game programmers: gui. You can define in an xml file your gui, or from Java code: the good thing here is you have decoupled from your game code gui management and this is really good.

For information see

[Nifty gui website](http://nifty-gui.lessvoid.com/)!

**My experiment**

In my experiment I've tried both Artemis and nifty-gui and results are good! My idea was to replicate my old

[You can't win](http://randomtower.blogspot.it/2009/09/you-cant-win-release.html)(I've wrote this game for

[Axiom contest](http://randomtower.blogspot.it/search/label/contest?updated-max=2010-12-14T22:26:00%2B01:00&max-results=20&start=20&by-date=false), build a entity component system for it, so is not my first time on this topic) with Artemis.

|

Writing a game with Artemis is simple, once you have understood the basic concept of entities and in particular of systems. You can write complex games and not force you in a rendering system, because you write rendering system!

This works perfectly with Nifty-Gui: just wrote a simple user interface (see screenshoot) and place into my code: here we are!

**Piece of code**

For example here a RenderingSystem of my experiment:

package it.artemis.hello.system; import it.artemis.hello.component.Transform; import it.artemis.hello.spatial.SpatialForm; import org.newdawn.slick.Color; import org.newdawn.slick.Graphics; import com.artemis.Aspect; import com.artemis.ComponentMapper; import com.artemis.Entity; import com.artemis.systems.EntityProcessingSystem; public class RenderSystem extends EntityProcessingSystem { private Graphics g; private ComponentMapperrenderMapper; private ComponentMapper trasformMapper; private boolean debug; @SuppressWarnings("unchecked") public RenderSystem(Graphics g, boolean debug) { super(Aspect.getAspectFor(SpatialForm.class, Transform.class)); this.g = g; this.debug = debug; } @Override public void initialize() { renderMapper = world.getMapper(SpatialForm.class); trasformMapper = world.getMapper(Transform.class); } @Override protected void process(Entity e) { Transform transform = trasformMapper.get(e); SpatialForm spatial = renderMapper.get(e); spatial.getSpatial().draw(transform.getX(), transform.getY()); if (debug) { g.setColor(Color.green); g.drawRect(transform.getX(), transform.getY(), spatial.getWidth(), spatial.getHeight()); g.setColor(Color.white); } } }

Nice, right? In this example I'm using SpatialForm (that hold entity image) and Transform (position, speed, rotation and so on) aspects and I'm using it in drawing of entities!

**Conclusions**

Experiment and investigations continues, but Artemis (in active development!) is a valid choice for any game developer and my suggestion is to have a decent gui written with nifty!

You can

[download source code from here](http://jpacman.googlecode.com/files/ArtemisNiftyShooter.zip)!

![]() |

## No comments:

## Post a Comment