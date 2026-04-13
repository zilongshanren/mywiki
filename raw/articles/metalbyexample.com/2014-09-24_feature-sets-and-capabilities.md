---
title: Feature Sets and Capabilities
url: https://metalbyexample.com/feature-sets/
published: '2014-09-24'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

One of the changes made to the Metal API in the iOS 8 GM was the addition of the `supportsFeatureSet:`

method to the `MTLDevice`

protocol. The purpose of this method is to differentiate between devices powered by the A7 and A8 processor, because these chips offer different capabilities to Metal.


## Feature Sets

Feature sets are characterized by two values: a GPU generation, and a feature set version. [Apple’s documentation on feature sets](https://developer.apple.com/library/ios/documentation/Miscellaneous/Conceptual/MetalProgrammingGuide/Dev-Technique/Dev-Technique.html#//apple_ref/doc/uid/TP40014221-CH8-SW11) currently documents two feature sets: GPU generation 1, version 1; and GPU generation 2, version 1. These are declared as follows:

typedef enum : NSUInteger { MTLFeatureSet_iOS_GPUFamily1_v1 = 0, MTLFeatureSet_iOS_GPUFamily2_v1 = 1 } MTLFeatureSet;

You can query whether a particular feature set is available on the current device by calling `supportsFeatureSet:`

on a Metal device. `GPUFamily1`

is explicitly identified by Apple with the A7 processor, while `GPUFamily2`

corresponds to the A8, the processor in the iPhone 6 and iPhone 6 Plus.

There are not too many substantial differences between the two, except that the A8 supports a greater number of color attachments on render passes (eight, instead of the four supported by the A7). The A8 also adds support for [Adaptive Scalable Texture Compression](http://en.wikipedia.org/wiki/Adaptive_Scalable_Texture_Compression) (ATSC), a relatively new compression available in Metal on the newest iOS devices.

## Capabilities

The sample project includes a class called `MBEDeviceCapabilities`

with the following interface:

@interface MBEDeviceCapabilities : NSObject + (instancetype)capabilitiesWithDevice:(id<MTLDevice>)device; @property (readonly) NSUInteger highestSupportedFeatureSet; @property (readonly) NSUInteger featureSetGPUFamily; @property (readonly) NSUInteger featureSetVersion; @property (readonly) NSUInteger maximumRenderPassColorAttachments; @property (readonly) BOOL supportsASTCPixelFormats; @end

Creating an instance of `MBEDeviceCapabilities`

produces an object that can supply the more granular device capability information displayed in the screenshots. This class infers the capabilities of the device based on the supported feature set reported by the device.

The [sample app](http://metalbyexample.com/wp-content/uploads/MetalCapabilities.zip) for this post displays the capabilities of the device the program is running on. For example, when running on an iPhone 6, the following display appears:

![The capabilities reported by an A8 device (iPhone 6)](../../assets/43fe0dcbdd01ba24.png)


![The capabilities reported by an A8 device (iPhone 6)](../../assets/43fe0dcbdd01ba24.png)

In contrast, here is the display for an iPhone 5s, which has the older A7 processor:

![The capabilities reported by an A7 device (iPhone 5s)](../../assets/4c33a685a84590f2.png)


![The capabilities reported by an A7 device (iPhone 5s)](../../assets/4c33a685a84590f2.png)

The bottom line on the display shows the concrete type of the Metal device returned by `MTLCreateDefaultSystemDevice`

. When running under the debugger, this is always `MTLDebugDevice`

. Interestingly, when not running under the debugger, the device class is device-specific: `AGXG3Device`

(for iPhone 5s and iPad mini with Retina display) or `AGXG4PDevice`

(for iPhone 6).

You can [download the sample code for this post here](http://metalbyexample.com/wp-content/uploads/MetalCapabilities.zip). If you run the project on your own device and see a different device class, please let us know in the comments.