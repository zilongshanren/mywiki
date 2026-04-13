---
title: Creating thumbnails with drag and drop and HTML5 canvas – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2012/02/creating-thumbnails-with-drag-and-drop-and-html5-canvas/
author: Chris Heilmann
published: '2012-02-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 Canvas is a very cool feature. Seemingly just an opportunity to paint inside the browser with a very low-level API you can use it to heavily convert and change image and video content in the document. Today, let’s take a quick look at how you can use Canvas and the FileReader API to create thumbnails from images dropped into a browser document.

The [final code is available on GitHub](https://github.com/codepo8/canvasthumber) and you can see an [online demo here](http://thewebrocks.com/demos/canvasthumber/). There is also a screencast available on YouTube:

## Step 1: Getting the files into the browser

The first step to resize images in the browser is to somehow get them. For this, we can just add an element in the page and assign drag and drop event handlers to it:

```
s.addEventListener( 'dragover', function ( evt ) {
evt.preventDefault();
}, false );
s.addEventListener( 'drop', getfiles, false );
```

Notice that we only prevent the default behaviour when we drag things over the element. This is to prevent the browser from just showing the images when we drag them in.

The `getfiles()`

function then does the hard work of reading all the files in and sending them on to the functions that do the resizing and image generation:

```
function getfiles( ev ) {
var files = ev.dataTransfer.files;
if ( files.length > 0 ) {
var i = files.length;
while ( i-- ) {
var file = files[ i ];
if ( file.type.indexOf( 'image' ) === -1 ) { continue; }
var reader = new FileReader();
reader.readAsDataURL( file );
reader.onload = function ( ev ) {
var img = new Image();
img.src = ev.target.result;
img.onload = function() {
imagetocanvas( this, thumbwidth, thumbheight, crop, background );
};
};
}
}
ev.preventDefault();
};
```

The `drop`

event gives us a property called `dataTransfer`

which contains a list of all the files that have been dropped. We make sure that there was at least one file in the drop and then iterate over them.

If the file type was not an image (or in other words the type property of the file does not contain the string “image”) we don’t do anything with the file and continue the loop.

If the file is an image we instantiate a new `FileReader`

and tell it to read the file as a Data URL. When the reader successfully loaded the file it fires its `onload`

handler.

In this handler we create a new image and set its `src`

attribute to the `result`

of the file transfer. We then send this image to the `imagetocanvas()`

function with the parameters to resize (in the demo these come from the form):

```
function imagetocanvas( img, thumbwidth, thumbheight, crop, background ) {
c.width = thumbwidth;
c.height = thumbheight;
var dimensions = resize( img.width, img.height, thumbwidth, thumbheight );
if ( crop ) {
c.width = dimensions.w;
c.height = dimensions.h;
dimensions.x = 0;
dimensions.y = 0;
}
if ( background !== 'transparent' ) {
cx.fillStyle = background;
cx.fillRect ( 0, 0, thumbwidth, thumbheight );
}
cx.drawImage(
img, dimensions.x, dimensions.y, dimensions.w, dimensions.h
);
addtothumbslist( jpeg, quality );
};
```

This function gets the desired thumbnail size and resizes the canvas to these dimensions. This has the added benefit of wiping the canvas so that no old image data would be added to our thumbnail. We then resize the image to fit into the thumbnail using a `resize()`

function. You can see for yourself what this one does in the source code, it just means the image gets resized to fit. The function returns an object with the width and the height of the new image and the x and y position where it should be positioned onto the canvas.

If we don’t want the full-size thumbnail but instead crop it we resize the canvas accordingly and reset x and y to 0.

If the user requested a background we fill the canvas with the colour. After that we put the image on the canvas with the x and y coordinates and the new width and height.

This takes care of creating a new thumbnail on the canvas, but we haven’t got it as an image in the document yet. To this end, we call `addtothumbslist()`

:

```
function addtothumbslist( jpeg, quality ) {
var thumb = new Image(),
url = jpeg ? c.toDataURL( 'image/jpeg' , quality ) : c.toDataURL();
thumb.src = url;
thumb.title = Math.round( url.length / 1000 * 100 ) / 100 + ' KB';
o.appendChild( thumb );
};
```

This one creates a new image and checks if the users wanted a JPG or PNG image to be created. PNG images tend to be better quality but also bigger in file size. If a JPG was requested we call the canvas’ `toDataURL()`

method with two parameters: the requested JPEG mime type and the quality of the image (ranging between 0 and 1 with 1 being best quality). If a PNG is wanted, we can just call `toDataURL()`

without any parameters as this is the default.

We set the `src`

of the image to the generated url string and add a title showing the size of the image in KB (rounded to two decimals). All that is left then is to add the thumb to the output element on the page.

That’s it, you can now drag and drop images into the browser to generate thumbnails. Right now, we can only save them one at a time (or if you have some download add-ons all at once). Would be fun to add [Zip.js](https://hacks.mozilla.org/gildas-lormeau.github.com/zip.js/) to the mix to offer them as a zip. I dare you! :)

More reading:

[Drag and Drop](https://developer.mozilla.org/en/DragDrop/Drag_and_Drop)on MDN[FileReader](https://developer.mozilla.org/en/DOM/FileReader)on MDN[Canvas](https://developer.mozilla.org/en/HTML/Canvas)on MDN

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 6 comments

Beben KobenFebruary 2nd, 2012 at 01:21AndreyFebruary 3rd, 2012 at 10:41mihaiMarch 9th, 2012 at 20:44RabinsXpMarch 26th, 2012 at 02:22JasonNovember 11th, 2012 at 13:43JasonNovember 12th, 2012 at 11:32