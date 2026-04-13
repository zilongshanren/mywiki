---
title: App Framework and Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/05/app-framework-and-firefox-os/
author: Ian Maffett
published: '2014-05-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Intel’s [App Framework](https://github.com/01org/appframework) is an open source, [MIT licensed](https://github.com/01org/appframework/blob/master/license.txt), cross platform HTML5 framework for building mobile applications. It is hosted on GitHub where you can contribute to the project, especially the [Firefox OS theme](https://github.com/01org/appframework/blob/master/css/firefox.css).

App Framework is comprised of three main areas.

- Query selector library
- UI/UX library
- Plugins

The query selector library implements a subset of jQuery* API’s, with additional API’s targeted for mobile development. The UI/UX library offers top notch performance on a broad range of devices, including responsive design for phones and tablets. Plugins, the heart of App Framework UI, allow developers to write and share code for App Framework applications.

# Firefox OS support

With the 2.1 launch of App Framework, Firefox OS is now officially supported. This was easy to accomplish, due to Firefox supporting vendor neutral prefixes on many CSS features, like CSS transforms. We will be adding an official Firefox OS theme soon.

# Getting the code

To see everything that is offered in the framework, take a look at the [App Framework website](http://app-framework-software.intel.com/). You can find the [quickstart guide](http://app-framework-software.intel.com/documentation.php), [API documentation](http://app-framework-software.intel.com/api.php), and the [UI component](http://app-framework-software.intel.com/components.php) preview. You can clone the source code at [GitHub](https://github.com/01org/appframework)

Download the zip from GitHub and extract the zip file. View the index.html file to see a sample of the kitchen sink and example API’s. You can test drive App Framework UI and see a demonstration of the provided plugins.

# Building your first app

Here we will build a sample Hello World app with App Framework UI. Create a new folder and copy over the following files from the kitchen sink into your project

- build/ui/appframework.ui.min.js
- build/css/af.ui.base.css
- build/css/icons.css

Next create an index.html file, manifest.webapp, and app.js. You can find documentation for the [manifest.webapp on MDN](https://developer.mozilla.org/en-US/Apps/Build/Manifest). See below for the folder structure for this project.

```
__folder__
index.html
manifest.webapp
js
appframework.ui.min.js
app.js
css
af.ui.base.css
icons.min.css
```

Open up your index.html file in your favorite editor and copy in the following code for the basic ‘Hello World’ app

```
```FF OS sample
Hello World

# Test

Now you can test your sample app on the Firefox OS simulator or a device. You should see the header with the title “Firefox OS”, “Hello World” in the content area, and a footer with a single icon at the bottom. Since we did not add any additional panels, there isn’t much you can do. Let’s update our code and add more. Open up index.html in your editor and change it to the following.

```
```FF OS sample

## View the new code

Run your updated code again in the simulator or device. You will see two items in the bottom tab bar, and a link to “Page 2”. Navigate to Page 2 and you will see the slide up transition, along with a stylized list. You can scroll the list using the built in JavaScript scroller. Hit the back button at the top to go back in the history stack.

# What’s next?

Get a [starter template](https://github.com/krisrak/appframework-templates) and start building your application! Check out the [App Framework](http://app-framework-software.intel.com) website for more documentation and tips.

We are working on a Firefox OS theme and you can [check our work out](https://github.com/01org/appframework/blob/master/css/firefox.css). We love feedback and are happy to fix any bugs found. Just head on over to GitHub and [report the issues](https://github.com/01org/appframework/issues). If you want to extend your app more, build plugins and share them with other developers

# Screenshots

Below are some screen shots from the Intel® XDK App Preview application, powered by App Framework. This is a cross platform application that runs on phones and tablets.

*Other names and brands may be claimed as the property of others.

## About Ian Maffett

Ian Maffett is a software engineer at Intel working on the Intel® XDK products. He is the creator of App Framework, a high performance mobile HTML5 framework for building cross platform applications. His primary focus is HTML5 performance and UX on mobile devices.

## 8 comments

Mte90May 28th, 2014 at 09:39Ian MaffettMay 28th, 2014 at 12:55Alfredo RamirezMay 28th, 2014 at 09:59Ian MaffettMay 28th, 2014 at 12:52Web developerMay 29th, 2014 at 02:21Chris HeilmannJune 9th, 2014 at 02:32Web developerJune 9th, 2014 at 03:13SorinJune 12th, 2014 at 01:39