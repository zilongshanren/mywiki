---
title: 'Blend4Web: the Open Source Solution for Online 3D – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2014/10/blend4web-the-open-source-solution-for-online-3d/
author: Yuri Kovelenov
published: '2014-10-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Half year ago Blend4Web was first released publicly. In this article I’ll show what Blend4Web is, how it is evolved and and how it can be used for web development.

## What Is Blend4Web?

In short, Blend4Web is an open source framework for creating 3D web applications. It uses [Blender](http://www.blender.org/) – the popular open source 3D modeling suite – as the primary authoring tool. 3D graphics is rendered by means of WebGL which is also an open standard technology. The two main keywords here – Blender and Web(GL) – explain the purpose of this engine perfectly.

The full source code of Blend4Web together with some usage examples is available under GPLv3 on [GitHub](https://github.com/TriumphLLC/Blend4Web) (there is also a commercial licensing option).

## The 3D Web

On June the 2nd Apple presented their new operating systems – OS X Yosemite and iOS 8 – both featuring WebGL support in their Safari browser. That marked the end of a 5 year cycle during which the WebGL technology has been evolving, starting with the first unstable browser builds (if anybody remembers Firefox 3.7 alpha?). Now, all the major browsers on all desktop and mobile systems support this open standard for rendering 3D graphics, everywhere, without any plugins.

That was a long and difficult road, along which Blend4Web development has been following WebGL development as a shadow. Broken rendering, tab crashes, security “warnings” from [some big guys](http://blogs.technet.com/b/srd/archive/2011/06/16/webgl-considered-harmful.aspx), unavailability in public browser builds, all sorts of fears, uncertainty and doubts. All this didn’t matter, because we have the opportunity to do 3D graphics (and sound) in browsers!

## Blender

The first Blender 2.5x builds appeared in summer 2010. At the time we, the programming geeks, were pushed to learn the basics of 3D modeling by the beautiful Sintel from the [open source movie](http://www.sintel.org/gallery/) of the same name. After choosing Blender, we could be as independent as possible, with a full open source pipeline organized on a Linux platform. Blender gave us the power to make our own 3D scenes, and later helped to attract talanted artists from its wonderful community to join us.

## Blend4Web Evolution in Demos

Our demo scenes matured together with the development of Blend4Web. The first one was a quite low-poly and almost non-interactive demo called [The Island](http://www.blend4web.com/en/demo/island/). It was created in 2011 and polished a bit before the public release. In this demo we introduced our Blender-based pipeline in which all the assets are stored in separate files and are linked into the main file for level design and further exporting (for this reason some of Blend4Web users call it “free Unity Pro”).

![](../../assets/1cf5ca8adffb6b18.jpg)


In [Fashion Show](http://www.blend4web.com/en/demo/fashion/) we developed cloth animation techniques. Some post-processing effects, dynamic reflection and particle systems were added later. After Blend4Web has gone public we summarized these cloth-releated tricks in [one of our tutorials](http://www.blend4web.com/en/article/48).

[The Farm](http://www.blend4web.com/en/demo/farm/) is a huge scene (in the scale of a browser): over 25 hectares of land, buildings, animated animals and foliage. We added some gamedev elements into it, including the ability of first-person walking, interacting with objects, driving a vehicle. The demo features spatial audio (via Web Audio) and physics (via [Bullet](http://bulletphysics.org/) and [Asm.js](http://asmjs.org/spec/latest/)). The [Freedesktop](http://www.freedesktop.org/wiki/) folks tried it as a benchmark while testing the Mesa drivers (and got “massive crashes” :).

![](../../assets/42faa8c73ba159a5.jpg)


We also tried some visualization and created [Nature Morte](http://www.blend4web.com/en/demo/naturemorte/). In this scene we used carefully crafted textures and materials, as well as post-processing effects to improve realism. However, the technology used for this demo was

quite simple and old-school, as we had no support for visual shader editing yet.

![](../../assets/762801bb645198a7.jpg)


Things have changed when Blender’s node materials have become available to our artists. They created over 40 different materials for the [Sports Car](http://www.blend4web.com/en/demo/sportscar/) model: chromed metal, painted metal, glass, rubber, leather etc.

In our latest release we stepped even further by adding support for the animation control by the user. Now interactivity can be implemented without any coding. In order to demonstrate the new opening possibilities we presented interactive [infographic of a light helicopter](http://www.blend4web.com/en/demo/helicopter/).

![](../../assets/3a9e06926b08a6ef.jpg)


Among the other possible applications of this simple yet effective tool (called NLA Script) we can list the following: interactive 3D web design, product promotions, learning materials, cartoons with the ability to choose between different story lines, point-and-click games and any other applications previously created with Flash.

## Using Blend4Web

It is very easy to start using Blend4Web – just download and install the Blender addon as shown in this video tutorial:

The most wonderful thing is that your Blender scene can be exported into a self-contained HTML file that can be emailed, uploaded to your own website or to a cloud – in short shared however you like. This freedom is a fundamental difference from numerous 3D web publishing services as we don’t lock our users to our technology by any means.

For those who want to create highly interactive 3D web apps we offer the [SDK](http://www.blend4web.com/en/downloads/). Some notable examples of what is possible with the [Blend4Web API](http://www.blend4web.com/api_doc/index.html) are demonstrated in our [programming tutorials](http://www.blend4web.com/en/tag/21/1/), ranging from web design to games.

Programming 3D web apps with Blend4Web is not much harder than building average RIAs. Unlike some other WebGL frameworks in the wild we tried to offload all graphics, animation and audio tasks to respective professionals. The programmer just loads the scene…

```
var m_data = require("data");
m_data.load("example.json", load_cb);
```

…and then writes the logic which triggers the 3D scene changes that are “hard-coded” by the artists, e.g. plays the animation for the user-selected object:

```
var m_scenes = require("scenes");
var m_anim = require("animation");
var myobj = m_scenes.pick_object(event.clientX, event.clientY);
m_anim.apply_def(myobj);
m_anim.play(myobj);
```

As you can see the APIs are structured in a CommonJS way which we believe is important for creating compact and fast web apps.

## The Future

There are many possible ways in which the Internet and IT will be going but there is no doubt that the strong and steady development of 3D Web is already here. We expect that more and more users will change their expectations about how web content should look and feel like. We’re gonna help the web developers meet these demands with plans to improve usability and performance and to implement new interesting graphics effects.

We also follow the development of [WebGL 2.0](http://www.khronos.org/registry/webgl/specs/latest/2.0/) (thanks Mozilla for your job) and expect to create even more nice things on top of it.

## Stay Tuned

Read our [blog](http://www.blend4web.com/en/blog/), join us on [Twitter](https://twitter.com/blend4web), [Google+](https://plus.google.com/115088226619544632679/posts), [Facebook](http://facebook.com/blend4web) and [Reddit](http://reddit.com/r/blend4web), watch the demos and tutorials on our [YouTube channel](http://www.youtube.com/user/blend4web), fork Blend4Web at [GitHub](https://github.com/TriumphLLC/Blend4Web).

## About
[
Yuri Kovelenov ](http://www.blend4web.com/)

Founder and development lead of Blend4Web - the open source framework for creating 3D web applications.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

DobladoVOctober 7th, 2014 at 15:54Yuri KovelenovOctober 7th, 2014 at 22:52Fabricio C ZuardiOctober 9th, 2014 at 17:17Yuri KovelenovOctober 9th, 2014 at 23:48