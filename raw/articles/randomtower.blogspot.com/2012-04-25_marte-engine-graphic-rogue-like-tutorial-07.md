---
title: Marte Engine Graphic Rogue Like Tutorial 07
url: https://randomtower.blogspot.com/2012/04/marte-engine-graphic-rogue-like_25.html
author: Pubblicato da Marte
published: '2012-04-25'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**More levels**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine).

This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start! In this tutorial we'll se how to handle different levels.

**More Levels**

In our rougelike I'm changing a bit way Trystan's follow: instead adding regions and a full "world" generation, I'll be satisfied with a simple new level generation each time player reach a go down stairs. Again, this ia choice we can always change later and it will require a small bit of code! First we need to add stairs to tiles, adding types:

public static final String STAIRS_UP = "stairs_up"; public static final String STAIRS_DOWN = "stairs_down";

and placing it into LevelBuilder:

public LevelBuilder addStairsUp(){ start = findFreePlace(); tiles[(int)start.x][(int)start.y] = Tile.STAIRS_UP; return this; } public LevelBuilder addStairsDown(){ int x; int y; do { x = (int) (Math.random() * width); y = (int) (Math.random() * height); } while (!isFree(x, y) && Math.abs(x - start.x) > 10 && Math.abs(y-start.y) > 10); end = new Vector2f(x,y); tiles[(int)end.x][(int)end.y] = Tile.STAIRS_DOWN; return this; }Code here is simple: for up stairs, find first free place. Instead for down stairs find a free tile at least 10 tiles distant. As you can notice, I'm also moved findFreePlace and isFree methods from Level class to LevelBuilder, because I need them in level generation, not only on level handling. You need to change Level convert method, to take care of new tiles types:

public Entity convert(String tile, int x, int y) { if (tile.equalsIgnoreCase(Tile.WALL)) { return new Tile(x, y, tile, true, 0, 2); } if (tile.equalsIgnoreCase(Tile.FLOOR)) { return new Tile(x, y, tile, false, 0, 5); } if (tile.equalsIgnoreCase(Tile.STAIRS_UP)) { return new Tile(x, y, tile, true, 7, 0); } if (tile.equalsIgnoreCase(Tile.STAIRS_DOWN)) { return new Tile(x, y, tile, true, 8, 0); }

We need also to change Creature.move method:

public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (collide(new String[]{Tile.WALL,FUNGUS, Tile.STAIRS_UP, Tile.STAIRS_DOWN}, cx, cy) == null) { x = cx; y = cy; } }

So when a creature move, we check also stairs! Almost finished, we responde collision on PlayerAi collide method:

public void collide(Entity other) { if (other instanceof Tile) { Tile tile = (Tile) other; if (tile.isDiggable()) { tile.changeType(Tile.FLOOR); } if (tile.isType(Tile.STAIRS_UP)){ ((GameWorld)creature.world).goUp(); } if (tile.isType(Tile.STAIRS_DOWN)){ ((GameWorld)creature.world).goDown(); } } }

And of course change GameWorld class:

package merlTut; import it.marteEngine.Camera; import it.marteEngine.World; import it.marteEngine.entity.Entity; import java.util.ArrayList; import java.util.List; import org.newdawn.slick.Color; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.geom.Vector2f; import org.newdawn.slick.state.StateBasedGame; public class GameWorld extends World { private Hero hero; private int tileWidth = 40; private int tileHeight = 30; public Level level; private static final int tileSize = 8; private static final int scaleFactor = 4; private CreatureFactory creatureFactory; public Listmessages; private int clearMessagesTimer; public LevelBuilder levelBuilder; public int depth = 0; private boolean newLevel; public GameWorld(int id, GameContainer container) { super(id, container); creatureFactory = new CreatureFactory(this); messages = new ArrayList (); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); // hero stats displayHp(container, g); // display messages displayMessages(container, g); // depth indicator drawCentered(container, g, "Level " + depth, 5); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)) { // goto menu world game.enterState(0); } if (hero.moved) { clearMessagesTimer++; updateAi(); } if (newLevel) { newLevel = false; newLevel(); } } private void updateAi() { for (Entity ent : getEntities()) { if (ent instanceof Creature) { Creature creature = (Creature) ent; creature.updateAi(); } } } @Override public void enter(GameContainer container, StateBasedGame game) throws SlickException { newLevel(); } private void newLevel() { // we destroy everything clear(); // add random generated cave levelBuilder = new LevelBuilder(tileWidth, tileHeight).makeCaves() .addStairs(); level = levelBuilder.build(); addAll(level.getEntities(), GAME); // add some fungus at free random locations for (int i = 0; i < 8; i++) { addAtEmptyRandomLocation(creatureFactory.newFungus()); } // add hero at first free place hero = creatureFactory.newHero(); addAtEmptyLocation(hero); // setting camera: this.setCamera(new Camera(this, hero, container.getWidth(), container .getHeight(), 512, 512, new Vector2f(32, 32))); setWidth(tileWidth * tileSize * scaleFactor); setHeight(tileHeight * tileSize * scaleFactor); messages.clear(); clearMessagesTimer = 0; } public void addAtEmptyRandomLocation(Creature creature) { int x; int y; do { x = (int) (Math.random() * tileWidth); y = (int) (Math.random() * tileHeight); } while (!levelBuilder.isFree(x, y)); creature.x = x * tileSize * scaleFactor; creature.y = y * tileSize * scaleFactor; add(creature); } public void addAtEmptyLocation(Creature creature) { Vector2f pos; do { pos = levelBuilder.findFreePlace(); } while (!levelBuilder.isFree((int) pos.x, (int) pos.y)); creature.x = pos.x * tileSize * scaleFactor; creature.y = pos.y * tileSize * scaleFactor; add(creature); } private void displayMessages(GameContainer container, Graphics g) { int bottom = container.getHeight() - 20; for (int i = 0; i < messages.size(); i++) { drawCentered(container, g, messages.get(i), bottom - i * 20); } if (messages.isEmpty()) { clearMessagesTimer = 0; } if (messages.size() > 5 || (clearMessagesTimer > 7 && !messages.isEmpty())) { clearMessagesTimer = 0; messages.remove(0); } } private void drawCentered(GameContainer container, Graphics g, String text, int y) { g.drawString(text, container.getWidth() / 2 - text.length() * 4, y); } private void displayHp(GameContainer container, Graphics g) { int total = hero.maxHp(); int current = hero.hp(); g.setColor(Color.red); if (total - current > 0) { g.fillRect(container.getWidth() - 40, 10 + total - current, 20, 10 + current); } else { g.fillRect(container.getWidth() - 40, 10, 20, 10 + current); } g.setColor(Color.gray); g.setLineWidth(10); g.drawRect(container.getWidth() - 40, 10, 20, 10 + total); g.setColor(Color.white); g.setLineWidth(1); } public void goDown() { depth++; newLevel = true; } public void goUp() { if (depth - 1 >= 0) { depth--; newLevel = true; } } }

As you can read, we change a little the code, using depth variable to remember at what depth hero is and introducing a new method newLevel

|

**Conclusion**

In this tutorial we have seen how to generate a new level when player use stairs up and down, changing a little our code, but without many changes!

You can download source

[code from here](http://jpacman.googlecode.com/files/marteEngineRLtutorial07.zip).

## No comments:

## Post a Comment