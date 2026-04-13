---
title: CCOrbitCamera Class Reference
url: http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_orbit_camera/
published: '2011-01-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import "`

[CCActionCamera.h](http://www.learn-cocos2d.com/)"

Inherits [CCActionCamera](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_action_camera/).

| (id) | -
|

[CCOrbitCamera](http://www.learn-cocos2d.com/unofficial-cocos2d-api-reference/html/interface_c_c_orbit_camera/) action Orbits the camera around the center of the screen using spherical coordinates

| + (id) actionWithDuration: | (float) | t |
||
| radius: | (float) | r |
||
| deltaRadius: | (float) | dr |
||
| angleZ: | (float) | z |
||
| deltaAngleZ: | (float) | dz |
||
| angleX: | (float) | x |
||
| deltaAngleX: | (float) | dx | ||

| - (id) initWithDuration: | (float) | t |
||
| radius: | (float) | r |
||
| deltaRadius: | (float) | dr |
||
| angleZ: | (float) | z |
||
| deltaAngleZ: | (float) | dz |
||
| angleX: | (float) | x |
||
| deltaAngleX: | (float) | dx | ||

| - (void) sphericalRadius: | (float *) | r |
||
| zenith: | (float *) | zenith |
||
| azimuth: | (float *) | azimuth | ||

positions the camera according to spherical coordinates