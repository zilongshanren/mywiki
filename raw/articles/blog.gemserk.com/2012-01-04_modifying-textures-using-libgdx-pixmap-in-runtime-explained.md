---
title: Modifying textures using libGDX Pixmap in runtime - Explained
url: https://blog.gemserk.com/2012/01/04/modifying-textures-using-libgdx-pixmap-in-runtime-explained/
published: '2012-01-04'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We have previously shown a bit how we were using LibGDX Pixmap to modify textures in runtime [here](https://blog.gemserk.com/2011/10/06/modifying-textures-using-libgdx-pixmap-in-runtime/) and [here](https://blog.gemserk.com/2011/10/10/detecting-collisions-using-libgdx-pixmap/) for a game prototype we were doing. In this post I want to share more detail of how we do that. The objective was to make destructible terrain like in Worms 2.

### Introduction

When you work with OpenGL textures, you can’t directly modify their pixels whenever you want since they are on OpenGL context. To modify them you have to upload an array of bytes using glTexImage2D or glTexSubImage2D. The problem is you have to maintain on the application side an array of bytes representing the modifications you want to do.

To simplify working with byte arrays representing images, [LibGDX](https://code.google.com/p/libgdx) provides a useful class named [Pixmap](https://code.google.com/p/libgdx/source/browse/trunk/gdx/src/com/badlogic/gdx/graphics/Pixmap.java) which is a map of pixels kept in local memory with some methods to interact with a native library to perform all modifications with better performance.

### Moving data from Pixmap to OpenGL Texture

In our prototypes, we wanted to remove part of the terrain whenever a missile touches it, like a Worms 2 explosion. That means we need some way to detect the collisions between the missile and the terrain and then a way to remove pixels from a texture.

We simplified the first problem by getting the color of the pixel only for the missile’s position and checking if it was transparent or not. A more correct solution could be using a bitmap mask to check collisions between pixels but we wanted to simplify the work for now.

For the second problem, given a radius of explosion of the missile, we used the pixmap fillCircle method by previously setting the color to (0,0,0,0) (fully transparent) and disabled Pixmap blending to override those pixels.

But that only modified the pixmap data, now we needed to modify the OpenGL texture. To do that, we called OpenGL glTexImage2D using the bytes of the pixmap as the new texture data and that worked correctly.

### Transforming from world coordinates to Pixmap coordinates

One problem when working with pixmaps is we have to map world coordinates (the position of the missile for example) to coordinates inside the Pixmap.

![](../../assets/75231cb111ed0b7a.png)


This image shows the coordinate system of the Pixmap, it goes from 0 to width in x and 0 to height in y.

![](../../assets/07c2409531167cbe.png)


This image shows how we normally need to move, rotate and resize the Pixmap in a game.

To solve this, we are using a LibGDX [Sprite](https://code.google.com/p/libgdx/source/browse/trunk/gdx/src/com/badlogic/gdx/graphics/g2d/Sprite.java) to maintain the Pixmap transformation, so we can easily move, rotate and scale it. Then, we can use that information to project a world coordinate to Pixmap coordinate by applying the inverse transform, here is the code:

```
public void project(Vector2 position, float x, float y)
{
position.set(x, y);
float centerX = sprite.getX() + sprite.getOriginX();
float centerY = sprite.getY() + sprite.getOriginY();
position.add(-centerX, -centerY);
position.rotate(-sprite.getRotation());
float scaleX = pixmap.getWidth() / sprite.getWidth();
float scaleY = pixmap.getHeight() / sprite.getHeight();
position.x *= scaleX;
position.y *= scaleY;
position.add( //
pixmap.getWidth() * 0.5f, //
-pixmap.getHeight() * 0.5f //
);
position.y *= -1f;
}
```


(note: it is the first version at least, it could have bugs and could be improved also)

To simplify our work with all this stuff, we created a class named [PixmapHelper](https://github.com/gemserk/angryships/blob/c497c2786594380dd195096a2af521e98566526a/angryships-core/src/main/java/com/gemserk/prototypes/pixmap/PixmapHelper.java) which manage a Pixmap, a Texture and a Sprite, so we could move the Sprite wherever we wanted to and if we modify the pixmap through the PixmapHelper then the Texture was automatically updated and hence the Sprite (since it uses internally the Texture).

The next video shows how we tested the previous work in a prototype were we simulated cluster bombs (similar to Worms 2):

### Some adjustments to improve performance

Instead of always working with a full size Pixmap by modifying it and then moved to the OpenGL texture, we created smaller Pixmaps of fixed sizes: 32x32, 64x64, etc. Then, each time we needed to make an explosion, we used the best Pixmap for that explosion and then we called glTexSubImage2D instead glTexImage2D to avoid updating untouched pixels. One limitation of this modification is we have to create and maintain several fixed size pixmaps depending on the modification size. Our current greater quad is 256x256 (almost never used).

Then, we changed to store each modification instead performing them in the moment the PixmapHelper erase method was called, and we added an update method which performs all modifications together. This improvement allow us to call Pixmap update method when we wanted, maybe one in three game updates or things like that.

### Conclusion

Despite using LibGDX Pixmap for better performance, moving data to and from OpenGL context is not a cheap operation, on Android devices this could means some pauses when refreshing the modified textures with the new data. However, there is a lot of space for performance improvement, some ideas are to work only with pixmap of less bits instead RGBA8888 and use that one as the collisions context and as the mask of the real image (even using shaders), between other ideas.

Finally, the technique looks really nice and we believe that it could be used without problems for a simple game but it is not ready yet to manage a greater game like Worms 2.

Hope you like the technique and if you use it, maybe even also share your findings.

P.S.: In case you were wondering: yes, I love Worms 2.