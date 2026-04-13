---
title: Shadowmap bias notes
url: http://c0de517e.blogspot.com/2011/05/shadowmap-bias-notes.html
published: '2011-05-13'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Hey, Thanks for that! I just implemented that into our pre-pass lighting renderer and it works much better then our previous bias (via the projection matrix).

Oh cool! I'm still catching up with GDC, too busy, I saw that website a while ago though and yes its exactly the same idea, I just didn't want to pay the price of fetching normals in our deferred shadowin pass so ended up using the view vector insted. Really stupid trick but it seems to solve a lot of shadow acne problems. These are some sketches I did at work to think about the biases and how o correctly use them, then I added the text and took two pictures with my cellphone...

## 3 comments:

Hey, Thanks for that! I just implemented that into our pre-pass lighting renderer and it works much better then our previous bias (via the projection matrix).

Sounds a lot like "Normal Offset Shadows" from GDC2011 poster? http://www.dissidentlogic.com/

Oh cool! I'm still catching up with GDC, too busy, I saw that website a while ago though and yes its exactly the same idea, I just didn't want to pay the price of fetching normals in our deferred shadowin pass so ended up using the view vector insted. Really stupid trick but it seems to solve a lot of shadow acne problems. These are some sketches I did at work to think about the biases and how o correctly use them, then I added the text and took two pictures with my cellphone...

Post a Comment