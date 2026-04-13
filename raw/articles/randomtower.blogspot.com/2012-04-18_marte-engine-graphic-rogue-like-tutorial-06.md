---
title: Marte Engine Graphic Rogue Like Tutorial 06
url: https://randomtower.blogspot.com/2012/04/marte-engine-graphic-rogue-like_18.html
author: Pubblicato da Marte
published: '2012-04-18'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Hitpoints, combat, messages**

Welcome reader to this tutorial! I'll show you how to build a roguelike with MarteEngine. For more information about MarteEngine, please see

[http://github.com/Gornova/MarteEngine](http://github.com/Gornova/MarteEngine). This tutorial is inspired from same serie from

[Trystan](http://trystans.blogspot.com/)and follow the same organization, so let's start!

In this tutorial we'll se how to take care of combat and feedback for player Hitpoints I'm following Trystan's tutorial line to line for this topic: just add max hitpoints, current hitpoint and attack and defense to Creature class:

package merlTut; import it.marteEngine.entity.Entity; public abstract class Creature extends Entity { private CreatureAi creatureAi; public static final int tileSize = 8; public static final int scaleFactor = 4; public static final int step = tileSize * scaleFactor; public final String FUNGUS = "fungus"; public boolean moved = false; private int maxHp; public int maxHp() { return maxHp; } private int hp; public int hp() { return hp; } private int attackValue; public int attackValue() { return attackValue; } private int defenseValue; public int defenseValue() { return defenseValue; } public Creature(float x, float y, int maxHp, int attack, int defense) { super(x, y); this.maxHp = maxHp; this.attackValue = attack; this.defenseValue = defense; } public void setCreatureAi(CreatureAi ai) { this.creatureAi = ai; } public void move(int dx, int dy) { float cx = x + dx * step; float cy = y + dy * step; if (collide(new String[]{Tile.WALL,FUNGUS}, cx, cy) == null) { x = cx; y = cy; } } @Override public void collisionResponse(Entity other) { creatureAi.collide(other); } public void updateAi() { creatureAi.update(); } public void attack(Creature other){ int amount = Math.max(0, attackValue() - other.defenseValue()); amount = (int)(Math.random() * amount) + 1; other.modifyHp(-amount); } public void modifyHp(int amount) { hp += amount; if (hp < 1) world.remove(this); } }

You can notice that attacking another creature will be a simple formula. Involves just attackvalue - defense value, plus of course some random value. Display hero's hp Now every creature have hitpoints, but player care in particular of brave hero's one. So let's display them! Add into GameWorld.render:

@Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); // hero stats displayHp(container,g); } private void displayHp(GameContainer container, Graphics g) { int total = hero.maxHp(); int current = hero.hp(); g.setColor(Color.red); if (total - current > 0){ g.fillRect(container.getWidth()-40, 10+total-current, 20, 10+current); } else { g.fillRect(container.getWidth()-40, 10, 20, 10+current); } g.setColor(Color.gray); g.setLineWidth(10); g.drawRect(container.getWidth()-40, 10, 20, 10+total); g.setColor(Color.white); }

|

If you run the game, can see a basic health bar on right of the screen! Messages Put some messages on screen is easy, first add a notify method on Creature class:

public void notify(String message, Object ... params){ creatureAi.onNotify(String.format(message, params)); }

and on CreatureAi corresponding method too:

public void onNotify(String format) { }

So let's start from PlayerAi: add a list of messages to handle a reference of it:

package merlTut; import java.util.List; import it.marteEngine.entity.Entity; public class PlayerAi extends CreatureAi { private Listmessages; public PlayerAi(Creature creature, List messages) { super(creature); this.messages = messages; } public void collide(Entity other) { if (other instanceof Tile) { Tile tile = (Tile) other; if (tile.isDiggable()) { tile.changeType(Tile.FLOOR); } } } public void onNotify(String message){ messages.add(message); } }

and change CreatureFactory, adding reference of GameWorld messages:

public Hero newHero(){ Hero hero = new Hero(0, 0, world,100,20,5); hero.name = "Hero"; hero.setCreatureAi(new PlayerAi(hero, world.messages)); return hero; }

and finally add reference on GameWorld:

public Listmessages; public GameWorld(int id, GameContainer container) { super(id, container); creatureFactory = new CreatureFactory(this); messages = new ArrayList (); }

Now it's time to display messages in GameWorld:

@Override public void render(GameContainer container, StateBasedGame game, Graphics g) throws SlickException { super.render(container, game, g); g.drawString("Game", 5, 5); // hero stats displayHp(container,g); // display messages displayMessages(container,g); }

using this utility methods:

private void displayMessages(GameContainer container, Graphics g) { int bottom = container.getHeight() -20; for (int i = 0; i < messages.size(); i++){ drawCentered(container, g,messages.get(i),bottom - i*20 ); } if (messages.isEmpty()){ clearMessagesTimer = 0; } if (messages.size() > 5 || (clearMessagesTimer > 7 && !messages.isEmpty())){ clearMessagesTimer = 0; messages.remove(0); } } private void drawCentered(GameContainer container, Graphics g, String text, int y){ g.drawString(text, container.getWidth()/2 -text.length()*4, y); }

Remember to cleare messages onEnter gameWorld adding this lines of code:

messages.clear(); clearMessagesTimer= 0;

Now don't forget to add some messages, for example of combat on creature attack method:

public void attack(Creature other){ int amount = Math.max(0, attackValue() - other.defenseValue()); amount = (int)(Math.random() * amount) + 1; other.modifyHp(-amount); notify(name+" attack the '%s' for %d damage.", other.name, amount); other.notify("The '%s' attacks you for %d damage.", name, amount); }

Note: I've tried to add some messages when Fungus spread, but is not so useful or after a bit so boring that I wipe out. But is possibile add messages from every creature!

**Conclusion**

|

In this tutorial we have done a little Gui for your player: now game display hero hp and some messages from combat, useful to understand what's going on!

As usual you can find source

[code here](http://jpacman.googlecode.com/files/marteEngineRLtutorial06.zip).

## No comments:

## Post a Comment