---
title: 5 Tips for Programmer Productivity
url: https://bitsquid.blogspot.com/2012/01/5-tips-for-programmer-productivity.html
author: Niklas
published: '2012-01-05'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

## 1. Embrace the now-principle

If something takes less than five minutes to do, do it immediately.

It seems like the lazy option, but postponing something actually takes a lot of effort. The task needs to be written down somewhere. Then you need to track it and prioritize it with respect to other tasks. You will probably think

*about*doing it lots of times, before you actually get down to

*doing*it. And then you have to understand what you meant when you wrote it down and try to get back in that same mindset.

For small tasks it is just not worth it.

Instead, just do it. Fix the issue right now while you are already thinking about it. It is faster, simpler and saves you the agony of an ever growing todo-list.

## 2. Fix the cause, not just the symptom

Don’t just fix problems. Fix the

*processes*that allowed the problems to occur, so that the same problems never occur again. See bugs not as nuisances, but as chances to improve your processes and increase the quality of your code.

If an artist tells you that she gets an ”Error when compiling unit” error, don’t just diagnose it and tell her: ”It’s because you have two nodes with the same name, that is not allowed.” At the

*very least*fix the error message so that it says ”Error when compiling unit ‘bed’. Two nodes have the same name ‘pillow’. One of them must be renamed so that names are unique.” Even better, fix the exporter or the tool, so that it is

*impossible*for the artist to create two nodes with the same name.

If you find an error that could have been caught by an assert, then add that assert so that it will find the error next time.

If someone asks you ”How can I configure the animation compression?”, don’t just answer them. Also write a short text that explains how it is done, and

*add that text to the documentation*.

In this way, you are not just patching holes and fixing leaks, you are actively making things better. This not only pleases the people who come to you with problems, it also makes your work feel more meaningful.

## 3. Try not to break concentration while ”the computer is working”

The job of programming is filled with a lot of weird little micro pauses. The code is compiling. The console is rebooting. The level is loading. The client is connecting. Etc.

In the best of worlds, these pauses would not exist, and by all means, do all you can to get rid of them. Make your code build faster. Hot reload data and scripts. Make a tool for quickly setting up a bunch of PS3s for a network test. Etc.

But even with the best of efforts, some pauses will likely remain. The question is what to do with them. The temptation is to take a short break from programming and do something else: check mail, answer a Skype, read two paragraphs of an interesting article, update the twitter feed, etc.

For me, these constant mental context switches can put a real damper on productivity, since they make it impossible to maintain concentration and flow.

Nor are these micro-excursions particularly relaxing. Reading two paragraphs of a web page while constantly glancing at a progress bar on the other monitor is not something that soothes my mind. Quite contrary, it is much more stressful than remaining in the zen-like state of concentrated work. It is much better to take one real break than a hundred micro breaks.

So for both productivity and peace of mind I now make a conscious effort to stay focused on the problem at hand while ”the computer is working”. I have a

[separate text editor](http://www.sublimetext.com/2), unaffected by IDE freezes, where I can work on related tasks, such as:

- Adding documentation
- Refactoring and code review
- Planning the next stage of implementation
- Writing script code that tests the system

It is still an ongoing battle against the Lure of the Internet, but I find that when I manage to stay focused I am both more productive and more relaxed.

## 4. Use source control even more than you think you should

Source control is not just for source code. With modern distributed source control systems such as Mercurial and Git it is dead simple to create a source repository anywhere and then later (if needed) push it to a server for backup/sharing.

Do you have configuration and settings files for your text editor, IDE, etc? Put them in source control so that you can easily share them between your different machines. Do they need to be installed in special locations. Put them in source control together with a script that installs them in the right place.

Do you use any third party libraries such as zlib, LuaJIT or stb_vorbis? Check them into source control. That way, if you have to do any modifications (bug fixes, fixes for compiler warnings, platform fixes, your own personal optimizations, etc) you will know exactly what you have changed. If a new version of the library is released you can use the source control diff to see what has changed upstream and merge it with your own local changes.

Does an API come with sample code? Before you start playing with that sample code, check it into source control. That way, you can always revert the samples back to their pristine state, without having to reinstall the API. And if you find a bug in the APIs and manage to reproduce it in one of the samples, you can use the source control tool to produce a .patch file for the sample that you can send to the API manufacturers as part of your bug report. That will keep both you and them happy.

## 5. Monitor your builds

Set up a build server that continuously builds all your executables (engine, tools, exporters, ...) in all configurations (debug, development, release) for all platforms, so you know as soon as possible if something breaks. Fixing a problem right away is much easier than doing it two months down the line.

The build server doesn’t have to be a complicated thing. It is more important that it exists than that it has all the bells and whistles. If you don’t have time to do something advanced

[just write a script](http://altdevblogaday.com/2011/05/11/write-a-script-for-it/)that compiles everything and reports the result. You can expand on that later.

Do the same for content. Write a script that loads all levels and spawns all units.

Use the report system that works best for you. We use Skype for internal real-time communication, so it makes sense to report broken builds over Skype. If e-mail or IRC works better for you, use that instead.

The blog was very informative thanks for sharing. Yellowstone Coat

ReplyDeleteStayColdApparel Have exclusive new Designs for you available in Pre-order




ReplyDeleteBook your with StayColdApparel "Stay Cold" (staying cold) to distance yourself from the opinions and expectations of others so you'll be able to achieve the freedom, to go your own way, live true to your own values and become yourself, no matter what! Its your life and you set the rules! Make the best out of it. Stay Cold.

For more details Visit us:- www.staycoldapparel.com

I couldn’t agree more that, establishing a solid online presence has become critical for all kinds of businesses in today’s ever-evolving digital market that’s why seo services are needed to enhance your website visibility on search engines

ReplyDeletehttps://www.lakhanisolution.com/search-engine-optimization/

This comment has been removed by the author.

ReplyDeleteWithout a doubt, I agree that The way that businesses manage their purchasing and stock control has been completely transformed by Purchase order and inventory management software . These powerful tools automate the entire procurement process, from the creation of purchase orders to the monitoring of inventory levels and replenishment management.



ReplyDeleteGreatly described, Start-up software solutions are critical to the success of new businesses. These tools can help with everything from project management and collaboration to marketing automation and customer relationship management.



ReplyDeleteGreat work! The way you describe your words is the best, very informative.The most popular general ledger software solutions represent financial management pillars in the business world. These powerful platforms provide a comprehensive and sophisticated method of recording, tracking, and analyzing financial transactions.

ReplyDeleteAppliances and emergency plumber near me systems can malfunction unexpectedly. Knowing whom to call in times of crisis is crucial to minimize damage and inconvenience.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteExcellently elucidated, The warehouse management system is the foundation of effective logistics and operations. This cutting-edge software solution adds a new level of organization to the complicated world of warehouses.

ReplyDeleteNicely explained, in today’s interconnected world companies are not only vying for attention on a global scale, but are also competing for attention in their local communities. Local seo services

ReplyDeleteprovide a tailored and targeted approach to enhance your setup and appear on google maps.

The availability of immediate assistance for login issues from Indibet login customer support team exemplifies their commitment to uninterrupted user engagement. It's a clear signal that they prioritize user satisfaction above all.

ReplyDeleteWhen I went shopping for a new LED TV, I was happily surprised by the reasonable led tv price in pakistan .There were so many options available that it was pretty simple to find the perfect LED TV within my budget. Researching revealed that numerous manufacturers offer excellent prices without compromising quality. It gives me comfort to know I can acquire a great TV without going over budget.Whether you want a high-end model with cutting-edge capabilities for your living room or a basic LED TV for your bedroom, you may discover a fantastic offer on LED TVs in Pakistan that suit your requirements.

ReplyDeleteFor those in the UK seeking the

ReplyDeletebest crypto wallet uk, security and functionality are paramount. Opt for a wallet that supports a wide range of cryptocurrencies. User-friendly interfaces make managing your crypto easier. Prioritize wallets with robust encryption and multi-factor authentication. User reviews can provide valuable insights into performance. Reliability is a must for any wallet. Lastly, good customer support can be very beneficial.In conclusion, wholesale suppliers are integral partners for businesses seeking cost-effective and efficient supply solutions. Their ability to offer competitive pricing, flexibility in orders, and consistent product quality makes them invaluable allies in the journey towards business growth and sustainability. By forging strong partnerships with reliable

ReplyDeletewholesale suppliers, businesses can enhance their operational efficiency and maintain a competitive edge in today's dynamic marketplace.A travel wifi hotspot helps avoid the hassle of searching for public Wi-Fi. I found Wifi Hire, and their service seems straightforward.

ReplyDelete