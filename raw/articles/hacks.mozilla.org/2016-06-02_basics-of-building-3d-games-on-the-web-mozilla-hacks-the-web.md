---
title: Basics of building 3D games on the Web – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/06/basics-of-building-3d-games-on-the-web/
author: Andrzej Mazur
published: '2016-06-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

You might think that 3D games are harder to develop than 2D because of the extra dimension you have to take into account, but it’s easier than you think. We’ve recently updated the [Games section on MDN](https://developer.mozilla.org/en-US/docs/Games/) with a collection of tutorials covering 3D development, with a focus on frameworks that offer shortcuts for developers who are getting started building games for the Web and are unfamiliar with WebGL.

![shapes](../../assets/aeeb61f6ddc7e910.png)


### WebVR and 3D game development

Virtual reality in the browser has made great progress this year, and the JavaScript API known as [WebVR](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/WebVR) is under development. The WebVR specification is on the road to [version 1.0](https://hacks.mozilla.org/2016/03/introducing-the-webvr-1-0-api-proposal/). This will be a huge milestone for virtual reality technology in the browser. As the WebVR API matures, it will be time to move from “experimental” demos to the “production-ready” stage of serious commercial games and applications.

The [A-Frame framework](https://aframe.io/) built on top of Three.js is [rapidly evolving](https://hacks.mozilla.org/2016/03/build-the-virtual-reality-web-with-a-frame/). There are case studies of interesting VR projects already like [Cardboard Dungeon](https://hacks.mozilla.org/2016/03/building-cardboard-dungeon-with-a-frame/) and [SECVRITY](https://hacks.mozilla.org/2016/05/exporting-an-indie-unity-game-to-webvr/). The framework itself has reached [version 0.2.0](https://hacks.mozilla.org/2016/03/a-frame-0-2-0-the-extensible-vr-web/) and is quickly gaining interest in the community. Its simple yet powerful approach uses markup to create VR experiences that works across platforms and devices. The result: New tutorials, demos, and plugins are being created every single day.

![VR_images](../../assets/e64085aa4f55da6a.png)


These are exciting times for cutting-edge VR experiments, but if you’re a fan of 2D games like me, jumping into the third dimension might be a challenge. Let’s explore the basics of 3D together, and see how some popular frameworks can help you achieve your goals more quickly, and create impressive games and demos.

The concept of [3D games on the Web](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/) is fundamentally about [rendering WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API) on [Canvas](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas) to create hardware-accelerated rich interactive animations. The [basic theory](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Basic_theory) revolves around the rendering pipeline, which manages the information about your creations, and displays them on the screen.

![mdn-games-3d-rendering-pipeline](../../assets/8b10de7fc254feb5.png)


### An overview of frameworks for 3D game development

You can do all that yourself in pure WebGL, or you can make your life easier, speed up development, and focus only on the important parts of your game idea with a variety of available frameworks. The MDN Games tutorials include:

[Building up a basic demo with Three.js](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_Three.js)[Building up a basic demo with PlayCanvas](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas)[Building up a basic demo with Babylon.js](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_Babylon.js)[Building up a basic demo with A-Frame](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_A-Frame)[GLSL Shaders](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/GLSL_Shaders)

[Three.js](http://threejs.org/) is the most popular tool for WebGL animations, while [PlayCanvas](https://playcanvas.com/) offers you a choice of using the [PlayCanvas engine](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas/engine) or the [online editor](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/Building_up_a_basic_demo_with_PlayCanvas/editor) to build a game or demo. [Babylon.js](http://babylonjs.com/) is often picked for its simple API and powerful features. The [A-Frame](http://aframe.io/) framework can also be used to build rapid prototypes of 3D worlds viewable immediately in virtual reality. We’ve also provided tutorials to cover fundamental concepts like shaders. Understanding what’s going on behind the scenes of the framework gives you greater control over how your game will look when all the post-processing is applied.

### Advantages of frameworks

What are the advantages of using a framework for game development? Frameworks provide benefits and shortcuts. Here are some examples:

![playcanvas-cover](../../assets/15a5bf3e82d7b71a.png)


You can offload work that feels repetitive compared to other parts of creating a game: loading assets, rendering the scene, or drawing everything on screen. You won’t have to manage the specific configuration of cameras, lights, and such. Instead, you can create some geometry, add animation, and forget about everything else – it will just work and you’ll see your creation immediately.

You won’t have to worry about differences in how browsers implement features – that is taken care of by the framework and exposed for you in a simple, high level API.

Frameworks add an extra layer that abstracts many things, so you can write less code and do more with less. A framework can help you focus on the core mechanics of your game. Sometimes a few lines of framework-specific code do exactly the same as dozens of lines of pure JavaScript implementation. (Keep in mind this isn’t always the case.)

![playcanvas-editor-cone](../../assets/5b693460bd6c8026.png)


Different frameworks offer different experiences: Three.js is generally used to create animations; Babylon.js, on the other hand, is focused on creating games. It can also take care of anti-aliasing for you. Both frameworks can be used successfully to create games, so the choice really depends on your preferences and project goals.

Some frameworks even add an extra layer of features and offer built-in physics engines, collision detection, or particle systems. All of that infrastructure is available to use in your project without the compatibility issues you’d need to address to use custom plugins or write these functionalities from scratch.

It’s easier to start and quickly prototype a scene using frameworks – they offer low level of complexity to build complex creations. See how the source code of a simple [2D Breakout game in pure JavaScript](https://developer.mozilla.org/en-US/docs/Games/Workflows/2D_Breakout_game_pure_JavaScript) is longer and more complicated than the [same game in Phaser](https://developer.mozilla.org/en-US/docs/Games/Workflows/2D_breakout_game_Phaser). Using a framework saves you time, so that you can focus on actually building something unique.

![playcanvas-github](../../assets/fe69a27df4ef2b0d.png)


### In conclusion

On the other hand, it is good to learn the language first to know how frameworks are built, why this way and not the other, and to be able to extend them if they are not doing exactly what you want them to. Frameworks tend to go in and out of fashion, and it can be an extra effort to learn their syntax. After all, you can always write a simple feature yourself in pure JavaScript – that’s a powerful skill.

Check out [my GitHub repository](https://github.com/end3r/MDN-Games-3D/) for a collection of demos showcasing how to build a simple 3D scene with the given tools or view them [online](http://end3r.github.io/MDN-Games-3D/).

Remember: you don’t have to use any specific framework, and can achieve comparable results in pure JavaScript with WebGL. The demos shown above were picked to illustrate how to use the most popular tools right now. If you think I’m missing something, you can write about it and add it to the Github collection of 3D demos above – all contributions are welcome. If I did not include your favourite framework you can suggest it in the comments below or write an intro yourself, so more people know about it.

Feel free to use the source code however you like — for example as a boilerplate for your new 3D project — and remember to show us what you’ve built on top of this! We’d love to hear from you right here in comments or over on the Github repo.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.