---
title: tar.js - tar files for the web.
url: https://enkimute.github.io/tar.js/
author: Enki's blog
published: '2017-04-04'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

GIT

![view on github](../../assets/cb9f317b98c6b74a.png)

# tar.js - tar files for the web.

Save on your connections when preloading lots of files with tar.js ..

tar.js loads a tarfile and exposes its files as Object URL’s. Downloading many small files can be a pain on your loading speeds - not anymore!

## Get tar.js

825 bytes - [https://enkimute.github.io/res/tar.min.js](https://enkimute.github.io/res/tar.min.js)

## How to use

```
<SCRIPT SRC="tar.min.js"></SCRIPT>
```


```
Tar('icons.tar',function(files){
for (var f in files) {
var i = new Image();
i.src = files[f];
document.body.appendChild(i);
};
});
```