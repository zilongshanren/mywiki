---
title: Cocos2D Gets An Overhaul With Your Help!
url: http://www.learn-cocos2d.com/2012/10/essential-cocos2d-koboldtouch/
author: Toni Sala says
published: '2012-10-18'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Since I started working on [KoboldTouch](http://www.learn-cocos2d.com/2012/10/koboldtouch-mvc-wrapper-cocos2d/) a couple things fell into place. Mainly that it would:

**Provide what Cocos2D leaves up to its users. Fixes what Cocos2D does badly. Adds what Cocos2D doesn’t do at all. Eases development with Cocos2D and accommodates actual developer needs.**

While Cocos2D is moving towards cross-platform with their Javascript API, **KoboldTouch will focus on adding & improving game design features**.

I have a hunch most Cocos2D developers have better iOS/Mac integration and game-specific features higher up on their wish list than cross-platform. Most of you are indies, hobbyists, pragmatists and Apple enthusiasts without the need or resources to do cross-platform development.

### KoboldTouch: Spiritual Successor

I first started working on [KoboldTouch](http://www.learn-cocos2d.com/2012/10/koboldtouch-mvc-wrapper-cocos2d/) a few weeks back. I initially undersold it as a “MVC wrapper for Cocos2D”. With what I have in mind **spiritual successor of Cocos2D** is more like it.

It’s going to be a framework to program iOS & Mac games in, where best practices evolve naturally, where Cocoa programmers feel right at home, where beginners are not left in a void * EXC_BAD_ACCESS … and where Cocos2D is still at the heart of it.

KoboldTouch takes control over Cocos2D, to allows users to implement best practices naturally. Cocos2D provides the view, KoboldTouch provides the controllers, models and the framework to write your code in.


#### The Goals for KoboldTouch

Take the good parts of Cocos2D, improve Kobold2D and fix what’s been criticized, build KoboldTouch as a Cocoa-esque game framework around Cocos2D views, add Lua scripting and ensure tight integration with Apple’s OS features.

Little by little I want to transform Cocos2D from the rendering engine that it is and embed it into KoboldTouch, the game development framework.

But most importantly:

#### Developers Drive Development

**Let the users guide development!**

I find it crazy and sad how many times Cocos2D developers are left on their own to re-reinvent the wheel, and what kind of odd code constructs they develop to store their game’s data, to program the flow of scenes, and to exchange data and run code on various objects in the game.

Because Cocos2D doesn’t provide the framework I think it should. It doesn’t teach nor encourage game development best practices. It’s especially appalling to me because working from user requirements, making their work easier, supporting and training them and providing guidance was my job for over 10 years.

And then there’s really ugly code in Cocos2D that seriously ought to be refactored…

#### The Cocos2D Improvement Program

Take Cocos2D’s tilemap renderer **CCTMXTiledMap** for instance.

**It’s slow** because it stupidly draws all the tiles of each layer, whether they’re on screen or not. **It consumes a lot of memory** because of that, too. And weirdly enough it **still uses pixel coordinates**, requiring you to **upscale TMX files** manually or with a tool and multiply some coords with the content scale factor. And it lacks important features.

Recently I began working on an improved orthogonal tilemap renderer for KoboldTouch. I feel sorry for not having started adding these improvements and features 2 years ago:

- renders only visible tiles, plus one extra row and column to enable scrolling
- is Retina-aware, all coordinates in points, upscaling (if needed or requested) done during load
- will support following a particular game object and scroll to position
- will support parallax scrolling for tile & object layers
- will support endless (wrap-around) scrolling, configurable per layer
- will support tile animations
- will support creating game objects via TMX object properties
- will support modification to all layers at runtime
- will have a debugging overlay that renders all polygon object locations
- properties do not require string to int/float conversion
- no coordinate conversion headaches when pairing tilemap and physics worlds

These features are my current development goal. That’s the feature set I would expect from a decent Tilemap renderer.

I have more of these improvements and additions on my plate. Most should be obvious if I say that my goal is to make all the game relevant Apple APIs readily accessible to Cocos2D developers. Game Center, Twitter, Facebook, iCloud, In-App Purchases - integration and ease of development are key, not cross-platform compromises and tacked-on solutions.

### Essential Cocos2D includes KoboldTouch

Essential Cocos2D is going to be a continuously updated **reference documentation for Cocos2D** with **best practices**.

But why stop there? It seems logical to bundle Essential Cocos2D with KoboldTouch, and an improved version of Kobold2D, to make it **the** essential service for Cocos2D developers.

Oh and by the way: **Essential Cocos2D** will launch on **November 1st, 2012**. In exactly two weeks!

#### Here’s where you come in!

I hate to work into the blue, not knowing if what I’m working on is necessary, useful, or even desirable. I value immediate feedback. I will happily take your requests and turn it into writing or code - the more generally helpful it is, the better.

By voting on suggestions and adding your own **you can direct development of KoboldTouch and the Essential Cocos2D documentation**. What code feature should I add next? Which topic should I write about this week? It’s really up to you!

I believe in the long term success for a spiritual successor to Cocos2D. One that is both a complete game engine and framework, while staying true to Apple’s platforms. Commercial with a fair price.

#### Sooooo … Let’s Talk About Money

Since I find it generally more comfortable to work while not having to worry about running out of caffeine (*****) anytime soon, here comes the bummer:

**Essential Cocos2D and KoboldTouch will be paid services.**

The yearly price is $200 at **$49,95 per quarter (subscription)** with an option I’ll be adding later to **join for a fortnight for $24,95 (single payment)**.

(*****) *Disclaimer:* I recently went cold turkey and stopped consuming caffeine. I’m now actually a more productive programmer, contrary to popular belief. I still need to consume *something* though. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


#### Subscription vs Pay-Once

The point of the **$25 pay-once** option will be that you can have a look around, get help, read the documentation, download whatever is currently available for download. Then maybe come back again in a couple months for another $25. You can continue to use whatever you downloaded in the meantime. I believe that’s a fair offer for those who are happy with a few updates per year and don’t want to subscribe.

Whereas **as a subscriber**, early adopter and continued supporter you not only **get three months for the price of one**, you will help shape the code, the documentation, everything I’m doing. You can come in any time and get help, request a feature, vote on a bug that’s blocking you, suggest a new article I should write. I’ll be sure to add bonuses for longterm subscribers over time, and I’ll work closely with you.

Plus: **If you own my Learn Cocos2D 2 book, I’ll give you your money back**! Save $40 per year by signing up for **$39,95 (-$10) per quarter -** just locate a password that’s printed in the (e)book.

#### Service vs Product

Why a subscription service, you might ask? I evaluated other options but frankly, I’m more comfortable running a service than selling individual products.

The reason is mainly psychological: working to satisfy regularly paying users is a lot more motivating. Especially since the goal is to make continuous improvements based on your suggestions. It also makes it so much easier to push updates by simply uploading them to the member area on my website. Lastly, the revenue is more constant and predictable.

And finally the subscription purposefully serves to limit the number of users, thus making it a better service. If more users sign up than I can handle, I will have the budget to pay fellow developers to help out with coding, documentation and support. Essential Cocos2D is designed to scale up smoothly.

You should know that Clickbank prohibits price changes for subscription products, there will be no surprises. The mandatory (!) *60-day money-back guarantee* applies, too.

### Kickstarting without Kickstarter

**Consider Essential Cocos2D to be a Kickstarter project without the Kickstarter disadvantages!**

Instead of paying on a promise that may or may not be delivered, that may or may not even get funded, you get immediate access to everything I’ve written and developed thus far. You can share your feedback with me and influence future developments and documentation. At any time you can see for yourself the value that’s already there, the value I’m adding over time and that the service lives up to its promise.

I’m aiming for 150 subscribers by May 2013 (6 months). That’s really all it takes to make the project feasible indefinitely. The more subscribers the more opportunities I can seize to speed up progress!

More budget certainly helps, and I’ll be sure to invest that back into the service one way or another. I’m not afraid to outsource individual tasks or hire developers. Ultimately I’m a limited resource, cloning is *still* not an option (damnit, science!) and there are so many great ideas to pursue.

I should mention that **you can help achieve this goal!** [Sign up for free as Affiliate with Clickbank](http://www.clickbank.com/help/affiliate-help/affiliate-basics/what-is-an-affiliate/), put up an affiliate link on your website and/or blog about it, and you get 30% (about $13.50 for $50) for each subscriber referred by you. For every rebill, too! More info on Nov 1st.

Christmas is on **November 1st** this year! I’m looking forward to welcoming you in two weeks.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I think you have something really interesting.

Waiting![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Are you aware of HKTMXTiledMap that already does a lot of those features you listed in your upgrade to CCTMX such as only rendering what is on screen and tile animations?

I’m well aware. I’m also aware there are cocos2d 2.0 compatibility issues, the developer is understandably busy working on his own game, and I need my own implementation anyway to do the really cool stuff (parallax, endless scrolling, object instantiation, mutable properties, …).

I want to overhaul cocos2d, not tack on yet another user created add-on class whose issues I don’t really know yet. So I tend to rather rewrite code even if some of the features already (partially) exist somewhere else in some form.

Hi Steffen, your work at kobold2d is very usefull. But unfortunatelly we need to change from kobold2d to another “cross-platform” engine.

We at JanduSoft, don’t like some “cross-platforms” platforms like unity (too heavy) or cocos2d with javascript, but we like the idea of having the same code over more platforms.

Make a Kobold2d engine based on c++ (cocos2d-x) and I’m sure you will have more customers. Me included.

I understand the need of developers like you to use a cross-platform game engine. But cross-platform engines are hard to develop, are often built on compromises, such as the programming language (C/C++, Javascript or Lua as lowest common denominator), performance (compatibility/portability layer), lack of native OS features and generally slower development due to the larger number of platforms and devices to support and test.

I think my time is spent better making a game development framework that’s native to Apple’s platforms. For one, there are already plenty of cross-platform solutions available (libgdx comes to mind if you’re looking for a free one). I can’t compete with most of them - if you look closely you’ll find that even the free cross-platform game engines are developed by whole developer teams, the rest are obviously venture funded companies or like cocos2d-x, sponsored with at least one developer focusing on a particular platform. I’d easily fall into the same trap as this guy - who made a better cross-platform C# game engine (ExEn) but the masses were driven to the popular choice (MonoGame) who have more developers and apparently, more bugs.

And then there’s not one modern (2D) game engine that is native to iOS or Mac. That’s a market niche where I want to move Kobold2D/KoboldTouch into, and make it stand out. Use the native platform’s OS features, programming language, coding guidelines, look and feel, and tightly integrate it with the OS.

I’m in! I think what you’re proposing is a natural evolution of the cycle of “publish book about SDK X” followed by upgrades upgrades upgrades (some of which break the code in the book) followed by “publish book about SDK X 2.0” etc. etc.

I’m not sure the long-term subscription works for a hobbyist like myself, but if one of my games takes off and I can support the subscription and do more full-time development I’d definitely go that route. As it is, the fortnight fee seems like a reasonable compromise.

Though you may have to define “fortnight” for some folks.![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I agree with Doug. I think the idea is great and I’m looking forward to checking out your hard work. My only issue is similar in that as a hobby programmer the subscription cost it out of range. The one time payment option may be workable depending on the limitations. If no doc is available online or offline after the fortnight expiration then the tools are going to be of limited use without a subscription. I do understand you’re making a living off this work so you have to do right by you first. I hope it works out. I own two editions of the book so I’m confident in the quality of the content.

I’m not entirely happy with the fortnight option having thought more about it. There may be situations that call for an immediate update, for example when a new iOS version breaks things, and users who bought it just a couple weeks earlier would then have to pay again to get the fix. That wouldn’t be fair. A longer support period seems in order, or at least free hotfixes.

As for pricing I looked at comparable commercial game engines (Corona, SIO2, Unity, …) and other game making tools (GameSalad, GameMaker Studio, …). Most ask between $200 to $400, some per year, several offer high-end “pro” options (> $500). When I considered pay-once vs subscription, it became obvious that even the pay-once products are sort of like subscriptions, since they offer frequent paid updates most users would opt-in to. It’s just a more voluntary kind of subscription.

My first goal, financially speaking, is to make sure the revenue is enough to support myself (100+ subscribers). The second goal (250+ subscribers) is to build a small team, outsource tasks, and do more of that as subscriber numbers hopefully keep growing. Eventually we can start to diversify products to allow a greater price range. Ideally I want everyone to be able to get a piece of KoboldTouch. The free Kobold2D will definitely benefit from the process, too.

I’ll start with the subscription first to learn how well it is received. I absolutely have no idea at this point. I just wish Clickbank would allow me to offer (semi) annual payments since quarterly payments are just so uncommon, but strangely they do not.

Sounds like a great idea, our programmers (incl. me) have some issued with Cocos2D that hopefully would be fixed in KoboldTouch (some TouchDispatcher issues, problems with there being one frame in-between when stuff happens, a horrible CCTransitionScene API etc).

$200/year sounds good.

My worry is probably that what if we start using KoboldTouch and build a bigger project using it, but then at some point for reasons unknown you stop supporting it (maybe you get hired by Zynga?! Or hit by a bus?). I assume it will be open source?

Ideally we’d start paying for and using KoboldTouch when it’s “done”, so we’d know that if development stops, we’re still safe and can continue the development in-house.

But I think it sounds reasonable to pay up front to get someone to spend time fixing Cocos2D’s problems, although, I’m still a bit in an undecided stage, as we’ve gotten used to Cocos2d and got our own classes to handle some problems that Cocos2D comes with.

Rest assured: I will not work for Zynga. They asked, I said no.

I can’t assure you about the bus thing. But if it makes anyone feel better, as long as I’m working on this all by myself I’ll gladly add this to the license: “Should Steffen die, all rights to KoboldTouch will be transferred into public domain.”. Of course if KT is successful and a company is founded to support it, that line would have to go because it wouldn’t be fair to the founding partners and employees who will be able to continue working on KT.

I like to better understand your issues, I think I know them but I can’t be 100% sure. If you would also share how you solved these issues, I’ll see if I can re-implement them in KoboldTouch. For the time being, you can re-use any custom class in KoboldTouch, for CCNode subclasses you would simply add your own custom ViewController to create an instance of the custom node class.

In the mid term I want to have an alternative API to cocos2d’s essential classes, because it’s not just transitions that are horrible. If you ever wanted to create your own CCAction class, oh boy you’re in for some surprise. And really most actions should run on the model, not the view, unless the animation is purely cosmetic.

Too expensive for my hobby budget. But I wish you the best of luck, have always enjoyed your brilliant code work and articles.

May be a silly question that I’m just missing the answer to but… where do we sign up? I’m game… (pun intended)

Thanks, and not a silly question. Launch is today. I’ll post it on this blog once available. Still applying finishing touches, uploading files, etc.

it might seem odd but once you start charging, only the serious ones will remain. I guess as I see it, I would be paying for what you have on offer right now for me to use, if I feel that you have joined the dark side (Disney, shudder… oh, it is not Disney, it is Zynga) then I stop using your tools, simple as that. How many developers have stopped using Cocos2D because the main developers went to work for Zynga?

It is nice to see Kobold2D evolve as a product and wish you all the best with it. However you might consider a low priced or free level for students or hobbyist or people without a budget that want to just give it a spin. This could have only the basic functionality, while the paid one could have the additional advanced functionality.

I don’t think

anydeveloper stopped using cocos2d because of Zynga. This isn’t the music industry where fans turn away from their favorite indie artist after he/she signed a deal with a big label. We’re talking about a piece of open source technology, freely available to all of us for any purpose. Who is creating it is merely a side note, what counts is whether that technology allows you to do what you need to do. In addition, developers invest time and money to learn and utilize the technology. Stepping away from it merely because of a change in ownership would be unwise if your goal is to ship an app.I do like to have a free version of KT some day. But that requires certain features developers would pay to use. Right now, that is KoboldTouch in its entirety. In the future, let’s say in 2014, I like to put out a basic version of KoboldTouch with fewer features, essentially just the framework plus a couple fundamental features.

Well, Steffen - since I decided to go back to learn coding (again, if you consider assembler on a C64/Amiga coding) I was enjoying your work.

Since I own your books, I hope I do qualify for the supporters-option in pricing - but count me in as loyal supporter… And, I am a hobbyist swell, but I will rather give my money to you and save time with my problems, so I can spend these few hours a months on my hobby-projects than wasting them with surfing for explanations and testing out 10 different approaches to a commonly known issue…

Looking forward to the release today.

Rgds from FFM,

Alex

That’s the spirit! I’ll talk to you later then, in the member forum.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


PS: Assembler is more than just coding. It’s applied cryptography!

[…] tomorrow’s launch of KoboldTouch I made a quick 6-minute presentation about KoboldTouch and what makes it […]