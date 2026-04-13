---
title: Our solution to handle multiple screen sizes in Android – Part two
url: https://blog.gemserk.com/2013/02/13/our-solution-to-handle-multiple-screen-sizes-in-android-part-two/
published: '2013-02-13'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Continuing with the [previous blog post](https://blog.gemserk.com/2013/01/22/our-solution-to-handle-multiple-screen-sizes-in-android-part-one), in this post we are going to talk about the code behind the theory. It consists in three concepts, the VirtualViewport, the OrthographicCameraWithVirtualViewport and the MultipleVirtualViewportBuilder.

### VirtualViewport

It defines a virtual area where the game stuff is contained and provides a way to get the real width and height to use with a camera in order to always show the virtual area. Here is the code of this class:

```
public class VirtualViewport {
float virtualWidth;
float virtualHeight;
public float getVirtualWidth() {
return virtualWidth;
}
public float getVirtualHeight() {
return virtualHeight;
}
public VirtualViewport(float virtualWidth, float virtualHeight) {
this(virtualWidth, virtualHeight, false);
}
public VirtualViewport(float virtualWidth, float virtualHeight, boolean shrink) {
this.virtualWidth = virtualWidth;
this.virtualHeight = virtualHeight;
}
public float getWidth() {
return getWidth(Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
}
public float getHeight() {
return getHeight(Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
}
/**
* Returns the view port width to let all the virtual view port to be shown on the screen.
*
* @param screenWidth
* The screen width.
* @param screenHeight
* The screen Height.
*/
public float getWidth(float screenWidth, float screenHeight) {
float virtualAspect = virtualWidth / virtualHeight;
float aspect = screenWidth / screenHeight;
if (aspect > virtualAspect || (Math.abs(aspect - virtualAspect) < 0.01f)) {
return virtualHeight * aspect;
} else {
return virtualWidth;
}
}
/**
* Returns the view port height to let all the virtual view port to be shown on the screen.
*
* @param screenWidth
* The screen width.
* @param screenHeight
* The screen Height.
*/
public float getHeight(float screenWidth, float screenHeight) {
float virtualAspect = virtualWidth / virtualHeight;
float aspect = screenWidth / screenHeight;
if (aspect > virtualAspect || (Math.abs(aspect - virtualAspect) < 0.01f)) {
return virtualHeight;
} else {
return virtualWidth / aspect;
}
}
}
```


So, if we have a virtual area of 640x480 and want to show it on a screen of 800x480 we can do the next steps in order to get the proper values that we have to use as the camera viewport for that screen:

```
VirtualViewport virtualViewport = new VirtualViewport(640, 480);
float realViewportWidth = virtualViewport.getWidth(800, 480);
float realViewportHeight = virtualViewport.getHeight(800, 480);
// now set the camera viewport values
camera.setViewportFor(realViewportWidth, realViewportHeight);
```


### OrthographicCameraWithVirtualViewport

In order to simplify the work when using LibGDX library, we created a subclass of LibGDX’s OrthographicCamera with specific behavior to update the camera viewport using the VirtualViewport values. Here is its code:

```
public class OrthographicCameraWithVirtualViewport extends OrthographicCamera {
Vector3 tmp = new Vector3();
Vector2 origin = new Vector2();
VirtualViewport virtualViewport;
public void setVirtualViewport(VirtualViewport virtualViewport) {
this.virtualViewport = virtualViewport;
}
public OrthographicCameraWithVirtualViewport(VirtualViewport virtualViewport) {
this(virtualViewport, 0f, 0f);
}
public OrthographicCameraWithVirtualViewport(VirtualViewport virtualViewport, float cx, float cy) {
this.virtualViewport = virtualViewport;
this.origin.set(cx, cy);
}
public void setPosition(float x, float y) {
position.set(x - viewportWidth * origin.x, y - viewportHeight * origin.y, 0f);
}
@Override
public void update() {
float left = zoom * -viewportWidth / 2 + virtualViewport.getVirtualWidth() * origin.x;
float right = zoom * viewportWidth / 2 + virtualViewport.getVirtualWidth() * origin.x;
float top = zoom * viewportHeight / 2 + virtualViewport.getVirtualHeight() * origin.y;
float bottom = zoom * -viewportHeight / 2 + virtualViewport.getVirtualHeight() * origin.y;
projection.setToOrtho(left, right, bottom, top, Math.abs(near), Math.abs(far));
view.setToLookAt(position, tmp.set(position).add(direction), up);
combined.set(projection);
Matrix4.mul(combined.val, view.val);
invProjectionView.set(combined);
Matrix4.inv(invProjectionView.val);
frustum.update(invProjectionView);
}
/**
* This must be called in ApplicationListener.resize() in order to correctly update the camera viewport.
*/
public void updateViewport() {
setToOrtho(false, virtualViewport.getWidth(), virtualViewport.getHeight());
}
}
```


### MultipleVirtualViewportBuilder

This class allows us to build a better VirtualViewport given the minimum and maximum areas we want to support performing the logic we explained in the [previous post](https://blog.gemserk.com/2013/01/22/our-solution-to-handle-multiple-screen-sizes-in-android-part-one/). For example, if we have a minimum area of 800x480 and a maximum area of 854x600, then, given a device of 480x320 (3:2) it will return a VirtualViewport of 854x570 which is a good match of a resolution which contains the minimum area and is smaller than the maximum area and has the same aspect ratio of 480x320.

```
public class MultipleVirtualViewportBuilder {
private final float minWidth;
private final float minHeight;
private final float maxWidth;
private final float maxHeight;
public MultipleVirtualViewportBuilder(float minWidth, float minHeight, float maxWidth, float maxHeight) {
this.minWidth = minWidth;
this.minHeight = minHeight;
this.maxWidth = maxWidth;
this.maxHeight = maxHeight;
}
public VirtualViewport getVirtualViewport(float width, float height) {
if (width >= minWidth && width <= maxWidth && height >= minHeight && height <= maxHeight)
return new VirtualViewport(width, height, true);
float aspect = width / height;
float scaleForMinSize = minWidth / width;
float scaleForMaxSize = maxWidth / width;
float virtualViewportWidth = width * scaleForMaxSize;
float virtualViewportHeight = virtualViewportWidth / aspect;
if (insideBounds(virtualViewportWidth, virtualViewportHeight))
return new VirtualViewport(virtualViewportWidth, virtualViewportHeight, false);
virtualViewportWidth = width * scaleForMinSize;
virtualViewportHeight = virtualViewportWidth / aspect;
if (insideBounds(virtualViewportWidth, virtualViewportHeight))
return new VirtualViewport(virtualViewportWidth, virtualViewportHeight, false);
return new VirtualViewport(minWidth, minHeight, true);
}
private boolean insideBounds(float width, float height) {
if (width < minWidth || width > maxWidth)
return false;
if (height < minHeight || height > maxHeight)
return false;
return true;
}
}
```


In case the aspect ratio is not supported, it will return the minimum area.

### Floating elements

As we explained in the previous post, there are some cases where we need stuff that should be always at fixed positions in the screen, for example, the audio and music buttons in Clash of the Olympians. In order to do that we need to make the position of those buttons depend on the VirtualViewport. In the next section where we explain how to use all together we show an example of how to do a floating element.

### Using the code together

Finally, here is an example showing how to use these concepts in a LibGDX application:

```
public class VirtualViewportExampleMain extends com.badlogic.gdx.Game {
private OrthographicCameraWithVirtualViewport camera;
// extra stuff for the example
private SpriteBatch spriteBatch;
private Sprite minimumAreaSprite;
private Sprite maximumAreaSprite;
private Sprite floatingButtonSprite;
private BitmapFont font;
private MultipleVirtualViewportBuilder multipleVirtualViewportBuilder;
@Override
public void create() {
multipleVirtualViewportBuilder = new MultipleVirtualViewportBuilder(800, 480, 854, 600);
VirtualViewport virtualViewport = multipleVirtualViewportBuilder.getVirtualViewport(Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
camera = new OrthographicCameraWithVirtualViewport(virtualViewport);
// centers the camera at 0, 0 (the center of the virtual viewport)
camera.position.set(0f, 0f, 0f);
// extra code
spriteBatch = new SpriteBatch();
Pixmap pixmap = new Pixmap(64, 64, Format.RGBA8888);
pixmap.setColor(Color.WHITE);
pixmap.fillRectangle(0, 0, 64, 64);
minimumAreaSprite = new Sprite(new Texture(pixmap));
minimumAreaSprite.setPosition(-400, -240);
minimumAreaSprite.setSize(800, 480);
minimumAreaSprite.setColor(0f, 1f, 0f, 1f);
maximumAreaSprite = new Sprite(new Texture(pixmap));
maximumAreaSprite.setPosition(-427, -300);
maximumAreaSprite.setSize(854, 600);
maximumAreaSprite.setColor(1f, 1f, 0f, 1f);
floatingButtonSprite = new Sprite(new Texture(pixmap));
floatingButtonSprite.setPosition(virtualViewport.getVirtualWidth() * 0.5f - 80, virtualViewport.getVirtualHeight() * 0.5f - 80);
floatingButtonSprite.setSize(64, 64);
floatingButtonSprite.setColor(1f, 1f, 1f, 1f);
font = new BitmapFont();
font.setColor(Color.BLACK);
}
@Override
public void resize(int width, int height) {
super.resize(width, height);
VirtualViewport virtualViewport = multipleVirtualViewportBuilder.getVirtualViewport(Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
camera.setVirtualViewport(virtualViewport);
camera.updateViewport();
// centers the camera at 0, 0 (the center of the virtual viewport)
camera.position.set(0f, 0f, 0f);
// relocate floating stuff
floatingButtonSprite.setPosition(virtualViewport.getVirtualWidth() * 0.5f - 80, virtualViewport.getVirtualHeight() * 0.5f - 80);
}
@Override
public void render() {
super.render();
Gdx.gl.glClearColor(1f, 0f, 0f, 1f);
Gdx.gl.glClear(GL10.GL_COLOR_BUFFER_BIT);
camera.update();
// render stuff...
spriteBatch.setProjectionMatrix(camera.combined);
spriteBatch.begin();
maximumAreaSprite.draw(spriteBatch);
minimumAreaSprite.draw(spriteBatch);
floatingButtonSprite.draw(spriteBatch);
font.draw(spriteBatch, String.format("%1$sx%2$s", Gdx.graphics.getWidth(), Gdx.graphics.getHeight()), -20, 0);
spriteBatch.end();
}
public static void main(String[] args) {
LwjglApplicationConfiguration config = new LwjglApplicationConfiguration();
config.title = VirtualViewportExampleMain.class.getName();
config.width = 800;
config.height = 480;
config.fullscreen = false;
config.useGL20 = true;
config.useCPUSynch = true;
config.forceExit = true;
config.vSyncEnabled = true;
new LwjglApplication(new VirtualViewportExampleMain(), config);
}
}
```


In the example there are three colors, green represents the minimum supported area, yellow the maximum supported area and red represents the area outside. If we see red it means that aspect ratio is not supported. There is a floating element colored white, which is always relocated in the top right corner of the screen, unless we are on an unsupported aspect ratio, in that case it is just located in the top right corner of the green area.

The next video shows the example in action:

UPDATE: you can download the source code to run on Eclipse from [here](https://drive.google.com/uc?export=download&id=0BzsSBPfIxwK_a0Y0Unc0aHBDaHc).

### Conclusion

In these two blog posts we explained in a simplified way how we managed to support different aspect ratios and resolutions for Clash of the Olympians, a technique that could be used as an acceptable way of handling different screen sizes for a wide range of games, and it is not hard to use.

As always, we hope you liked it and that it could be useful for you when developing your games. Opinions and suggestions are always welcome if you want to comment 🙂 and also share it if you liked it and think other people could benefit from this code.

Thanks for reading.