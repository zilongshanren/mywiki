---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CC3OpenGLES11Engine.h>`


| void |
|

[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) manages the state of the OpenGL ES 1.1.

engine.

OpenGL ES 1.1 is designed to be a state machine that operates asynchronously from the application code that calls its functions. Calls to most gl* functions queue up commands to the GL engine that are processed by the GL engine asynchronously from the gl* call.

This design allows GL command execution to be run on a different processor than the application is running on, specifically a hardware-assisted GPU.

To maximize the throughput and performance of this design, it is important that GL state is changed only when necessary, and that querying of the GL state machine is avoided wherever possible.

By routing all GL requests through [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/), this class can keep track of the GL state change requests made to the GL engine, and will only forward such requests to the GL engine if the state really is changing.

OpenGL defines many functions and state change options. The overall GL functionality covered by [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) is broken down into the major areas of interest, and each of these areas is managed by a separate tracking manager. Each of these tracking managers is available through a specific property on this [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) class.

To allow this state tracking to be available and consistently tracked across the complete application, [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) is implemented as a singleton design pattern. You can access the singleton instance by invoking [[CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) engine] anywhere in your application code.

The two methods open and close define a scope context under which tracking will occur. Once the open method is called, for state tracking to work, ALL OpenGL ES calls that are tracked by the engine MUST be directed through it, until the matching close method is invoked.

The open method is invoked by the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance when 3D drawing begins, and the close method is invoked by the [CC3World](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_world/) instance when 3D drawing ends.

If your application requires access to OpenGL ES 1.1 state or functionality that is not covered by the trackers attached to this engine, you can add that functionality in one of two ways:

Adds the specified tracker to the collection of trackers that are to be closed.

Invoked automatically when the value of the specified tracker is set in the GL engine.

Once 3D rendering is completed, the close method of this class causes the value in each of the changed trackers to be restored to the GL engine by invoking the close method on each of the trackers in this collection.

Adds the specified tracker to the collection of trackers that are to be opened.

Invoked automatically when a tracker has been added somewhere in the hierarchy.

When the CC3OpenGGLES11Engine singleton is created, all primitive element trackers ([CC3OpenGLES11StateTrackerPrimitive](http://www.learn-cocos2d.com/)) are added using this method. When the open method of this instance is invoked, those that need to read their original value from the GL engine do so.

Most trackers only need to be opened once in order to read the original value from the GL engine. Once that has occurred, the tracker will be removed from this collection. Trackers that are configured to read the value on each frame render cycle (as indicated by returning YES in the shouldAlwaysReadOriginal property) will remain in this collection.

| void CC3OpenGLES11Engine::close | ( | ) | ` [virtual]` |

Closes tracking of GL state.

All gl* function calls that make changes to GL engine state made between the invocation of the open method and this close method MUST be routed through this [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton.

Implements [CC3OpenGLES11StateTracker](http://www.learn-cocos2d.com/#a814137ad8462cf5af45a28c2e6eea012).

| void CC3OpenGLES11Engine::initializeTrackers | ( | ) | ` [virtual]` |

Template method that initializes the tracker managers.

Customized subclasses that add additional tracker managers can override this method if necessary.

Automatically invoked during instance initialization. The application should not invoke this method.

| void CC3OpenGLES11Engine::open | ( | ) | ` [virtual]` |

Opens tracking of GL state.

All gl* function calls that make changes to GL engine state made between the invocation of this open method and the corresponding close method MUST be routed through this [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) singleton.

Implements [CC3OpenGLES11StateTracker](http://www.learn-cocos2d.com/#a93288638c8b8efc38af9976a58277c3e).

Most, but not all GL functionality and state is managed by the trackers attached to this [CC3OpenGLES11Engine](http://www.learn-cocos2d.com/api-ref/1.0/cocos3d/html/interface_c_c3_open_g_l_e_s11_engine/) instance.

In the case where your application wishes to track GL state that is not already included in the trackers managed by this instance, you can create a subclass of [CC3OpenGLES11StateTrackerManager](http://www.learn-cocos2d.com/) and set it in this property.

The value of this property is nil, unless an application adds an extension tracker.

The state tracking manager that tracks GL client capabilities state.

The state tracking manager that tracks GL fog state.

The state tracking manager that tracks GL engine hints.

The state tracking manager that tracks GL lighting state.

The state tracking manager that tracks GL materials state.

The state tracking manager that tracks GL matrix state.

The state tracking manager that tracks GL platform functionality state.

The state tracking manager that tracks GL server capabilities state.

The state tracking manager that tracks general GL state.

The state tracking manager that tracks GL textures state.

CCArray * CC3OpenGLES11Engine::trackersToClose` [read, assign]` |

A collection of trackers that are to closed when this instance is closed at the end of each frame render cycle.

At the beginning of each render cycle, this collection is empty. Trackers that make changes to the GL state are automatically added here when the GL state change is made.

CCArray * CC3OpenGLES11Engine::trackersToOpen` [read, assign]` |

A collection of trackers that are to opened when this instance is opened at the start of each frame render cycle.

Initially, most trackers are added to this collection automatically, but any trackers that are set to read their GL state only once are removed once the GL value has been read.

The state tracking manager that tracks GL vertex array state.