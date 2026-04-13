---
title: Marte Engine Graphic Rogue Like Tutorial 03
url: https://randomtower.blogspot.com/2012/03/marte-engine-graphic-rouge-like.html
author: Pubblicato da Marte
published: '2012-03-26'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Camera and random caves**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same series from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start! In this third tutorial we want to have camera, scrolling to explore a more vast caves and generate some random caves to explore!

**Camera**

Hero want to explore a big cave, but space on pc screen is limited, so we need a camera. First change GameWorld to add it and set following on hero:

package merlTut; import it.marteEngine.World; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.geom.Vector2f; import org.newdawn.slick.state.StateBasedGame; import org.newdawn.slick.util.Log; public class GameWorld extends World { private Hero hero; public GameWorld(int id, GameContainer container) { super(id, container); hero = new Hero(64, 64); add(hero); add(new Wall(128, 128)); add(new Wall(96, 128)); add(new Wall(64, 128)); this.setCamera(new Camera(this, hero, container.getWidth(), container.getHeight(),512,512,new Vector2f(32,32))); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)) { // goto menu world game.enterState(0); } } }

Run the game, you can see that now that camera follow player in his run!

**Random caves**

We want to have a brave hero into some caves, but what is better than some random caves? As mentioned into

[Trystan blog](http://trystans.blogspot.com/2011/08/roguelike-tutorial-03-scrolling-through.html)it's better to organize your code to handle this. First of all we need to delete Wall class and then add a Tile class, to keep track of all types of tiles in our game:

package merlTut; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class Tile extends Entity { private static final int tileSize = 8; private static final int scaleFactor = 4; public static final String WALL = "wall"; public static final String FLOOR = "floor"; public static final String BOUNDS = "bounds"; public Tile(float x, float y, String type, boolean collidable, int sheetx,int sheety) { super(x, y); setGraphic(ResourceManager.getSpriteSheet("env").getSubImage(sheetx, sheety).getScaledCopy(scaleFactor)); if (collidable) { collidable = true; setHitBox(0, 0, tileSize*scaleFactor, tileSize*scaleFactor); addType(SOLID); } else { collidable = false; addType(type); } } }

We keep it simple, just adding some information on constructor: if tile is collidable (floor is not collidable!) and what are coordinates into spritesheet. First we create a Level:

package merlTut; import java.util.ArrayList; import java.util.List; import it.marteEngine.entity.Entity; public class Level { private static final int tileSize = 8; private static final int scaleFactor = 4; public int width; public int height; public String[][] tiles; public Level(String[][] tiles) { this.tiles = tiles; this.width = tiles.length; this.height = tiles[0].length; } private Entity convert(String tile, int x, int y) { if (tile.equalsIgnoreCase("wall")) { return new Tile(x * tileSize*scaleFactor, y * tileSize*scaleFactor, tile, true, 0, 2); } if (tile.equalsIgnoreCase("floor")) { return new Tile(x * tileSize *scaleFactor, y * tileSize*scaleFactor, tile, false, 0, 5); } return null; } public ListgetEntities() { List result = new ArrayList (); for (int x = 0; x < width; x++) { for (int y = 0; y < height; y++) { result.add(convert(tiles[x][y], x, y)); } } return result; } }

as you can see a Level is just a matrix of strings: a level builder will take care of level creation. Level have also a nice getEntities method, to quick transform string matrix into entities, to be added later to gameWorld. So we create a nice class, LevelBuilder, to take care of level creation:

package merlTut; public class LevelBuilder { public int width; public int height; public String[][] tiles; public LevelBuilder(int width, int height) { this.width = width; this.height = height; this.tiles = new String[width][height]; } public Level build() { return new Level(tiles); } private LevelBuilder randomizeTiles() { for (int x = 0; x < width; x++) { for (int y = 0; y < height; y++) { tiles[x][y] = Math.random() < 0.5 ? Tile.FLOOR : Tile.WALL; } } return this; } private LevelBuilder smooth(int times) { String[][] tiles2 = new String[width][height]; for (int time = 0; time < times; time++) { for (int x = 0; x < width; x++) { for (int y = 0; y < height; y++) { int floors = 0; int rocks = 0; for (int ox = -1; ox < 2; ox++) { for (int oy = -1; oy < 2; oy++) { if (x + ox < 0 || x + ox <= width || y + oy < 0 || y + oy <= height) continue; if (tiles[x + ox][y + oy] == Tile.FLOOR) floors++; else rocks++; } } tiles2[x][y] = floors >= rocks ? Tile.FLOOR : Tile.WALL; } } tiles = tiles2; } return this; } public LevelBuilder makeCaves() { return randomizeTiles().smooth(8); } }

Here we follow Trystan's approach, but not adding bounds, because we take care of level limit adding a reference into hero for world:

public Hero(float x, float y, GameWorld gameWorld) { super(x, y); this.world = gameWorld; ..

and using it in updateMovements method:

private void updateMovements() { if (collide(SOLID, x, y - step) == null && pressed(UP) && y- step >=0) { move(0, -1); } else if (collide(SOLID, x, y + step) == null && pressed(DOWN) && y+step < world.height ) { move(0, 1); } else if (collide(SOLID, x + step, y) == null && pressed(RIGHT) && x+step < world.width ) { move(1, 0); } else if (collide(SOLID, x - step, y) == null && pressed(LEFT) && x - step >= 0) { move(-1, 0); } }

In the end we need to getEntities from LevelBuilder and add to GameWorld:

package merlTut; import it.marteEngine.Camera; import it.marteEngine.World; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.geom.Vector2f; import org.newdawn.slick.state.StateBasedGame; public class GameWorld extends World { private Hero hero; private int tileWidth = 40; private int tileHeight= 30; private static final int tileSize = 8; private static final int scaleFactor = 4; public GameWorld(int id, GameContainer container) { super(id, container); hero = new Hero(10*tileSize * scaleFactor, 7*tileSize*scaleFactor, this); this.setCamera(new Camera(this, hero, container.getWidth(), container.getHeight(),512,512,new Vector2f(32,32))); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)) { // goto menu world game.enterState(0); } } @Override public void enter(GameContainer container, StateBasedGame game) throws SlickException { clear(); addAll(new LevelBuilder(tileWidth, tileHeight).makeCaves().build().getEntities(), GAME); add(hero); setWidth(tileWidth*tileSize*scaleFactor); setHeight(tileHeight*tileSize*scaleFactor); } }

You can notice that Wall references are gone and that in constructor we just add hero reference. Enter method is a special method for MarteEngine world's: when we change from menuWorld from gameWorld responding to user input, we can have a full new random cave to explore, without restarting the game! Not for final game, but for debug-developing is perfect! Find a free place for Hero As you can notice, sometimes level generation create a cave with hero into a wall, this is not good! We can solve this, adding hero into Level an utility method to find a free place for our hero:

public Vector2f findFreePlace(){ for (int x = 0; x < width; x++) { for (int y = 0; y < height; y++) { if (tiles[x][y].equalsIgnoreCase(Tile.FLOOR)){ return new Vector2f(x,y); } } } return new Vector2f(); }

and then modify GameWorld for adding hero. First GameWorld constructor don't do nothing:

public GameWorld(int id, GameContainer container) { super(id, container); }adding stuff is all on enter method:

@Override public void enter(GameContainer container, StateBasedGame game) throws SlickException { // we destroy everything clear(); // add random generated cave Level level = new LevelBuilder(tileWidth, tileHeight).makeCaves().build(); addAll(level.getEntities(), GAME); // add hero hero = new Hero(0, 0, this); hero.setPosition(level.findFreePlace().scale(tileSize*scaleFactor)); add(hero); // setting camera: this.setCamera(new Camera(this, hero, container.getWidth(), container.getHeight(),512,512,new Vector2f(32,32))); setWidth(tileWidth*tileSize*scaleFactor); setHeight(tileHeight*tileSize*scaleFactor); }

So first of all we clear all entities from world, then call random generation of cave and finally add hero position and set camera on top of it.

![]() |

**Conclusion**

In this tutorial we have done many important steps! Now hero can explore a random generated cave and player can follow his movements using game camera.

You can

[found here eclipse project](http://jpacman.googlecode.com/files/marteEngineRLtutorial03.zip)with source code.

I love you (not homo)

ReplyDelete