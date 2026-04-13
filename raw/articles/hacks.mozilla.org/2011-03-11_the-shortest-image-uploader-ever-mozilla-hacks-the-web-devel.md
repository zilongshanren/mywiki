---
title: The shortest image uploader – ever! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/03/the-shortest-image-uploader-ever/
author: Paul Rouget
published: '2011-03-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A couple of line of JavaScript. That’s all you need.

*This is a very short Image Uploader, based on imgur.com API. If you want to do more complex stuff (like resize, crop, drawing, colors, …) see my previous post.*

Back-story. I’ve been talking to [Imgur.com](http://imgur.com)‘s owner (Hi Alan!). He [recently added Drag’n Drop support](http://imgur.com/blog/2010/12/08/drag-and-dropload/) to his image sharing website. But also, Alan allows [Cross-Domain XMLHttpRequest](http://hacks.mozilla.org/2009/07/cross-site-xmlhttprequest-with-cors/) (thank you!). So basically, you can use his [API](http://api.imgur.com) to upload pictures to his website, from your HTML page, with no server side code involved – at all.

And here is an example of what you can do:

(see the full working code on [github](https://github.com/paulrouget/miniuploader/tree/gh-pages) – live version [there](http://paulrouget.github.com/miniuploader) )

(also, you’ll need to understand FormData, see [here](https://hacks.mozilla.org/2010/05/formdata-interface-coming-to-firefox/))

```
function upload(file) {
// file is from a tag or from Drag'n Drop
// Is the file an image?
if (!file || !file.type.match(/image.*/)) return;
// It is!
// Let's build a FormData object
var fd = new FormData();
fd.append("image", file); // Append the file
fd.append("key", "6528448c258cff474ca9701c5bab6927");
// Get your own key: http://api.imgur.com/
// Create the XHR (Cross-Domain XHR FTW!!!)
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://api.imgur.com/2/upload.json"); // Boooom!
xhr.onload = function() {
// Big win!
// The URL of the image is:
JSON.parse(xhr.responseText).upload.links.imgur_page;
}
// Ok, I don't handle the errors. An exercice for the reader.
// And now, we send the formdata
xhr.send(fd);
}
```

That’s all :)

Works on Chrome and Firefox 4 (**Edit:**) and Safari.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 18 comments

Tobias PlutatMarch 11th, 2011 at 04:30Robin BerjonMarch 11th, 2011 at 05:15Pedro AssunçãoMarch 11th, 2011 at 05:26gmoulinMarch 11th, 2011 at 06:11Álvaro G. VicarioMarch 11th, 2011 at 06:19rad_gMarch 11th, 2011 at 06:40Isuru NanayakkaraApril 5th, 2012 at 04:39Scott BakerMarch 11th, 2011 at 09:07Fahd AlwashmiMarch 11th, 2011 at 09:16Mark SmithMarch 11th, 2011 at 13:47Paul RougetMarch 14th, 2011 at 04:40johnMarch 11th, 2011 at 22:07Ward MuylaertMarch 14th, 2011 at 04:53voidmindMarch 14th, 2011 at 06:30johnMarch 14th, 2011 at 09:08TimJune 17th, 2011 at 10:13zeufJuly 19th, 2012 at 18:15Forrest O.September 26th, 2012 at 03:53