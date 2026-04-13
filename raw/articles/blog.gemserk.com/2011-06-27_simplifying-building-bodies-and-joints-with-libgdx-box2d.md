---
title: Simplifying building bodies and joints with libGDX Box2D
url: https://blog.gemserk.com/2011/06/27/simplifying-building-bodies-and-joints-with-libgdx-box2d/
published: '2011-06-27'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In almost all of our latest games we are using [libGDX](http://www.badlogicgames.com/wordpress/) as our main game library. As it comes with a wrapper of well known physics library [Box2D](http://www.box2d.org/), we are using it as well.

Some times when creating a Box2D body, you have to initialize a lot of stuff, you have to create a BodyDef and a FixtureDef and then create the Body with the BodyDef, after that create the fixture on the body using the FixtureDef, it could be a bit confuse.

The next code snippet shows an example of that:

BodyDef bodyDef = new BodyDef(); FixtureDef fixtureDef = new FixtureDef(); bodyDef.type = BodyType.StaticBody; bodyDef.bullet = false; // ... more stuff Shape shape = new CircleShape(); shape.setRadius(radius); fixtureDef.shape = shape fixtureDef.friction = 1f; // ... more fixtureDef stuff Body body = world.createBody(bodyDef); body.createFixture(fixtureDef);

To improve this a bit, I have created a [BodyBuilder](https://github.com/gemserk/commons-gdx/blob/master/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/box2d/BodyBuilder.java) which lets you build Box2D physics bodies in less code lines.

The following code snippet shows an example of using the BodyBuilder:

Body body = bodyBuilder .mass(1000f) .circleShape(radius * 0.1f) .position(x, y) .restitution(0f) .type(BodyType.StaticBody) .categoryBits(MiniPlanetCategoryBits) .build();

As you can see, it looks smaller and cleaner. However, it has the limitation (because I was lazy when I did the class) it works for only one fixture def, if you want to build a complex body that will be a problem.

There is also a similar builder for Joints named [JointBuilder](https://github.com/gemserk/commons-gdx/blob/master/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/box2d/JointBuilder.java) but it is just started.

The following code snippet shows an example of using the JointBuilder:

Joint joint = jointBuilder.distanceJoint() .bodyA(bodyA) .bodyB(bodyB) .collideConnected(false) .length(1.5f) .build();

If you are using libGDX Box2D as well, both classes could be of help despite they are incomplete.