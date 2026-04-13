---
title: 're:Creation week #5. Improved level format and saving system.'
url: https://eliasdaler.wordpress.com/2014/08/10/recreation-week-5/
published: '2014-08-10'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Previous weeks**:

[Week #0: Preparation](https://eliasdaler.wordpress.com/2014/07/07/week-0-preparation/%20)[Week #1: Things are getting bigger](https://eliasdaler.wordpress.com/2014/07/13/recreation-week-1/)[Week #2 and #3. AI stuff and vacation](https://eliasdaler.wordpress.com/2014/07/28/recreation-dev-log-week-2-and-3/)[Week #4. New graphics, chests, doors, screen transitions](https://eliasdaler.wordpress.com/2014/08/03/recreation-week-4/)

# Foreword

![](../../assets/fa5fa134389744bb.png)


Last week I’ve posted this screenshot of re:Creation to [/r/IndieGaming](http://www.reddit.com/r/IndieGaming/) to know what people think about new graphics. I expected 2 or 3 people tell me something like: *“it’s good, keep working”* or *“that’s bad, keep working”*. [The thread](http://www.reddit.com/r/IndieGaming/comments/2ci43t/recreation_got_new_graphics_what_do_you_think/) got lots of upvotes and comments and there was lots of constructive critique which I didn’t expect. Some people said the game looks really great. This was really awesome and now I know in which direction art style should be moving.

And here’s what I’ve been doing this week.


# Improved level format.

I talk a lot about Lua and how it helps me during development process, but I haven’t talked about how level system works. I use plain text for levels because loading from it is faster than getting values from scripts. There’s a lot information stored in file: tileset it uses, tile information ,information about objects on the level and some other things.

I’ve been storing objects like this:

OBJECTS BEGIN house_1,12,16 old_man,40,40 ... // etc OBJECTS END

This is was enough information, because I can create every object with just one line of code.

EntityManager::createEntity("old_man", 40, 40);

But I realized that I needed to store direction information for some entities so they can look in the direction I want when the level loads. I then started to store it like this:

old_man,40,40,Down

Some entities needed tags, so I can quickly access particular entity by the tag. I started to store ovjects like this:

old_man,40,40,Down,OLD_MAN

But some entities don’t have tags or direction, so there’s no need to store information about that. That format was also not very human readable. I had to memorize the order of information stored in string.

So I’ve decided I can do better. Now the object information is stored like this:

name=old_man,x=40,y=40,dir=Down,tag=OLD_MAN

A lot better! It’s now human readable and easier to parse and get information from it.

Parsing works like this:

- get line from file
- separate by ‘,’ and store each token in string array
- for each token, separate by ‘=’ and then if the first token is “name”, assign entity name to be the second token, else if the first token is “x” then … you get the idea.

# Saving system

This is where the things got a lot harder!

You see, it’s easy to save the game if the player can’t return to previous levels. You just save a current level info, some player stats and that’s all.

I’m developing the open-world game, so I have to save lots of information like NPCs player has talked with, quest status or chests which player opened. And I can’t modify scripts or level files.

What if the player completes one level and decides to save on the next level? How can the game get entity information from the previous level?

One solution is to save the game each time a player enters another level. But this is not a very good solution, because the player might want to play the level from the point he saved the game himself.

Here’s my solution *(if someone has better solution, please, tell about it in comments or e-mail me: eliasdaler@yandex.ru)*

First of all, I assign tags to important entities like chests, doors, triggers and npcs. Imagine that

**level1**has

**CHEST_HAMMER**and

**level2**has

**CHEST_SWORD**

I have a global world struct which has different

**std::map**s

*(in case you don’t know:*

**std::map**is like a dictionary, you can access different values by the key, which is a**std::string**in this case)std::map<std::string, ChestInfo> chests;

When you open a chest, this **std::map** is modified. When I save the information, I use Lua.

I create a Lua table using **LuaBridge**. It has this structure:

saveTable = { fileName = "level1", chests = { { tag = "CHEST_HAMMER", isOpened = true }, { tag = "CHEST_SWORD", isOpened = false } }, ... -- etc }

When the game loads a save file, chests **std::map** is filled with information about objects no matter if they’re on the level player has saved previously or not. If the player enters a next level, the game adds new values to the** std::map** using tags each “special” object has. If the entity tag starts with “**CHEST_**“, new value is added to *chests***std::map**, etc.

Imagine that player has completed **level1**, opened **CHEST_HAMMER,** went to** level2** and saved there. The **chests** table in script will have two values:** CHEST_HAMMER** and **CHEST_SWORD**

When the player loads the game again, information about chests and other entities loads from the save file. The * chests* map is filled with information about each chest on each level player had visited.

The game doesn’t have to load

**level1**to know that

**CHEST_HAMMER**exists and it has been opened. The game knows it from the save file! Player can save on

**level2**again and the game saves info about

**level1**entities too , because it has it from previously loaded save file.

It may sound easy now, but it almost took a week for me to figure out and implement. I hope someone finds it useful.

# Multi-line dialogues

Well, this was easy to implement, but the game looks even more complete now.

[http://gfycat.com/BrokenDecentAnnelid](http://gfycat.com/BrokenDecentAnnelid)

That’s all for this week. Thanks for reading! Follow me on twitter for new updates. **@EliasDaler**