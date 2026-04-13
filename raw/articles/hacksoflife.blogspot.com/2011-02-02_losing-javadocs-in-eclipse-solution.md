---
title: 'Losing Javadocs in Eclipse: SOLUTION'
url: http://hacksoflife.blogspot.com/2011/02/losing-javadocs-in-eclipse-solution.html
author: Chris
published: '2011-02-02'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The traditional method to solving this issue is to delete the eclipse .metadata directory. This does in fact work (I tried it) but it also requires you to redownload and setup the Android ADT...plus you lose ALL of your eclipse settings and preferences. If you're like me and have custom fonts and syntax highlighting setup, then that's a nuisance.

The "right way" (and by right way I mean "this worked for me and i didn't lose data) to solve this problem is to follow these instructions:

- In eclipse, right click on your Android project and select Properties
- On the menu on the left, select "Java Build Path"
- On the right hand side, select the "tab" labelled "Libraries".
- Here you should see the Android SDK that you're targeting. For example: "Android 2.2".
- Click on the arrow to the left of the Android SDK to expand the sublevels.
- Find "Android.jar" and click on the arrow to the left of that one as well to expand it.
- You'll see a setting called "Javadoc location". Select that and then click on the "Edit" button.
- At the top, RESELECT the path to your javadocs. This is usually "path_to_android_sdk/android-sdk-mac_86/docs/reference/". I say RESELECT because even if it's right, you should browse and do it over anyway.
- Click on "validate". You should be all set now!

Thank you!

ReplyDeletethanks so much... you've made my day. ;)

ReplyDeleteThanks!!! :)

ReplyDeleteThank you very much friend!

ReplyDeletewhere to download doc

ReplyDeleteThanks for help!

ReplyDeleteThanks a lot dude!

ReplyDeleteSo grateful!