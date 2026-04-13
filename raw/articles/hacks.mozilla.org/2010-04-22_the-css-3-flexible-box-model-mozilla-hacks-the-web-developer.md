---
title: The CSS 3 Flexible Box Model – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/04/the-css-3-flexible-box-model/
author: Paul Rouget
published: '2010-04-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This article about the Flexible Box Layout was written by Jérémie Patonnier, French open Web enthusiast.*

## The flexible box model

CSS 3 introduces a brand new box model in addition of the traditional box model from CSS 1 and 2. The flexible box model determines the way boxes are distributed inside other boxes and the way they share the available space.

You can see the specification [here](http://www.w3.org/TR/css3-flexbox/).

This box model is similar to the one used by XUL (the user interface language used by Firefox). Some others languages use similar box models such as XAML or GladeXML.

Usually the flexible box model is exactly what you need if you want to create fluid layouts which adapt themselves to the size of the browser window or elastic layouts which adapt themselves to the font size.

In this article, all my examples are based on the following HTML code:

```
1
2
3
```

## Distributing boxes: so what?

By default, the traditional CSS box model distributes boxes vertically depending on the HTML flow. With the flexible box model, it’s possible to specify the order explicitly. You can even reverse it. To switch to the flexible box model, set the property `display`

to the value `box`

(or `inline-box`

) on a box which has child boxes.

```
display: box;
```

### Horizontal or vertical distribution

The `box-orient`

property lets you specify the distribution axis. `vertical`

and `horizontal`

values define how boxes are displayed. Other values (`inline-axis`

and `block-axis`

) have the same effect, but also let you define the baseline alignment itself (basically the boxes are treated like “inline” boxes).

```
body{
display: box;
box-orient: horizontal;
}
```

### Reversed distribution

The property `box-direction`

allows you to set the order in which the boxes appear. By default–when you simply specify the distribution axis–the boxes follow the HTML flow and are distributed from top to bottom if you are using a vertical axis and from left to right if you are using a horizontal axis. By setting `box-direction`

to `reverse`

, you can reverse the boxes’ distribution order. It acts as if you actually reversed the order of the elements in the HTML.

Be careful with this property because it changes the way some other properties work, which can produce some unexpected behavior.

```
body {
display: box;
box-orient: vertical;
box-direction: reverse;
}
```

### Explicit distribution

The property `box-ordinal-group`

lets you specify the order in which the boxes will be distributed. This is the ultimate customization opportunity, because you can define the order you want, regardless of the HTML flow order. Those groups are defined by a number starting at 1 (which is the default value). So the box model will first distribute those groups, then all the boxes inside each group. The distribution occurs from the lowest value (the group numbered 1) to the highest (the groups numbered 2 and above).

```
body {
display: box;
box-orient: vertical;
box-direction : reverse;
}
#box1 {
box-ordinal-group: 2;
}
#box2 {
box-ordinal-group: 2;
}
#box3 {
box-ordinal-group: 1;
}
```

## And what about flexibility?

If changing the natural HTML flow order is huge, the real fun begins when you start to deal with the available space.

### Box sizing

By default, a box is not flexible. It becomes flexible only if it has the property `box-flex`

with a value of at least 1.

If a box is not flexible, it will be as wide as possible to make its content visible without any overflow. Its size can be forced with the properties `width`

and `height`

(or their `min-*`

, and `max-*`

alternatives).

If a box is flexible, its size will be computed as follows:

- The explicit size declarations (
`width`

,`height`

,`min-*`

and`max-*`

) - The size of the parent box and all the remaining available inner space.

So, if the boxes haven’t any size declarations, their sizes will fully depend on their parent box’s size. It will work like this: the size of box is equal to the size of its parent multiplied by the value of the its `box-flex`

property divided by the sum of all the `box-flex`

properties values of all boxes included in its parent.

On the other hand, if one or more boxes have an explicit size statements, the size of all those boxes is computed and all the flexible boxes share the remaining available space on the same principle as above.

It probably sounds a bit tricky, but with some examples it will become easier.

#### All boxes are flexible

In the next example, box 1 is twice the size of box 2 and box 2 has the same size as box 3. It looks the same as using percentages to set the boxes’ sizes. But there is a big difference. If you add a box, you don’t need to recalculate its size. With the flexible box model, each time you add a box, all the others automatically shrink to make room for the new one.

```
body {
display: box;
box-orient: horizontal;
}
#box1 {
box-flex: 2;
}
#box2 {
box-flex: 1;
}
#box3 {
box-flex: 1;
}
```

#### Some boxes have a fixed size

In the next example, box 3, which is not flexible, is 160px in width. In this case, there’s 240px of free space available for boxes 1 and 2. So, box 1 will be 160px in width (240px x 2/3) and box 2 will be 80px in width (240px x 1/3). If you wish, you can make box 3 flexible as well. In this case the way the size of this box is computed will be almost the same as with the property `min-width`

.

```
body {
display: box;
box-orient: horizontal;
width: 400px;
}
#box1 {
box-flex: 2;
}
#box2 {
box-flex: 1;
}
#box3 {
width: 160px;
}
```

### Managing overflow

Because we can mix flexible boxes, inflexible boxes, and flexible boxes which have preset sizes, It’s possible for the sum of all the boxes’ sizes to be larger or smaller than the parent box size. So you can have too much space or not enough.

#### I have too much space available; what do I do?

The available space gets distributed depending on the properties `box-align`

and `box-pack`


The property `box-pack`

manages the way the space is distributed on the horizontal axis and can have one of four possible values: `start`

, `end`

, `justify`

, or `center`


`start`

: All the boxes are on the left side of the parent box and all the remaining space is on the right side.`end`

: All the boxes are on the right and the remaining space is on the left`justify`

: The available space is divided evenly in-between each boxes`center`

: The available space is divided evenly on each side of the parent box

The property `box-align`

manages the way the space is distributed on the vertical axis and can have one of five values: `start`

, `end`

, `center`

, `baseline`

, and `stretch`


`start`

: The top edge of each box is placed along the top of the parent box and all the remaining space is placed below.`end`

: The bottom edge of each box is placed along the bottom of the parent box and all the remaining space is placed above.`center`

: The available space is divided evenly and placed half above and half below.`baseline`

: All children are placed with their baselines aligned and the remaining space is placed before or after as necessary (*This is a simplification about how this value really works, but you see the point*).`stretch`

: The height of each boxes is adjusted to fit the parent box height

A warning about how those properties work: they are strongly influenced by the use of the properties `box-orient`

and `box-direction`

. They can cause some unexpected behavior (for example, the behavior of values `start`

and `end`

could be fully reversed). I hope that once the specification is finalized, we’ll have more information about how those properties work together.

```
body {
display: box;
box-orient: horizontal;
/* The content of the body is horizontally centered */
box-pack: center;
/* and vertically as well ... o/ */
box-align: center;
width: 100%;
height : 100%;
}
```

#### What happens if I don’t have enough space?

Just like with the traditional box model, the overflow property lets you to define the way it’s managed. No surprise here.

However, you must be careful here too. Indeed, the use of the properties `box-orient`

and `box-direction`

can mess it up. For example, you can see elements overflowed to the right instead of the left or to the top instead of the bottom. Take the time to experiment before trying to use it on a big project or you could go mad.

You can also avoid overflow by making the boxes run over multiple lines (or columns, depending on the orientation) by setting the property `box-lines`

to `multiple`

.

### Okay, cool, but does it work in real life?

Yes it does! Both Gecko and WebKit have vendor-prefixed implementations of a box model (**Note**: The current state of the specification does not reflect Mozilla’s or WebKit’s implementation). This means that Firefox, Safari, Chrome, and any browsers that use one of those rendering engines are able to use the features described in this article. If you use one of those awesome browsers, [here is a little demo of the flexible box model in action](http://hacks.mozilla.org/wp-content/uploads/2010/04/exemple-blog.html).

If you’re not using a browser implementing a box model, this screenshot shows you what it looks like:

![An example of the flexible box model with a blog layout](../../assets/f2982726668854f6.png)


## To conclude

You can start to use this box model to layout your HTML documents with modern web browsers. Be careful though, it’s the really first iteration of a W3C Working Draft. There will certainly be some changes. Anyway, the implementations available in Gecko and Webkit are extremely consistent and mature, so if there are changes, they should not be that troublesome.

This box model is a very easy and simple way to solve some usual problems in web design (form layout, page footers, vertical centering, disassociation of visual flow from HTML flow, etc.). I strongly suggest you become familiar with it because it could become a standard tool for web designers in the near future (if Microsoft decides to include it in IE, it could become so very fast).

What is already available is a good start to play with. But at this point, the way the traditional box model and the flexible box model interact is not very clear (for example, it’s impossible to use `position:relative`

with the properties `left`

or `top`

on a box which uses the property `box-ordinal-group`

). This will be improved, but don’t be surprised if your work habits are somewhat undermined. Another tricky point: the way all the properties relative to this new box model interact can be sometimes really confusing. This should remind you of the day you discovered the `float`

property. ;)

### For further information

- Shawn J. Goff:
[CSS3 Flexible Box Layout Module](http://shawnjgoff.com/blog/css3-flexible-box-layout-module) - CSS3.info:
[Introducing the flexible box layout module](http://www.css3.info/introducing-the-flexible-box-layout-module/) - W3C:
[Flexible Box Layout Module](http://www.w3.org/TR/css3-flexbox/)

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 105 comments

ChristianApril 22nd, 2010 at 10:22ChristianApril 22nd, 2010 at 10:23Paul RougetApril 22nd, 2010 at 11:05James John MalcolmApril 22nd, 2010 at 11:18Paul RougetApril 22nd, 2010 at 23:27Kroc CamenApril 22nd, 2010 at 10:27James John MalcolmApril 22nd, 2010 at 11:09NormanApril 22nd, 2010 at 10:32Hans WurestApril 22nd, 2010 at 17:32Hans WurestApril 22nd, 2010 at 17:33JamieApril 22nd, 2010 at 19:50HavvyApril 22nd, 2010 at 22:17LoïcApril 22nd, 2010 at 23:33jpvincentApril 23rd, 2010 at 01:24DanApril 23rd, 2010 at 05:50Paul RougetApril 23rd, 2010 at 06:41Ian ObermillerApril 23rd, 2010 at 14:02Don WilliamsApril 23rd, 2010 at 19:12Paul RougetApril 24th, 2010 at 04:24thinsoldierOctober 13th, 2010 at 09:25voracityApril 24th, 2010 at 05:41MikeApril 29th, 2010 at 05:30RyanApril 23rd, 2010 at 22:00Paul RougetApril 24th, 2010 at 04:26ShaunApril 23rd, 2010 at 23:06voracityApril 24th, 2010 at 05:23thinsoldierOctober 13th, 2010 at 09:28discoleoApril 24th, 2010 at 08:01⬡May 1st, 2010 at 03:25UmanApril 24th, 2010 at 08:30John HaugelandApril 25th, 2010 at 10:01Sergio de la GarzaApril 26th, 2010 at 08:29Sergio de la GarzaApril 26th, 2010 at 09:20Shay HoweApril 26th, 2010 at 12:50BigABApril 26th, 2010 at 12:55PhilipApril 27th, 2010 at 07:20WesApril 27th, 2010 at 10:17denisdengApril 29th, 2010 at 02:29ren1999April 29th, 2010 at 06:22Thomas GossmannApril 30th, 2010 at 08:32Christopher BlizzardApril 30th, 2010 at 09:21Luke DornyApril 30th, 2010 at 13:20Martin KliehmMay 4th, 2010 at 06:16OlivierMay 5th, 2010 at 06:26stefanMay 6th, 2010 at 08:03Zoe GillenwaterAugust 3rd, 2010 at 11:51MattMay 13th, 2010 at 06:54GiorgioMay 13th, 2010 at 10:44Emil IvanovMay 17th, 2010 at 18:06Martin *toiMay 19th, 2010 at 11:38SamJune 7th, 2010 at 00:31MikeJuly 17th, 2010 at 11:26gonAlonsoJuly 20th, 2010 at 03:59Zoe GillenwaterAugust 10th, 2010 at 13:08Geoff KendallAugust 19th, 2010 at 11:05MichaelNovember 15th, 2010 at 13:51MattAugust 20th, 2010 at 02:10Geoff KendallAugust 20th, 2010 at 04:33thinsoldierSeptember 13th, 2010 at 10:17Paul IrishOctober 4th, 2010 at 17:09TimOctober 7th, 2010 at 14:57thinsoldierOctober 13th, 2010 at 09:21thinsoldierOctober 13th, 2010 at 09:35thinsoldierOctober 13th, 2010 at 09:36thinsoldierOctober 13th, 2010 at 09:37EugeneNovember 7th, 2010 at 05:19EugeneDecember 17th, 2010 at 13:33wesDecember 18th, 2010 at 10:36⬡November 21st, 2010 at 18:36MichaelNovember 22nd, 2010 at 01:33⬡November 22nd, 2010 at 12:51Brett WidmannDecember 9th, 2010 at 08:51rodrigo moraesDecember 14th, 2010 at 06:26κατασκευη ιστοσοσελιδων WebsitesFebruary 19th, 2011 at 02:42Marc DiethelmMarch 1st, 2011 at 03:39GhigoMarch 22nd, 2011 at 10:09EugeneMarch 23rd, 2011 at 01:18LaurentNovember 25th, 2011 at 10:42JCNovember 26th, 2011 at 06:07EugeneDecember 8th, 2011 at 06:12WesDecember 8th, 2011 at 17:08Michael C.December 8th, 2011 at 18:05WesDecember 8th, 2011 at 23:15Michael C.December 9th, 2011 at 01:12φωτοβολταικαDecember 23rd, 2011 at 04:24pdJanuary 3rd, 2012 at 06:47αποκριατικες στολεςJanuary 11th, 2012 at 05:09garra rufa fish spaJanuary 16th, 2012 at 11:22Jean-Yves PerrierApril 25th, 2012 at 17:05κατασκευή ιστοσελίδωνJune 19th, 2012 at 04:05seanJune 22nd, 2012 at 10:36φωτοβολταικαJune 26th, 2012 at 23:17ashishAugust 12th, 2012 at 23:26chrixianOctober 26th, 2012 at 23:31πλαστικός χειρουργόςNovember 14th, 2012 at 15:43εξωσωματική γονιμοποίησηJanuary 30th, 2013 at 02:00