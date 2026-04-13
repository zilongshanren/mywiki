---
title: Marte Engine Graphic Rogue Like Tutorial 08
url: https://randomtower.blogspot.com/2012/05/marte-engine-graphic-rogue-like.html
author: Pubblicato da Marte
published: '2012-05-02'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Concept, Line, Field of view, Fog of war**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll explore how to use and handle line of sight and field of view, because our hero cannot see through walls!

**Concept**

To understand what we are doing, thing about what is around you. For every object or creature around you, you can draw an invisible line between your eyes and target. This is called Field of view: in reality you cannot see behind you without movement, but this is a videogame, so we can imagine that brave hero have legendary senses to "feel" positions of walls, creatures, object even behind him!

**Line**

We start to define a line, using

[Bresenham's Line algoritm](http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)and follow Trystan's implementation in Java:

package merlTut; import java.util.ArrayList; import java.util.Iterator; import java.util.List; import org.newdawn.slick.geom.Point; public class Line implements Iterable{ private List points; private int scaleFactor = 4; private int tileSize = 8; private int step = scaleFactor * tileSize; public List getPoints() { return points; } public Line(int x0, int y0, int x1, int y1) { points = new ArrayList (); int dx = Math.abs(x1 - x0); int dy = Math.abs(y1 - y0); int sx = x0 < x1 ? step : -step; int sy = y0 < y1 ? step : -step; int err = dx - dy; while (true) { points.add(new Point(x0, y0)); if (x0 == x1 && y0 == y1) break; int e2 = err * 2; if (e2 > -dx) { err -= dy; x0 += sx; } if (e2 < dx) { err += dx; y0 += sy; } } } @Override public Iterator iterator() { return points.iterator(); } }

As you can see Line it's only a collection of points, each one have a difference of a step. A step (1 in trystan's example, 32 in our example), is just consequence of what we are using. Because we

[decided](http://randomtower.blogspot.it/2011/11/marte-engine-graphic-rouge-like_30.html)to use oryx's tilesets with 8 pixel of sizes and scale them factor of 4, step is 8*4 =32. Simple enough, right?

**Tile**

We need to understand, before draw a line, if something will stop line of sight. We just add to Tile class this method:

public boolean isGround() { if (isType(FLOOR)){ return true; } return false; }

For now, everything stop line of sight, except Floor type. This is intuitive, but we can change that later. Little objects (gold?), will not stop line of sight of our hero!

**Creatures vision radius**

We need to add to creature vision radius property:

private int visionRadius; public int visionRadius() { return visionRadius; } public Creature(float x, float y, int maxHp, int attack, int defense, int visionRadius) { super(x, y); this.hp = maxHp; this.maxHp = maxHp; this.attackValue = attack; this.defenseValue = defense; this.visionRadius = visionRadius; }

and use implement this statistic into Hero and Fungus classes:

public Hero(float x, float y, GameWorld gameWorld, int maxHp, int attackValue, int defenseValue, int visionRadius) { super(x*tileSize*scaleFactor, y*tileSize*scaleFactor, maxHp, attackValue, defenseValue, visionRadius); ... public Fungus(float x, float y, int maxHp, int attackValue, int defenseValue, int visionRadius) { super(x * tileSize * scaleFactor, y * tileSize * scaleFactor, maxHp, attackValue, defenseValue, visionRadius);Of course we need to change CreatureFactory to set visionRadius:

package merlTut; public class CreatureFactory { private GameWorld world; public CreatureFactory(GameWorld world){ this.world = world; } public Hero newHero(){ Hero hero = new Hero(0, 0, world,100,20,5,7 * 32); hero.name = "Hero"; hero.setCreatureAi(new PlayerAi(hero, world.messages)); return hero; } public Fungus newFungus(){ Fungus fungus = new Fungus(0, 0,10,0,0,0); fungus.name = "Fungus"; fungus.setCreatureAi(new FungusAI(fungus,this)); return fungus; } }

I agree with Trystan's approach. If everything was set using constructor, adding new parameter rise new errors on Eclipse (or your IDE),

**BUT**help you in create an object (a creature in our case) without forgetting any crucial properties not set.

Having a such important value without using it is not so good, so add a canSee method on creature: public boolean canSee(Entity creature) { return creatureAi.canSee((int)creature.x, (int)creature.y); }

we delegate implementation to creatureAi, but instead to implement function in every CreatureAi (FungusAi, PlayerAi) we put this implementation directly into CreatureAi:

public boolean canSee(int wx, int wy) { if ((creature.x - wx) * (creature.x - wx) + (creature.y - wy) * (creature.y - wy) > creature.visionRadius() * creature.visionRadius()) return false; for (Point p : new Line((int)creature.x, (int)creature.y, wx, wy)) { if (creature.tile((int)p.getX(), (int)p.getY()).isGround() || p.getX() == wx && p.getY() == wy) continue; return false; } return true; }

I'm not sure this is the best idea, but later having in each ai implementation a useful method like this one will help creature's ai to make better decisions! Tile You can notice that there is an undefined method on creature: tile. We'll do it now!

public Tile tile(int wx, int wy) { return ((GameWorld)world).tile(wx, wy); }

Again we delegate to gameWorld to find right tile at given coordinate:

public Tile tile(int wx, int wy) { for (Entity ent : getEntities()) { if (ent!=null && ent.x == wx && ent.y == wy){ if (ent instanceof Tile){ return (Tile) ent; } } } return null; }

Code is self-explanatory: just check every entities that are on given coordinate and if is a tile, return it!

**Field of view**

Because all rendering logic is called into GameWorld.render method, we need to change it! Remember initial thoughts? World is rendered on screen only if hero can see it, so we need to check this. I've added a new function on GameWorld:

private void fieldOfView() { for (Entity ent : getEntities()) { if (!ent.equals(hero)|| (ent.name != null && ent.name.equalsIgnoreCase("hero"))){ if (hero.canSee(ent)){ ent.visible = true; } else { ent.visible = false; } } } }

The tricky part here is how MarteEngine render eneities: because every entity have a visible attribute, we can decide, BEFORE draw it, if hero see it (visibile= true) or not (visible = false). Later, in render method, we can call before fieldOfView and then super.render, so MarteEngine will draw for us all entities, according to camera and more important visibile attribute:

@Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { fieldOfView(); super.render(container, game, g); g.drawString("Game", 5, 5); // hero stats displayHp(container, g); // display messages displayMessages(container, g); // depth indicator drawCentered(container, g, "Level " + depth, 5); }

|

**Fog of War**

Hero and player too, have memory, so why not add of of war? For ones are not familiar with this concept, think about where you are. You always remember walls seen before, even if now are out of your sight, right? We can represent this on our little game using a simple trick: sign what tiles, creature (ours games objects) have seen before and then draw on top of it a transparent gray image. So first, of all, build a simple 32x32 gray transparent image (I've used Gimp), here my result:

![]() |

As mentioned in

[second tutorial](http://randomtower.blogspot.it/2011/11/marte-engine-graphic-rouge-like_30.html), with MarteEngine we need to map these resources using resources.xml file. For a single image you should add a line like this one:

We need a GameEntity to take care of this common logic between tiles and creatures, so we add it to our project:

package merlTut; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.SlickException; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class GameEntity extends Entity { private boolean saw = false; public GameEntity(float x, float y) { super(x, y); } @Override public void render(GameContainer container, Graphics g) throws SlickException { GameWorld gameWorld = (GameWorld) world; if (gameWorld.hero.canSee(this)) { saw = true; super.render(container, g); } else { if (saw && !(this instanceof Creature)) { super.render(container, g); g.drawImage(ResourceManager.getImage("box"), x, y); } } } }

Render method is simple enough: when hero can see other GameEntities, we remember this line of sight and after, when object is out of sight, we draw the box after GameObject image. Using this class we need to extend with Tile and Creature class from GameEntity:

public abstract class Creature extends GameEntity {

and

public class Tile extends GameEntity {

a simple change to add a useful feature for player

|

package merlTut; public class CreatureFactory { private GameWorld world; public CreatureFactory(GameWorld world){ this.world = world; } public Hero newHero(){ Hero hero = new Hero(0, 0, world,100,20,5,5 * 32); hero.name = "Hero"; hero.setCreatureAi(new PlayerAi(hero, world.messages)); return hero; } public Fungus newFungus(){ Fungus fungus = new Fungus(0, 0,10,0,0,0); fungus.name = "Fungus"; fungus.setCreatureAi(new FungusAI(fungus,this)); return fungus; } }

**Conclusion**

Using Bresenham's Line algoritm it's possible to have a simple field of view for our game, without pain. Again there are lot of choices to do here, with many tecniques (as Trystan

[suggests](http://roguebasin.roguelikedevelopment.org/index.php/Articles#Line_of_sight.2C_field_of_vision)).

And with a little effort have ready fog of war too!

You can download

[source code from here.](http://jpacman.googlecode.com/files/marteEngineRLtutorial08.zip)

## No comments:

## Post a Comment