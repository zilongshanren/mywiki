---
title: Custom UE4 UMG "Screen Sizes" Configuration
url: https://allarsblog.com/2017/10/01/custom-ue4-umg-screen-sizes-configuration/
author: Michael Allar
published: '2017-10-01'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

Written using UE4 4.17 and 4.18 Preview, results my vary.

Sometimes its useful to have your game UI work correctly with weird screen sizes that most players will never use. One example of this is if you frequently do multiplayer PIE testing where your client windows might have odd sizes such as 940x470 or 800x600. If your UI doesn't support these sizes, it can be pretty painful to add this support as the default UMG Screen Sizes preview list mostly consists of sizes with 16:9 or 9:16 aspect ratios. Manually switching to 'Custom' mode and typing in your testing resolutions can be pretty slow and cumbersome.

In order to speed up my switching between these resolutions, I've added my custom testing resolutions to this Screen Size list.

![Custom Screen Sizes listed in the dropdown.](../../assets/afea00d81ca67078.png)


In the above image you'll see I've added my 940x470 testing resolution which is incredibly handy when testing 4 players on a 1080p screen, thus its name "2x2 1080 940x470".

This is achieved by adding a config file to your project named `DefaultEditorPerProjectUserSettings.ini`

with the following contents:

```
[/Script/UnrealEd.LevelEditorPlaySettings]
; custom screen resolutions helpful for multi-client debugging
+MonitorScreenResolutions=(Description="800x600",Width=800,Height=600,AspectRatio="4:3")
+MonitorScreenResolutions=(Description="640x480",Width=640,Height=480,AspectRatio="4:3")
+MonitorScreenResolutions=(Description="1024x768",Width=1024,Height=768,AspectRatio="4:3")
+MonitorScreenResolutions=(Description="2x2 1080 940x470",Width=940,Height=470,AspectRatio="2:1")
+MonitorScreenResolutions=(Description="3x2 1080 600x450",Width=600,Height=450,AspectRatio="4:3")
+MonitorScreenResolutions=(Description="2x2 4k 1800x900",Width=1800,Height=900,AspectRatio="2:1")
```


The contents here are pretty self-explanatory. Simply add a new line with the desired description, width, height, and aspect ratio and you're good to go. Please note that you will have to restart your editor for it to detect these config changes.

The categories of the screen sizes, such as `Monitors`

and `Televisions`

, are currently hardcoded. Here are a list of screen size categories you can use taken from the Engine defaults:

```
+LaptopScreenResolutions=(Description="Apple MacBook Air 11",Width=1366,Height=768,AspectRatio="16:9")
+MonitorScreenResolutions=(Description="19\" monitor",Width=1440,Height=900,AspectRatio="16:10")
+PhoneScreenResolutions=(Description="Apple iPhone 4, 4S, iTouch 4 (Portrait)",Width=640,Height=960,AspectRatio="2:3")
+TabletScreenResolutions=(Description="Apple iPad 2, iPad Mini (Portrait)",Width=768,Height=1024,AspectRatio="~3:4")
+TelevisionScreenResolutions=(Description="720p (HDTV, Blu-ray)",Width=1280,Height=720,AspectRatio="16:9")
```


In addition to having your new resolutions displayed here, they will also be displayed in the PIE Advanced Settings dialog which is incredibly convenient if you're often testing multiplayer clients and want to use different resolutions:

![Easily switch PIE resolutions](../../assets/99b81d527eb0cbe2.png)