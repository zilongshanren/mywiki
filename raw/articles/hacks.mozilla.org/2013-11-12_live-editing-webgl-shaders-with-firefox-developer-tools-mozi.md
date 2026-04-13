---
title: Live editing WebGL shaders with Firefox Developer Tools – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/11/live-editing-webgl-shaders-with-firefox-developer-tools/
author: Jeff Griffiths
published: '2013-11-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you’ve seen Epic Games’ HTML5 port of [‘Epic Citadel’](http://www.unrealengine.com/html5/), you have no doubt been impressed by the amazing performance and level of detail. A lot of the code that creates the cool visual effects you see on screen are written as *shaders* linked together in *programs* – these are specialized programs that are evaluated directly on the GPU to provide high performance real-time visual effects.

Writing Vertex and Fragment shaders are an essential part of developing 3D on the web even if you are using a library, in fact the [Epic Citadel demo](https://blog.mozilla.org/futurereleases/2013/05/02/epic-citadel-demo-shows-the-power-of-the-web-as-a-platform-for-gaming/) includes over 200 shader programs. This is because most rendering is customised and optimised to fit a game’s needs. Shader development is currently awkward for a few reasons:

- Seeing your changes requires a refresh
- Some shaders are applied under very specific conditions

Here is a screencast that shows a how to manipulate shader code using a relatively simple WebGL demo:

Starting in Firefox 27 we’ve introduced a new tool called the ‘Shader Editor’ that makes working with shader programs much simpler: the editor lists all shader programs running in the WebGL context, and you can live-edit shaders and see immediate results without interrupting any animations or state. Additionally editing shaders should **not** impact WebGL performance.

## Enabling the Shader Editor

The Shader Editor is not shown by default, because not all the web pages out there contain WebGL, but you can easily enable it:

- Open the Toolbox by pressing either F12 or Ctrl/Cmd + Shift + I.
- Click on the ‘gear’ icon near the top edge of the Toolbox to open the ‘Toolbox Options’.
- On the left-hand side under ‘Default Firefox Developer Tools’ make sure ‘Shader Editor’ is checked. You should immediately see a new ‘Shader Editor’ Tool tab.

## Using the Shader Editor

To see the Shader Editor in action, just go to a WebGL demo [such as this one](http://learningwebgl.com/lessons/lesson04/index.html) and open the toolbox. When you click on the shader editor tab, you’ll see a reload button you will need to click in order to get the editor attached to the WebGL context. Once you’ve done this you’ll see the Shader Editor UI:

- On the left you have a list of programs, a vertex and fragment shader corresponds to each program and their source is displayed and syntax highlighted in the editors on the right.
- The shader type is displayed underneath each editor.
- Hovering a program highlights the geometry drawn by its corresponding shaders in red – this is useful for finding the right program to work on.
- Clicking on the eyeball right next to each program hides the rendered geometry (useful in the likely case an author wants to focus solely on some geometry but not other, or to hide overlapping geometry).
- The tool is responsive when docked to the side.

## Editing Shader Programs

The first thing you’ll notice about Shader program code is that it is **not** JavaScript. For more information on how Shader programs work, I highly recommend you start with the WebGL demo on the [Khronos wiki](http://www.khronos.org/webgl/wiki/Tutorial#Creating_the_Shaders) and/or Paul Lewis’ excellent [HTML5 Rocks post](http://www.html5rocks.com/en/tutorials/webgl/shaders/). There also some great long standing tutorials on the [Learning WebGL](http://learningwebgl.com/blog/?page_id=1217) blog. The Shader Editor gives you direct access to the programs so you can play around with how they work:

- Editing code in any of the editors will compile the source and apply it as soon as the user stops typing;
- If an error was made in the code, the rendering won’t be affected, but an error will be displayed in the editor, highlighting the faulty line of code; hovering the icon gutter will display a tooltip describing the error.

Learn more about the [Shader Editor on the Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Tools/Shader_Editor/).

Here is a second screencast showing how you could directly edit the shader programs in the Epic Citadel demo:

## About Victor Porof

Mozillian, hacker, working on Firefox DevTools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

krisNovember 12th, 2013 at 10:59JsxNovember 13th, 2013 at 04:28ArasNovember 12th, 2013 at 11:20Victor PorofNovember 12th, 2013 at 11:23foxtrotNovember 12th, 2013 at 11:30Dusan BosnjakNovember 14th, 2013 at 15:48foxtrotNovember 15th, 2013 at 13:28AndyNovember 12th, 2013 at 14:03Victor PorofNovember 13th, 2013 at 00:10Benoit JacobNovember 14th, 2013 at 12:40pdNovember 13th, 2013 at 11:06LukeNovember 13th, 2013 at 20:43Victor PorofNovember 14th, 2013 at 03:25Patrick CozziNovember 16th, 2013 at 20:16makcNovember 21st, 2013 at 10:56Victor PorofNovember 25th, 2013 at 08:53makcNovember 25th, 2013 at 09:18