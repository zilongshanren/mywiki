---
title: 'cocos2d Book, Chapter 11: Isometric Tilemaps'
url: http://www.learn-cocos2d.com/2010/09/cocos2d-book-chapter-11-isometric-tilemaps/
author: Daniele Says
published: '2010-09-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 11 - Isometric Tilemaps

After Chapter 10 introduced Tiled and working with orthogonal tilemaps it’s time to step things up a notch and delve into isometric tilemaps. It starts with basic principles of isometric tilemaps and editing before going into detail on what’s different code-wise compared to orthogonal tilemaps. Obviously this has to include how to determine which isometric tile was touched and how to move a character across an isometric tilemap.

### Summary of working on Chapter 10 - Working with Tilemaps

This chapter introduces you to tilemaps, what they are and what benefits and tradeoffs they provide. Without a doubt the most popular editor for tilemaps for use with cocos2d is the [Tiled Map Editor](http://www.mapeditor.org/). I explain how to use it over several pages before going into code and actually loading your first tilemap using cocos2d’s CCTMXTiledMap class.

Loading a tilemap is just half the story. You’ll also learn how to manipulate the tilemap layers and individual tiles, as well as scrolling the tilemap and centering the touched tile on screen. The code takes care that the tilemap is never scrolled outside its boundaries.![2010-09-06_15.25.13](../../../wordpress/wp-content/uploads/2010-09-06_15.25.13-300x156.png)


While working with the Object Layer feature of Tiled (CCTMXObjectGroup in cocos2d) I noticed it’ll be handy to display the rectangles on the screen. So you’ll also learn a little custom drawing using OpenGL ES respectively cocos2d’s wrapper functions in CCDrawPrimitives.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

31 december…….so far.![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


i will buy the book!

Hmmm … the goal is to have it out before Xmas. Amazon’s release date estimation may be a little off.

yes…but amazon need at least 10 days to sent in italy, so i really hope to have it about 31 Dic.

Really? That’s awful. I get my Amazon orders within 1-2 business days if it’s available.

You don’t happen to live on an island?![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I know some of the german north sea islands are exempt from Amazon’s express delivery (I guess they haven’t figured out how to do air drops directly onto your address) and generally take a couple days longer to deliver the order.

yes, really! amazon doesn’t exist in italy. Amazon consider shipment in italy too expensive\unreliable.

Now we can order ONLY books (from .co.uk or USA) with international ship.

Damn apress, still no new chapters added, I’m afraid we won’t get more till book is released.

So much for preordering![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


I’m told they will be made available after they have been given editorial signoff. The first five chapters were published as is, eg. first drafts. That’s why it’s taking so long to publish the next chapters.

I just checked and chapters 5 & 6 are now ready for my final review, I’ll do that over the weekend and hopefully chapter 6 will be signed off soon.

Hi. I bought your book and am enjoying working through it. Nice work.

How does one scroll in a new tilemap? The max size is 2048×2048. What if one wants to bring in a new map when e.g. player starts reaching the upper map.y and I want to start scrolling in another tilemap. Do I just set the self.theMap = [CCTMXTiledMap tiledMapWithTMXFile:@”nextMap.tmx”]; ? If so where is this set. Im really confused with this and would appreciate the help.

Thanks.

That’s going to be difficult, usually what most games do in such a case is to load the next level (eg new scene loading a different tilemap).

I’m not sure if you can create a seamless world. Theoretically you could create another TMXTiledMap with another map and position it so that it is adjacent to the existing map, but you’d be having two maps in memory at once plus the additional overhead of moving both at the same time and the additional code that determines when a new map should be loaded. I’m not saying it can’t be done but it’s going to be challenging at least.

Damn, thats bad news. Ok thanks. Would it be a good idea game wise to use the maximum size of the tilemap(when the play reaches the top of the tilemap) to create some kind of checkpoint illusion and load up the next map using some animation trick to make it appear seamless? Maybe Tilemaps arent the way to go. How would you suggest this be done? The only reason I am using tilemaps is because I want to detect collision as well as mark tiles and spawnable space for enemy objects and tokens. What is another good way to detect these spaces(collision and spawn) on an environment which scrolls an area of around 35 iphone y axis(35×480) screens? Sorry for the heavy questions. Appreciate the help.

Tilemaps are certainly the easiest way to check the collisions since you’ll be working with just checking indices. For a free-roaming world without tiles you’d have to define collision areas, either rectangles or a position and a radius. And that isn’t too hard either, the problem here is more one of editing: there’s no such editor currently available that works with Cocos2D to do this. Tilemaps are still the way to go.

For switching to another level i’d use the good old trick of teleporters or cave entrances or whatever you want, then show an intermission screen. This could be a simple loading screen or something fancier like zooming in on the player, fading out the surrounding tiles, then loading the level and doing the same thing backwards. I suggest to start simple and just load a different map. You can polish the transitions near the end of the project, until then you have more important things to do, eg making the game fun to play. 😉

Ok thanks. Would one need to load a new stage or how would the environment be reset? Just reset the map object to the new tilemap and move the player to a location?

How does a game like Sonic handle this transition between areas? If they dont use a tile system, how are the areas set to be collidable in e.g. file game screens later. Scrolling through continuous game screens? Im confused to how objects, e.g. a platform is detected for collision using its coordinates when its view comes into place and its coords replace a previous images coords. (when no tiles are used.) I hope this makes sense 😉

First of all…great book…it’s the best of the bunch!, really helped to get me started and I’m using a lot of the ideas and samples as the basis for my first game.

But I have a problem…with retina display enabled, all the code for the isometric TMX gets screwed up (I have -hd versions of the TMX and the tiles png).

My issues are with the positioning functions. Can you details which are “point safe” and which ones will always use pixels. Do you have any hints for retina support with tilemaps? (setting a sprite to a tile location, working out the scroll position etc).

I’ve recoded some of the functions, but I’m having to put in a lot of “if (isRetina) {} else {}”… must be a better way (hopefully).

cheers

Moose

No need for any if (isRetina) etc… here is what I did, the problematic function in the book is floatingTilePosFromLocation… NOTE the only thing I added for retina is dividing the tile size by the content scale factor. That’s all ya need to do! (The tileSize is in pixels, not points)

-(CGPoint) floatingTilePosFromLocation:(CGPoint)location tileMap:(CCTMXTiledMap*)tileMap

{

// Tilemap position must be added as an offset, in case the tilemap position is not at 0,0 due to scrolling

CGPoint pos = ccpSub(location, tileMap.position);

//CGPoint pos = ccp(0,0);

float halfMapWidth = tileMap.mapSize.width * 0.5f;

float mapHeight = tileMap.mapSize.height;

float tileWidth = tileMap.tileSize.width / CC_CONTENT_SCALE_FACTOR();

float tileHeight = tileMap.tileSize.height / CC_CONTENT_SCALE_FACTOR();

CGPoint tilePosDiv = CGPointMake(pos.x / tileWidth, pos.y / tileHeight);

float mapHeightDiff = mapHeight - tilePosDiv.y;

// Cast to int makes sure that result is in whole numbers, tile coordinates will be used as array indices

float posX = (mapHeightDiff + tilePosDiv.x - halfMapWidth);

float posY = (mapHeightDiff - tilePosDiv.x + halfMapWidth);

return CGPointMake(posX, posY);

}

Thanks for that! I’ll update the code for the second revision of the book.

Thanks a bunch. This has been bugging be for few days.

I have searched and tried almost everything however I am still struck with my problem. Tile Maps have been discussed here extensively however I am not able to find my solution.

My TileMap (Cocos2D scene) is on top of a UIScroll View and its doesn’t cover the whole screen area. Its like Tap zoo, so I am able to fing tile position correctly when I click within the tile however when I touch outside the Map it still gives me wrong data (it gives me tile position that’s beneath that touch)..

I tried many things to check if the touch is atleast within the map but I am out of ideas now..(tried GID, tried making whole map collidable but nothing works till now![:(](../../../wordpress/wp-includes/images/smilies/frownie.png)


-(CGPoint) tilePosFromLocation:(CGPoint)location tileMap:(CCTMXTiledMap*)tileMap

{

// Tilemap position must be subtracted, in case the tilemap position is scrolling

CGPoint pos = ccpSub(location, tileMap.position);

float halfMapWidth = tileMap.mapSize.width * 0.5f;

float mapHeight = tileMap.mapSize.height;

float tileWidth = tileMap.tileSize.width;

float tileHeight = tileMap.tileSize.height;

CGPoint tilePosDiv = CGPointMake(pos.x / tileWidth, pos.y / tileHeight);

float inverseTileY = mapHeight - tilePosDiv.y;

// Cast to int makes sure that result is in whole numbers

float posX = (int)(inverseTileY + tilePosDiv.x - halfMapWidth);

float posY = (int)(inverseTileY - tilePosDiv.x + halfMapWidth);

// make sure coordinates are within isomap bounds

posX = MAX(0, posX);

posX = MIN(tileMap.mapSize.width - 1, posX);

posY = MAX(0, posY);

posY = MIN(tileMap.mapSize.height - 1, posY);

/*

if (posX < tileMap.mapSize.width && posY 0 && posY > 0)

{

printf(“Inside\n”);

}

else {

printf(“Outside\n”);

}

*/

return CGPointMake(posX, posY);

}

This is how I am trying to find if tile position but how do I check if the touch was within map or outside map? Any help will be highly appreciated.

Thanks.

I ran into this issue myself. The only solution I could come up with was to extend the map with “dummy” tiles instead of allowing the user to touch the space outside the tilemap. If I remember correctly this problem occurs only on two sides, where you would have negative tile coordinates.

I believe this is a deficiency of the tilemap implementation in Cocos2D. CCTMXLayer should correctly report invalid tile coordinates respectively allow the user to test for invalid coordinates.