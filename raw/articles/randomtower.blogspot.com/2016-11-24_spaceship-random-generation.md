---
title: Spaceship random generation
url: https://randomtower.blogspot.com/2016/11/spaceship-random-generation.html
author: Pubblicato da Marte
published: '2016-11-24'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

**Disclaimer**: a roguelike is a genre of games where characters are used for visual representation of game world. I've made few roguelike too:

[CryptoRL](http://randomtower.blogspot.it/2015/08/cryptorl-release-10_28.html)and

[CryptoRl2](http://randomtower.blogspot.it/2016/03/cryptorl-2-update-010.html).

### Spaceship generation

I'm working on a small prototype of spaceship room generator. What does it mean ?Imagine a spaceship like

[Enterprise](https://en.wikipedia.org/wiki/Starship_Enterprise)or

[Galactica](https://en.wikipedia.org/wiki/Battlestar_Galactica_(2004_TV_series)), from a top/down perspective. A spaceship is made of different kind of rooms types: engine room, dormitory room, armoury room and so on. It's like a dungeon in fantasy games, where every room can be used by crew for a specific need or function.

### Different kind of algorithms

There are a lot of different kind of algorithms out there, here some ideas:**: works fine for cave-based dungeons (I've used this for**

[Random walk](http://www.roguebasin.com/index.php?title=Random_Walk_Cave_Generation)[CryptoRL2](http://randomtower.blogspot.it/2016/03/cryptorl-2-update-010.html)), but not so cool for ships, because is too unpredictable and can create small corridors with awkward turns. I think is fine for cave dungeons, but need more work on it. Pure cellular automata feel, at least for me, like I'm missing something, some "crucial points"

**: like in**

[Grid based dungeon](http://www.roguebasin.com/index.php?title=Grid_Based_Dungeon_Generator)[Spelunky](http://www.spelunkyworld.com/)a dungeon is just a space divided using a grid (see

[here](http://tinysubversions.com/spelunkyGen/)and

[here](http://tinysubversions.com/spelunkyGen2/)for an introduction). On random generation, there is a random walk between "start cell" (decided from one side of the grid) and "end cell" (decided from opposite side of the grid). After that "rooms" will be placed on each cell of the grid, taken randomly from a "pool" of templates (based on a theme).

Results here is good and can be realized easily with an high degree of randomness. I think this method is more suited for a random ship-dungeon, because you can create rooms for basic system (engine, dormitory, engineering bay, escape pods, etc..) mixed with "special rooms" (captain room, stargate room, alien nest and so on) on a grid with a specific shape (square, rectangle, ellipse, with wings, Battlestar Galactica and so on) and iterate on it

**: place rooms randomly and connect them using corridors. I don't really like this way for my theme, what do you think about it?**

[Classic room/corridor](http://www.roguebasin.com/index.php?title=Dungeon-Building_Algorithm)**: I think with my theme is fine, but I need to use "square splitting" strategy and will be become like grid based dungeon, more or less.**

[Bsp](http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation)### Grid based random generation

My solution is based on grid based one, using following room types (remember, i'ts a roguelike!) as string:RANDOM_WALK = '#';

NONE = ' ';

EMPTY_ROOM = 'e';

ENGINE_ROOM = 'n';

LAB_ROOM = 'l';

DORMITORY_ROOM = 'd';

PRISON_ROOM = 'p';

ARMORY_ROOM = 'a';

FARM_ROOM = 'f';

STORAGE_ROOM = 's';

CORE_ROOM = 'c';

AI_ROOM = '!';

LANDING_BAY_ROOM = 'b';

INFIRMARY_ROOM = 'i';

HIBERNATION_ROOM = 'h';

CHAPEL_ROOM = '*';

AUDITORIUM_ROOM = 'u';

ROBOT_ROOM = 'r';


KEY = 'K';

DOOR = 'D';

I'm using also a template for ship generation, so every random generation will generate rooms inside that template (a 10x10 grid), where 'e' means that is possible to place a room type into that space:


ee

ee

eeee

eeeeee

ee ee

The proposed method divide the ship in three part: up (u), middle (m) and lower (l), in the following way:

uu

uu

mmmm

mmmmmm

ll ll

I'm using this information to place rooms, so for example engine rooms can be created only in the lower part or lab part only in the middle. Of course there are rooms that can be placed everywhere, like dormitory or storage room. Also following suggestion from this

[thread](http://forums.roguetemple.com/index.php?topic=5217.0)I'm using right/left symmetry for random generation, so with the same template and here a result:

f|and after filling right part with mirror information from the left one a random generated spaceship:

s|

dd||

psc|||

bs ||

ff

ss

dddd

psccsp

bs sb

With a little bit of legend can have more meaning:

f = farm

s = storage room

d = dormitory

p = prison room

c = core room

b = landing bay

As you can see in this example, this ship seems to be a merchant ship, with a lot of storage, a landing bay for small vessels run by from main spaceship to planet and a farm.. because you want to eat something into space, right ?

### Conclusion

I think I'm in the right way, using grid based placement, to create randomly spaceships, a perfect setting of a roguelike!

See you soon and feel free to comment if you want!

## No comments:

## Post a Comment