---
title: Finally, online multiplayer!
url: https://etodd.io/2010/02/08/finally-online-multiplayer/
published: '2010-02-08'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Finally, online multiplayer!

I've updated the browser plugin to finally support full online multiplayer! [Go try it!](http://a3p.sourceforge.net/play.html) I think the plugin is now stable enough that I am promoting it as the officially recommended method of playing the game. :)

Of course, there are still some problems. Namely, in Internet Explorer the mouse control doesn't work. Testing so far has shown Firefox 3 and Chrome (on Windows) handle the game very well.

So give it a whirl, and please post any errors or bugs you get, along with your OS and browser!

[edit] Complete feature list:

- The lobby server is finally live!
- Reloading and clips. Units that are reloading are highlighted to show their vulnerability.
- Shadow mapping
- New map: "Orbital"
- Improved unit controls: you can only buy two helper units now, but you can control them more easily with the Q and E keys.
- New weapon: Pistol. Shoots darts capable of pinning enemies to the wall in certain circumstances.
- Shattering glass; AI bots can't see or pathfind through the glass. You can shoot the glass to let them through, or leave it and use it to your advantage.
- Drastically improved network performance and reliability. In addition to a slew of bug fixes and optimizations, the new network code uses data compression and client-side interpolation to keep things running smooth. Bandwidth usage was cut down by about 60% in some cases.