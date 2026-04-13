---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCActionCamera.h>`




[List of all members.](/)

Public Member Functions
|
| id | [initWithDuration:radius:deltaRadius:angleZ:deltaAngleZ:angleX:deltaAngleX:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/#a88a52c92e7dac0264ac7032bf6cf6536) (float t,[radius] float r,[deltaRadius] float dr,[angleZ] float z,[deltaAngleZ] float dz,[angleX] float x,[deltaAngleX] float dx) |
| void | [sphericalRadius:zenith:azimuth:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/#a25efcdb240e724c8338126dcccbc05f2) (float *r,[zenith] float *zenith,[azimuth] float *azimuth) |
Static Public Member Functions
|
| id | [actionWithDuration:radius:deltaRadius:angleZ:deltaAngleZ:angleX:deltaAngleX:](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/#a9b358cef606a0288c7dcf214003a40c9) (float t,[radius] float r,[deltaRadius] float dr,[angleZ] float z,[deltaAngleZ] float dz,[angleX] float x,[deltaAngleX] float dx) |
Protected Attributes
|
float | **radius_** |
float | **deltaRadius_** |
float | **angleZ_** |
float | **deltaAngleZ_** |
float | **angleX_** |
float | **deltaAngleX_** |
float | **radZ_** |
float | **radDeltaZ_** |
float | **radX_** |
float | **radDeltaX_** |


## Detailed Description

[CCOrbitCamera](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action Orbits the camera around the center of the screen using spherical coordinates


## Member Function Documentation

| id CCOrbitCamera::actionWithDuration:radius:deltaRadius:angleZ:deltaAngleZ:angleX:deltaAngleX: |
( |
float |
*t*, |
|
|
[radius] float |
*r*, |
|
|
[deltaRadius] float |
*dr*, |
|
|
[angleZ] float |
*z*, |
|
|
[deltaAngleZ] float |
*dz*, |
|
|
[angleX] float |
*x*, |
|
|
[deltaAngleX] float |
*dx* |
|
) |
| ` [static, virtual]` |

creates a [CCOrbitCamera](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action with radius, delta-radius, z, deltaZ, x, deltaX

| id CCOrbitCamera::initWithDuration:radius:deltaRadius:angleZ:deltaAngleZ:angleX:deltaAngleX: |
( |
float |
*t*, |
|
|
[radius] float |
*r*, |
|
|
[deltaRadius] float |
*dr*, |
|
|
[angleZ] float |
*z*, |
|
|
[deltaAngleZ] float |
*dz*, |
|
|
[angleX] float |
*x*, |
|
|
[deltaAngleX] float |
*dx* |
|
) |
| ` [virtual]` |

initializes a [CCOrbitCamera](../../../../../api-ref/1.0/cocos2d-iphone/html/interface_c_c_orbit_camera/) action with radius, delta-radius, z, deltaZ, x, deltaX

| void CCOrbitCamera::sphericalRadius:zenith:azimuth: |
( |
float * |
*r*, |
|
|
[zenith] float * |
*zenith*, |
|
|
[azimuth] float * |
*azimuth* |
|
) |
| ` [virtual]` |

positions the camera according to spherical coordinates


The documentation for this interface was generated from the following file: