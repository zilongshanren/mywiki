---
title: Report from San Francisco Gigabit Hack Days with US Ignite – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/07/report-from-san-francisco-gigabit-hack-days-with-us-ignite/
author: Ali Almossawi
published: '2012-07-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/15.jpg)


This past weekend, the [Internet Archive](http://archive.org) played host to a crew of futurist hackers for the [San Francisco Gigabit Hack Days](http://sfgighackdays.eventbrite.com).

The two-day event, organized by Mozilla and the City of San Francisco, was a space for hackers and civic innovators to do some experiments around the potential of community fiber and gigabit networks.

## Kick-off

The event kicked off Saturday morning with words from Ben Moskowitz and Will Barkis of Mozilla, followed by the Archive’s founder Brewster Kahle. Brewster talked a bit about how the Archive was imagined and built as a “temple to the Internet.”

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/12.jpg)


San Francisco’s Chief Innovation Officer, Jay Nath, talked about the growing practice of hackdays in the city and the untapped potential of the City’s community broadband network. The SF community broadband network is a 1Gbps network that provides Internet access for a wide range of community sites within San Francisco—including public housing sites, public libraries, city buildings and more.

These partners are eager to engage with developers to use the network as a testbed for high bandwidth applications, so we quickly broke off to brainstorm possible hacks.

Among the proposals: an app to aggregate and analyze campaign ads from battleground states; apps to distribute crisis response; local community archives; 3D teleconferencing for education and medicine; “macro-visualization” of video, and fast repositories of 3D content. Read on for more details.

## Hacking

Ralf Muehlen, network engineer, community broadband instigator, and all-around handyman at the Archive prepared for the event in a few very cool ways—unspooling many meters of gigabit ethernet cable for hackers, and provisioning a special “10Gbps desktop.”

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/19.jpg)

The 10Gbps desktop in action


The 10Gbps desktop was a server rack with an industrial strength network card, connected to raw fiber and running Ubuntu. While not a very sensible test machine, the 10Gbps desktop was an awesome way to stress the limits of networks, hardware, and software clients. Video hackers Kate Hudson, Michael Dale, and Jan Gerber created a video wall experiment to simultaneously load 100 videos from the Internet Archive, weighing in at about 5Mbps each. On this machine, unsurprisingly, the main bottleneck was the graphics card. Casual testing revealed that Firefox does a pretty good job of caching and loading tons of media where other browsers choked or crashed, though its codec support is not as broad, making these kinds of experiments difficult.

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/17.jpg)


## Demos

Here are some of the results of the event:

*Macro-visualization of video*

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/video.jpg)


Kate Hudson, Michael Dale, and Jan Gerber created an app that queues the most popular stories on Google News and generates a video wall.

The wall is created by searching the Archive’s video collection by captions and finding matches. Imagined as a way of analyzing different types of coverage around the same issue, the app has a nice bonus feature: real-time webcam chat, in browser, using [WebRTC](http://www.webrtc.org/). If two users are hovered over the same video, they’re dropped into an instant video chat room, ChatRoulette-style.

The demo uses some special capabilities of the Archive and can’t be tested at home just yet, but we’re looking to get the code online as soon as possible.

*Scalable 3D content delivery*

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/threefab.png)


As Jeff Terrace writes in his [post-event blog](http://jterrace.blogspot.com/2012/07/gigabit-hack-weekend.html): “3D models can be quite big. Games usually ship a big DVD full of content or make you download several gigabytes worth of content before you can start playing… [by] contrast, putting 3D applications on the web demands low-latency start times.”

Jeff and Henrik Bennetsen, who work on federated 3D repositories, wanted to showcase the types of applications that can be built with online 3D repositories and fast connections. So they hacked an “import” button into [ThreeFab](http://blackjk3.github.com/threefab/), the three.js scene editor.

Using Jeff’s hack, users can load models asynchronously in the background directly from repositories like Open3DHub (CORS headers are required for security reasons). The models are seamlessly loaded from across the web and added into the current scene.

This made for an awesome and thought-provoking line of inquiry—what kind of apps and economies can we imagine using 3D modeling, manipulation, and printing across fast networks? Can 3D applications be as distributed as typical web applications tend to be?

Bonus: as a result of the weekend, the Internet Archive is working on enabling CORS headers for its own content, so hopefully we will be able to load 3D/WebGL content directly from the Archive soon.

*3D videoconferencing using point cloud streams*

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/pointstream.png)

XB PointStream loads data from Radiohead's House of Cards music video

Andor Salga, author of an excellent JS library called [XB PointStream](http://asalga.wordpress.com/category/xb-pointstream/), wanted to see if fast networks could enable 3D videoconferencing.

Point clouds are 3D objects represented through volumetric points rather than mesh polygons. They’re interesting to graphics professionals for a number of reasons—for one, they can have very, very high-resolution and appear very life-like.

Interestingly, sensor arrays like the low-cost [Microsoft Kinect](http://www.xbox.com/en-US/KINECT) can be used to generate point cloud meshes on the cheap, by taking steroscopic “depth images” along with infrared. (It may sound far out, but it’s the basis for a whole new wave of motion-controlled videogames).

Using Kinect sensors and WebGL, it should be possible to create a 3D videoconferencing system on the cheap. Users on either end would be able to pan around a 3D model of a person they’re connected to, almost like a hologram.

This type of 3D video conferencing would be able to communicate depth information in a way that traditional video calls can’t. Additionally, these kinds of meetings could be recorded, then played back with camera interaction, allowing users to get different perspectives of the meetings. Just imagine the applications in the health and education sectors.

For his hack, Andor and a few others wanted to prototype a virtual classroom that would—for instance—enable scientists at San Francisco’s Exploratoreum to teach kids at community sites connected to San Francisco’s community broadband network.

After looking at a few different ways of connecting the Kinect to the browser, it appeared that startup [Zigfu](http://zigfu.com/) offers the best available option: a browser plugin that provides an API to Kinect hardware. San-Francisco native Amir Hirsch, founder of Zigfu, caught word of the event and came by to help. The plan was to use Websockets to sync the data between two users of this theoretical system. The team didn’t get a chance to complete the prototype by the end of the weekend, but will keep hacking.

Point clouds are typically very large data sets. Especially if they are dynamic, a huge amount of data must transfer from one system to another very quickly. Without very fast networks, this kind of application would not be possible.

*Other hacks*

Overall, this was a fantastic event for enabling the Internet Archive to become a neighborhood cloud for San Francisco, experimenting on the sharp edges of the internet, and building community in SF. A real highlight was to see 16-year-old Kevin Gil from [BAVC’s Open Source track](http://www.bavc.org/youth-programs/programs/digital-pathways/dp-open-source) lead a group of teenaged hackers in creating an all-new campaign ad uploader interface for the Archive—quite impressive for any weekend hack, let alone one by a team of young webmakers.

![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/4.jpg)


![](https://blog.mozillaignite.org/wp-content/uploads/2012/07/4.jpg)

From left: Ralf Muehlen, Tim Pozar, and Mike McCarthy, the minds behind San Francisco's community broadband network

Thank everyone for spending time with us on a beautiful SF weekend, and see you next time!

## Get Involved

If you’re interested in the future of web applications, fast networks, and the Internet generally, check out [Mozilla Ignite](http://mozillaignite.org).

Now through the end of summer, you can [submit ideas](https://mozillaignite.org/about/) for “apps from the future” that use edge web technologies and fast networks. The best ideas will earn awards from a $15k prize pool.

Starting in September, you can apply into the Mozilla Ignite apps challenge, with $485,000 in prizes for apps that demonstrate the potential of fast networks.

Check out the site, follow us @[mozillaignite](https://hacks.mozilla.org/twitter.com/mozillaignite), and let us know where you see the web going in the next 10 years!

## 6 comments

tracey jaquithAugust 6th, 2012 at 14:28Forrest O.September 19th, 2012 at 07:02tracey jaquithSeptember 28th, 2012 at 11:21Forrest O.October 28th, 2012 at 18:10MattOctober 26th, 2012 at 11:42MattOctober 26th, 2012 at 11:47