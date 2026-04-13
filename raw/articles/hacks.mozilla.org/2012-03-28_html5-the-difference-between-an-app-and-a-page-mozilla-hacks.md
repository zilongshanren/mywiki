---
title: 'HTML5: The difference between an App and a Page. – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2012/03/html5-the-difference-between-an-app-and-a-page/
author: Joe Stagner
published: '2012-03-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## HTML5 is only one part of the”Stack”

HTML5 is really more than one thing. In the strictest sense, HTML5 is fifth major revision of the W3C specification of the markup language that is used to create web pages.

But in a practical sense, HTML5 is far more than that. For developers, HTML is a wave of technologies that are evolving and gaining browser implementations along roughly the same time-line as the markup language itself. Many of the related technologies are being spearheaded by the Web Hypertext Application Technology Working Group (whatwg.org), but still other technologies in this genre are driven from elsewhere. For example WebGL, the 3D rendering engine for Web Apps, is driven at [Khronos](http://www.khronos.org), and [Mozilla’s WebAPI team](https://wiki.mozilla.org/WebAPI) is leading a collection of relevant API work including a comprehensive array of device-specific APIs. And the [W3C was a Device APIs Working Group](http://www.w3.org/2009/dap/)

Mozilla is also investing heavily in an initiative to facilitate the use of standards-based Web technologies to build applications that can be installed and used in the same way a “native” applications would be.

There are many reasons that doing so might be desirable, not the least of which is the ability to build much or all of your application for use on many different devices and platforms using a single set of development technologies.

Developers can already build HTML Applications (with help from the HTML5 [Apps documentation](https://developer.mozilla.org/en-US/apps) ) and submit their applications to the [Mozilla Marketplace](https://marketplace.mozilla.org/).

## App versus Page ?

When people start talking about building apps with HTML5, one of the early questions that comes to the conversation is “What’s the difference between an app and a page?”

This is bit of a difficult question to answer because of the very wide range of answers which can all be true, but which may be completely different.

While your HTML5 app *should* be more than a simple HTML5 page, technically speaking it doesn’t have to be. Using the steps outlined in the guide “[Getting Started with making (HTML5) apps](https://developer.mozilla.org/en/Apps/Getting_Started)”, you could simply create an apps manifest file and submit your HTML page as an app.

When an Open Web app runs, the Mozilla Web Runtime installs local copies of the HTML5 markup and all of the other web assets that are specified using an HTML5 Cache Manifest ( [read here](https://developer.mozilla.org/en/Offline_resources_in_Firefox) ).

If a Web page is dynamically generated, as in an ASP.NET, PHP, etc., application, any cached version represents a snapshot of a single point in time. When submitted as an app, the page actually “becomes” an app, getting a launcher item similar to native apps on whatever the host operating system is. When the app is launched, the local assets are used if there is no Internet connection or if the caching mechanism determines that the assets have not changed since they were last downloaded.

By doing the above we have not added any additional functionality to our application. All we have done by declaring our page to be an app is to get the run-time to copy the bits locally and to run those local bits if the device is off line or if the bits haven’t changed.

## Does this get us anything ?

## Is there value in just this simple step ?

Yes, it gets us three valuable improvements:

- Users can see our page even if they are not connected because the run-time renders the cached version if there is no Internet connection.
- Processor cycles and bandwidth consumption from our infrastructure or hosting are greatly reduced because new bits are only fetched when they are needed.
- Performance improves because resources are loaded locally by default.

Many organizations are starting with this approach because very little technical effort is necessary and it can be done very quickly. In most cases all you need to do is to create an app manifest file ([ more info here](https://developer.mozilla.org/en/Apps/Getting_Started) ) and to submit the app to the marketplace. Developers can [submit apps now at the Mozilla marketplace Developer Submission site](https://marketplace.mozilla.org/en-US/login?to=/en-US/developers) so that they will be available to consumers when the “buy side” of the marketplace opens later this year.)

But if that’s all you do with your app, you are missing the opportunity.

Take a look at [http://caniuse.com/](http://caniuse.com/) for a snapshot view of technologies that are available to developers using the modern web runtime.

Whether we are building a real Open Web App from scratch or we are converting an HTML page to an app and then adding modern features, HTML5 era technologies let us really start to developer client / server applications that utilize the browser and its host resources, thereby reducing our server requirements while improving the end user’s experience.

Developers can do things like :

- Read and write data locally and sync with a server when appropriate.
- Run multiple threads of execution at the same time.
- Exchange content with other applications, or share logic with them.
- Interact with the device on which their app is running.
- Touch user interface
- GPS
- Camera
- Richly integrate multimedia.
- And much more…..


Since apps’ source code is deployed to a single URL and is updated on the device on which the app runs only when updates are necessary, versioning is low cost and friction free. This makes it easy to start by making a page and then iteratively adding features one after another.

## Lets do it !

Since this model makes it so easy to get started, why not give at a try?

Follow the guidance here : [https://developer.mozilla.org/en/Apps/Getting_Started](https://developer.mozilla.org/en/Apps/Getting_Started)

And submit your app here : [https://marketplace.mozilla.org/](https://marketplace.mozilla.org/)

## 5 comments

Maxime Chevalier-BoisvertMarch 28th, 2012 at 16:58Robert NymanMarch 29th, 2012 at 10:58Corey GwinMarch 28th, 2012 at 18:36Robert NymanMarch 29th, 2012 at 10:59OlivierApril 29th, 2012 at 07:53