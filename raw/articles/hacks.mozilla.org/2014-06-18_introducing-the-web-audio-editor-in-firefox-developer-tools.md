---
title: Introducing the Web Audio Editor in Firefox Developer Tools – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/06/introducing-the-web-audio-editor-in-firefox-developer-tools/
author: Jordan Santell
published: '2014-06-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In Firefox 32, the Web Audio Editor joins the Shader Editor and Canvas Debugger in Firefox Developer Tools for debugging media-rich content on the web. When developing HTML5 games or fun synthesizers using web audio, the Web Audio Editor assists in visualizing and modifying all of the audio nodes within the [web audio AudioContext](https://developer.mozilla.org/en-US/docs/Web/API/AudioContext).

## Visualizing the Audio Context

When working with the [Web Audio API](http://webaudio.github.io/web-audio-api/)‘s modular routing, it can be difficult to translate how all of the audio nodes are connected just by listening to the audio output. Often, it is challenging to debug our AudioContext just by listening to the output and looking at the imperative code that creates audio nodes. With the Web Audio Editor, all of the [AudioNodes](https://developer.mozilla.org/en-US/docs/Web/API/AudioNode) are rendered in a directed graph, illustrating the hierarchy and connections of all audio nodes. With the rendered graph, a developer can ensure that all of the nodes are connected in a way that they expect. This can be especially useful when the context becomes complex, with a network of nodes dedicated to manipulating audio and another for analyzing the data, and we’ve seen some [pretty impressive uses of Web Audio](http://webaudiodemos.appspot.com/Vocoder/) resulting in such graphs!

To enable the Web Audio Editor, open up the options in the Developer Tools, and check the “Web Audio Editor” option. Once enabled, open up the tool and reload the page so that all web audio activity can be monitored by the tool. When new audio nodes are created, or when nodes are connected and disconnected from one another, the graph will update with the latest representation of the context.

## Modifying AudioNode Properties

Once the graph is rendered, individual audio nodes can be inspected. Clicking on an AudioNode in the graph opens up the audio node inspector where [AudioParam](https://developer.mozilla.org/en-US/docs/Web/API/AudioParam)‘s and specific properties on the node can be viewed and modified.

## Future Work

This is just our first shippable release of the Web Audio Editor, and we are looking forward to making this tool more powerful for all of our audio developers.

- Visual feedback for nodes that are playing, and time/frequency domain visualizations.
- Ability to create, connect and disconnect audio nodes from the editor.
- Tools for debugging
[onaudioprocess](https://developer.mozilla.org/en-US/docs/Web/API/ScriptProcessorNode#Event_handlers)events and audio glitches. - Display additional AudioContext information and support multiple contexts.
- Modify more than just primitives in the node inspector, like adding an AudioBuffer.

We have many [dream features and ideas](https://gist.github.com/jsantell/ee1be41bc87968d7b170) that we’re excited about, and you can view all [open bugs](https://bugzilla.mozilla.org/buglist.cgi?component=Developer%20Tools%3A%20Web%20Audio%20Editor&product=Firefox&bug_status=__open__&list_id=10101182) for the Web Audio Editor or [submit new bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox&component=Developer%20Tools%3A%20Web%20Audio%20Editor). Be sure to check out the [MDN documentation](https://developer.mozilla.org/en-US/docs/Tools/Web_Audio_Editor) on the Web Audio Editor and we would also love [feedback and thoughts at our UserVoice feedback channel](http://mzl.la/devtools) and on [Twitter @firefoxdevtools](http://twitter.com/firefoxdevtools).

## About
[
Jordan Santell ](http://jsantell.com)

Mozillian, audio tools & SDK hacker, web audio nerd, metal head

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

Carl SutherlandJune 18th, 2014 at 11:07Jordan SantellJune 18th, 2014 at 11:24Simon SpeichJune 25th, 2014 at 03:22JanJune 29th, 2014 at 13:52DominikJune 18th, 2014 at 12:23Paul RougetJune 18th, 2014 at 12:37DominikJune 19th, 2014 at 02:48K. GaddJune 18th, 2014 at 18:13DominikJune 19th, 2014 at 02:49AlexJune 20th, 2014 at 04:31Jordan SantellJune 20th, 2014 at 10:25AlexJune 20th, 2014 at 10:49Jordan SantellJune 20th, 2014 at 16:24AlexJune 20th, 2014 at 23:02Anthony BaxterJune 21st, 2014 at 20:26Ukash KartJuly 1st, 2014 at 07:34