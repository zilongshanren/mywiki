---
title: Measuring Game Engine Popularity
url: http://www.learn-cocos2d.com/2013/07/measuring-game-engine-popularity/
author: PrimaryFeather says
published: '2013-07-25'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

How do you measure the popularity of a game engine and compare it with others?

Reminded of the [TIOBE Programming Language Index](http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html) and the [Transparent Programming Language Popularity Index](http://lang-index.sourceforge.net/) I couldn’t find a comparable site measuring game engine popularity.

So I sat down and concluded that I can do a simple manual test rather quickly. These are the measurements anyone can take easily:

- Forum topic, post and member counts (if available)
[Stackoverflow.com](http://stackoverflow.com/)and[gamedev.stackexchange.com](http://gamedev.stackexchange.com/)tag counts- Google search query results

### Popularity of Cocos2D Variants

Let’s begin by comparing the popularity of the various Cocos2D variants. The difficulty here lies in properly excluding all the other cocos2d variants. That cocos2d-iphone is commonly referred to as just “cocos2d” makes it difficult to measure just the cocos2d-iphone popularity and to remove that number from all other engine variants.

I tried to overcome this by including or excluding specific tags in Stackoverflow and Gamedev searches:

**cocos2d-iphone:**[cocos2d-iphone] or [cocos2d] -[python] -[java] -[javascript] -[c++] -[html5]**cocos2d-x:**[cocos2d-x] or [cocos2d] [c++] -[python] -[java] -[javascript] -[html5]**cocos2d-android:**[cocos2d-android] or [cocos2d] [android] -[cocos2d-x] -[c++] -[python] -[objective-c] -[html5]**cocos2d-javascript:**[cocos2d-js] or [cocos2d-javascript] or [cocos2d] [javascript]**cocos2d (python):**[cocos2d-python] or [cocos2d] [python]**cocos2d-xna:**[cocos2d-xna] or [cocos2d] [xna]**cocos2d-html5:**[cocos2d-html5]**cocos3d:**[cocos3d]**kobold2d:**[kobold2d]**cocosbuilder:**[cocosbuilder]

**Stackoverflow.com** tag search results:

![Screen Shot 2013-07-25 at 14.48.31](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-14.48.31.png)


Okay, let’s try that again **with cocos2d-iphone removed** so the other variants can be compared in relation to each other:


![Screen Shot 2013-07-25 at 14.51.48](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-14.51.48.png)


Cocos2d-xna sports 2 question, so there’s actually a tiny bit of column there.

On **GameDev.stackexchange.com** we get far fewer search results but in relation the graph is almost identical:

![Screen Shot 2013-07-25 at 14.54.15](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-14.54.15.png)


GameDev again **without cocos2d-iphone**:

![Screen Shot 2013-07-25 at 14.54.23](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-14.54.23.png)


Kobold2D, CocosBuilder and cocos2d-html5 have no questions on GameDev.

Let’s try Google using bracketed search terms and where ambiguity affected search results I also excluded search terms. For example *“cocos2d” -cocos2d-iphone -cocos2d-x -etc* to try and narrow down just the search results for the original Python version of cocos2d.

![Screen Shot 2013-07-25 at 15.07.45](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.07.45.png)


Interestingly cocos2d-x comes out on top. This may be due to its popularity in China, and/or perhaps because it has been backed by China Unicom since its inception so there was/is presumably a greater interest in marketing it.

Google again but with the dominant contenders cocos2d-iphone and cocos2d-x removed:

![Screen Shot 2013-07-25 at 15.07.51](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.07.51.png)


Cocos2d-html5 has a relatively large number of search results, most of them being sites from Asia so it’s no wonder that this isn’t reflected on an english site like stackoverflow.com.

### Popularity of (popular) Game Engines

Let’s try comparing the popularity of various game engines which are popular on Stackoverflow, meaning at least 500 results from tag-based search queries. This reveals PhoneGap to be the surprise winner:

![Screen Shot 2013-07-25 at 15.27.14](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.27.14.png)


The same queries applied to GameDev sees PhoneGap completely missing from the results while XNA clearly takes the lead:

![Screen Shot 2013-07-25 at 15.27.20](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.27.20.png)


When I took these engines to google, one thing became obvious: I couldn’t just google “corona” or “unity” unless I wanted to include results for beer and spiritual living.

I did some tests and found that search for the engine’s name combined with “game development” (ie “cocos2d game development”) resulted in the most hits for the most game engines, so I went with that search term.

And for cocos2d-iphone specifically I used the general term “cocos2d”, which means cocos2d-iphone is representative for all variants of the engine (I forgot to update the label). I included cocos2d-x to see it in relation to the entire cocos2d ecosystem.

![Screen Shot 2013-07-25 at 15.34.28](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.34.28.png)


By the way, the search for “cocos2d-iphone game development” gives 8,300 results compared to 11,700 for “cocos2d-x game development”.

### Is cocos2d-iphone more popular than Unity?

Good question. Probably not.

The above values only provide very rough estimates and there are a number of issues (see next section). In google searches cocos2d has the bonus of having many engine variants, which means more hits in search queries on the general term “cocos2d”.

One way to compare two engines more directly is by comparing the forum stats, at least this gives you an impression on how active the community is. I picked three engines whose forums provided these stats.

Since cocos2d-iphone’s forum doesn’t reveal it’s member count, I estimated it to 45,000 based on number of topics and posts in relation to member count of the other three forums. I’d say that’s very likely to be accurate within a range of plus/minus 15%.

![Screen Shot 2013-07-25 at 15.51.49](../../../wordpress/wp-content/uploads/Screen-Shot-2013-07-25-at-15.51.49.png)


It should be noted that the XNA community also hosts the DirectX and Direct3D forums. Seeing that Unity’s community has about two thirds of the members as the entire Windows game developer community is rather impressive. On the other hand, the Unity community seems to be a much chattier bunch compared to the XNA/DirectX community (more members, more topics but far fewer posts).

Whether that’s a bad thing or not is up for debate and would require. You’d have to pick a couple threads and see for yourself. Like companies or restaurants, each forum has its own culture and different target audiences.

Knowing that the ratio of registered community members vs “silent” users is usually far, far below 5%, we can estimate that there could be up to half a million cocos2d developers, and possibly 3 million Unity developers.

Alas, as it turns out [Unity just recently announced it hit the 2 million registered developers mark](http://blogs.unity3d.com/2013/07/09/another-million-unity-developers-in-the-house/).

### Caveats and Considerations

Obviously, the sheer number of questions asked on Q&A sites has only indirect relation to an engine’s popularity. The forum topic and post counts are much better measurements. Why? Because the users of one engine may simply be more used to ask questions on a Q&A site than others. And users of engines that aren’t well represented on a specific Q&A site may be less inclined to start asking their questions there.

If an engine is not easily understood nor well documented, the number of threads on a Q&A site will likely be higher than for an engine that is easy to use, well documented and where users find outstanding support through official channels.

Google search queries then are limited to a specific keyword which may be over- or underrepresented for particular game engines. The use of brackets is also crucial, since searching for *xxx game development* vs *“xxx game development”* can change the number of search results from tens of millions down to a couple hundred.

Since search queries seemed to reveal greater accuracy with brackets, possibly rooting out a lot of SEO optimizations as well as unrelated terms (for example Unity, Torque and Corona are very ambiguous terms).

Lastly, keep in mind that some engines have been around for longer than others (cocos2d-iphone vs cocos2d-x) while commercial engines often have a google bonus because they typically pay for SEO, content marketing, press releases and other search rank optimizations.

### Final Words

Don’t read too much into these numbers and comparisons.

Do use the same approach whenever you compare game engine and eventually have to choose one. Skip all engines that have neither a healthy community nor a frequent release schedule unless you feel fully capable of helping yourself if need be.

You should check more closely what developers are chatting about - if you find plenty of reasonable questions go unanswered, while developers rant about features on the fringe, and moderators seem to be non-existant or indulge in chit-chat, this gives you an impression of the support quality besides the sheer number of topics and posts.

You would also want to check other metrics, specifically the release cycle ie number and frequency of commits on github or release announcements.

These factors are just as crucial in picking a good game engine than the engine’s features themselves. That doesn’t mean you can’t find everything you need in a narrow-focused, newly-conceived, tiny-community game engine if it perfectly fits your bill. Don’t be foolish and consider only the top three engines listed on google or in other lists.

Do check out the engines on the fringes instead of opting for the popular choice - the most popular option is typically also rather difficult to master (Unity, DirectX, etc) though the learning curve does pay off if you want to do it for a living as either employee or freelancer - because you’ll be more likely to land a job with Unity or DirectX than with libgdx or SDL.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Thanks for the great analysis!

It’s really hard to get really representative stats about the actual usage of any engine. For example, Starling users rarely go to stackoverflow, because Starling’s community forum is so active. And when you just count the total number of posts/threads in a forum, you’d have to take into account how long it’s been running.

To see at least a snapshot of the forum activity, you can look at how recent the current threads on the front page are. Interesting enough, I see that Starling’s oldest post on the front page is almost always “younger” than the last post on the Cocos2D forum. Does that mean that Starling is more popular than Cocos2D? Probably not, but at least it’s a good sign for Starling. 😉

[…] sums it up. Now for the details. Since my last game engine popularity measurement I tried to improve and streamline the […]