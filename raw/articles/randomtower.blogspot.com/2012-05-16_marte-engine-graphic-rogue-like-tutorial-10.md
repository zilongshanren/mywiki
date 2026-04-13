---
title: Marte Engine Graphic Rogue Like Tutorial 10
url: https://randomtower.blogspot.com/2012/05/marte-engine-graphic-rogue-like_16.html
author: Pubblicato da Marte
published: '2012-05-16'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Items, inventory and inventory screen**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll add add items to our game and an interface, inventory screen, to organize and control them!

**Items**

First we need items to display so pick again from Oryx's objects and put reference into resource.xml:


Will start with a simple Item: potion, because heroes always want some when traveling in dark places! So define an Item class:

package merlTut; import it.marteEngine.ResourceManager; import it.marteEngine.entity.Entity; public class Item extends GameEntity { private static final int tileSize = 8; private static final int scaleFactor = 4; public static final String ITEM = "item"; public static final String POTION_RED = "red Potion"; public Item(float x, float y, String type, boolean collidable, int sheetx, int sheety) { super(x * tileSize * scaleFactor, y * tileSize * scaleFactor); setGraphic(ResourceManager.getSpriteSheet("obj") .getSubImage(sheetx, sheety).getScaledCopy(scaleFactor)); name = type; addType(type, ITEM); if (collidable) { setHitBox(0, 0, tileSize * scaleFactor, tileSize * scaleFactor); } else { collidable = false; } } @Override public void collisionResponse(Entity other) { if (other instanceof Hero) { Hero hero = (Hero)other; hero.pickup(this); } } public void use(Creature creature) { if (creature instanceof Hero) { if (isType(POTION_RED)){ creature.modifyHp(10); creature.notify("'%s' use '%s' + %s Hp", creature.name, name, "10"); world.remove(this); creature.inventory().remove(this); } } } }

Item is just a container of graphics and action: use method define for every types of items what they can do. For now our mighty red potion modify hero hp of 10, useful, right? Used potions is removed from inventory and then from world! Inventory Inventory is a new class of this tutorial, let's add it to the project:

package merlTut; import java.util.Iterator; import java.util.LinkedList; import java.util.List; public class Inventory implements Iterable- { private LinkedList
- items; private int max; public List
- getItems() { return items; } public Item get(int i) { return items.get(i); } public Inventory(int max){ this.max = max; items = new LinkedList
- (); } public void add(Item item){ if (!isFull()){ items.add(item); } } public void remove(Item item){ items.remove(item); } public boolean isFull(){ return items.size() >= max; } @Override public Iterator
- iterator() { return items.iterator(); } public int size() { return items.size(); } public void useItem(int itemNumber, Creature creature) { if (0 <= itemNumber && itemNumber < size()){ if (get(itemNumber)!=null){ get(itemNumber).use(creature); } } } public void remove(int itemNumber) { if (itemNumber< size() && get(itemNumber)!=null){ items.remove(itemNumber); } } }

I used LinkedList because order matters (and because I don't like Trystan's arrays for items).

Inventory have a capacity and items don't stack: you can collect 20 potions and have no more space for nothing else! I like also idea to make Inventory Iteratable for Items, so I can use for each statement! ItemFactory I differ again from Trystan's approach: instead having one big factory for all, I want to specialize them: let's see ItemFactory!

package merlTut; public class ItemFactory { public ItemFactory(){ } public Item newPotionRed(){ Item item = new Item(0, 0, Item.POTION_RED, true, 12, 0); item.name = "Red Potion"; return item; } }

So create a new red potion it's three lines, useful, right? Now let's add it into GameWorld.newLevel:

// add some random items for (int i = 0; i < 20; i++) { addAtEmptyRandomLocation(itemFactory.newPotionRed()); }

Some potions to start with, screenshot time:

|

**Creatures wants an inventory**

Every creature will have an inventory (even Hero!), so start with Creature class:

package merlTut; import it.marteEngine.entity.Entity; public abstract class Creature extends GameEntity { public static final int scaleFactor = 4; public static final int tileSize = 8; public static final int step = tileSize * scaleFactor; private int attackValue; private CreatureAi creatureAi; private int defenseValue; public final String FUNGUS = "fungus"; public final String BAT = "bat"; private int hp; private int maxHp; public boolean moved = false; private int visionRadius; private Inventory inventory; public Creature(float x, float y, int maxHp, int attack, int defense, int visionRadius) { super(x, y); this.hp = maxHp; this.maxHp = maxHp; this.attackValue = attack; this.defenseValue = defense; this.visionRadius = visionRadius; this.inventory = new Inventory(20); } public void attack(Creature other) { int amount = Math.max(0, attackValue() - other.defenseValue()); amount = (int) (Math.random() * amount) + 1; other.modifyHp(-amount); notify(name + " attack the '%s' for %d damage.", other.name, amount); other.notify("The '%s' attacks you for %d damage.", name, amount); } public int attackValue() { return attackValue; } public boolean canSee(Entity creature) { return creatureAi.canSee((int) creature.x, (int) creature.y); } @Override public void collisionResponse(Entity other) { creatureAi.collide(other); } public int defenseValue() { return defenseValue; } public int hp() { return hp; } public int maxHp() { return maxHp; } public void modifyHp(int amount) { hp += amount; if (hp > maxHp){ hp = maxHp; } if (hp < 1) world.remove(this); } public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (cx >= 0 && cx < world.width && cy >= 0 && cy < world.height) { if (collide(new String[] { Tile.WALL, FUNGUS, Tile.STAIRS_UP, Tile.STAIRS_DOWN, BAT, Item.ITEM}, cx, cy) == null) { x = cx; y = cy; } } } public void notify(String message, Object... params) { creatureAi.onNotify(String.format(message, params)); } public Tile tile(int wx, int wy) { return ((GameWorld) world).tile(wx, wy); } public void setCreatureAi(CreatureAi ai) { this.creatureAi = ai; } public void updateAi() { creatureAi.update(); } public int visionRadius() { return visionRadius; } public Inventory inventory() { return inventory; } public void pickup(Item item){ if (inventory.isFull() || item == null){ notify("inventory full for '%s'",name); } else { notify("pickup a '%s'",item.name); world.remove(item); inventory.add(item); } } public void drop(Item item){ if (item!=null){ notify("drop at the ground a '%s'",item.name); inventory.remove(item); item.x = x; item.y = y; world.add(item); } } public void modifyAttackValue(int amount){ attackValue+=amount; } }

We also add some method useful for all creatures: drop, pickup, etc..

|

**Inventory screen**

In our rougelike inventory is not just a list, instead we can have some basic hud. For now all actions come from keyboard, so we need to keet this in mind. Plus we want to move all hud information into one single class, Hud. We'll move all messages and health information of our hero too:

package merlTut; import it.marteEngine.ResourceManager; import java.util.List; import org.newdawn.slick.Color; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Image; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.state.StateBasedGame; public class Hud { private Listmessages; private int clearMessagesTimer; private Hero hero; private int inventoryX; private int inventoryY; private GameContainer container; private Image slot; private Image goldSlot; private Image stat; public static boolean inventoryMode = false; public Hud(GameContainer container, List messages){ this.container = container; this.messages = messages; slot = ResourceManager.getSpriteSheet("gui").getSubImage(0,0); goldSlot = ResourceManager.getSpriteSheet("gui").getSubImage(1,0); stat = ResourceManager.getImage("stat"); } public void setHero(Hero hero){ this.hero = hero; } public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { // hero stats displayHp(container, g); // display messages displayMessages(container, g); // inventory if (inventoryMode){ renderInventory(container, g); g.drawImage(stat, 250,80); drawCentered(container, g, "HP " + hero.hp() + " / "+hero.maxHp(), 120); drawCentered(container, g, "Attack " + hero.attackValue(), 140); drawCentered(container, g, "Defense" + hero.defenseValue(), 160); } } public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { if (hero.moved) { clearMessagesTimer++; } } void drawCentered(GameContainer container, Graphics g, String text, int y) { g.drawString(text, container.getWidth() / 2 - text.length() * 4, y); } private void displayMessages(GameContainer container, Graphics g) { int bottom = container.getHeight() - 20; for (int i = 0; i < messages.size(); i++) { drawCentered(container, g, messages.get(i), bottom - i * 20); } if (messages.isEmpty()) { clearMessagesTimer = 0; } if (messages.size() > 3 || (clearMessagesTimer > 7 && !messages.isEmpty())) { clearMessagesTimer = 0; messages.remove(0); } } public void clear(Hero hero) { messages.clear(); clearMessagesTimer = 0; setHero(hero); } private void renderInventory(GameContainer container, Graphics g) { // draw inventory grid int x = 0; int y = 0; for (y=0 ; y < 2; y++){ for (x = 0; x < 10 ; x++){ g.drawImage(slot, 25 + x*60, 300 + y*60); } } y = 0; x = 0; int count = 0; // fill inventory grid for (Item item : hero.inventory()) { if (item!= null && item.getCurrentImage()!= null){ count++; g.drawImage(item.getCurrentImage(), 35 + x*60, 310 + y*60); x++; if (count >= 10 && y == 0){ y++; x=0; } } } // draw selected grid place by player g.drawImage(goldSlot, 25 + inventoryX*60, 300 + inventoryY*60); // display item type int itemNumber = inventoryX + inventoryY*10; if (itemNumber < hero.inventory().size() && hero.inventory().get(itemNumber)!=null){ drawCentered(container, g, hero.inventory().get(itemNumber).name, 250); } } private void displayHp(GameContainer container, Graphics g) { int total = hero.maxHp(); int current = hero.hp(); g.setColor(Color.red); if (total - current > 0) { g.fillRect(container.getWidth() - 40, 10 + total - current, 20, 10 + current); } else { g.fillRect(container.getWidth() - 40, 10, 20, 10 + current); } g.setColor(Color.gray); g.setLineWidth(10); g.drawRect(container.getWidth() - 40, 10, 20, 10 + total); g.setColor(Color.white); g.setLineWidth(1); } public void keyPressed(int key, char c) { if (key == Input.KEY_I){ inventoryMode = inventoryMode ? false: true; } if (inventoryMode){ if (key == Input.KEY_RIGHT){ inventoryX = inventoryX +1 >= 10 ? -1 : inventoryX; inventoryX = inventoryX +1 < 10 ? inventoryX+1 : inventoryX; } if (key == Input.KEY_LEFT){ inventoryX = inventoryX -1 < 0 ? 10 : inventoryX; inventoryX = inventoryX -1 >= 0 ? inventoryX-1 : inventoryX; } if (key == Input.KEY_UP){ inventoryY = inventoryY -1 >=0 ? inventoryY-1 : 1; } if (key == Input.KEY_DOWN){ inventoryY = inventoryY +1 <=1 ? inventoryY+1 : 0; } if (key == Input.KEY_SPACE){ int itemNumber = inventoryX + inventoryY*10; hero.inventory().useItem(itemNumber,hero); } if (key == Input.KEY_D){ int itemNumber = inventoryX + inventoryY*10; hero.drop(hero.inventory().get(itemNumber)); } if (key == Input.KEY_ESCAPE){ inventoryMode = false; } container.getInput().clearKeyPressedRecord(); container.getInput().consumeEvent(); } } }

|

As you can see, interface is ready to display! Just press I and player can navigate using arrows and then select a red potion and use it too:

|

Just remember to clear GameWorld too:

package merlTut; import it.marteEngine.Camera; import it.marteEngine.World; import it.marteEngine.entity.Entity; import java.util.ArrayList; import java.util.List; import org.newdawn.slick.GameContainer; import org.newdawn.slick.Graphics; import org.newdawn.slick.Input; import org.newdawn.slick.SlickException; import org.newdawn.slick.geom.Vector2f; import org.newdawn.slick.state.StateBasedGame; public class GameWorld extends World { public Hero hero; private int tileWidth = 40; private int tileHeight = 30; public Level level; private static final int tileSize = 8; private static final int scaleFactor = 4; private CreatureFactory creatureFactory; private ItemFactory itemFactory; public ListYou can see the trick? We are also adding new items: steel sword and gold key! See complete code of this tutorial for more informations!messages; public LevelBuilder levelBuilder; public int depth = 0; private boolean newLevel; private Hud hud; public GameWorld(int id, GameContainer container) { super(id, container); creatureFactory = new CreatureFactory(this); itemFactory = new ItemFactory(); messages = new ArrayList (); hud= new Hud(container,messages); } @Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); // depth indicator hud.drawCentered(container, g, "Level " + depth, 5); // render hud hud.render(container, game, g); } @Override public void update(GameContainer container, StateBasedGame game, int delta) throws SlickException { super.update(container, game, delta); Input input = container.getInput(); if (input.isKeyPressed(Input.KEY_ESCAPE)) { // goto menu world game.enterState(0); } hud.update(container, game, delta); if (hero.moved) { updateAi(); } if (newLevel) { newLevel = false; newLevel(); } } private void updateAi() { for (Entity ent : getEntities()) { if (ent instanceof Creature) { Creature creature = (Creature) ent; creature.updateAi(); } } } @Override public void enter(GameContainer container, StateBasedGame game) throws SlickException { newLevel(); } private void newLevel() { // we destroy everything clear(); // add random generated cave levelBuilder = new LevelBuilder(tileWidth, tileHeight).makeCaves() .addStairs(); level = levelBuilder.build(); addAll(level.getEntities(), GAME); // add some fungus at free random locations for (int i = 0; i < 8; i++) { addAtEmptyRandomLocation(creatureFactory.newFungus()); } //add some bats for (int i = 0; i < 15; i++) { addAtEmptyRandomLocation(creatureFactory.newBat()); } // add hero at first free place hero = creatureFactory.newHero(); addAtEmptyLocation(hero); // add some random items for (int i = 0; i < 20; i++) { addAtEmptyRandomLocation(itemFactory.newPotionRed()); } addAtEmptyRandomLocation(itemFactory.newGoldKey()); addAtEmptyRandomLocation(itemFactory.newSteelSword()); // setting camera: this.setCamera(new Camera(this, hero, container.getWidth(), container .getHeight(), 512, 512, new Vector2f(32, 32))); setWidth(tileWidth * tileSize * scaleFactor); setHeight(tileHeight * tileSize * scaleFactor); hud.clear(hero); } public void addAtEmptyRandomLocation(GameEntity entity) { int x; int y; do { x = (int) (Math.random() * tileWidth); y = (int) (Math.random() * tileHeight); } while (!levelBuilder.isFree(x, y)); entity.x = x * tileSize * scaleFactor; entity.y = y * tileSize * scaleFactor; add(entity); } public void addAtEmptyLocation(Creature creature) { Vector2f pos; do { pos = levelBuilder.findFreePlace(); } while (!levelBuilder.isFree((int) pos.x, (int) pos.y)); creature.x = pos.x * tileSize * scaleFactor; creature.y = pos.y * tileSize * scaleFactor; add(creature); } public void goDown() { depth++; newLevel = true; } public void goUp() { if (depth - 1 >= 0) { depth--; newLevel = true; } } public Tile tile(int wx, int wy) { for (Entity ent : getEntities()) { if (ent!=null && ent.x == wx && ent.y == wy){ if (ent instanceof Tile){ return (Tile) ent; } } } return new Tile(wx,wy, Tile.FLOOR, false, 0, 5); } public Item item(int wx, int wy) { for (Entity ent : getEntities()) { if (ent!=null && ent.x == wx && ent.y == wy){ if (ent instanceof Item){ return (Item) ent; } } } // TODO: pensare oggetto vuoto! return new Item(wx,wy, Tile.FLOOR, false, 0, 5); } @Override public void keyPressed(int key, char c) { hud.keyPressed(key, c); } }

**Conclusion**

Explain all work done in this tutorial is hard topic, but following simple steps is simple. We have defined first and item, then an inventory. So player interact with inventory using an inventory screen, defined into a Hud class.

You can

[download source code here](http://jpacman.googlecode.com/files/marteEngineRLtutorial10.zip).

## No comments:

## Post a Comment