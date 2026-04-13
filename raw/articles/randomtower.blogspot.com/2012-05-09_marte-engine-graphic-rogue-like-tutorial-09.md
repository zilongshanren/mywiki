---
title: Marte Engine Graphic Rogue Like Tutorial 09
url: https://randomtower.blogspot.com/2012/05/marte-engine-graphic-rogue-like_09.html
author: Pubblicato da Marte
published: '2012-05-09'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Wandering monsters!**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll add more interesting type of monsters, wandering one!

**Bat**

First of all we need to define bat class:

package merlTut; import it.marteEngine.ResourceManager; public class Bat extends Creature { public Bat(float x, float y, int maxHp, int attack, int defense, int visionRadius) { super(x * tileSize * scaleFactor, y * tileSize * scaleFactor, maxHp, attack, defense, visionRadius); setGraphic(ResourceManager.getSpriteSheet("char").getSubImage(14, 12) .getScaledCopy(scaleFactor)); addType(BAT); setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); } }

Because we have already defined Creature class for Fungus, adding a new monster is not an hard task, just add new Creature type on Creature class:

public final String BAT = "bat";

and add a check on move method:

public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (cx >=0 && cx < world.width && cy > 0 && cy < world.height){ if (collide(new String[]{Tile.WALL,FUNGUS, Tile.STAIRS_UP, Tile.STAIRS_DOWN, BAT}, cx, cy) == null) { x = cx; y = cy; } } }

Bat is a wandering monsters so add a wander method on CreatureAi class:

public void wander(){ int mx = (int)(Math.random() * 3) - 1; int my = (int)(Math.random() * 3) - 1; creature.move(mx, my); }

Like for

[Trystan's tutorial](http://trystans.blogspot.com/2011/09/roguelike-tutorial-09-wandering.html)wander it's simple enough for our bat, so define a BatAi using wandering:

package merlTut; import it.marteEngine.entity.Entity; public class BatAi extends CreatureAi { private CreatureFactory factory; public BatAi(Creature creature, CreatureFactory factory) { super(creature); this.factory = factory; } @Override public void update(){ wander(); wander(); } @Override public void collide(Entity other) { if (other instanceof Hero) { Hero hero = (Hero)other; hero.attack(creature); } } }

**Adding bats to the game**

We add to Creature factory an utility method for bats:

public Bat newBat(){ Bat bat = new Bat(0, 0,10,0,0,0); bat.name = "Bat"; bat.setCreatureAi(new BatAi(bat,this)); return bat; }

and call it from GameWorld newLevel method:

private void newLevel() { // we destroy everything clear(); // add random generated cave levelBuilder = new LevelBuilder(tileWidth, tileHeight).makeCaves() .addStairs(); level = levelBuilder.build(); addAll(level.getEntities(), GAME); // add some fungus at free random locations for (int i = 0; i < 8; i++) { addAtEmptyRandomLocation(creatureFactory.newFungus()); } //add some bats for (int i = 0; i < 15; i++) { addAtEmptyRandomLocation(creatureFactory.newBat()); } // add hero at first free place hero = creatureFactory.newHero(); addAtEmptyLocation(hero); // setting camera: this.setCamera(new Camera(this, hero, container.getWidth(), container .getHeight(), 512, 512, new Vector2f(32, 32))); setWidth(tileWidth * tileSize * scaleFactor); setHeight(tileHeight * tileSize * scaleFactor); messages.clear(); clearMessagesTimer = 0; }Fifhteen bats is enough for now!

|

**Conclusion**

Adding new creatures is easy: decide image on spritesheet, define a new class, a new ai and using CreatureFactory we can add new bats in our dungeons!

You can download

[source code from here](http://jpacman.googlecode.com/files/marteEngineRLtutorial09.zip).

## No comments:

## Post a Comment