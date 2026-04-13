---
title: How To Offset UE4 Pop-Up Notifications
url: https://allarsblog.com/2020/07/25/how-to-offset-ue4-pop-up-notifications/
author: Michael Allar
published: '2020-07-25'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

I made a tutorial about how to move the notifications that the Unreal Engine editor can spew in case you... need to move them.

Basically, just modify the following in Engine\Source\Runtime\Slate\Private\Framework\Notifications\NotificationManager.cpp:

```
namespace NotificationManagerConstants
{
// Offsets from the bottom-right corner of the work area
const FVector2D NotificationOffset( 15.0f + 1520.0f, 15.0f + 360.f);
}
```