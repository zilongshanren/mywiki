---
title: Marte Engine Graphic Rogue Like Tutorial 05
url: https://randomtower.blogspot.com/2012/04/marte-engine-graphic-rogue-like_11.html
author: Pubblicato da Marte
published: '2012-04-11'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Stationary monsters!**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll se how to create stationary monsters, basic type of monsters Fungus Let's create a new Creature, Fungus:

package merlTut; import it.marteEngine.ResourceManager; public class Fungus extends Creature { public Fungus(float x, float y) { super(x*tileSize*scaleFactor, y*tileSize*scaleFactor); setGraphic(ResourceManager.getSpriteSheet("env").getSubImage(12, 6).getScaledCopy(scaleFactor)); addType(FUNGUS); setHitBox(0, 0, tileSize*scaleFactor, tileSize*scaleFactor); } }

and don't forgot to add Creature Type FUNGUS con Creature class:

public final String FUNGUS = "fungus";

Add FungusAi, boring for now, I know that!

package merlTut; public class FungusAI extends CreatureAi { public FungusAI(Creature creature) { super(creature); } }

And add a CreatureFactory. A factory is a class that builds new classes so it's easy to add, in our case, creatures:

package merlTut; public class CreatureFactory { private GameWorld world; public CreatureFactory(GameWorld world){ this.world = world; } public Hero newHero(){ Hero hero = new Hero(0, 0, world); hero.setCreatureAi(new PlayerAi(hero)); return hero; } public Fungus newFungus(){ Fungus fungus = new Fungus(0, 0); fungus.setCreatureAi(new FungusAI(fungus)); return fungus; } }

We include two factory methods: Fungus and Hero. Notice that we don't set creature position, because we need some information about tiles for that. I've thought about this and Trystan's solution is simple enought to help us layer, so take a look to GameWorld constructor method:

private CreatureFactory creatureFactory; public GameWorld(int id, GameContainer container) { super(id, container); creatureFactory = new CreatureFactory(this); }

We add creatureFactory variable for GameWorld, so we can use it later on enter method:

@Override public void enter(GameContainer container, StateBasedGame game) throws SlickException { // we destroy everything clear(); // add random generated cave level = new LevelBuilder(tileWidth, tileHeight).makeCaves().build(); addAll(level.getEntities(), GAME); // add some fungus at free random locations for (int i = 0; i < 8; i++) { addAtEmptyRandomLocation(creatureFactory.newFungus()); } // add hero at first free place hero = creatureFactory.newHero(); addAtEmptyLocation(hero); // setting camera: this.setCamera(new Camera(this, hero, container.getWidth(), container.getHeight(),512,512,new Vector2f(32,32))); setWidth(tileWidth*tileSize*scaleFactor); setHeight(tileHeight*tileSize*scaleFactor); }

Using creature factory we can create creatures in one line and add into game at random or first free position, using this utility methods:

public void addAtEmptyRandomLocation(Creature creature){ int x; int y; do { x = (int)(Math.random() * tileWidth); y = (int)(Math.random() * tileHeight); } while (!level.isFree(x, y)); creature.x = x*tileSize*scaleFactor; creature.y =y*tileSize*scaleFactor; add(creature); } public void addAtEmptyLocation(Creature creature){ Vector2f pos ; do { pos =level.findFreePlace(); } while (!level.isFree((int)pos.x, (int)pos.y)); creature.x = pos.x*tileSize*scaleFactor; creature.y = pos.y*tileSize*scaleFactor; add(creature); }

|

**Killable fungus**

You can notice hero can stay on top of Fungus: we add capability to fungus to be killed, changing check of collision on Creature:

public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (collide(new String[]{Tile.WALL,FUNGUS}, cx, cy) == null) { x = cx; y = cy; } }

We check collision between moving Creature (in our case Hero) and WALL and FUNGUS. Collision is resolved into FungusAi, like for PlayerAi:

package merlTut; import it.marteEngine.entity.Entity; public class FungusAI extends CreatureAi { public FungusAI(Creature creature) { super(creature); } public void collide(Entity other) { if (other instanceof Hero) { creature.world.remove(creature); } } }

And so fungus are killable!

**FungusCraft!**

Trystan notice Fungus are pretty boring: static enemy don't nothing. But what if.. fungus spread around? First we need to add an update method on CretureAI:

package merlTut; import it.marteEngine.entity.Entity; public abstract class CreatureAi { protected Creature creature; public CreatureAi(Creature creature){ this.creature = creature; this.creature.setCreatureAi(this); } public void collide(Entity other) { } public void update( ){ } }

this method will be called when player moves, on every in-game creature. Again, this is our choice: we can think about a real-time rougelike or turnbased one: So ovveride it into FungusAi and define a spread method too:

@Override public void update() { if (spreadcount < 5 && Math.random() < 0.02) spread(); } private void spread() { int tx = (int) creature.x / (tileSize * scaleFactor); int ty = (int)creature.y / (tileSize * scaleFactor); int x = (int) (tx + (int) (Math.random() * 11) - 5); int y = (int) (ty + (int) (Math.random() * 11) - 5); if(!((GameWorld)creature.world).level.isFree(x, y)){ return; } spreadcount++; Creature child = factory.newFungus(); child.x = x * tileSize * scaleFactor; child.y = y * tileSize * scaleFactor; ((GameWorld)creature.world).add(child); }

A little change for Level.isFree(x,y) to take care of widht and height of the level:

public boolean isFree(int x, int y){ if (x>= 0 && y >= 0 && x < width && y < height && tiles[x][y].equalsIgnoreCase(Tile.FLOOR)){ return true; } return false; }

Again a change on Hero.updateMovements method:

private void updateMovements() {

if (pressed(UP) && y- step >=0) {

move(0, -1);

moved = true;

} else if (pressed(DOWN) && y+step < world.height ) {

move(0, 1);

moved = true;

} else if (pressed(RIGHT) && x+step < world.width ) {

move(1, 0);

moved = true;

} else if (pressed(LEFT) && x - step >= 0) {

move(-1, 0);

moved = true;

} else {

moved = false;

}

}

moved variable is true only when player order hero to move, so we can update all other creatures logic in GameWorld.update:

@Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)) { // goto menu world game.enterState(0); } if (hero.moved){ updateAi(); } } private void updateAi() { for (Entity ent : getEntities()) { if (ent instanceof Creature) { Creature creature = (Creature) ent; creature.updateAi(); } } }Because in MarteEngine's world we have tiles, creatures and other types of entities, we must update Ai for creature type only.

**Conclusion**

![]() |

With little effort we can add any type of creature using CreatureFactory and act like we want using CreatureAi implementations. Fungus spread is only an example of what we can do: for example now we can define Fungus with same graphics but with different behaviours, using different FungusAi implementations.

You can

[download source code here](http://jpacman.googlecode.com/files/marteEngineRLtutorial05.zip).

## No comments:

## Post a Comment