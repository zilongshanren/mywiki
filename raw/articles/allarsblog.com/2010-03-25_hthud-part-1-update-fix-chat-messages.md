---
title: 'HTHUD: Part 1 - Update: Fix Chat Messages'
url: https://allarsblog.com/2010/03/25/hthud-part-1-update-fix-chat-messages/
author: Michael Allar
published: '2010-03-25'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

I've stumbled across something I forgot to include in HTHUD: Part 1, and that is two lines of code that display our console and chat messages.

It directly fixes PrintScreenDebug() if you are using that function.

### HTHUD

[csharp]function DrawGameHud()

{

DisplayLocalMessages();

DisplayConsoleMessages();

DrawLivingHud();

}[/csharp]