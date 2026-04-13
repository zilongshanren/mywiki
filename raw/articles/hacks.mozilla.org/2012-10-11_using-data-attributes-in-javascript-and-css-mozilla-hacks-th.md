---
title: Using data-* attributes in JavaScript and CSS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/10/using-data-attributes-in-javascript-and-css/
author: Chris Heilmann
published: '2012-10-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When HTML5 got defined one of the things that was planned for was extensibility in terms of data that should be in the HTML, but not visible. The [data-* attributes](http://www.w3.org/TR/html5/global-attributes.html#embedding-custom-non-visible-data-with-the-data-attributes) allow us to store extra information on HTML elements without needing to use a non-semantic element or pollute the class name. In essence this is what we did with custom attributes before.

These data attributes can be used in many ways, some are a bad idea but others are a good plan. The rule of thumb is that content that should be visible and accessible should not be stored in them. The reason is that assistive technology is not likely to be able to access them and search crawlers don’t index them either.

The syntax is dead easy. Say you have an article and you want to store some extra information that doesn’t have any visual representation. Just use data attributes for that:

...

Reading those out in JavaScript is also very simple. You could use `getAttribute`

to read them but the HTML5 standard defines a simpler way: a [DOMStringMap](http://www.w3.org/TR/html5/common-dom-interfaces.html#domstringmap) you can read out via a `dataset`

property:

```
var article = document.querySelector('#electriccars'),
data = article.dataset;
// data.columns -> "3"
// data.indexnumber -> "12314"
// data.parent -> "cars"
```

Each property is a string (even if you omit the quotes in the HTML) and can be read and written. In the above case setting article.dataset.columns = 5 would change that attribute.

Now, as data-attributes are plain HTML attributes you can even access them from CSS. For example to show the parent data on the article you can use generated content in CSS:

```
article::before {
content: attr(data-parent);
}
```

You can also use the attribute selectors in CSS to change styles according to the data:

```
article[data-columns='3']{
width: 400px;
}
article[data-columns='4']{
width: 600px;
}
```

You can see all this working together [in this JSBin example](http://jsbin.com/ujiday/2/edit).

Data attributes can also be stored to contain information that is constantly changing, like scores in a game. Using the CSS selectors and JavaScript access here this allows you to build some nifty effects without having to write your own display routines. See the [following screencast](http://www.youtube.com/watch?v=On_WyUB1gOk) for an example using generated content and CSS transitions:

## Issues with data-attributes

Sadly enough it seems there is nothing that is so simple and useful that doesn’t come with a price. In this case the main issues to consider are that Internet Explorer [does not support the dataset](http://caniuse.com/#feat=dataset) but you’d need to read them out with

`getAttribute()`

instead. The other issue is that the [performance of reading data-attributes](http://jsperf.com/data-dataset)compared to storing this data in a JS data warehouse is bad. Using

`dataset`

is even slower than reading the data out with `getAttribute()`

.That said, though, for content that is not to be shown they are a great solution and maybe we can get them into the next IE soon.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 11 comments

MaujorOctober 11th, 2012 at 06:46Robert NymanOctober 11th, 2012 at 09:16leoman730October 11th, 2012 at 06:59Robert NymanOctober 11th, 2012 at 09:17RafaelOctober 12th, 2012 at 08:29Robert NymanOctober 12th, 2012 at 12:29ArthurOctober 12th, 2012 at 14:00Robert NymanOctober 14th, 2012 at 05:13fbenderOctober 16th, 2012 at 06:34fbenderOctober 16th, 2012 at 11:29AlessandroOctober 17th, 2012 at 03:16