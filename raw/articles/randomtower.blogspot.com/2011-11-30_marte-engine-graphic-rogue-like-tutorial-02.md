---
title: Marte Engine Graphic Rogue Like Tutorial 02
url: https://randomtower.blogspot.com/2011/11/marte-engine-graphic-rouge-like_30.html
author: Pubblicato da Marte
published: '2011-11-30'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Resources, Menu and Game worlds, Hero and Walls**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from Trystan (

[http://trystans.blogspot.com/](http://trystans.blogspot.com/)) and follow the same organization, so let's start!

In this second tutorial we have in mind to show you how to load and use resources, setup a menu/game worlds, show brave hero moving into dungeons and controlling it using keyboard..

**Resources**

Rougelike we are building is not a text rougelike. Instead I've decided to use beautiful-retro Oryx tileset,

[http://forums.tigsource.com/index.php?topic=8970.0](http://forums.tigsource.com/index.php?topic=8970.0)and here

[http://www.oryxdesignlab.com/sprites/](http://www.oryxdesignlab.com/sprites/)

Why this choice?

Because I want a retro feel for this rougelike, but not so much retro! Please keep in mind that Oryx tilesets are licensed using

[Creative Commons non commercial](http://creativecommons.org/licenses/by-nc-nd/3.0/us/%20)means thanks Oryx, don't make money with it and no alter his work!

So let's download Oryx tileset from his site,

[here](http://www.oryxdesignlab.com/sprites/%20)We need for this tutorial two tileset: lofi_char.png and lofi_enviroment.png , just copy it into your data directory.

Now open data/resource.xml and change it as follow:

as mentioned into

[tutorial 01](http://randomtower.blogspot.com/2011/11/marte-engine-graphic-rouge-like.html), we will use MarteEngine resource manager to load our assets, in particular oryx tilesets. Note debug information when game runs:

*DEBUG:Trying to load spritesheet file 'lofi_char.png' with width 8 and height 8 without transparent color at key 'char'...*

*DEBUG:Trying to load spritesheet file 'lofi_environment.png' with width 8 and height 8 without transparent color at key 'env'...*

Means that tilesets are loaded correctly!

**Menu and Game worlds**

It's time to setup a decent menu/game transitions, so add a new Main.java file as follow;

package merlTut; import it.marteEngine.ResourceManager; import java.io.IOException; import org.newdawn.slick.AppGameContainer; import org.newdawn.slick.GameContainer; import org.newdawn.slick.SlickException; import org.newdawn.slick.state.StateBasedGame; import org.newdawn.slick.util.Log; public class Main extends StateBasedGame { private static boolean ressourcesInited; public Main(String title) { super(title); } @Override public void initStatesList(GameContainer container) throws SlickException { initResources(); // add worlds addState(new MenuWorld(0, container)); addState(new GameWorld(1, container)); } public static void initResources() throws SlickException { if (ressourcesInited) return; try { ResourceManager.loadResources("data/resources.xml"); } catch (IOException e) { Log.error("failed to load ressource file 'data/resources.xml': " + e.getMessage()); throw new SlickException("Resource loading failed!"); } ressourcesInited = true; } public static void main(String[] argv) { try { AppGameContainer container = new AppGameContainer(new Main( "Marte Engine Rouge Like Tutorial")); container.setDisplayMode(640, 480, false); container.setTargetFrameRate(60); container.start(); } catch (SlickException e) { e.printStackTrace(); } } }

Keep in mind that every world MUST have and unique Id, for example MenuWorld have id 0 and GameWorld 1. Also create GameWorld and MenuWorld:

package merlTut; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.state.StateBasedGame; import it.marteEngine.World; public class MenuWorld extends World { public MenuWorld(int id, GameContainer container) { super(id, container); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Menu, press space to play", 5, 5); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_SPACE)){ // goto game world game.enterState(1); } } } package merlTut; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.state.StateBasedGame; import it.marteEngine.World; public class GameWorld extends World { public GameWorld(int id, GameContainer container) { super(id, container); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)){ // goto menu world game.enterState(0); } } }

Run Main.java and notice that you can change two worlds using space and escape from your keyboard. Having two different worlds for menu and game helps you in organize your game and separate your code logic, again a good thing!

**Hero**

Hero is player avatar into game: as rougelike, is the most thing in game. So let's show it! First, decide what tile you want for your brave hero:

![]() |

Hero will be in your code as MarteEntine entity, so let's create it!

package merlTut; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class Hero extends Entity { public static final String HERO = "hero"; private static final String UP = "up"; private static final String DOWN = "down"; private static final String LEFT = "left"; private static final String RIGHT = "right"; private static final int tileSize = 8; private static final int scaleFactor = 4; private static final int step = tileSize * scaleFactor; public Hero(float x, float y) { super(x, y); setGraphic(ResourceManager.getSpriteSheet("char").getSubImage(1, 0).getScaledCopy(scaleFactor)); setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); addType(HERO); defineControls(); } private void defineControls() { define(UP, Input.KEY_W, Input.KEY_UP); define(DOWN, Input.KEY_S, Input.KEY_DOWN); define(LEFT, Input.KEY_A, Input.KEY_LEFT); define(RIGHT, Input.KEY_D, Input.KEY_RIGHT); } private void updateMovements() { if (pressed(UP)) { move(0, -1); } else if (pressed(DOWN)) { move(0, 1); } else if (pressed(RIGHT)) { move(1, 0); } else if (pressed(LEFT)) { move(-1, 0); } } private void move(int dx, int dy) { x += dx * step; y += dy * step; } @Override public void update(GameContainer container, int delta) throws SlickException { super.update(container, delta); updateMovements(); } }

There are some key points to understand here! First set orys's tile as graphics for your brave hero, with this code:

*setGraphic(ResourceManager.getSpriteSheet("char").getSubImage(1, 0).getScaledCopy(scaleFactor));*

here we are using ResouceManager to get char spriteseet and in particular one image. We scale it, to have a bigger image: for retro feel and to have something to see too.

*setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); addType(HERO);*

here we are defining some code for collisions: first hitbox around hero position and then adding type of this entity: HERO of course, so will be more easy to check collisions against it later.

private void defineControls() { define(UP, Input.KEY_W, Input.KEY_UP); define(DOWN, Input.KEY_S, Input.KEY_DOWN); define(LEFT, Input.KEY_A, Input.KEY_LEFT); define(RIGHT, Input.KEY_D, Input.KEY_RIGHT); } //then we define controls: using arrows and WASD to move brave hero! private void updateMovements() { if (pressed(UP)) { move(0, -1); } else if (pressed(DOWN)) { move(0, 1); } else if (pressed(RIGHT)) { move(1, 0); } else if (pressed(LEFT)) { move(-1, 0); } } private void move(int dx, int dy) { x += dx * step; y += dy * step; } @Override public void update(GameContainer container, int delta) throws SlickException { super.update(container, delta); updateMovements(); }

And update logic, of course: every entities are updated from his world and for Hero we update movements, control if movements keys are pressed and move hero according to it (remember: origin of screen is on top left or your screen!).

Move itself is trivial: just change coordinates of entity using directions and step. Note that step is decided as tileset size (8 pixels) multiply for scalefactor (4): this means that every step of our hero mean 32 pixels on screen!

Just don't forget to add hero to gameWorld:

public GameWorld(int id, GameContainer container) { super(id, container); add(new Hero(64, 64)); }

Run Main and you can see on gameWorld a moving hero!

|

**Walls**

An alone hero in an empty world is not so exciting, so let's add some static walls. First define Wall class:

package merlTut; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class Wall extends Entity { private static final int tileSize = 8; private static final int scaleFactor = 4; public Wall(float x, float y) { super(x, y); setGraphic(ResourceManager.getSpriteSheet("env").getSubImage(0, 2).getScaledCopy(scaleFactor)); setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); addType(SOLID); } }

Note that Wall have a special collision type: SOLID. This means that we don't want that hero can pass it! And then adding some walls into GameWorld:

public GameWorld(int id, GameContainer container) { super(id, container); add(new Hero(64, 64)); add(new Wall(128,128)); add(new Wall(96,128)); add(new Wall(64,128)); }

Walls are in place, but if your run game, hero can pass it without stopping it! That's not possible! You have to check collisions between walls and player and most logic place is to handle it when player moves, on Hero.updateMovements method:

private void updateMovements() { if (collide(SOLID, x, y-step)==null && pressed(UP)) { move(0, -1); } else if (collide(SOLID, x, y+step)==null && pressed(DOWN)) { move(0, 1); } else if (collide(SOLID, x+step, y)==null && pressed(RIGHT)) { move(1, 0); } else if (collide(SOLID, x+step, y)==null && pressed(LEFT)) { move(-1, 0); } }

we use MarteEngine collide function to check if (when player move on a certain direction, making a step), there is a SOLID entity. If no SOLID entity is found, hero can move. Run example again: now player can't move inside walls, and this is good!

|

Note: if you define a debug key, using this code in Main.main method

public static void main(String[] argv) { try { ME.keyToggleDebug = Input.KEY_1;

using key "1" on keyboard you can see as red rectangles entities hitboxes:

useful when you develop your game, no?

**Conclusion**

In this second tutorial we have setup menu and game worlds, learned how to have a hero moving on screen and some walls to check collision against.

You can

[download eclipse project from here](http://jpacman.googlecode.com/files/marteEngineRLtutorial02.zip), good coding!

## No comments:

## Post a Comment