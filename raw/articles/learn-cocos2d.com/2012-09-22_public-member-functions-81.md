---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/2.0/cocos2d-iphone/html/interface_c_c_orbit_camera/
published: '2012-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#import <CCActionCamera.h>`




[List of all members.](../../../../../api-ref/2.0/cocos2d-iphone/html/class_c_c_orbit_camera-members/)


## Detailed Description

[CCOrbitCamera](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action Orbits the camera around the center of the screen using spherical coordinates


## Member Function Documentation

+ (id) [actionWithDuration:](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_action_interval/#a08fbc347478cca16ab1fe936a1770dc0) |
|
(float) |
*t* |
| radius: |
|
(float) |
*r* |
| deltaRadius: |
|
(float) |
*dr* |
| angleZ: |
|
(float) |
*z* |
| deltaAngleZ: |
|
(float) |
*dz* |
| angleX: |
|
(float) |
*x* |
| deltaAngleX: |
|
(float) |
*dx* |
|
|
| |

creates a [CCOrbitCamera](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action with radius, delta-radius, z, deltaZ, x, deltaX

- (id) [initWithDuration:](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_action_interval/#a720052392c29747218924b70af412d6c) |
|
(float) |
*t* |
| radius: |
|
(float) |
*r* |
| deltaRadius: |
|
(float) |
*dr* |
| angleZ: |
|
(float) |
*z* |
| deltaAngleZ: |
|
(float) |
*dz* |
| angleX: |
|
(float) |
*x* |
| deltaAngleX: |
|
(float) |
*dx* |
|
|
| |

initializes a [CCOrbitCamera](../../../../../api-ref/2.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action with radius, delta-radius, z, deltaZ, x, deltaX

| - (void) sphericalRadius: |
|
(float *) |
*r* |
| zenith: |
|
(float *) |
*zenith* |
| azimuth: |
|
(float *) |
*azimuth* |
|
|
| |

positions the camera according to spherical coordinates


The documentation for this class was generated from the following file: