---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/latest/Kobold2D/html/interface_c_c_director_07_kobold_extensions_08/
published: '2012-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

`#include <CCDirectorExtensions.h>`


| BOOL |
|

extends CCDirector

| float CCDirector(KoboldExtensions)::contentScaleFactorHalved | ( | ) | ` [virtual]` |

Gives you the scale factor halved: contentScaleFactor * 0.5f

| float CCDirector(KoboldExtensions)::contentScaleFactorInverse | ( | ) | ` [virtual]` |

Gives you the inverse of the scale factor: 1.0f / contentScaleFactor

| BOOL CCDirector(KoboldExtensions)::isRetinaDisplayEnabled | ( | ) | ` [virtual]` |

Tells you whether Retina Display is currently enabled. It does not tell you if the device you're running has a Retina display. it could be a Retina device but Retina display may simply not be enabled.

BOOL CCDirector(KoboldExtensions)::currentDeviceIsIPad` [read, assign]` |

Tells you if the app is currently running on the iPad rather than iPhone or iPod Touch.

BOOL CCDirector(KoboldExtensions)::currentDeviceIsSimulator` [read, assign]` |

Tells you if the app is currently running in the iPhone/iPad Simulator.

BOOL CCDirector(KoboldExtensions)::currentPlatformIsIOS` [read, assign]` |

Tells you if the app is currently running on iOS.

BOOL CCDirector(KoboldExtensions)::currentPlatformIsMac` [read, assign]` |

Tells you if the app is currently running on Mac.

NSUInteger CCDirector(KoboldExtensions)::frameCount` [read, assign]` |

Returns the number of frames drawn since the start of the app. You can use this to check if certain events occured in the same frame, to ensure that something happens exactly n frames from now regardless of framerate, or to implement a custom framerate display. The frameCount variable is never reset at runtime, only when the app is restarted. An overflow occurs if the app remains running for over 828 days of continuous operation, assuming a steady 60 frames per second.

BOOL CCDirector(KoboldExtensions)::isSceneStackEmpty` [read, assign]` |

Checks if the scene stack is still empty, which means runWithScene hasn't been called yet.

CGPoint CCDirector(KoboldExtensions)::screenCenter` [read, assign]` |

Gives you the screen center position (in points), ie half of the screen size

CGPoint CCDirector(KoboldExtensions)::screenCenterInPixels` [read, assign]` |

Gives you the screen center position (in pixels), ie half of the screen size

CGRect CCDirector(KoboldExtensions)::screenRect` [read, assign]` |

Gives you the screen size as a CGRect (in points) spanning from 0, 0 to screenWidth, screenHeight

CGRect CCDirector(KoboldExtensions)::screenRectInPixels` [read, assign]` |

Gives you the screen size as a CGRect (in pixels) spanning from 0, 0 to screenWidth, screenHeight

CGSize CCDirector(KoboldExtensions)::screenSize` [read, assign]` |

Gives you the screen size as a CGSize struct (in points)

CGPoint CCDirector(KoboldExtensions)::screenSizeAsPoint` [read, assign]` |

Gives you the screen size as a CGPoint struct (in points)

CGPoint CCDirector(KoboldExtensions)::screenSizeAsPointInPixels` [read, assign]` |

Gives you the screen size as a CGPoint struct (in pixels)

CGSize CCDirector(KoboldExtensions)::screenSizeInPixels` [read, assign]` |

Gives you the screen size as a CGSize struct (in pixels)