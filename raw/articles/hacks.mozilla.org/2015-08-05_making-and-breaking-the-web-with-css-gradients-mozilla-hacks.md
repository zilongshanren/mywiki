---
title: Making and Breaking the Web With CSS Gradients – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/08/making-and-breaking-the-web-with-css-gradients/
author: Mike Taylor
published: '2015-08-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## What is CSS prefixing and why do I care?

“Browser vendors sometimes add prefixes to experimental or nonstandard CSS properties, so developers can experiment but changes in browser behavior don’t break the code during the standards process. Developers should wait to include the unprefixed property until browser behavior is standardized.”


As a Web developer, users of your web sites will be affected if you use prefixed CSS properties which later have their prefixes removed—especially if syntax has changed between prefixed and unprefixed variants.

There are steps you can take in stewardship of an unbroken Web. Begin by checking your stylesheets for outdated gradient syntax and updating with an unprefixed modern equivalent. But first, let’s take a closer look at the issue.

## What are CSS gradients?

CSS gradients are a type of [CSS <image> function](http://www.w3.org/TR/css3-images/#image-values) (expressed as a property value) that enable developers to style the background of block-level elements to have variations in color instead of just a solid color.

[The MDN documentation on gradients](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Using_CSS_gradients)gives an overview of the various gradient types and how to use them. As always, CSS Tricks has top notch

[coverage on CSS3 gradients as well](https://css-tricks.com/css3-gradients/).

## Removing (and then not removing) prefixed gradients from Firefox

In [Bug 1176496](https://bugzilla.mozilla.org/show_bug.cgi?id=1176496), we tried to remove support for the old -moz- prefixed linear and radial gradients. Unfortunately, we soon [realized](https://groups.google.com/forum/#!topic/mozilla.compatibility/ekZBqfOnzTc/discussion) that it broke the Web for enough sites ([[1]](https://bugzilla.mozilla.org/show_bug.cgi?id=1182775), [[2]](https://bugzilla.mozilla.org/show_bug.cgi?id=1182861), [[3]](https://bugzilla.mozilla.org/show_bug.cgi?id=1183504), [[4]](https://bugzilla.mozilla.org/show_bug.cgi?id=1183602), [[5]](https://webcompat.com/issues/1061), [[6]](https://webcompat.com/issues/1393)) that we had to add back support (for now).

## Sin and syntax

Due to changes in the spec between the -moz- prefixed implementation and the modern, prefix-less version, it’s not possible to just remove prefixes and get working gradients.

Here’s a simple example of how the syntax has changed (for linear-gradient):

```
/* The old syntax, deprecated and prefixed, for old browsers */
background: -prefix-linear-gradient(top, blue, white);
/* The new syntax needed by standard-compliant browsers (Opera 12.1,
IE 10, Firefox 16, Chrome 26, Safari 6.1), without prefix */
background: linear-gradient(to bottom, blue, white);
```


In a nutshell, `to`

and `at`

keywords were added, `contain`

and `cover`

keywords were removed, and the angle coordinate system was changed to be more consistent with other parts of the platform.

When IE10 came out with support for prefixless new gradients, [IEBlog wrote an awesome post](http://blogs.msdn.com/b/ie/archive/2012/06/25/unprefixed-css3-gradients-in-ie10.aspx) illustrating the differences between the prefixed (old) syntax and the new syntax; check that out for more in-depth coverage. The [css-tricks.com article on CSS3 gradients](https://css-tricks.com/css3-gradients/) also has a good overview on the history of CSS gradients and its syntaxes (see “Tweener” and “New” in the “Browser Support/Prefixes” section).

## OK, so like, what should I do?

You can start checking your stylesheets for outdated gradient syntax and making sure to have an unprefixed modern equivalent.

Here are some tools and libraries that can help you maintain modern, up-to-date, prefixless CSS:

If you’re already using the PostCSS plugin [Autoprefixer](https://github.com/postcss/autoprefixer), you won’t have to do anything. If you’re not using it yet, consider adding it to your tool belt. And if you prefer a client-side solution, Lea Verou’s [prefix-free.js](http://leaverou.github.io/prefixfree/) is another great option.

In addition, the web app [Colorzilla](http://www.colorzilla.com/gradient-editor/) will allow you to enter your old CSS gradient syntax to get a quick conversion to the modern prefixless conversion.

[Masatoshi Kimura has added a preference](https://bugzilla.mozilla.org/show_bug.cgi?id=1186636) that can be used to turn off support for the old -moz- prefixed gradients, giving developers an easy way to visually test for broken gradients. Set `layout.css.prefixes.gradients`

to `false`

(from about:config) in [Nightly](https://nightly.mozilla.org/). This pref should ship in Firefox 42.

## Modernizing your CSS

And as long as you’re in the middle of editing your stylesheets, now would be a good time to check the rest of them for overall freshness. Flexbox is an area that is particularly troublesome and in need of unbreaking, but [good resources](https://css-tricks.com/old-flexbox-and-new-flexbox/) [exist to ease the pain](https://css-tricks.com/using-flexbox/). CSS `border-image`

is also an area that had [changes between prefixed and unprefixed versions](http://dbaron.org/log/20120612-border-image).

Thanks for your help in building and maintaining a Web that works.

## About
[
Mike Taylor ](https://miketaylr.com)

Mike works as a Web Compatibility Engineer for Mozilla from his home in Austin, TX.

## 3 comments

Colin EberhardtAugust 6th, 2015 at 23:57Andy MercerAugust 16th, 2015 at 11:08Mike TaylorAugust 7th, 2015 at 09:25