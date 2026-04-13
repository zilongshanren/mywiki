---
title: TexturePacker goes GUI!
url: http://www.learn-cocos2d.com/2010/10/texturepacker-gui/
author: Marcotronic Says
published: '2010-10-31'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

The previously command-line-only [TexturePacker](http://www.code-and-web.de/texturepacker) tool now has a nice GUI. It’s called the “Pro” version and for a reason. So far, I’ve been using [Zwoptex](http://zwoptexapp.com/) for creating Texture Atlases, but I’ll certainly give TexturePacker Pro a try.

At first glance, what I liked was that it told me when the Texture Atlas was “full”, eg. not all sprites could fit into that Texture Atlas. And the always present list of image filenames on the right side is a welcome feature. Although Zwoptex does have this list as well, it’s almost rendered useless because it’s a seperate view option.

Zwoptex’ price has changed since I checked last time, it’s now at only $14.95. TexturePacker Pro costs $17.95, it’s command line version $9.95 and the upgrade from command line to Pro is $7,95, so you’re saving a whopping $0.05! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


### A couple words on pricing

I find both tools are underselling themselves. Zwoptex was initially at $24.95 and even that price seemed “cheap” to me, given how much trouble it saved me and how much faster and more memory efficient it made my projects. I would say that a price range of $30 to $50 would be more than fair for those tools. I can imagine that the TexturePacker command line version at $9.95 and now the Pro version probably forced Zwoptex to adjust its price.

Problem is: this isn’t a market where people choose their tool based on a $3 price difference. Also, it decreases margins for upgrade prices, with TexturePacker upgrade already below $10. Those low-end prices incur a proportionally large amount of transaction fees, paid to the eCommerce vendor, making them less viable. Since this is also not a mass market, but a niche, it would be wiser if both upgraded their prices back to reasonable regions, around or above $30.

Likewise, [Particle Designer](http://particledesigner.71squared.com/index.php?page=buy) is also absolutely undervalued at $7.99. Those low prices undercut the value in tools, and make tool development less and less attractive than it already is. And if anything, cocos2d and the other engines need one thing above all else: tools. And good ones!

Be it [Ricardos mysterious “world editor”](http://www.cocos2d-iphone.org/forum/topic/5015#post-51096) or the [Physics + Tilemap IDE](http://www.cocos2d-iphone.org/forum/topic/9064) ([website](http://tato123.wordpress.com/)) or the other game editing tools currently being worked on - if any one of them is being released as a commercial product but sold for less than $30, I’m going to be very mad at you! If it’s less than $60 I’ll still be mad at you, not very, but still mad.

### Rant

Seriously, this isn’t the App Store! It’s developers you’re selling to, and they do value useful tools. Just because cocos2d is free doesn’t mean that all tools surrounding it need to be cheap (or free for that matter). Take [Sprite Manager ](http://www.anbsoft.com/middleware/sm2/)2 for example. It sells for $75 (per seat!) and isn’t all that different from Zwoptex or TexturePacker Pro. If it were a standalone app it would probably pale in comparison! You might argue that SM2 is for Unity, and their developers are less price sensitive - I don’t think so, and some are even more price sensitive because they just made that huge investment in the first place.

In general you could say that those developers who invest several hundred $$ into a game engine (and toolset) are simply more serious about game development. You do have those enthusiasts working with cocos2d as well, but they’re probably outnumbered by a lot of hobbyists and “I’ll give it a try” kind of people who simply join because of the fun involved, and because the only investment in cocos2d is time and they got plenty of that. The question is: do you want to be kind to the hobbyists, or do you want to build a sustainable business? Plus, Zwoptex and Texturer Packer are also being used by Corona developers.

Now you may also be arguing that a cheaper price allows more developers to enjoy the tools and we’re a friendly bunch and not a commercial, greedy corporation. Sure. But those prices do devalue everyone’s tools, so if anyone wanted to build a tool that takes maybe not just 1-2 months to build (initially), but maybe 4-6 months or more before it’s going to be useful, those price points are not very encouraging to start such a project. That doesn’t mean it won’t happen, but I do know that those people who could pull this off, are generally terrible at doing business. And easily influenced by comparable prices, punching a few numbers, and then getting on with their next train of thought which probably involves solving an obscure programming problem.

And the kind of tool that needs this time investment is the one I’ve been looking forward to since I first started working with cocos2d in May 2009. Back at the time I was convinced that by the end of 2009 cocos2d would be having a game editor or at least something to build the GUI and screens with. I wished for a fully-fledged, professional game level editor, with a physics editor, sprite animation builder, asset management, and whatever else you can dream of.

Now, if that ever happened, it shouldn’t cost less than $100. If you can provide killer features like Box2D integration or scripting game logic, ask twice as much. And offer Lite and Pro versions with a variety of feature sets to make the most out of what developers need and what they are willing to pay extra for niche, but very useful features if you need them.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I totally agree! Those tools are really extremely underprized.

And you are right: A really good “Game Editor” thingy with physics and all the stuff you mentioned shouldn´t really be under $100. I´m sure it would even sell very well with a prize of $500-$1000. Or a payment on title-basis e.g.

If I had the time to create such a Game Editor myself or the money to hire some developers for this I would have created such a tool already and I´m sure I would have become very very rich with the right marketing strategy already.

There is a huuuuuuge market for these kind of tools!

Marco

You say huge market because it’s a stomach feeling, or do you have actual data or an argument based on circumstancial evidence?

For example, if you consider Corona to be a “tool” and it attracted 15,000 developers, which puts it way past the $1 Mio revenue mark even with pessimistic calculations, it doesn’t take a genius to figure out that a tool sold to Corona developers, selling for $50 with only 10% of Corona users buying it, will make $75.000 in revenue. Make it a yearly payment, and you’re all set for the next 2-3 years.

that huge market feeling is merely a rough guess but exactly for the same reasons you mentioned in your Corona example. I mainly have that Game Editor idea in mind, generating e.g. cocos2D code with all the tilemap, physics, level editor, scene management stuff etc. producing code (possibly readable and manually maintainable if you like) with a good performance or producing “hidden code” that you usually don´t edit manually. Ideally with a scripting functionality within (e.g. with LUA) - let´s call it “Game Salad” generating stable code with a high performance, more flexibility and the possibility to script things with LUA or let´s call it “Corona Game Engine” with a nice GUI and all that Tilemap, Level Editor things.

When I started to develop games for myself years ago on Windows I played a bit with “Game Maker” by Mark Overmars (wich is now under the hood of Yoyo Games) - I totally loved this concept because you have a nice GUI for all that stuff you desire as a game developer but you still have the chance to code things if you like and you could extend Game Maker with own DLLs (I developed a sound extension with Delphi at that time). As I´ve seen Game Maker is available for Mac now, too, (also totally underprized by the way…) and an iPhone/iPad deployment seems to be in development right now.

My rough guess is that if you market such a Game Maker like tool for iPhone development you´ll be rich in no time just because something comparable is just not available yet and you could be so much more productive with a tool like this for game development and I´m sure you could sell it for let´s say $500-$1000. Time is money and such a tool would be a great time saver.

Marco

Oh, you too? I know that at least 4 game editing tools are currently in development for cocos2d. Two were already mentioned on the forum (Riq’s mysterious “world editor” and the Phyics + Tilemap IDE). One probably falls into that “Game Maker” category. The fourth I have no idea what it’s going to be like but I’m sure it won’t disappoint. And well, I had already done some groundwork on a game editor while I was writing the book, but now that I would have had the time to work on it, I find that others are already working on tools in so many directions, I don’t want to jump into a possibly crowded market and possibly face the same issue as Zwoptex & TexturePacker, if another tool would be very similar to my own. I’ll wait and see what others are doing, if those tools end up being a nice effort but ultimately flawed, if only because no one is working on their tool full time or if they remain niche, or their user experience leaves a lot to be desired (I fully agree with Robert here), then maybe I’ll get that fully fleshed out idea for a 2D game editor (written and conceived exactly 1 year ago) back out of the drawer and start working on it.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Game Maker is awesome, I made a few games with it and I was the first to write a Physics DLL, which inspired a lot of physics-based games. That was maybe 8 years ago. I think GM is (or was) priced at $15, which is ok given that the majority of users seem to be kids aged 10-16 years.

Something comparable isn’t available yet? What about Gamesalad then?

- Do GameSalad games run with high performance (or any even “good”)? I don´t think so

(Okay Game Maker games weren´t high performance games, either… 😉 )

- Does GameSalad have scripting capabilities yet? Not as far as I know.

This may come but still there is nothing really usable, I think. I´ve bought a GameSalad license (indy) recently but the results don´t really satisfy me.

I´m really looking forward to Riq´s World Editor thingy! Hope that will be something cool! 😉

Marco

PS: Cool to hear you were a Game Maker Fan, too!

That’s true, GS performance is a problem from what I hear.

Not sure what I should expect of Riq’s editor. He’s shown that his focus is on engine programming, and hardcore at that. I’ve seen game engine programmers develop tools before, even for their own engines, and the results were always way too technical and in general not a pleasure to use. So just from these experiences I remain really skeptical about that because you really have to have the tools development in you. And one crucial requirement for a game tool developer is that you have to be a game developer to actually know what is expected and how people are using the engine and how tools are supposed to work and what problems they’re supposed to solve. The game engine coder’s tools that I’ve seen ended up representing the game engine’s structure close to 1:1 which rarely matches how game designers think about the game. Right now I’m betting that one of the game editing tools developed by cocos2d users stand a better chance of providing what developers need, the Tilemap & Physics IDE looks promising, but 4 weeks with no update and I’m thinking this project will remain in it’s infancy, or may not even see the light of the day, eventually being uploaded as work in progress on github for others to gnaw on.

I’m sorry if I’m overly pessimistic. I’ve seen too often that promising projects (like Gleed2D for example) are being worked on feverishly, only to be dropped and eventually released as open source, as if open source were a scrapyard. I doubt that Riq’s editor will have that problem, because I have no doubt in my mind that it’s going to be a commercial product, and rightfully so. But again, in that case I’m more concerned about actual usability.

Regardless, please show me that you can, I’d like to be proven wrong in these cases!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Good point. Pricing should also be based on how many sales you expect. In cases like this, where these tools are being made for a very niche market, sales will be low, so prices should be higher. Especially since tools like these saves devs a lot of time so they don’t have to build something similar themselves, which directly equates to money. You can only really afford to make the price cheap when you expect a ton of sales (like the classic “App Store Gamble”).

Exactly, weirdly enough, the first reaction to “not so great sales” is to lower the price. That seems so commonplace that every seminar about founding a company or becoming self-employed that I’ve attended (must have been about four or five) warned about that. In most cases, it’s *not* the price that influences sales respectively it’s not the reason why people aren’t buying. There’s a number of factors to be considered.

Love the rant…. So true…. I hope those dev’s and future ones read this!

I talked to other devs today who said the same thing. Zwoptex being way too cheap, when I told them it’s now only $15 there was only headshaking. Then we went on to rant about software that’s way too highly priced ($5.000 for a Flash code package) or just awkwardly licensed (yearly payments for a class that plays a car engine sound and has more code for license and anti-piracy checks than actually playing the sound).

I was pretty much forced to reduce the price on Zwoptex lower than texture packer for the time being. The feature set is much less of Texture Packer pro but it’s benefits are in the User Interface ( Progress meters, auto updating etc.. ) while lacking some of the power features ( Extruding etc.. ).

I’m working on Zwoptex 1.5 which will be a major release and include a lot of great goodies at that point I’ll be reevaluating where the tool sits in the spectrum and price it accordingly.

In the end the tool that is the best to use will win the user over regardless of features. A lot of people will probably still pick Zwoptex over Texture Packer for a variety of reasons or vice versa.

-Robert

That’s understandable, and what I expected. In this case, I don’t know why TexturePacker Pro wasn’t priced at $30. I’m sure that would have worked better for the both of you.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I’m looking forward to v1.5, if there’s one good thing about competition is that it makes one work harder.

Ah - the prices 😉

I simply would not mind earning more. But I am currently new in the market - with a strong but not yet known product. Zwoptex is referenced everywhere: In the cocos sources, examples, test code, documentation, wiki… Peope think that Zwoptex is the “native” sprite creation tool for cocos.

This is why my price was set to something near Zwoptex but a bit lower….

And there is a “problem” with a community like cocos: Cocos is free - many users are indie developers - so people expect to get cheap tools. Why pay for a small sprite sheet creator when everything else is for free.

For a bigger company the price is too low…

I understand the argument. But lets look at it this way: TexturePacker Pro has some more features than Zwoptex, even Robert says so. With the confidence that it’s the better product (for the moment, Zwoptex v1.5 might change that) I would have looked at Zwoptex’ price ($25) and set its price *higher* because it’s justified. The job then becomes telling why and convincing the customers that it’s better. It’s one thing to attract customers by saying “hey look, my tool is cheaper than the other tool everyone is using”. The other is “hey look, my tool is better than the other tool everyone is using, and I’m going to tell you why”. I believe the latter is actually easier because it’s based on facts that you can promote, not merely on price, which is a very weak motivator. That’s right, despite customers often being price aware, that’s only true if you have a large selection of equal items, see supermarket - and even then there’s those who would rather spend 50% extra on a branded item, despite both being virtually the same.

The problem with the “my tool is better, that’s why it costs more” approach may very well be a psychological thing. You’d actually have to tell people that they have a choice and convince them why your product is the better choice. Since both tools do the same job, the focus should be on “It does everything Zwoptex does, plus A, B and C. That’s why it costs more.”. It would require to go head to head, to tell people they have a choice, to directly compete in features and marketing, and by offering feature comparisons of the tools (as has been done on the Cocos2D wiki, I’m surprised that this was even allowed - one day I’d like to see that happen with Starterkits, but … hmmm, on what features would we compare them? I think then it would become very obvious that those products compete only indirectly, but that’s a totally different matter).

Given a little time and constant promotion, everyone will come to know about both tools equally well. Zwoptex will have an advantage for a while simply because it was first to market and has been mentioned more often, it’s in people’s minds alright. But there’s a lot you can do to change that. But, as always, it’s easier to change the price than to do constant promotion and slowly grow your market. Slashing the price is the easy way out that’s done too often but is just as often the wrong way.

As for people being price aware: it’s true, Cocos2D is free. But consider for a moment here that Ricardo has been living off his source code sales for 2,5 years now, and they are priced at $199 to $349. Not everyone has the money for that, but enough people frequently buy these Starterkits to generate at least a decent amount of income. While Ricardo states he is not getting rich (by whose standards?) and not making as much as working for a big company (which company and which position? You can easily make $10,000 a month in most big companies if you’re the lead engine developer), he’d be stupid not to promote his products if he was in danger of actually going broke, so I’m assuming the income for him must be in the “comfortable” range.

The biggest aspect here however is the amount of respect people have. Ricardo made Cocos2D so he has a relatively easy time selling his products without actually promoting them. For me, with no promotion, sales aren’t that good but the revenue is still over $1,000 per month on average, and I guess I have the “pro developer” and book author in my favor. The RPG Game Kit is slowly picking up, I don’t have any numbers but I believe its user base is slowly growing, I only know the initial start was not so great. That is surely because there’s a product whose developer wasn’t known at the time, there was no trust and respect built between potential customers and developer, something which I believe goes a long way in the market of selling to other developers. My first reaction was “What, he made a game in ’95? Way to sell …”. 😉 But I think the RPG Kit author Nate Weiss is also slowly improving his public profile and product through frequent updates.

The question is, how many more people buy TexturePacker Pro because it’s half the price what it could be, and how many of the customers would have gladly paid double the price? If that amounts to more than 50% of the customers, you’re losing money. But the biggest seller above all else is personal profile combined with an investment in the product shown through frequent updates. I haven’t done any updates to my Starterkit, and it’s showing in slowly declining sales. It’s not just the not updating, it’s not having a reason to mention it over and over again that’s hurting my sales right now. It’s definitely not because people are choosing the other products, or because their price was slashed, because no one else offers the code for Line-Drawing games. In your face, direct competition. :p

But that’s not a comfort that you or Robert have. Your choice is either a price war, or constantly improving your products. I opt for the latter but I’m unhappy that you chose the former at the first sight of competition.

This is a really interesting conversation. The price of tools has been in our minds recently as well while working on Particle Designer 1.3. When we released Particle Designer we were thinking that we didn’t want to price ourselves at a level that would stop people getting access to Particle Designer. The response to the product has been amazing and for sure we could have made significant money on it given it’s sales if it had been priced much higher. For us this was also a learning curve as there was not real example of how to price tools in this area, especially around other assets that are free, such as Cocos2D.

What we didn’t do when pricing it was think about the effort required to keep the tool innovative. We have been working for the last four months on Version 1.3 which is going to add a new significant feature in the form of editing particle emitters live on iOS devices. The feature has been complete for a while but we have been working on ironing out annoying instability issues.

This new version has been taking significant time to complete and get right. It has honestly shown us that we priced Particle Designer much too low to start with and with the introduction of other tools around engines such as Cocos2D, it does have the impact of undervaluing other tools being developed.

I agree that tools for devs are really important and gives them time to work on innovation with the game.

At 71Squared we want to continue creating tools for game developers as well as app developers. I’m currently working on Glyph Designer which again we think is going to be a really handy native OS X tool for creating cool bitmaps fonts for the likes of Cocos2D.

Given our experience, we will be announcing that the price of Particle Designer will be increasing when v1.3 is released. The effort that has gone into version 1.3 is significant and there is still more we want to add. By increasing the price we feel we will be protecting our ability to continue to support and innovate the product and also help protect the value these tools have in the community. The more developers that see this area as a thriving marketplace with good revenues, the more developers will look at creating new tools for everyone to use.

We have not decided on a final price yet and it’s not going to be some insane increase, but it will be representative of what we feel the value is for the tool. We are also planning on selling the apps through the Mac App Store as well. As Apple will be taking 30% of the price we will need to take that into account going forward.

I think competition is good, it’s what drives some of the best innovation. I don’t think the decision is going to be around cost alone. The application that provides the most appropriate features is what people will choose and as we have found, putting out new releases with great new features takes time and effort which the price of the app needs to reflect.

Mike

Thanks for this comment, Mike. I could not live without Particle Designer, if I needed to I would even spend up to $100 for the new version. But then I’m a professional developers, used to buying professional software and weighing the price against the time saved (or spent creating the tool myself). If you think that way, it’s always easy to see the great value in game tools.

As for Cocos2D being free, what many often forget is that you get the engine for free but not the support. So if you want actual code samples (which for me is the best way to learn a new code base) for the past 2.5 years your best option was to buy the code from Riq for $199 through $349. And developers have been paying for that enough to earn him a (what I assume to be a) comfortable living. So the commercial aspects are already there and developers are buying enough to make it worthwhile. Of course, I’m guessing the vast majority won’t (the Xcoders like to get their stuff for free) and if the goal is to allow as many developers as possible to benefit from a tool, while still being able to earn enough, there’s only one option: offer product variations and price them based on their feature set. For example, you could release the feature set of Particle Designer v1.2 for the current price or even free, which will contain the features a lot of developers will be happy with. At the same time, the low-cost or free version of the product promotes the more expensive one, which also adds powerful features like tweaking particles on the device. At least that’s what I would do. And if you look at Unity or a lot of other products, you’ll find this versioning of a product is quite common and works well. Especially if you have an upgrade path and enough relevant features to create several versions of the same product.

Great to hear about Glyph Designer, it’s about time that I can get rid of Hiero with all its bugs and oddities.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


PS: if PD 1.3 will be coming out before Xmas, let me know. I’ll include it in the Linkvent Calendar: http://www.learn-cocos2d.com/2010/11/cocos2d-linkvent-calendar-2010/