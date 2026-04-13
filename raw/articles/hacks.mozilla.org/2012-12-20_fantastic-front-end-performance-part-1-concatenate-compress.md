---
title: Fantastic front-end performance Part 1 – Concatenate, Compress & Cache – A
  Node.JS Holiday Season, part 4 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/fantastic-front-end-performance-part-1-concatenate-compress-cache-a-node-js-holiday-season-part-4/
author: Shane Tomlinson
published: '2012-12-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is episode 4, out of a total 12, in the

[A Node.JS Holiday Season series]from Mozilla’s Identity team. It’s the first post about how to achieve better front-end performance.

In this part of our “A Node.JS Holiday Season” series we’ll talk about front-end performance and introduce you to tools we’ve built and use in Mozilla to make the Persona front-end be as fast as possible.

We’ll talk about [connect-cachify](https://github.com/mozilla/connect-cachify/), a tool to automate some of the most important parts of front-end performance.

Before we do that, though, let’s recap quickly what we can do as developers to make our solutions run on the machines of our users as smooth as possible. If you already know all about performance optimisations, feel free to proceed to the end and see how connect-cachify helps automate some of the things you might do by hand right now.

## Three Cs of client side performance

The web is full of information related to performance best practices. While many advanced techniques exist to tweak every last millisecond from your site, three basic tools should form the foundation – concatenate, compress and cache.

## Concatenation

The goal of concatenation is to minimize the number of requests made to the server. Server requests are costly. The amount of time needed to establish an HTTP connection is sometimes more expensive than the amount of time necessary to transfer the data itself. Every request adds to the overhead that it takes to view your site and can be especially problematic on mobile devices where there is significant connection latency. Have you ever browsed to a shopping site on your mobile phone while connected to the Edge network and grimaced as each image loaded one by one? That is connection latency rearing its head.

[SPDY](http://en.wikipedia.org/wiki/SPDY) is a new protocol built on top of HTTP that aims to reduce page load time by combining resource requests into a single HTTP connection. Unfortunately, at the present time only recent versions of Firefox, Chrome and Opera support this new protocol.

Combining external resources wherever possible, though old fashioned, works across all browsers and does not degrade with the advent of SPDY. Tools exist to combine the three most common types of external resources – JavaScript, CSS and images.

### JavaScript & CSS

A site with more than one external JavaScript inclusion should consider combining the scripts into a single file for production. Browsers have traditionally blocked all other rendering while JavaScript is downloaded and processed. Since each requested JavaScript resource carries with it a certain amount of latency, the following is slower than it needs to be:

```
```

By combining four requests into one, the total amount of time the browser is blocked due to latency will be significantly reduced.

```
```

Working with combined JavaScript while still in development can be very difficult so concatenation is usually only done for a production site.

Like JavaScript, individual CSS files should be combined into a single resource for production. The process is the same.

### Images

Data URIs and image sprites are the two primary methods that exist to reduce the number of requested images.

#### data: URI

A data URI is a special form of a URL used to embed images directly into HTML or CSS. Data URIs can be used in either the src attribute of an img tag or as the url value of a background-image in CSS. Because embedded images are base64 encoded, they require more bytes but one less HTTP request than the original external binary image. If the included image is small, the increased byte size is usually more than offset by the reduction in the number of HTTP requests. Neither IE6 nor IE7 support data URIs so know your target audience before using them.

#### Image sprites

Image sprites are a great alternative whenever a data URI cannot be used. An image sprite is a collection of images combined into a single larger image. Once the images are combined, CSS is used to show only the relevant portion of the sprite. Many tools exist to create a sprite out of a collection of images.

A drawback to sprites comes in the form of maintenance. The addition, removal or modification of an image within the sprite requires a congruent change to the CSS.

[Sprite Cow](http://www.spritecow.com/) helps you get the background-position, width and height of sprites within a spritesheet as a nice bit of copyable css.

## Removing extra bytes – minification, optimization & compression

Combining resources to minimize the number of HTTP requests goes a long way to speeding up a site, but we can still do more. After combining resources, the number of bytes that are transferred to the user should be minimized. Minimizing bytes usually takes the form of minification, optimization and compression.

### JavaScript & CSS

JavaScript and CSS are text resources that can be effectively minified. Minification is a process that transforms the original text by eliminating anything that is irrelevant to the browser. Transformations to both JavaScript and CSS start with the removal of comments and extra whitespace. JavaScript minification is much more complex. Some minifiers perform transforms that replace multi-character variable names with a single character, remove language constructs that are not strictly necessary and even go so far as to replace entire statements with shorter equivalent statements.

[UglifyJS](https://github.com/mishoo/UglifyJS), [YUICompressor](http://developer.yahoo.com/yui/compressor/) and [Google Closure Compiler](https://developers.google.com/closure/compiler/) are three popular tools to minify JavaScript.

Two CSS minifiers include YUICompressor and [UglifyCSS](https://github.com/fmarcia/UglifyCSS).

### Images

Images frequently contain data that can be removed without affecting its visual quality. Removing these extra bytes is not difficult, but does require specialized image handling tools. Our own Francois Marier has written two blog posts on [working with PNGs](http://feeding.cloud.geek.nz/2011/12/optimising-png-files.html) and [with GIFs](http://feeding.cloud.geek.nz/2009/10/reducing-website-bandwidth-usage.html).

[Smush.it](http://www.smushit.com/ysmush.it/) from Yahoo! is an online optimization tool. [ImageOptim](http://imageoptim.com/) is an equivalent offline tool for OSX – simply drag and drop your images into the tool and it will reduce their size automatically. You don’t need to do anything – ImageOptim simply replaces the original files with the much smaller ones.

If a loss of visual quality is acceptable, re-compressing an image at a higher compression level is an option.

### The Server Can Help Too!

Even after combining and minifying resources, there is more. Almost all servers and browsers support [HTTP compression](http://en.wikipedia.org/wiki/HTTP_compression). The two most popular compression schemes are deflate and gzip. Both of these make use of efficient compression algorithms to reduce the number of bytes before they ever leave the server.

## Caching

Concatenation and compression help first time visitors to our sites. The third C, caching, helps visitors that return. A user who returns to our site should not have to re-download all of the resources again. HTTP provides two widely adopted mechanisms to make this happen, cache headers and ETags.

Cache headers come in two forms and are suitable for static resources that change infrequently, if ever. The two header options are `Expires`

and `Cache-Control: max-age`

. The `Expires`

header specifies the date after which the resource must be re-requested. `max-age`

specifies how many seconds the resource is valid for. If a resource has a cache header, the browser will only re-request that resource once the cache expiration date has passed.

An ETag is essentially a resource version tag that is used to validate whether the local version of a resource is the same as the server’s version. An ETag is suitable for dynamic content or content can change at any time. When a resource has an ETag, it says to the browser “Check the server to see if the version is the same, if it is, use the version you already have.” Because an ETag requires interaction with the server, it is not as efficient as a fully cached resource.

### Cache-busting

The advantage to using time/date based cache-control headers instead of ETags is that resources are only re-requested once the cache has expired. This is also its biggest drawback. What happens if a resource changes? The cache has to somehow be busted.

Cache-busting is usually done by adding a version number to the resource URL. Any change to a resources URL causes a cache-miss which in turn causes the resource to be re-downloaded.

For example if http://example.com/logo.png has a cache header set to expire in one year but the logo changes, users who have already downloaded the logo will only see the update a year from now. This can be fixed by adding some sort of version identifier to the URL.

```
http://example.com/v8125/logo.png
```

or

```
http://example.com/logo.png?v8125
```

When the logo is updated, a new version is used meaning the logo will be re-requested.

```
http://example.com/v8126/logo.png
```

or

```
http://example.com/logo.png?v8126
```

## Connect-cachify – A NodeJS library to serve concatenated and cached resources

[Connect-cachify](https://github.com/mozilla/connect-cachify/) is a NodeJS middleware developed by Mozilla that makes it easy to serve up properly concatenated and cached resources.

While in production mode, connect-cachify serves up pre-generated production resources with a cache expiration of one year. If not in production mode, individual development resources are served instead, making debugging easy. Connect-cachify does not perform concatenation and minification itself but instead relies on you to do this in your project’s build script.

Configuration of connect-cachify is done through the setup function. Setup takes two parameters, `assets`

and `options`

. `assets`

is a dictionary of production to development resources. Each production resource maps to a list its individual development resources.

`options`

is an optional dictionary that can take the following values:`prefix`

– String to prepend to the hash in links. (**Default: none**)`production`

– Boolean indicating whether to serve development or production resources. (**Defaults to true**)`root`

– The fully qualified path from which static resources are served. This is the same value that you’d send to the static middleware. (**Default: ‘.’**)

### Example of connect-cachify in action

First, let’s assume we have a simple HTML file we wish to use with connect-cachify. Our HTML file includes three CSS resources as well as three Javascript resources.

```
...
```Dashboard: Hamsters of North America
...
...

#### Set up the middleware

Next, include the connect-cachify library in your NodeJS server. Create your production to development resource map and configure the middleware.

```
...
// Include connect-cachify
const cachify = require('connect-cachify');
// Create a map of production to development resources
var assets = {
"/js/main.min.js": [
'/js/lib/jquery.js',
'/js/magick.js',
'/js/laughter.js'
],
"/css/dashboard.min.css": [
'/css/reset.css',
'/css/common.css',
'/css/dashboard.css'
]
};
// Hook up the connect-cachify middleware
app.use(cachify.setup(assets, {
root: __dirname,
production: your_config['use_minified_assets'],
}));
...
```

To keep code DRY, the asset map can be externalized into its own file and used as configuration to both connect-cachify and your build script.

#### Update your templates to use cachify

Finally, your templates must be updated to indicate where production JavaScript and CSS should be included. JavaScript is included using the “cachify_js” helper whereas CSS uses the “cachify_css” helper.

```
...
```Dashboard: Hamsters of North America
<%- cachify_css('/css/dashboard.min.css') %>
...
<%- cachify_js('/js/main.min.js') %>
...

#### Connect-cachified output

If the `production`

flag is set to false in the configuration options, connect-cachify will generate three link tags and three script tags, exactly as in the original. However, if the `production`

flag is set to true, only one of each tag will be generated. The URL in each tag will have the MD5 hash of the production resource prepended onto its URL. This is used for cache-busting. When the contents of the production resource change, its hash also changes, effectively breaking the cache.

```
...
```Dashboard: Hamsters of North America
...
...

That’s all there is to setting up connect-cachify.

## Conclusion

There are a lot of easy wins when looking to speed up a site. By going back to basics and using the three Cs – concatenation, compression and caching – you will go a long way towards improving the load time of your site and the experience for your users. Connect-cachify helps with concatenation and caching in your NodeJS apps but there is still more we can do. In the next installment of A NodeJS Holiday Season, we will look at how to generate dynamic content and make use of ETagify to still serve maximally cacheable resources.

## Previous articles in the series

This was part four in [a series with a total of 12 posts about Node.js](https://hacks.mozilla.org/category/a-node-js-holiday-season/). The previous ones are:

[Tracking Down Memory Leaks in Node.js](https://hacks.mozilla.org/2012/11/tracking-down-memory-leaks-in-node-js-a-node-js-holiday-season/)[Fully Loaded Node](https://hacks.mozilla.org/2012/11/fully-loaded-node-a-node-js-holiday-season-part-2/)[Using secure client-side sessions to build simple and scalable Node.JS applications](https://hacks.mozilla.org/2012/12/using-secure-client-side-sessions-to-build-simple-and-scalable-node-js-applications-a-node-js-holiday-season-part-3/)

## 5 comments

Steve SoudersDecember 21st, 2012 at 16:45Lloyd HilaielJanuary 31st, 2013 at 10:20srigiDecember 28th, 2012 at 06:06Lloyd HilaielJanuary 31st, 2013 at 10:16Andrew GriffithsFebruary 22nd, 2013 at 06:02