---
title: Archers Vs Zombies - Dev Log - Controls
url: https://blog.gemserk.com/2011/04/18/archers-vs-zombies-dev-log-controls/
published: '2011-04-18'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

This post is an introduction and analysis of different type of game controls I am working in order to improve the game playability.

To control the bow I need to know basically the next stuff:

- direction or angle of the shot
- power
- if it is being charging or not
- if should fire or not

Each proposed bow control provides this stuff in its own way (using one or multiple touch, using the keyboard, etc). I will explain how each one achieve that, and comment some pros and cons I think they have as controllers.

### Type 1

The player presses one position in the screen, drags the pointer to another position and then releases it to fire the arrow. The angle is calculated by the difference vector between the pointer pressed position and the pointer released position and the power is calculated by the length of that vector.

```
<br />
when pointer released:<br />
vector p0 = pointer.pressedPosition<br />
vector p1 = pointer.releasedPosition<br />
diff = p0.sub(p1)<br />
angle = diff.angle()<br />
power = diff.length()<br />
```


#### Pros

- It is supposed to simulate the movement an archer does when he fires a real bow

#### Cons

- turned out to be non-intuitive

### Type 2

The player presses some point in the screen, drags the pointer to the position he wants and then releases it to fire the arrow. Optionally, the arrow could be fired in the moment the screen is pressed instead when it is released. The angle is calculated by the difference vector between the pointer position and the bow position, and the power by its length.

```
<br />
when pointer released:<br />
vector p = pointer.releasedPosition<br />
diff = p.sub(bowPosition)<br />
angle = diff.angle()<br />
power = diff.length()<br />
```


#### Pros

- Easy to control and provides a way to shoot really fast

### Type 3

Similar to the others, the player pointer is pressed, dragged an released to fire the arrow. The angle is calculated by multiplying the y coordinate of the pointer position by a factor, and the power is calculated by the x coordinate multiplied by a factor too.

```
<br />
when pointer released:<br />
vector p = pointer.releasedPosition<br />
angle = p.y * c1<br />
power = p.x * c2<br />
```


#### Pros

- Easy to control too, when you want more fire power you move to the right, when you want less you move to the left. In a similar way, if you want to increment the fire angle move the pointer up, if you want to decrement it, move the pointer down.

#### Cons

- It is not clear the relationship between the angle and the y coordinate and between the power and the x coordinate

### Type 4

It is similar to the the first type but both positions are specified by two different pointers of a multi touch device.

```
<br />
vector p0 = pointer0.position<br />
vector p1 = pointer1.position<br />
diff = p0.sub(p1)<br />
angle = diff.angle()<br />
power = diff.length()<br />
```


#### Pros

- We are taking advantage of multi touch device capabilities
- It is supposed to simulate firing a real bow
- By holding one touch you could press and release the other to fire arrows quickly

#### Cons

- Requires a multi touch device
-
- Multi touch feature doesn’t work so well on some multi touch devices
- In devices with small screens using multi touch could require a lot of screen space, that means less space to see what is happening in the game</ul> ### Type 5


`The idea is to modify the angle of the bow by touching up/down keys and control the bow power by holding space key, the arrow is fired after space key was released (could be another key mapping). `<br /> when up pressed:<br /> increase angle<br /> when down pressed:<br /> decrease angle<br /> when space pressed:<br /> increment power<br /> when space released:<br /> fire and reset power to 0<br /> ` Pros * Seems to be a natural way to control the bow and used in similar games ([Castle Attack](http://www.youtube.com/watch?v=EtQoxiwpz3o), [Epic War](http://www.freewebarcade.com/game/epic-war/), [Worms](http://www.youtube.com/watch?v=ROxvkCu5_fo), etc) Cons * Hardware keyboard is required, it will not work on common android devices * Could be a bit slow for the game I have in mind ## Conclusion After working on different types of controls, I realized that the needed stuff to control the bow could be separated in sub controllers, one for the angle, one for the power and others. Using this approach, it will be easy to create mixed controls like, for example, angle is modified by the arrow keys and power by a relative pointer position to the bow, or make a controller like type 2 where the power depends on the pressed time instead the distance of the pointer position to the bow. For touch devices, I want to try also HUD elements like slide bars and buttons to control the bow as some games does ([Minigore](http://www.youtube.com/watch?v=smdQE8OI2cE)). Game mechanics are not defined yet. One thing to notice is that some controls will not work with a fast paced game where you have to shoot several arrows to kill incoming enemies, other controls will not work with slow paced games where you have to aim exactly where you want each arrow and more strategy is needed like, for example, deciding which enemy to kill first. Some of the listed types will be implemented, plus an easy way to switch between them, so they could be tested. After that, I hope you could give them a try and tell me what do you think. Thanks for reading. UPDATE: I added to the [latest development version](http://www.gemserk.com/prototipos/archervsworld-latest/launch-webstart.jnlp) (probably buggy) a way switch between different bow controllers by touching a button on the top right corner of the screen. For now, you have to discover yourself each controller 😀 (I forgot to put some controller label in some place).`

-