---
title: Marte Engine Graphic Rogue Like Tutorial 11
url: https://randomtower.blogspot.com/2012/05/marte-engine-graphic-rogue-like_23.html
author: Pubblicato da Marte
published: '2012-05-23'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Hunger and food**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll add food and hunger mechanics to our rougelike! This tutorial is different from other parts. In particular follow on all

[points Trystan's tutorial](http://trystans.blogspot.it/2011/09/roguelike-tutorial-11-hunger-and-food.html), so let's start!

package merlTut; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class Item extends GameEntity { private static final int tileSize = 8; private static final int scaleFactor = 4; public static final String ITEM = "item"; public static final String POTION_RED = "red Potion"; public static final String GOLD_KEY = "gold Key"; public static final String STEEL_SWORD = "steel sword"; public static final String FOOD = "food"; private int foodValue; public Item(float x, float y, String type, boolean collidable, int sheetx, int sheety) { super(x * tileSize * scaleFactor, y * tileSize * scaleFactor); setGraphic(ResourceManager.getSpriteSheet("obj") .getSubImage(sheetx, sheety).getScaledCopy(scaleFactor)); name = type; addType(type, ITEM); if (collidable) { setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); } else { collidable = false; } } @Override public void collisionResponse(Entity other) { if (other instanceof Hero) { Hero hero = (Hero) other; hero.pickup(this); } } public void use(Creature creature) { if (creature instanceof Hero) { if (isType(POTION_RED)) { creature.modifyHp(10); creature.notify("'%s' use '%s' + %s Hp", creature.name, name, "10"); world.remove(this); creature.inventory().remove(this); } if (isType(STEEL_SWORD)) { creature.modifyAttackValue(5); creature.notify("'%s' equip a '%s' + %s atk", creature.name, name, "5"); world.remove(this); creature.inventory().remove(this); } if (isType(FOOD)) { creature.eat(this); creature.notify("'%s' eat '%s' +%s food", creature.name, name, foodValue()); } } } public int foodValue() { return foodValue; } public void modifyFoodValue(int amount) { foodValue += amount; } }

We have add food value and FOOD type to Items, so cretures can interact with it.. eating it! So modify Creature class:

package merlTut; import it.marteEngine.entity.Entity; public abstract class Creature extends GameEntity { public static final int scaleFactor = 4; public static final int tileSize = 8; public static final int step = tileSize * scaleFactor; private int attackValue; private CreatureAi creatureAi; private int defenseValue; public final String FUNGUS = "fungus"; public final String BAT = "bat"; private int hp; private int maxHp; public boolean moved = false; private int visionRadius; private Inventory inventory; private int maxFood; private int food; public Creature(float x, float y, int maxHp, int attack, int defense, int visionRadius) { super(x, y); this.hp = maxHp; this.maxHp = maxHp; this.attackValue = attack; this.defenseValue = defense; this.visionRadius = visionRadius; this.inventory = new Inventory(20); this.maxFood = 100; this.food = maxFood; } public void attack(Creature other) { int amount = Math.max(0, attackValue() - other.defenseValue()); amount = (int) (Math.random() * amount) + 1; other.modifyHp(-amount); notify(name + " attack the '%s' for %d damage.", other.name, amount); other.notify("The '%s' attacks you for %d damage.", name, amount); } public int attackValue() { return attackValue; } public boolean canSee(Entity creature) { return creatureAi.canSee((int) creature.x, (int) creature.y); } @Override public void collisionResponse(Entity other) { creatureAi.collide(other); } public int defenseValue() { return defenseValue; } public int hp() { return hp; } public int maxHp() { return maxHp; } public void modifyHp(int amount) { hp += amount; if (hp > maxHp) { hp = maxHp; } if (hp < 1) { leaveCorpse(); world.remove(this); } } public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (cx >= 0 && cx < world.width && cy >= 0 && cy < world.height) { if (collide(new String[] { Tile.WALL, FUNGUS, Tile.STAIRS_UP, Tile.STAIRS_DOWN, BAT, Item.ITEM }, cx, cy) == null) { x = cx; y = cy; } } } public void notify(String message, Object... params) { creatureAi.onNotify(String.format(message, params)); } public Tile tile(int wx, int wy) { return ((GameWorld) world).tile(wx, wy); } public void setCreatureAi(CreatureAi ai) { this.creatureAi = ai; } public void updateAi() { modifyFood(-1); creatureAi.update(); } public int visionRadius() { return visionRadius; } public Inventory inventory() { return inventory; } public void pickup(Item item) { if (inventory.isFull() || item == null) { notify("inventory full for '%s'", name); } else { notify("pickup a '%s'", item.name); world.remove(item); inventory.add(item); } } public void drop(Item item) { if (item != null) { notify("drop at the ground a '%s'", item.name); inventory.remove(item); item.x = x; item.y = y; world.add(item); } } public void modifyAttackValue(int amount) { attackValue += amount; } private void leaveCorpse() { Item corpse = new Item(x / (tileSize * scaleFactor), y / (tileSize * scaleFactor), Item.FOOD, true, 13, 1); corpse.modifyFoodValue(maxHp * 3); world.add(corpse); } public int food() { return food; } public int maxFood() { return maxFood; } public void modifyFood(int amount) { food += amount; if (food > maxFood) { food = maxFood; } else if (food < 1 && isPlayer()) { modifyHp(-1000); } } public boolean isPlayer(){ return this instanceof Hero ? true: false; } public void eat(Item item){ modifyFood(item.foodValue()); inventory.remove(item); } public void dig(Tile tile) { modifyFood(-5); tile.changeType(Tile.FLOOR); } }

Nothing new from Trystan's tutorial. We just add ability to every creature to interact with foods and more important on every update (move) of Creature and when Hero dig.. need of food go up! On Hero class we also add a message, becaus Hero can die:

@Override public void removedFromWorld() { notify("Hero died, press ESC to continue"); }

Hud have also to display food, so change render method:

public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { // hero stats displayHp(container, g); displayFood(container,g); // display messages displayMessages(container, g); // inventory if (inventoryMode){ renderInventory(container, g); g.drawImage(stat, 250,80); drawCentered(container, g, "HP " + hero.hp() + "/"+hero.maxHp(), 120); drawCentered(container, g, "Food " + hero.food() + "/"+hero.maxFood(), 140); drawCentered(container, g, "Attack " + hero.attackValue(), 160); drawCentered(container, g, "Defense" + hero.defenseValue(), 190); } }

and new display food bar, so player can see how much food have left Hero, before die in starvation!

private void displayFood(GameContainer container, Graphics g) { int total = hero.maxFood(); int current = hero.food(); g.setColor(Color.green); if (total - current > 0) { g.fillRect(container.getWidth() - 90, 10 + total - current, 20, 10 + current); } else { g.fillRect(container.getWidth() - 90, 10, 20, 10 + current); } g.setColor(Color.gray); g.setLineWidth(10); g.drawRect(container.getWidth() - 90, 10, 20, 10 + total); g.setColor(Color.white); g.setLineWidth(1); }

we make also on PlayerAi a little change:

public void collide(Entity other) { if (other instanceof Tile) { Tile tile = (Tile) other; if (tile.isDiggable()) { creature.dig(tile); } if (tile.isType(Tile.STAIRS_UP)){ ((GameWorld)creature.world).goUp(); } if (tile.isType(Tile.STAIRS_DOWN)){ ((GameWorld)creature.world).goDown(); } } }

to a creature can "dig" a tile more easily.

|

**Conclusion**

A quote from

[Trystan's tutorial](http://trystans.blogspot.it/2011/09/roguelike-tutorial-11-hunger-and-food.html)can help to understand why I want this kind of feature in my game:

*"It's a subtle effect but it gives the player a decision to make when full and carrying a lot of food and under the right circumstances overeating may become a useful strategy."*

Now player not only go around, but pay his moves in terms of food. Find exit is more important: true heroes cannot die from starvation!

You can

[download source code from here](http://jpacman.googlecode.com/files/marteEngineRLtutorial11.zip).

## No comments:

## Post a Comment