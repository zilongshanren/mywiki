---
title: A-Frame 0.2.0 – The Extensible VR Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/03/a-frame-0-2-0-the-extensible-vr-web/
author: Kevin Ngo
published: '2016-03-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[A-Frame](https://aframe.io) is a framework that makes it easy to build virtual reality (VR) content for the Web. It provides:

- The ability to build 3D scenes with declarative HTML.
- Responsive WebVR scenes that work out of the box on multiple platforms.
- An
[entity-component-system pattern](https://wikipedia.org/wiki/Entity_component_system)which promotes composability and extensibility.

After three fun and busy months of development, we are proud to announce the release of A-Frame version 0.2.0. This version’s overarching theme is *extensibility*. For WebVR to evolve quickly, in a period in which VR is dominated by closed native ecosystems, A-Frame needs to enable open experimentation and rapid iteration. A-Frame’s inherent extensibility grants developers permissionless innovation, making it the VR-flavored embodiment of the [Extensible Web Manifesto](https://www.w3.org/community/nextweb/2013/06/11/the-extensible-web-manifesto/).

*If you’re not familiar, read [A-Frame’s previous introduction on Mozilla Hacks](https://hacks.mozilla.org/2016/03/build-the-virtual-reality-web-with-a-frame/).

![A-Frame Community Examples](../../assets/4fd79245b5b65d1c.gif)


## Since Launch

A-Frame has received an overwhelmingly positive response by democratizing immersive 3D content creation on the Web. By the numbers:

- Over 1500 stars, 25 contributors, 550 commits on the
[A-Frame GitHub repository](https://github.com/aframevr/aframe). - Over 470 people have joined the
[A-Frame community Slack channel](https://aframevr-slack.herokuapp.com)to ask questions, show off projects, and just generally socialize. - Over 100 awesome creations by people listed on the
[awesome-aframe repository](https://github.com/aframevr/awesome-aframe). - Over 50 projects showcased on the
[Made With A-Frame Tumblr](http://aframevr.tumblr.com/).

Members of the community have used A-Frame for some interesting use cases:

[Donovan Kraeker](http://kraeker.com)of[DrawVR](http://drawvr.com)has built[several VR stores](http://vr.ispystore.ca/)to enhance his existing e-commerce properties.[Ryan James](http://drryanjames.github.io/), a PhD student and researcher at the University of Washington, has[applied virtual reality to medical education](https://www.youtube.com/watch?v=eYyuEjhD-k8).[Don McCurdy](https://twitter.com/donrmccurdy), a software engineer at Google, has recreated a scene from the popular indie game,[Monument Valley](https://sandbox.donmccurdy.com/vr/monument/).

And A-Frame has received some high-profile use:

[Amnesty International UK](https://www.amnesty.org.uk/), in partnership with design firm[Junior](http://junior.io), created[360 Syria](http://www.360syria.com/), an experience that transports viewers to the besieged city of Aleppo, Syria to witness the devastation of barrel bombing on its citizens.[The Washington Post](https://washingtonpost.com/)publishedwhich transports people to the surface of the Red Planet to learn about space exploration programs.[Mars: An Interactive Journey](https://www.washingtonpost.com/graphics/business/mars-journey/)

## Improved Extensibility in A-Frame 0.2.0

A-Frame brought the * entity-component-system* pattern to HTML. Everything in a

[scene](https://aframe.io/docs/core/scene.html)is an

[entity](https://aframe.io/docs/core/entity.html). An entity is a general placeholder object that inherently does nothing and renders nothing. Components are buckets of reusable data and logic; when plugged into entities, components provide them appearance, behavior, and functionality. Developers can write components to do whatever they want, with direct access to three.js, and then share them with the community. Anything that is possible with three.js and WebGL is possible in A-Frame.

Since A-Frame’s initial release, we have been largely refining the [component API](https://aframe.io/docs/core/component.html). We went through cycles of creating components, discovering limitations in the API, and then writing patches to improve A-Frame. By dogfooding our own framework, we were able to discover obstacles in extending A-Frame:

- Component API has been enhanced with property types, schema configurations, and more lifecycle methods (
`pause`

,`play`

,`tick`

). - Primitives (convenience elements such as
) are able to take components.`<a-sphere>`


In addition, we opened up more escape hatches for developers to delve deeper. They can now:

- Define custom property types for more flexible component APIs.
- Register GLSL shaders or three.js materials.
- Register primitives.
- Register systems to provide global scope and services to components.

Read the [full version 0.2.0 release notes](https://github.com/aframevr/aframe/releases/tag/v0.2.0) for more detail.

## Incarnation of the Extensible VR Web

The Extensible Web encourages healthy competition between ideas and APIs. Only once emerging ideas and APIs are established should they be standardized. Embracing this philosophy is mandatory in order for WebVR to succeed, else it’ll be another case of the Web being late to the party when all the chips have already been eaten. A-Frame is an embodiment of these ideas.

As mentioned before, with A-Frame being built upon an entity-component-system pattern, developers can write, share, and plug in components that extend new features. If a feature doesn’t yet exist or isn’t up to par, the community can run with it. The ecosystem already features community-built components that enable gamepad controls, speech recognition, and physics. With this short-term innovation scheme, developers can rapidly experiment with ideas in order to help advance not only A-Frame but WebVR.

For example, [Don McCurdy](https://twitter.com/donrmccurdy) iterated on standard A-Frame components in his A-Frame playground repository, while the core A-Frame team worked on enabling extensibility. From that, he has refactored and enhanced A-Frame’s entire controls system alongside physics. With those components proven, we will upstream them to the collection of standard A-Frame components.

Several people in the community were looking for a way to render text and HTML elements as textures in A-Frame. Student [Max Krieger](https://twitter.com/a9_io) stepped up and wrote components to enable using a `<canvas>`

element as a texture and to enable text wrapping.

Also, [Ben Nolan](https://twitter.com/bnolan) of [SceneVR](https://www.scenevr.com/) recently ported his client-side code to use A-Frame. He is developing components that enable interactive and multi-user experiences, features the core A-Frame team was targeting for later this year. What’s more, Ben is working on an [WYSIWYG](https://wikipedia.org/wiki/WYSIWYG) editor for A-Frame scenes. We are working on an editor as well.

This virtuous cycle of the community enabling features and sharing components continues to be a huge boon for the WebVR ecosystem. Rather than designing slowly behind closed doors, we built A-Frame to pull the entire web community into the effort. Together we’ll try lots of things and slowly focus on the ones that work.

## Looking Ahead

We’ll be working on building more demos, improving interactivity, and crunching down on performance. Once the polyfill is stabilized, we will quickly release [WebVR 1.0 support](https://hacks.mozilla.org/2016/03/introducing-the-webvr-1-0-api-proposal/) into A-Frame.

## About
[
Kevin Ngo ](http://ngokevin.com)

Kevin is a virtual reality developer at Mozilla and a core developer on A-Frame, an open-source WebVR framework. He is @ngokevin_ on Twitter.

## 2 comments

Angel Celis BottoMarch 31st, 2016 at 16:34Ian Sun.RaApril 27th, 2016 at 23:01