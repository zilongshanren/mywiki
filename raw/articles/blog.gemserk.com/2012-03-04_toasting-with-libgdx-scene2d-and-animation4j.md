---
title: Toasting with LibGDX Scene2D and Animation4j
url: https://blog.gemserk.com/2012/03/04/toasting-with-libgdx-scene2d-and-animation4j/
published: '2012-03-04'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

For our latest Vampire Runner update we changed to use [LibGDX](http://libgdx.badlogicgames.com/) scene2d instead Android GUI. The main reason for the change is that we wanted to use a common GUI API for Android and PC, and sadly we can’t do that using Android API. With LibGDX scene2d we can code once and run in both platforms.

In particular, the toast feature of the Android API was really interesting to have and we want to share how we implemented it using LibGDX scene2d.

### Toasting

A toast is defined as a scene2d Window that shows some text and disappear after a while, this is a pseudo code to give the idea of how to create that toast window:

Actor toast(String text, float time, Skin skin) { Window window = new Window(skin); window.add(new Label(text, skin)); ... window.action(new Action() { act(float delta) { // update the animation // if the animation is finished, we remove the window from the stage. } }); ... return window; }

To animate the toast, we create a TimelineAnimation using [animation4j](https://github.com/gemserk/animation4j/) defining that the window should move from outside the screen to inside the screen, wait some time and then go out of the screen again. The code looks like this:

TimelineAnimation toastAnimation = Builders.animation( // Builders.timeline() // .value(Builders.timelineValue(window, Scene2dConverters.actorPositionTypeConverter) // .keyFrame(0f, new float[] { window.x, outsideY }) // .keyFrame(1f, new float[] { window.x, insideY }) // .keyFrame(4f, new float[] { window.x, insideY }) // .keyFrame(5f, new float[] { window.x, outsideY }) // ) // ) // .started(true) // .delay(0f) // .speed(5f / time) // .build();

That code creates a new animation which modifies the position of the Window each time update() method is called.

Of course, you can animate the Window using LibGDX custom Actions or another animation framework like [Universal Tween Engine](https://code.google.com/p/java-universal-tween-engine/), that is up to you.

If you want to see the code itself, you can see the Actor factory named [Actors](https://github.com/gemserk/commons-gdx/blob/7fecb83c85cce9a2bceb38b582bef3dde2a3e929/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/scene2d/Actors.java) at our [Github of commons-gdx](https://github.com/gemserk/commons-gdx).

In our subclass of Game, we added an empty Stage updated in each render() method, and a toast(string) method which creates a toast as explained before using default Skin and time.

MyGame extends Game { Stage stage; float defaultTime; Skin defaultSkin; render() { // all our game update and render logic ... stage.act(delta); stage.draw(); } toast(String text) { stage.add(Actors.toast(text, defaultTime, defaultSkin); } }

So, if we want to toast about something, we only have to call game.toast(“something”) and voilá.

You can see a running example of this, you can run the Gui.Scene2dToastPrototype of our [prototypes webstart](http://www.gemserk.com/prototipos/prototypes-release/launch-webstart.jnlp) (recommended), or watch the next video:

### Conclusion

Despite being a bit incomplete and buggy yet, scene2d API is almost easy to use and it is great if you want to do simple stuff.

Using scene2d is great for our simple need of GUI interfaces because we can quickly test all the stuff in PC. In Vampire Runner we are using scene2d for the feedback dialog, the new version available dialog and for the change username screen.

An interesting thing to have in mind when using scene2d API is that you can make your own Skin to achieve a more integrated look and feel.

As always, hope you like the post and could be of help.