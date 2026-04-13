---
title: Using CORS to load WebGL textures from cross-domain images – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2011/11/using-cors-to-load-webgl-textures-from-cross-domain-images/
author: Benoit Jacob
published: '2011-11-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In Firefox, as well as in Chrome, it is now possible to load cross-domain images into WebGL textures, if they have been approved by [CORS](http://en.wikipedia.org/wiki/Cross-Origin_Resource_Sharing).

Most prominently, this feature allows for impressive 3D mapping applications such as [Google MapsGL](http://maps.google.com/mapsgl) and [Nokia Maps 3D](http://maps3d.svc.nokia.com/webgl/).

### What happened

Earlier this year, the[ Editor’s Draft WebGL specification](http://www.khronos.org/registry/webgl/specs/latest/) got [updated](http://hacks.mozilla.org/2011/06/cross-domain-webgl-textures-disabled-in-firefox-5/) in response to a security concern. The [additions](http://www.khronos.org/registry/webgl/specs/latest/#4.2) were:

- A mandatory clause disallowing usage of cross-domain elements as WebGL textures in the general case.
- A non-normative clause specifically allowing cross-domain elements that have CORS approval. For that occasion, the HTML specification on the
[<img> element](http://www.whatwg.org/specs/web-apps/current-work/multipage/embedded-content-1.html#the-img-element)got updated to add a[new crossorigin attribute](http://www.whatwg.org/specs/web-apps/current-work/multipage/embedded-content-1.html#attr-img-crossorigin).

The first got implemented in Firefox 5, the second is now in Firefox 8.

### How to use this feature

There are [two CORS modes](http://www.whatwg.org/specs/web-apps/current-work/multipage/fetching-resources.html#cors-settings-attribute): “anonymous” and “use-credentials”. We’ll focus on “anonymous” as it’s the common case. A great example of images served with anonymous CORS is Google Maps imagery, such as:

In order to load it with CORS as a WebGL texture, we set the crossOrigin attribute on it:

var earthImage = new Image(); earthImage.crossOrigin = "anonymous";

Now we load it as usual:

earthImage.onload = function() { // whatever you usually to do load WebGL textures }; earthImage.src = "http://khm0.googleapis.com/kh?v=95&x=0&y=0&z=0";

That’s it! Aside from setting the crossOrigin attribute, we didn’t have to do anything. Here is the ** full self-contained example**.

### The HTTP headers

If we study the HTTP headers for this image (using, for example, Firefox’s Web Console), we find that the *Request Headers* contain

Origin: null

which is the effect of having set this crossOrigin attribute on the img element. And the *Response Headers* contain

Access-Control-Allow-Origin: null

which is the effect of the server supporting CORS for this file.

### Doing this in HTML

Of course, one could also set this attribute in HTML, in which case it’s case-insensitive:

<img src="http://khm0.googleapis.com/kh?v=95&x=0&y=0&z=0" crossorigin="anonymous">

And since “anonymous” is both the missing-value-default and the invalid-value-default for the crossorigin attribute, we can pass any invalid value for it, or even just omit its value:

<img src="http://khm0.googleapis.com/kh?v=95&x=0&y=0&z=0" crossorigin>

### Coming soon: CORS approval for Canvas 2D drawImage

What if you first draw a CORS-approved cross-domain image onto a 2D

canvas, and then use that canvas as the source of a WebGL texture? The

good news is that this [will work](https://bugzilla.mozilla.org/show_bug.cgi?id=685518) in Firefox 9, which is hitting the Beta

channel soon. This fix means that demos like [this](http://www.clicktorelease.com/code/weather/) will work really

nicely in Firefox 9.

## About Benoit Jacob

I am a software engineer at Mozilla Corp., working on Gecko, specifically the Graphics and WebGL parts. I work from Mozilla's Toronto office.

## 6 comments

Henri AstreNovember 8th, 2011 at 14:34Benoit JacobNovember 8th, 2011 at 19:43Ben AdamsNovember 10th, 2011 at 07:51BillDecember 15th, 2011 at 18:20Benoit JacobDecember 15th, 2011 at 21:01Henri AstreDecember 17th, 2011 at 15:55