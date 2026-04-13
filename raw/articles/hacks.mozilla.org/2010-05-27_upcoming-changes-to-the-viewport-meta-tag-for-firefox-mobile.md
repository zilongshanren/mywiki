---
title: upcoming changes to the viewport meta tag for firefox mobile – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2010/05/upcoming-changes-to-the-viewport-meta-tag-for-firefox-mobile/
author: Christopher Blizzard
published: '2010-05-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a guest post by Matt Brubeck who works on the Firefox Mobile team.*

The upcoming release of [Mobile Firefox (Fennec)](https://wiki.mozilla.org/Mobile/Fennec) 1.1 features improved

support for the `<meta name="viewport">`

tag. Previous version of Fennec supported the `width`

, `height`

, and `initial-scale`

viewport properties, but had [problems](http://starkravingfinkle.org/blog/2010/01/perils-of-the-viewport-meta-tag/) with some sites designed for iPhone and Android browsers. We now support the same properties Mobile Safari does, and we also changed Fennec to render mobile sites more consistently on screens of different sizes and resolutions.

touch.facebook.com before:

![](../../assets/5d907f614a2e08af.png)


touch.facebook.com after:

![](../../assets/83da63101b3df219.png)


You can see these changes for yourself in the latest [Fennec 1.1](http://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/latest-mobile-1.9.2/) and [trunk](http://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/latest-mobile-trunk/) nightly builds for Maemo, Android, Windows, Mac, or Linux.

## Background

Mobile browers like Fennec render pages in a virtual “window” (the viewport), usually wider than the screen, so they don’t need to squeeze every page layout into a tiny window (which would break many non-mobile-optimized sites). Users can pan and zoom to see different areas of the page.

Mobile Safari introduced the “viewport meta tag” to let web developers control the viewport’s size and scale. Many other mobile browsers now support this tag, although it is not part of any web standard. Apple’s [documentation](http://developer.apple.com/safari/library/documentation/AppleApplications/Reference/SafariWebContent/UsingtheViewport/UsingtheViewport.html#//apple_ref/doc/uid/TP40006509-SW29) does a good job explaining how web developers can use this tag, but we had to do some detective work to figure out exactly how to implement it in Fennec. For example, Safari’s documentation says the content is a “comma-delimited list,” but existing browsers and web pages use any mix of commas, semicolons, and spaces as separators.

## Viewport basics

A typical mobile-optimized site contains something like the following:

```
```

The `width`

property controls the size of the viewport. It can be set to a specific number of pixels like `width=600`

or to the special value `device-width`

value which is the width of the screen in CSS pixels at a scale of 100%. (There are corresponding `height`

and `device-height`

values, which may be useful for pages with elements that change size or position based on the viewport height.)

The `initial-scale`

property controls the zoom level when the page is first loaded. The `maximum-scale`

, `minimum-scale`

, and `user-scalable`

properties control how users are allowed to zoom the page in or out.

## A pixel is not a pixel

The iPhone and many popular Android phones have 3- to 4-inch (7–10 cm) screens with 320×480 pixels (~160 dpi). Firefox for Maemo runs on the Nokia N900, which has the same physical size but 480×800 pixels (~240 dpi). Because of this, the last version of Fennec displayed many pages about one third smaller (in actual, physical size) than iPhone or Android. This caused usability and readability problems on many touch-optimized web sites. Peter-Paul Koch wrote about this problem in [A pixel is not a pixel](http://www.quirksmode.org/blog/archives/2010/04/a_pixel_is_not.html).

Fennec 1.1 for Maemo will use 1.5 hardware pixels for each CSS “pixel”, following the lead of Android’s WebKit-based browser. This means a page with `initial-scale=1`

will render at close to the same physical size in Fennec for Maemo, Mobile Safari for iPhone, and the Android Browser on both [HDPI and MDPI](http://developer.android.com/guide/practices/screens_support.html#range) phones. This is consistent with the [CSS 2.1 specification](http://www.w3.org/TR/CSS2/syndata.html#length-units), which says:

If the pixel density of the output device is very different from that of a typical computer display, the user agent should rescale pixel values. It is recommended that the pixel unit refer to the whole number of device pixels that best approximates the reference pixel. It is recommended that the reference pixel be the visual angle of one pixel on a device with a pixel density of 96dpi and a distance from the reader of an arm’s length.


For web developers, this means that 320px be full width in portrait mode at scale=1, on all of the above-mentioned handheld devices, and they may size their layouts and images accordingly. But remember that not all mobile devices are the same width; you should also make sure that your pages work well in landscape mode, and on larger devices like the iPad and Android tablets.

On 240-dpi screens, pages with `initial-scale=1`

will effectively be zoomed to 150% by both Fennec and Android WebKit. Their text will be smooth and crisp, but their bitmap images will probably not take advantage of the full screen resolution. To get sharper images on these screens, web developers may want to design images – or whole layouts – at 150% of their final size (or 200%, to support the rumored 320-dpi iPhone) and then scale them down using CSS or viewport properties.

Right now Fennec uses the same default ratio of 1.5 on all devices. (It’s a hidden preference that can be changed in about:config or by an add-on.) Later we’ll need to change this – as well as many other parts of Fennec’s user interface – to work correctly on screens with different pixel densities. Note that the default ratio of 1.5 is true only when the viewport scale equals 1. Otherwise, the relationship between CSS pixels and device pixels depends on the current zoom level.

## Viewport width and screen width

Many sites set their viewport to `"width=320, initial-scale=1"`

to fit precisely onto the iPhone display in portrait mode. As mentioned above, this caused [problems](http://starkravingfinkle.org/blog/2010/01/perils-of-the-viewport-meta-tag/) when Fennec 1.0 endered these sites, especially in landscape mode. To fix this, Fennec 1.1 will expand the viewport width if necessary to fill the screen at the requested scale. This matches the behavior of Android and Mobile Safari, and is especially useful on large-screen devices like the iPad. (Allen Pike’s [Choosing a viewport for iPad sites](http://www.antipode.ca/2010/choosing-a-viewport-for-ipad-sites/) has a good explanation for web developers.)

For pages that set an initial or maximum scale, this means the `width`

property actually translates into a *minimum* viewport width. For example, if your layout needs at least 500 pixels of width then you can use the following markup. When the screen is more than 500 pixels wide, the browser will expand the viewport (rather than zoom in) to fit the screen:

```
```

Fennec 1.1 also adds support for `minimum-scale`

, `maximum-scale`

, and `user-scalable`

, with defaults and limits similar to [Safari’s](http://developer.apple.com/safari/library/documentation/AppleApplications/Reference/SafariHTMLRef/Articles/MetaTags.html). These properties affect the initial scale and width, as well as limiting changes in zoom level.

Mobile browsers handle orientation changes slightly differently. For example, Mobile Safari often just zooms the page when changing from portrait to landscape, instead of laying out the page as it would if originally loaded in landscape. If web developers want their scale settings to remain consistent when switching orientations on the iPhone, they must add a `maximum-scale`

value to prevent this zooming, which has the sometimes-unwanted side effect of preventing users from zooming in:

```
```

This is not necessary in Fennec; when the device changes orientation, Fennec updates the viewport size, the page layout, and JavaScript/CSS properties like `device-width`

, based on its new “window” dimensions.

## Standards

There is clearly demand for the viewport meta tag, since it is supported by most popular mobile browsers and used by thousands of web sites. It would be good to have a true standard for web pages to control viewport properties. According to the HTML5 spec, extensions to the `meta`

element should first be registered on the [WHATWG wiki](http://wiki.whatwg.org/wiki/MetaExtensions) and then go through the W3C standards process. If this happens, then we at Mozilla will work to make sure we can implement any changes made during standardization.

## 5 comments

Martin KliehmMay 27th, 2010 at 11:18Wurdebalg HurrstMay 27th, 2010 at 11:52Ms2gerMay 28th, 2010 at 04:50Martin KliehmMay 28th, 2010 at 06:50Kam-Yung SohJuly 15th, 2010 at 21:40