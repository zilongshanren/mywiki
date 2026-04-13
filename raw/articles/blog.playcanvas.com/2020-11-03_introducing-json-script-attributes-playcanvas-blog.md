---
title: Introducing JSON Script Attributes | PlayCanvas Blog
url: https://blog.playcanvas.com/introducing-json-script-attributes
author: Steven Yau
published: '2020-11-03'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

![JSON Script Attributes Preview](../../assets/90f7947d73770093.jpg)


We have levelled up the Script Attributes that makes it much easier to organize and group related attributes together.

Using JSON, developers are able to define a schema for a data object that has multiple attributes and have them grouped together in the Inspector.

In the example below, we have created a JSON schema with the name ‘settings’ and has the attributes ‘gravity’, ‘startingHealth’ and ‘godMode’.

`GameManager.attributes.add('settings', {`

type: 'json',

schema: [{

name: 'gravity',

type: 'number',

default: -9.8

}, {

name: 'startingHealth',

type: 'number',

default: 20

}, {

name: 'godMode',

type: 'boolean',

default: false

}]

});



In the Inspector, the data object is shown as a collapsible section:

![Collapsible script settings](../../assets/ceb172530d629437.gif)


Even better, **these data objects can made into an array**! This is a huge improvement over having to organize multiple attribute arrays that was difficult to update and error prone to maintain.

Example JSON schema for an array of enemies:

`GameManager.attributes.add('enemies', {`

type: 'json',

schema: [{

name: 'health',

type: 'number',

default: 10

}, {

name: 'type',

type: 'number',

enum: [

{ 'Close Combat': 1 },

{ 'Range': 2 },

{ 'Both': 3 }

]

}, {

name: 'templateAsset',

type: 'asset',

assetType: 'template'

}],

array: true

});



Becomes the following in the inspector which is so much cleaner!

![Arrays of JSON objects](../../assets/1a31dcaeb980037d.png)


Read more in the [documentation](https://developer.playcanvas.com/user-manual/scripting/script-attributes/) and let us hear your feedback in the [forums](https://forum.playcanvas.com/)!