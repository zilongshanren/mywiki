---
title: Actionscript 3 load BitmapData
url: https://randomtower.blogspot.com/2010/03/actionscript-3-load-bitmapdata.html
author: Pubblicato da Marte
published: '2010-03-17'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

I've found this intersting

[page](http://readlist.com/lists/chattyfig.figleaf.com/flashcoders/1/9300.html)explain how to load an image (for example a PNG) into a BitmapData class (useful with

[Flashpunk](http://flashpunk.net/)too), i report here so anyone waste time anymore:


package

{

import flash.display.Bitmap;

import flash.display.BitmapData;

import flash.display.Sprite;


[SWF(width = "800", height = "600")]

public class Main extends Sprite

{


[Embed(source="test.png")]

public var MyEmbed:Class;


public function Main()

{

var bit:BitmapData = getBitmapData();

}

public function getBitmapData():BitmapData

{

var image:Bitmap = new MyEmbed();

return image.bitmapData;

}

}

}

You need a test.png, obviously :D you can found a little

[Flashdevelop working example here](http://jpacman.googlecode.com/files/TestEmbed.zip).

## No comments:

## Post a Comment