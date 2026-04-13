---
title: Kobold2D Project Starter Tool
url: http://www.learn-cocos2d.com/2011/08/kobold2d-project-starter-tool/
author: Orville Chomer says
published: '2011-08-11'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

#### The Goal

Kobold2D users should never have to run a bash script, ever. Any project or asset management task most users will want to perform should be done with a visual tool.

#### The Problem

I mentioned before that I had problems turning the [Kobold2D](http://www.kobold2d.org/) project templates into the [Xcode 4 Project Template format](http://www.learn-cocos2d.com/store/xcode4-template-documentation/). In fact, it turned out to be impossible due to the nature of Kobold2D’s workspace setup.

Since I want to have a wide variety of project templates in Kobold2D, and definitely more than the three rudimentary templates that cocos2d-iphone offers, I needed some way to allow users to start new projects based on a template.

#### The Solution

What I came up with is the Kobold2D Project Starter Tool:

Simple and elegant. This tool scans the projects in Kobold2D templates folder, which are regular Xcode projects with a common naming scheme (eg. *_Hello-Kobold2D-Template_*), and presents them to the user including a description.

Select a project template, give it a name and click **Create**. The tool will copy the template project to the Kobold2D folder next to all the other projects. All occurrences of *_XXXX-Template_* are renamed to the user supplied project name (which is cleaned to remove illegal characters). Then the project is added to the Kobold2D.xcworkspace which the tool will open right away.

#### The Benefits

I think the biggest benefit by far is that anyone can turn his or her Xcode project into a template, simply by following the naming scheme. Anyone can create and distribute their own Kobold2D project templates.

Note: in the screenshot there are only 7 templates listed. I’ll definitely add more for the Kobold2D v1.0 release, most will be based on projects discussed in my Learn Cocos2D book. The first preview version (v0.9x) of Kobold2D will be available in about two weeks.


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Just wondering… I installed Kobold2d… where is the Project Starter program located so that I can run it.

It came up automatically when I installed Kobold2d, but how do I open it going forward?

It’s in each versioned folder of Kobold2D. By default that will be: ~/Kobold2D/Kobold2D-v1.0/Kobold2D Project Starter.app