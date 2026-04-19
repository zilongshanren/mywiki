---
title: 'WebPad: Bring your Own Controller'
url: https://claire-blackshaw.com/blog/2011/09/webpad-bring-your-own-controller/
author: Claire Blackshaw
published: '2011-09-09'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![WebPad: Bring your Own Controller](../../assets/4e402aebc4c1a4e8.png)


WiiU vs Everyone

![](/images/Blog/wiiu-300x300.png)

Going to take a break from my Useless Designer series to talk about a personal project which has me very excited. While [judging Dare](http://www.claire-blackshaw.com/blog/2011/08/judging-daring-doers/) I came across a good idea which could be brilliant: using a mobile device as the controller in a shared space. The idea was shown by[ Lucky Ghost](http://daretobedigital.com/team-information-2011/team.php?idTeam=1547) using the iPhone and a native iOS app. However, Apple would never let it through the AppStore and not everyone likes Apple. The idea was good but limited, but then a solution hit me there and then and I excitedly shared it with them.

The game hosts a web-service providing HTML5 WebApp with WebSockets transforming any modern mobile device into the controller.

This is of course intended to take place over a WiFi or LAN connection. The concept of a controller which is mutable, touch-screen joy, and capable of delivering privileged information to the player is exciting and could break new genres. Just look up your nearest designer.

Playing a game in a shared space using the power of a computer (or console) to show pretty graphics and using a common space, while at the same time having the ability to display privileged information is really interesting. Consider card games, inventory management or the popular party game Werewolf. The simplest concept is pure conversions of mechanics from board games and similar, but the more advanced ideas are truly exciting.

Something the Wii-U touches on with its single controller, but fails to take far enough, is the brilliance of privileged information. Not to mention the cost barrier that the Wii-U introduces, perhaps if they allowed the DS with download-play to function as a Wii-U style controller it would be cool but I digress... the real point is that people already own phones, tablets and netbooks, removing the cost barrier specific hardware introduces.

### Pros & Cons of a Web App with WebSockets

## Pros |
## Cons |
| Code Once - HTML5 All Modern Platforms | Per browser / device follies can break this (>_<) |
| No Install, Always up to Date | Deliver of Assests |
| Normal TCP Sockets | No UDP option |
| Device is powerful thin client Can handle processing client-side | Network Latency must be designed around |
| Touch Screen == Contextual Controls | Web Sockets & HTML5 are moving targets |

This idea fizzed over and my brain immediately started suggesting ideas. I mentioned it to some dev friends and they had ideas of their own. It was clear there was a demand for this and it dawned on me to write a library which supplies the framework to quickly develop games with WebPad controllers.

With Unity, which is one of my favourite environments to roll home projects in while being popular with indies, I set out to make a Library for the Asset Store. After some fun with Unity & threads along with the joys of working with an in development spec, thank you [WebSockets](http://en.wikipedia.org/wiki/WebSocket). Working with a moving spec is a joy I could write another post about. Still, the person who wrote the hybi-00 handshake /response spec should be shot! But I digress...

I just wanted to share this concept that has me so excited. So after getting a rough prototype together I fired an email off to Unity Asset store guys looking for advice on how to distro code securely on the store but still haven’t got a response. So now I’m considering just making it an open source project and throwing it up on GitHub.

Would love to hear thoughts on this and I’ll post again when the project is ready for general use.