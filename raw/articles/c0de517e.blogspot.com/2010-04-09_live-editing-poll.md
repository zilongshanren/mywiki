---
title: Live-editing poll
url: http://c0de517e.blogspot.com/2010/04/live-editing-poll.html
published: '2010-04-09'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*p.s. the item descriptions are too long, they are wrapped when voting but now when visualizing the results. If you want to view the results the numbers will be hidden. I'll post the results and an analysis here, but if you want, copying the window and pasting it works...*

## 6 comments:

My vote is for Other. :)


On the last console engine I worked with, the binary cooking tools were tightly integrated with real-time editing and a streaming system. In essence every asset in the game was "cooked" into a binary blob that was streamed into memory on the target console. Real-time edits were performed by re-cooking the asset on the PC then transmitting it to the target console over a socket.

The in memory structure of that asset would be changed, while the game was running. It many cases this would work fine, as long as the code read the values from the cooked memory directly, rather then using a cached copy. In other cases, the runtime would have special handling functions which would tear down and recreate the assets from scratch, using the newly updated version.

To see the poll results in Firefox it's a good idea to right click on it and select This Frame / Show Only This Frame.

Reg: you can also highlight some of the text and a scroll bar will appear, but anyway the vote seems stable now, as soon as I have some time I will write a report on it

In my hobby project the game can run inside the editor. The editor is mostly a GUI(using Winform) to the editing functionality that's part of the game. The exceptions are import of assets, and serialization. This is mostly because I use XNA and those parts are only available on Windows, but I'm not sure I would like them in my game code anyway.


The engine we use at work don't have much in the way of live editing unfortunately.

Hello, thanks for your comment on my blog. I agree with you I'll try to write something less boring... thanks again for your time! =)

Oh yeah, just one more thing... I can't comment about your blog since I'm not knowledgeable enough to tell you what to code/write, instead of just accepting what I like among your articles... =P

Post a Comment