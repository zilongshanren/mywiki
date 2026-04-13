---
title: Simplifying building bodies and joints with libGDX Box2D - 2
url: https://blog.gemserk.com/2011/07/12/simplifying-building-bodies-and-joints-with-libgdx-box2d-2/
published: '2011-07-12'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

[BodyBuilder](https://github.com/gemserk/commons-gdx/blob/38a16739f73b6f90011686277359a3496e771b0c/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/box2d/BodyBuilder.java), which I commented on a [previous post](https://blog.gemserk.com/2011/06/27/simplifying-building-bodies-and-joints-with-libgdx-box2d/), has been updated to work with multiple fixtures, keeping simplicity.

Internally, it uses a FixtureDef builder named [FixtureDefBuilder](https://github.com/gemserk/commons-gdx/blob/8ba60cc93b33e2e02667c548536a83d50a453b3b/commons-gdx-core/src/main/java/com/gemserk/commons/gdx/box2d/FixtureDefBuilder.java) which lets you specify a fixture definition for each fixture.

Here is an example of how it looks now it supports multiple fixture definitions:

Body body = bodyBuilder .fixture(bodyBuilder.fixtureDefBuilder() .circleShape(radius * 0.1f) .categoryBits(CategoryBits.MiniPlanetCategoryBits) .restitution(0f)) .fixture(bodyBuilder.fixtureDefBuilder() .circleShape(radius) .categoryBits(CategoryBits.AllCategoryBits) .sensor()) .position(x, y) .mass(1f) .type(BodyType.StaticBody) .userData(e) .build();

The previous example shows how to declare two fixtures for a Body, one of them is a sensor. For you to know, I am using that code in Super Flying Thing to declare the destination planet (that’s the name for now), the sensor is to detect when the ship is near to trigger an event and then attach it to the planet by creating a Box2D Joint.

If you are a game programmer, it could be useful to maintain your code clean and simple.