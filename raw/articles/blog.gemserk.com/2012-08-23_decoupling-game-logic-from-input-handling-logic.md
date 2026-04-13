---
title: Decoupling game logic from input handling logic
url: https://blog.gemserk.com/2012/08/23/decoupling-game-logic-from-input-handling-logic/
published: '2012-08-23'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In this post we want to share how we are decoupling our game logic from the input handling as we explained briefly in a [previous post](https://blog.gemserk.com/2011/08/09/multiple-android-controls-for-super-flying-thing/) about different controls we tested for Super Flying Thing.

### Introduction

There are different ways to handle the input in a game. Basically, you could have a framework that provides a way to define event handlers for each input event, or to poll input values from the API. [LibGDX](http://libgdx.badlogicgames.com/) provides both worlds so it is up to you what you consider best for your game. We prefer to poll for input values for the game logic itself.

When starting to make games, you probably feel tempted to add the input handling logic in one or more base concepts of your game, for example, if you were making Angry Birds you probably would add it to the Slingshot class to detect when to fire a bird or not. That is not totally bad if you are making a quick prototype but it is not recommended for long term because it would be harder to add or change between different control implementations.

### Abstracting the input

To improve a bit this scenario in our games, we are using an intermediary class named Controller. That class provides values more friendly and related with the game concepts. A possible Controller class for our example could be:

```
class SlingshotController {
boolean charging;
Vector2 direction;
}
```


Now, we could process the input handling in one part of the code and update a common Controller instance shared between it and the game logic. Something like this:

```
class SlingshotMouseControllerLogic extends InputListener {
Slingshot slingshot;
SlingshotController controller;
public boolean touchDown (InputEvent event, float x, float y, int pointer, int button) {
slingshotPosition = slingshot.getPosition();
controller.charging = slingshotPosition.isNear(x,y);
return controller.charging;
}
public void touchUp (InputEvent event, float x, float y, int pointer, int button) {
if (!controller.charging)
return;
controller.charging = false;
}
public void touchDragged (InputEvent event, float x, float y, int pointer) {
if (!controller.charging)
return;
slingshotPosition = slingshot.getPosition();
controller.direction.set(slingshotPosition);
controller.direction.sub(x,y);
}
}
```


Or if you are polling the input:

```
class SlingshotMouseControllerLogic implements Updateable {
Slingshot slingshot;
SlingshotController controller;
boolean touchWasPressed = false;
public void update(float delta) {
boolean currentTouchPressed = Gdx.input.isPressed();
slingshotPosition = slingshot.getPosition();
x = Gdx.input.getX();
y = Gdx.input.getY();
if (!touchWasPressed && currentTouchPressed) {
controller.charging = slingshotPosition.isNear(x,y);
touchWasPressed = true;
}
if(touchWasPressed && !currentTouchPressed) {
controller.charging = false;
touchWasPressed = false
}
if (!controller.charging)
return;
controller.direction.set(slingshotPosition);
controller.direction.sub(x,y);
}
}
```


Now, the Slingshot implementation will look something like this:

```
class Slingshot {
// multiple fields
// render logic
Controller controller;
boolean wasCharging = false;
update() {
if (controller.charging && !wasCharging) {
// starts to draw stuff based on the state we are now charging...
// charges a bird in the slingshot.
wasCharging = true;
} else if (!controller.charging && wasCharging) {
// stops drawing the slingshot as charging
// fires the bird!!
wasCharging = false;
}
// more stuff...
}
}
```


As you can see, the game concept Slingshot doesn’t know anything about input anymore and we could switch to use the keyboard, Xbox 360 Controller, etc, and the game logic will not notice the change.

### Conclusion

Decoupling your game logic from the input by abstracting it in a class is a good way to keep your game logic depending mainly on game concepts making it easier to understand and improving its design. Also, it is a good way to create several controls for the game (input, AI, network, recorded input, etc), while the game logic don’t even notice the change.

This post provides a really simple concept, the concept of abstraction, it is nothing new and probably most of the game developers are already doing this, even though we wanted to share it, maybe it is helpful for someone.

We tried to use simple and direct code in this post to increase understandability, however in our games, as we use an entity system framework, we do it a bit different using components, scripts and systems instead of direct classes for concepts like the class Slingshot we presented in this post, but that’s food for another blog post.

Finally, we use another abstraction layer over the framework input handling which provides us a better and simplified API to poll info from, that’s why we prefer to poll values, food for another post as well.

Hope you like it, as always.