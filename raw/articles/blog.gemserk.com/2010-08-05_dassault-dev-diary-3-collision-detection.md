---
title: Dassault Dev Diary 3 - Collision Detection
url: https://blog.gemserk.com/2010/08/05/dassault-dev-diary-3/
published: '2010-08-05'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

The idea of this post is to share some techniques you could use in order to optimize collision detection in your game, but without implementation detail.

Sometimes when we are developing games, part of our logic could be based on the fact that two objects are in contact or not. In Dasasult, we want to know when bullets are in contact with other objects (for example: droids, scene obstacles or the level limits) and we want to know the area where a droid can walk.

Every object we want to check collisions has a position and a polygon shape defining its form in the collision space. Collision detection between objects is performed by checking collisions between their shapes.

The cost of our collision detection by now is heavy because we are checking collisions between all objects. If we increase the number of objects, then the performance is going to be affected. So, if that is the case, then we could have in mind some optimizations to improve it.

The first one is based on the fact that an object A collides with B then B collides with A and the same when not colliding. We could have a structure to mark whenever we check an object colliding with another object and then use that mark to avoid check the inverse collision. That will let us improve a bit because we will have only half collisions detection but with the cost of memory for the new structure.

The second one is to use bounding boxes for fast intersection detection. The idea is to avoid collision detection between game objects if their bounding boxes are not colliding. The most used shapes for this purpose are: Axis Aligned Bounding Boxes (AABB), Oriented Bounding Boxes (OBB) and Spheres.

For Dassault objects we used AABBs because they are really easy to build and work with.

Bounding boxes are really good when perfect collision is too heavy, but we have a new structure for each object and we have to update it whenever the object changes its position, size or angle.

![](../../assets/7e2f88fbb8884db0.png)


Figure: droids and obstacles bounding boxes.

The third one is based on the spatial information of the objects to avoid intersection detection with objects far from each other.

Spatial structures are used for this purpose. The idea is to divide the space in zones so we could know in any time, for example, which objects are in a given zone or which zones contains a given object. There are several types of spatial structures: Grids, Octrees/Quadtrees, Binary Space Partitioning (BSP), Kd-trees, etc.

Note: these structures are commonly used for other purposes, for example, frustrum culling and networking algorithms.


For Dassault we used Quadtrees because we have some knowledge of them and a partial implementation to start with, also they work fine with AABBs.

When using spatial structures, we could improve a lot the performance because we can avoid to check a lot of collisions, but also we are growing in the information to maintain and we should be aware that each time an object moves we have to update in which zone is it now. Each spatial structure has its own pros and cons for different cases, you should have them in mind when choosing one for your game.

The next example show a possible use of spatial information (using grid partitioning):

![](../../assets/a0484028a9b93cda.png)


Figure: example of objects in different zones

If we take a look at the image, we have object 1 in zone A and B, object 2 in zone B and object 3 in zone D. In one moment we would like to detect collisions for object 1, then we check collisions only with objects in zone A and B, that is, object 2.

After you decided the spatial structure to use, collision detection could be performed like this:

for each object in my zone { colliding = false if (getStoredCollision(me, object) != null) return getStoredCollision(me, object) else if (collisionBetweenBoundingBoxes(me, object) == false) colliding = false else colliding = perfectCollision(me, object) storeCollision(me, object, colliding) return colliding }

Conclusion

The solution we used worked as we thought and let us to improve a bit the performance of the game. However, the current implementation could be too featureless based on your game requirements, sometimes you need more information from collisions like the points of contact, the movement direction of each colliding object, the normal vector of the contact points for each object, etc. If you want that stuff and more you could use a physics engine, for example, [Box2d](http://www.box2d.org/) or [Bullet Physics Library](https://code.google.com/p/bullet/) (both libraries have Java ports).

Well, hope you enjoyed the post, feel free to make a comment if not.