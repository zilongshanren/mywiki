---
title: Web Font preloading for HTML5 games – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/06/webfont-preloading-for-html5-games/
author: Belén Albeza
published: '2016-06-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In game development there are two methods of **rendering text**: via *bitmap fonts* and *vector fonts*. Bitmap fonts are essentially a *sprite sheet* image that contains all the characters of a given font. The sprite sheet uses a regular font file (traditionally `.ttf`

). How does this apply to game development on the Web and HTML5 games?

You can use bitmap fonts as usual – they are just images, after all, and most HTML 5 game engines or libraries support them straight away. For vector font rendering, we can rely on any font that is accessible via CSS: this includes both system fonts already present in the player’s computer (like Arial or Times New Roman), or Web Fonts, which can be downloaded on the fly, if they are not already present in the system.

However, not all game engines or frameworks include mechanisms to load these fonts as regular assets –like images or audio files – and rely on them being present already. This can lead to quirks in which the game tries to render a text in a font that is not loaded yet… Instead, the player will get no text, or text rendered with an alternate or default font.

In this article we will explore some techniques for preloading Web Fonts into our games, and describe how to integrate them with a popular 2D game framework: [Phaser](http://phaser.io).

## How Web Font loading works

There are two ways of loading a Web Font: via CSS (using [@font-face](https://developer.mozilla.org/en/docs/Web/CSS/@font-face)) or via JavaScript (using the [Font Loading API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Font_Loading_API)). The CSS solution has been available for some time; while the JavaScript API is not widely adopted yet by browsers. If you want to release a game these days, we recommend the CSS method for its portability.

### Declaration with @font-face

This is simply a declaration in your CSS code that allows you to set up a font family and point to the places where it can be fetched. In this snippet we declare a font family named Amatica SC, and assume that we have a TTF file as an asset.

```
@font-face {
font-family: 'Amatica SC';
font-style: normal;
font-weight: 400;
src: local('Amatica SC'),
local('AmaticaSC-Regular'),
url(fonts/amaticasc-regular.ttf) format('truetype');
}
```


Note: In addition to pointing to specific files, we can also point to font names that might be installed in the user’s computer (in this case, Amatica SC or AmaticaSC-Regular).

### Actual loading

It’s important to remember that **declaring a font family via CSS does not load the font**! The font is loaded only when the browser detects for the first time that it’s going to be used.

This can cause a visual glitch: either the text is rendered with a default font and then changes to the Web Font (this is known as FOUT or Flash Of Unstyled Text); or the text isn’t rendered at all and remains invisible until the font becomes available. In websites this is usually not a big deal, but in games (Canvas/WebGL) **we don’t get the automatic browser re-rendering when the font is available**! So if we try to render the text and the font is not available, it *is* a big deal.

So we need to actually download the font before we try to use it in our game…

## How to force a Web Font download

### The CSS Font Loading API

The [JavaScript API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Font_Loading_API) does force a font to load. As of today, it only works on Firefox, Chrome, and Opera (you can check for the most up-to-date font-loading support information in [caniuse.com](http://caniuse.com/#feat=font-loading)).

Note that when using `FontFaceSet`

, you still need to declare your fonts somewhere –in this case, with `@font-face`

in the CSS.

### Typekit’s Web Font Loader

This is an open-source loader developed by TypeKit and Google – you can check out [the Web Font Loader repository in Github](https://github.com/typekit/webfontloader). It can load self-hosted fonts, as well as fonts from popular repositories like Typekit, Google Fonts, etc.

In the following snippet we will load Amatica SC directly from Google Fonts and specify a callback function – to render text in a 2D canvas– that will be invoked when the fonts are loaded and ready for use:

### FontFace Observer library

FontFace Observer is [another open-source loader](https://github.com/bramstein/fontfaceobserver) that doesn’t contain ad-hoc code for common font repositories. If you are self-hosting your fonts, this might be a better choice than Typekit’s since it is a lighter-weight file size.

This library uses a `Promise`

interface – but don’t worry, there’s a version with a polyfill if you need to support older browsers. Here again, you need to declare your fonts via CSS as well, so the library knows where to go to fetch them:

## Integrating font loading in Phaser

Now that we’ve seen how to load Web Fonts in HTML5, let’s discuss how to integrate these fonts with a game engine. The process will differ from one engine or framework to another. I have picked Phaser as an example, since it’s widely used for 2D game development. You can take a look at some online examples here:

And, of course, there is [the Github repository](https://github.com/mozdevs/webfont-preloading) with full source code, so you can take a closer look at what I’ve built.

Here’s how Phaser works: the game is divided in game states, each of which executes a sequence of phases. The most important phases are: `init`

, `preload`

, `create`

, `render`

, and `update`

. The preload phase is where we must load game assets like images, sounds, etc. but unfortunately Phaser’s Loader does not provide a method for font preloading.

There are several ways to bypass or work around this issue:

### Delaying font rendering

We can use the Font Loading API or a library to force a font download in the preload phase. However, this creates a problem. Phaser’s Loader doesn’t allow us to indicate it when all loading is completed. This means we can’t pause the Loader and prevent the preload phase from ending so that we can switch to create – this is where we would want to set up our game world.

A first approach would be to delay the text rendering until the font is loaded. After all, we have a callback available in the promise, right?

```
function preload() {
// load other assets here
// ...
let font = new FontFaceObserver('Amatica SC');
font.load().then(function () {
game.add.text(0, 0, 'Lorem ipsum', {
font: '12px Amatica SC',
fill: '#fff'
});
}
}
```


There is a problem with this approach: What happens if the callback is invoked before the `preload`

phase has ended? Our Phaser.Text object would then be wiped out once we switch to `create`

.

What we can do is guard the creation of the text under two flags: one that indicates that the font has loaded, and a second one that indicates that the create phase has started:

```
var fontLoaded = false;
var gameCreated = false;
function createText() {
if (!fontLoaded || !gameCreated) return;
game.add.text(0, 0, 'Lorem ipsum', {
font: '12px Amatica SC',
fill: '#fff'
});
}
function preload() {
let font = new FontFaceObserver('Amatica SC');
font.load().then(function () {
fontLoaded = true;
createText();
});
}
function create() {
gameCreated = true;
createText();
}
```


The main disadvantage of this method is that we completely ignore Phaser’s Loader. Since this doesn’t queue the font as an asset, the game will *start* and the fonts will not be there — this will probably cause a blinking effect or a glitch. Another problem is that the “Loading” screen or bar will ignore fonts, will display as if 100% loaded, and switch to the game even though our font assets still haven’t loaded.

### Using a custom loader

What if we could modify Phaser’s Loader and add it to whatever we need? We can! We can extend Phaser.Loader and add a method to the prototype that will queue an asset – a *web font*! The problem is that we need to modify one internal (meant for private use) Phaser.Loader method, `loadFile`

, so we can tell the Loader how to load the font, and when loading has been finished.

```
// We create our own custom loader class extending Phaser.Loader.
// This new loader will support web fonts
function CustomLoader(game) {
Phaser.Loader.call(this, game);
}
CustomLoader.prototype = Object.create(Phaser.Loader.prototype);
CustomLoader.prototype.constructor = CustomLoader;
// new method to load web fonts
// this follows the structure of all of the file assets loading methods
CustomLoader.prototype.webfont = function (key, fontName, overwrite) {
if (typeof overwrite === 'undefined') { overwrite = false; }
// here fontName will be stored in file's `url` property
// after being added to the file list
this.addToFileList('webfont', key, fontName);
return this;
};
CustomLoader.prototype.loadFile = function (file) {
Phaser.Loader.prototype.loadFile.call(this, file);
// we need to call asyncComplete once the file has loaded
if (file.type === 'webfont') {
var _this = this;
// note: file.url contains font name
var font = new FontFaceObserver(file.url);
font.load(null, 10000).then(function () {
_this.asyncComplete(file);
}, function () {
_this.asyncComplete(file, 'Error loading font ' + file.url);
});
}
};
```


Once this code is in place, we need to create an instance of it and swap it into `game.load`

. This swapping must take place as soon as possible: in the `init`

phase of the first game state executed.

```
function init() {
// swap Phaser.Loader for our custom one
game.load = new CustomLoader(game);
}
function preload() {
// now we can load our font like a normal asset
game.load.webfont('fancy', 'Amatica SC');
}
```


The advantage of this method is real integration with the loader, so if we have a loading bar it will not finish until the font has been completely downloaded (or timed out). The disadvantage, of course, is that we are overriding an internal method of Phaser, so we have no guarantee that our code will continue to work in future versions of the framework.

### A silly workaround…

A method that I have been using in game jams is to not start the game *at all* until I know that the font is ready. Since most browsers won’t render a text until the web font has been loaded, I just create a splash screen with a Play button that uses the web font… This way I know that the button will be visible once that font has loaded, so it’s safe to start the game then.

The obvious disadvantage is that we are not starting to load assets until the player presses that button… But it does work and it is very simple to implement. Here’s an screenshot example of one of these splash screens, created with regular HTML5 DOM elements and CSS animations:

![Screen Shot 2016-06-28 at 15.23.24](../../assets/b97770a3c8942535.png)


And there you have it, Web Font rendering in HTML5 games! In the future, once the Font Loading API is more mature, HTML5 game engines and frameworks will start to integrate it in their code, and hopefully we won’t have to do this ourselves or find a usable workaround.

Until then, happy coding! :)

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## One comment

CreativeSparkJuly 11th, 2016 at 14:07