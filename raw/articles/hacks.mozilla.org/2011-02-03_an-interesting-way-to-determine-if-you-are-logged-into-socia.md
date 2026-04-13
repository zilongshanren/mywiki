---
title: An interesting way to determine if you are logged into social web sites – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/02/an-interesting-way-to-determine-if-you-are-logged-into-social-web-sites/
author: Chris Heilmann
published: '2011-02-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Do you remember the trick how to find out [that you went to certain web sites by analysing link colour](http://dbaron.org/mozilla/visited-privacy) (now [patched in Firefox](http://hacks.mozilla.org/2010/03/privacy-related-changes-coming-to-css-vistited/comment-page-1/))? There is much your browser tells about you if you just create a few HTML elements.

Mike Cardwell [has found an interesting way to detect if you are logged into social web sites](https://grepular.com/Abusing_HTTP_Status_Codes_to_Expose_Private_Information). The easiest trick lies with GMail. Mike created a photo and uploaded it to Google. If you add this image to an HTML document and add event handlers for the success and failure case you can check if the visitor is logged in or not – as the photo gets delivered when you are and GMail delivers a 404 document when you are not:


This works in all browsers and can be used to for example send `mailto:`

links to GMail directly. Notice that this just checks that you are logged in, it doesn’t mean you get access to content.

For Facebook and Twitter, this doesn’t quite work. Instead, Mike tries to read content with the APIs and relies on errors to be thrown on 404 responses:

```
```

This fails to work in Internet Explorer and Opera, but still works nicely for the other browsers. In Firefox you can work around this using the [Request Policy](https://www.requestpolicy.com/) add-on.

It’d be interesting to see what other social web sites can be detected with some simple onload and onerror handlers. Know any others?

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 14 comments

Jan!February 4th, 2011 at 01:20Paul RougetFebruary 4th, 2011 at 01:42Jan!February 4th, 2011 at 01:50Chris HeilmannFebruary 4th, 2011 at 02:08Thanasis PolychronakisFebruary 4th, 2011 at 03:50Giorgio MaoneFebruary 4th, 2011 at 10:02StormyFebruary 4th, 2011 at 10:32WulfTheSaxonFebruary 4th, 2011 at 11:22Giorgio MaoneFebruary 4th, 2011 at 11:25Paul RougetFebruary 4th, 2011 at 11:47PierreFebruary 5th, 2011 at 06:01nemoFebruary 5th, 2011 at 16:03Joss CrowcroftFebruary 6th, 2011 at 08:11dazbo100March 15th, 2011 at 13:02