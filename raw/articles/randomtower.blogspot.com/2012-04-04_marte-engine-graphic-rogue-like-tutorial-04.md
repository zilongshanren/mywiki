---
title: Marte Engine Graphic Rogue Like Tutorial 04
url: https://randomtower.blogspot.com/2012/04/marte-engine-graphic-rogue-like.html
author: Pubblicato da Marte
published: '2012-04-04'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Creature and CreatureAi, Hero and digging**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this fourth tutorial we will see how to organize your creatures (hero and enemies, and why not, allies too!) code in a nice way.

**First, some thoughts**

Organize your creature code is a matter of choices: no one could tell you "you are wrong here!", because you decide your scope and your idea of what a rougelike is. In our game we need to take care of many interactions between player and other creatures and (in future) objects. My choice is to follow Trystan's solution (adapted to MarteEngine characteristics) and build an abstract Creature class that extends MarteEngine's Entity and put in this superclass all utility code we need, for example collision detection (happens only when player move for now) and collision response. Again,

[Delegation Pattern](http://en.wikipedia.org/wiki/Delegation_pattern)seems right choice: have a CreatureAi abstract class and delegate to concrete class how to handle collision response.

In our case, when player move and collide with a wall, can dig it. It's seems over complicated for now, but think in great: different creatures with different types of response on hero actions or other creature's actions: mess this kind of logic with creature basic logic (loading sprite, render logic or update cycle from slick) not seems so good! Creature and CreatureAi As explained we follow Trystan's tutorial and add two abstract classes:

package merlTut; import it.marteEngine.entity.Entity; public abstract class Creature extends Entity { private CreatureAi creatureAi; public static final int tileSize = 8; public static final int scaleFactor = 4; public static final int step = tileSize * scaleFactor; public Creature(float x, float y) { super(x, y); } public void setCreatureAi(CreatureAi ai) { this.creatureAi = ai; } public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (collide(Tile.WALL, cx, cy) == null) { x = cx; y = cy; } } @Override public void collisionResponse(Entity other) { creatureAi.collide(other); } }

Creature will be extend by our hero later, but note two things: Creature take care to check on move collision with Walls and using collisionResponse callback method of MarteEngine, delegate response to CreatureAi implementation. So take a look to generic CreatureAi:

package merlTut; import it.marteEngine.entity.Entity; public abstract class CreatureAi { protected Creature creature; public CreatureAi(Creature creature){ this.creature = creature; this.creature.setCreatureAi(this); } public void collide(Entity other) { } }

Basic, right? Just a reference to creature ai is controlling and here our first Ai, PlayerAi:

package merlTut; import it.marteEngine.entity.Entity; public class PlayerAi extends CreatureAi { public PlayerAi(Creature creature) { super(creature); } public void collide(Entity other) { if (other instanceof Tile) { Tile tile = (Tile) other; if (tile.isDiggable()) { tile.changeType(Tile.FLOOR); } } } }

With this when there is a collision between hero and a Tile and this tile is diggable, we can change tile into a floor (diiig!). Tile Before see hero code, change of Tile class are required, just add this two methods:

public boolean isDiggable(){ if (isType(WALL)){ return true; } return false; } public void changeType(String type){ if (type!=null){ if (type.equalsIgnoreCase(FLOOR)){ clearTypes(); addType(FLOOR); collidable = false; setGraphic(ResourceManager.getSpriteSheet("env").getSubImage(0, 5).getScaledCopy(scaleFactor)); } } }

and the Hero Because we have a good organization of code before, change of Hero class involves extends Creature instead of Entity:

public class Hero extends Creature { change updateMovements method: private void updateMovements() { if (collide(SOLID, x, y - step) == null && pressed(UP) && y- step >=0) { move(0, -1); } else if (collide(SOLID, x, y + step) == null && pressed(DOWN) && y+step < world.height ) { move(0, 1); } else if (collide(SOLID, x + step, y) == null && pressed(RIGHT) && x+step < world.width ) { move(1, 0); } else if (collide(SOLID, x - step, y) == null && pressed(LEFT) && x - step >= 0) { move(-1, 0); } }

and remove move method (with already defined static vars on creature class).

**Conclusion**

In this tutorial we have defined a foundation for creatures ai code and collision responses and solved a problem on cave exploration: hero can be trapped inside caves with no exit!

As usual you can find

[source here](http://jpacman.googlecode.com/files/marteEngineRLtutorial04.zip).

## No comments:

## Post a Comment