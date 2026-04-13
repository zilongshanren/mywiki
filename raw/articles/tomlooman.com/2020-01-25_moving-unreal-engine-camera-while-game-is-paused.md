---
title: Moving Unreal Engine Camera While Game Is Paused
url: https://tomlooman.com/unreal-engine-moving-camera-paused/
author: Tom Looman
published: '2020-01-25'
source_blog: Tom Looman
source_site: https://www.tomlooman.com/
category: unreal engine
fetched: '2026-04-13'
---

You can continue to move/rotate your camera while game logic is PAUSED in Unreal Engine. Unfortunately, it’s a little obscure to set up so here is a quick overview with C++.

```
PlayerController::bShouldPerformFullTickWhenPaused (true) // Allows Camera Updates during PlayerController Tick.
```


```
UWorld::bIsCameraMoveableWhenPaused (true) // Fixes TXAA/MotionBlur glitches.
```


*bIsCameraMoveableWhenPaused* doesn’t actually allow rotation itself but fixes TAA and MotionBlur while paused.

Here is an example of exposing this to Blueprint:

```
void ULZGameplayStatics::SetCameraMoveableWhenPaused(const UObject* WorldContextObject, bool bNewIsMoveable)
{
if (ensure(WorldContextObject))
{
WorldContextObject->GetWorld()->bIsCameraMoveableWhenPaused = bNewIsMoveable;
}
}
```


Finally, make sure your InputEvent related to camera input executes while paused using **ExecuteWhenPaused** checkbox.

![](../../assets/0f33104b4669a7a7.jpg)


This checkbox isn’t necessary when used inside PlayerController since the FullTick checkbox enables **full** processing of input! (which may be an undesirable side effect, make sure your other PlayerController input is manually blocked as needed using **IsGamePaused**-node)

That’s it! You may need to enable **TickEvenWhilePaused** in whatever Pawn/Actor is performing logic related to your camera input in its Tick function.