---
title: 'Firefox: 46 features you might not know about – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2010/02/firefox-46-features/
author: Paul Rouget
published: '2010-02-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Ever since the release of Firefox 3 we’ve been doing a lot of work to add new capabilities for web developers. We thought it would be worth it to make a post that actually listed all of the features that we knew about and people might not know about. This contains everything that we’ve done over the last three releases or so, but calls out stuff that’s new in 3.6.

Enjoy!

###
CSS


-
[@font-face](https://developer.mozilla.org/en/CSS/@font-face)

- Display online fonts (supports WOFF and TTF fonts)
-
[pointer-events](https://developer.mozilla.org/en/CSS/pointer-events) - Click through elements
-
[:-moz-locale-dir(ltr/rtl)](https://developer.mozilla.org/en/CSS/%3a-moz-locale-dir(ltr))

- Know if you are in a ltr or rtl context
-
[:indeterminate pseudo-class](https://developer.mozilla.org/web-tech/2009/02/05/a-new-checkbox-type/)

- For “indeterminate” radio and checkboxes
-
[Media Queries](https://developer.mozilla.org/En/CSS/Media_queries)

- Select CSS depending on the media (size, aspect-ratio, colors, orientation, resolution). has new classes to detect if you’re on a touch device.
-
[Structural pseudo-classes](https://developer.mozilla.org/En/CSS/%3anth-child)

- :nth-child, :nth-last-child, :nth-of-type, :nth-last-of-type, …
-
[-moz-border-radius](https://developer.mozilla.org/en/CSS/-moz-border-radius)

- Rounded borders
-
[CSS Transforms](https://developer.mozilla.org/En/CSS/Using_CSS_transforms)

- Scale, translate, skew and rotate your elements
-
[CSS Gradients](https://developer.mozilla.org/en/Using_gradients)

- Use linear and radial gradients as backgrounds
-
[Multiple Background](https://developer.mozilla.org/en/CSS/Multiple_backgrounds)

- Use images, gradients and other items all as part of the same background
-
[Background size](https://developer.mozilla.org/en/CSS/Scaling_background_images)

- Define the size of your background images
-
[CSS Columns](https://developer.mozilla.org/En/CSS/-moz-column-rule)

- Display your content in columns
-
[Text Shadow](https://developer.mozilla.org/En/CSS/text-shadow)

- Shadow around text
-
[Box Shadow](https://developer.mozilla.org/En/CSS/-moz-box-shadow)

- Shadow around elements
-
[Border image](https://developer.mozilla.org/En/CSS/-moz-border-image)

- Use images as border for your elements
-
[rem length unit](http://www.w3.org/TR/css3-values/#lengths)

- Size your elements compared to the root text element
-
[Image Rendering Algorithm](https://developer.mozilla.org/en/CSS/image-rendering)

- Optimize speed or quality for resized images

###
XMLHttpRequest


-
[Cross Domain XMLHttpRequest](https://developer.mozilla.org/En/HTTP_access_control)

- Allows XMLHttpRequest to other domains
-
[Monitoring Request Progress](https://developer.mozilla.org/En/Using_XMLHttpRequest#Monitoring_progress)

- Calculate percentages of uploads or downloads
-
[Send binary data](https://developer.mozilla.org/En/Using_XMLHttpRequest#Sending_binary_data)

- Send non-ASCII content
-
[Read binary data from a request](https://developer.mozilla.org/En/Using_XMLHttpRequest#Handling_binary_data) - Read binary data sent by a server from an XMLHttpRequest

###
Offline


-
[Offline and online events](https://developer.mozilla.org/en/Online_and_offline_events)

- Get notified when the browser goes online or offline
-
[localStorage](https://developer.mozilla.org/en/DOM/Storage#localStorage)

- Store persistent data
-
[HTML5 Application Cache](https://developer.mozilla.org/en/Offline_resources_in_Firefox)

- Build an application for offline use in Firefox

###
Content


-
[Video Tag (poster attribute)](https://developer.mozilla.org/En/HTML/Element/Video)

- Embed videos directly in your web page
-
[Audio Tag](https://developer.mozilla.org/En/HTML/Element/Audio)

- Embed audio files in your web pages
-
[Canvas Element](https://developer.mozilla.org/en/HTML/Canvas)

- Draw bitmap data with JavaScript
-
[Animated PNG graphics](https://developer.mozilla.org/en/Animated_PNG_graphics)

- Animate your transparent PNG graphics
-
[SVG Support](https://developer.mozilla.org/en/SVG)

- Draw, manipulate and get events for vector graphics
-
[ForeignObject](http://www.w3.org/TR/SVG11/extend.html#ForeignObjectElement)

- Add HTML content inside an SVG element
-
[Apply SVG effects and transforms to plain old HTML content](https://developer.mozilla.org/En/Applying_SVG_effects_to_HTML_content)

- CSS mask, clip-path, or filter with SVG

###
Interaction


-
[In-page Drag and Drop](https://developer.mozilla.org/En/DragDrop/Drag_and_Drop)

- Cleanly support Drag and Drop inside of your web application
-
[Drag and Drop files from the Desktop](http://hacks.mozilla.org/2009/12/file-drag-and-drop-in-firefox-3-6/)

- Drag and drop files directly from the operating system into your web page
-
[DNS Pre-fetching](https://developer.mozilla.org/En/Controlling_DNS_prefetching)

- Speed up web page loading with DNS prefetching
-
[Geolocation](https://developer.mozilla.org/En/Using_geolocation)

- Retrieve someone’s GPS coordinates or Street address
-
[Mouse gesture events](https://developer.mozilla.org/En/DOM/Mouse_gesture_events)

- Swipe, Magnify and Rotate from your mousepad
-
[Detecting device orientation](https://developer.mozilla.org/en/Detecting_device_orientation)

- Events for detecting machine orientation
-
[Web Based protocol handlers](https://developer.mozilla.org/en/Web-based_protocol_handlers)

- Set up a web app to support a protocol like “mailto:” or “phone:”
-
[Detecting document width and height changes](https://developer.mozilla.org/en/DOM/Detecting_document_width_and_height_changes)

- Figure out when someone changes the size of a document
-
[Communicate between windows and iframes](https://developer.mozilla.org/en/DOM/window.postMessage)

- Securely send messages from one document to another

###
JavaScript and API


-
[Native JSON](https://developer.mozilla.org/En/Using_native_JSON)

- Encode and decode JavaScript objects safely and quickly
-
[Web Workers](https://developer.mozilla.org/En/Using_web_workers)

- Run JavaScript code in a thread
-
[File API](https://developer.mozilla.org/en/Using_files_from_web_applications)

- Read the binary content of files from Drag and Drop and File Upload controls
-
[QuerySelector](https://developer.mozilla.org/En/DOM/Locating_DOM_elements_using_selectors)

- Find an element in the web page through a CSS Selector
-
[classList](https://developer.mozilla.org/en/DOM/element.classList)

- Easily manipulate the classes of an element
-
[defer and async attributes for scripts elements](https://developer.mozilla.org/En/HTML/Element/Script)

- Improve the performance of page loads with new script attributes

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 16 comments

Tony MechelynckFebruary 24th, 2010 at 08:07Marcel KorpelFebruary 27th, 2010 at 14:21Marcel KorpelFebruary 27th, 2010 at 15:07vinyllFebruary 24th, 2010 at 09:45PJFebruary 24th, 2010 at 13:40Paul RougetFebruary 24th, 2010 at 13:42Tony MechelynckFebruary 25th, 2010 at 15:47DaoFebruary 24th, 2010 at 15:12Ken SaundersFebruary 24th, 2010 at 16:21voracityFebruary 24th, 2010 at 21:23Brett ZamirFebruary 25th, 2010 at 01:32Jakob K…March 17th, 2010 at 14:56George WhiteAugust 23rd, 2010 at 04:38Reynir Heiðberg StefánssonNovember 11th, 2010 at 04:19