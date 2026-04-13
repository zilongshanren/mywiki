---
title: Accessibility features in Firefox on Android – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/10/accessibility-features-in-firefox-on-android/
author: Eitan Isaacson
published: '2012-10-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of our principles in the [Mozilla Manifesto](http://www.mozilla.org/about/manifesto.html) states that the Internet ”is a global public resource that must remain open and accessible”. Our goal is to remove barriers that traditionally block participation, such as affordability, language and disability.

We have been working hard to bring [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox) to everyone on the planet, including blind and visually impaired users. Firefox 15 for Android introduced preliminary screen reader support. In Firefox 17 we have come full circle, and now support Jelly Bean’s advanced accessibility features. To get these great features right away, [download Firefox for Android from the Google Play store](http://mzl.la/Zo8TmI).

## What are Accessibility Features?

Firefox is designed to meet the needs of the broadest population possible. Sometimes that is not enough. In the case of blind and visually impaired users, a conventional graphical interface with a touch screen is not usable. Assistive technologies such as screen readers exist to bridge that gap. They provide speech and audible feedback that represents the visual state of the application. They may also provide alternative interaction modes that make more sense for blind users. For example, a user could explore the visible items on a screen by moving their finger across the screen and have the screen reader tell them what is under their finger.

## Accessible by Default

We believe that equal access requires Firefox for Android to be ready for any type of user once it is installed, with no extra setup steps or addons. When Firefox for Android launches for the first time on a blind user’s device, it should start talking and be responsive to the user’s input.

Firefox for Android is the first Android Web browser that integrates tightly with Android’s native accessibility framework and supports TalkBack, Android’s screen reader. This provides a consistent feel with the rest of the device, and the user’s specific screen reader configuration.

## Under The Hood

Our Android accessibility solution leverages the same powerful accessibility engine we use on the desktop. This means that it is fast, and [leads the industry](http://html5accessibility.com/) in support of standards such as [WAI-ARIA](http://www.w3.org/WAI/intro/aria.php) and HTML5.

## Touch Exploration & Gestures

Android’s built-in accessibility features have been modernizing ever since Ice Cream Sandwich. Users can now explore the contents of the screen with the tip of their finger and have whatever is under their finger read out loud. Jelly Bean introduces “flick navigation”, a user could swipe left or right to navigate the contents of the screen in a linear fashion.

We have worked hard to support all of those features in Firefox for Android as well and stay apace with Android’s evolving Accessibility and offer a consistent user experience.

## Quick Navigation

Web pages can be very big, complex, and contain a lot of content. When a screen reader user visits a large page it can be tiring and time consuming to step through every item on the page until they find what they are looking for. That is why we introduced Quick Navigation Keys. With the help of a physical keyboard or the Eyes-Free Keyboard, a user can press “k” repeatedly to step through all the hyperlinks on the page. Similar keys are available for headings, list items, various form fields, and more.

This type of feature is familiar to desktop screen reader users. But the Android screen reader does not have this kind of functionality, so we decided to implement ourselves.

## Trying It Out

Accessibility on Jelly Bean is really easy to set up and play with. Go to *System settings->Accessibility->TalkBack* and enable it. Once TalkBack is enabled move your finger across the screen, you will hear audio feedback and speech telling you what your finger is resting on. Close your eyes and try to find different apps on the home screen. Are you getting the feel for it? If you want to sequentially step through items swipe your finger left or right quickly across the screen. If you want to activate an item (say, Firefox Beta?) double tap.

You already know everything you need to know about using Firefox with TalkBack. Launch it, explore the interface with your finger, swipe left and right, and double tab to activate items. This is a good opportunity to try out websites and applications you created and test to see how accessible they are. Could you manage with your eyes closed?

Here is a short video of Firefox Beta on a Nexus 7 working with TalkBack:

## Conclusion

What we are most proud about in our accessibility story on Android is the invisibility of our solution. It integrates well, and it gets out of the way to allow blind users to enjoy the easy and fast mobile browsing experience that Firefox for Android provides.

## About
[
Eitan Isaacson ](http://blog.monotonous.org/)

Eitan is a member of Mozilla's accessibility team. Mobile accessibility solutions are primarily what gets him excited.

## 11 comments

Deedra WatersOctober 11th, 2012 at 12:57Robert NymanOctober 11th, 2012 at 12:59tapperOctober 11th, 2012 at 19:58Robert NymanOctober 11th, 2012 at 23:42Gill BatesOctober 12th, 2012 at 07:34Eitan IsaacsonOctober 12th, 2012 at 12:37TickerOctober 16th, 2012 at 18:21Marco ZeheOctober 17th, 2012 at 05:51Caspy7November 19th, 2012 at 17:00Eitan IsaacsonNovember 19th, 2012 at 18:25Juan Pablo BelloJanuary 9th, 2013 at 17:40