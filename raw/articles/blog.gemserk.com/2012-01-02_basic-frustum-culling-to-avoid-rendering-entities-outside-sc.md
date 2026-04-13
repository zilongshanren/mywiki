---
title: Basic frustum culling to avoid rendering entities outside screen
url: https://blog.gemserk.com/2012/01/02/basic-frustum-culling-to-avoid-rendering-entities-outside-screen/
published: '2012-01-02'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As we were having some performance issues with Vampire Runner and we didn’t have a clear idea of what was happening, we started trying some improvement techniques. The first one we implemented was a basic frustum culling technique to avoid trying to render objects outside of the screen.

### Basic implementation

First, we created an Artemis component named FrustumCullingComponent with a Rectangle representing the bounds of that entity to easily detect if the entity is inside the screen or not. For now, as it is a basic implementation, the rectangle was only modified when the entity was created. So, for example, if we know an entity was able to rotate during the game, then we create a bigger bounding box using box diagonal.

Then, we added a method to our custom 2d Camera implementation to get the camera frustum (by making the corresponding transformations).

Finally, we modified our Artemis render system to check before rendering if an entity has or not a FrustumCullingComponent, if it hasn’t one, then we perform the render logic as we always did. If it has one, then we check if the bounds of that entity overlaps with the camera frustum, if it does, then we render as we always did, if it doesn’t, then we avoid rendering that entity.

Here is an example of the bounds and the frustum of the camera:

![](../../assets/8ccd442475f15aa5.png)


In the image, the element (a) and (b) are rendered because their bounds overlaps with the camera frustum. The element (c) is not rendered because its bounds are totally outside the camera frustum.

### Conclusion

For Vampire Runner, we didn’t notice the difference of having this technique enabled or not since the game always render fast (on our devices) and we had no metrics of the render process time. However, as it was really easy to implement this basic version of the technique, we believe it should help to maintain render performance, and we can reuse the logic for all of our games.

As always, hope you like it.