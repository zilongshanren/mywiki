---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_device/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A device is a logical mapping to an audio device through the OpenAL implementation.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_device/#details)

`#include <ALDevice.h>`


| id |
|

A device is a logical mapping to an audio device through the OpenAL implementation.

| void ALDevice::clearBuffers | ( | ) | ` [virtual]` |

Clear all buffers being used by sources of contexts opened on this device.

| id ALDevice::deviceWithDeviceSpecifier: | ( | NSString* | deviceSpecifier | ) | ` [static, virtual]` |

Open the specified device.

| deviceSpecifier | The device to open (nil = default device). |

| void * ALDevice::getProcAddress: | ( | NSString* | functionName | ) | ` [virtual]` |

Get the address of the specified procedure (C function address).

| functionName | the name of the procedure to get. |

| id ALDevice::initWithDeviceSpecifier: | ( | NSString* | deviceSpecifier | ) | ` [virtual]` |

Initialize with the specified device.

| deviceSpecifier | The device to open (nil = default device). |

| bool ALDevice::isExtensionPresent: | ( | NSString* | name | ) | ` [virtual]` |

Check if the specified extension is present.

| name | The extension to check. |

Handles suspending and interrupting for this object.

ALCdevice * ALDevice::device` [read, assign]` |

The OpenAL device pointer.

NSArray * ALDevice::extensions` [read, assign]` |

List of strings describing all extensions available on this device (NSString*).

int ALDevice::majorVersion` [read, assign]` |

The specification revision for this implementation (major version).

int ALDevice::minorVersion` [read, assign]` |

The specification revision for this implementation (minor version).