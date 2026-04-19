---
title: 'Stingray Renderer Walkthrough #6: RenderInterface'
url: https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-6.html
author: Tobias
published: '2017-02-22'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Today we will be looking at the `RenderInterface`

. I’ve struggled a bit with deciding if it is worth covering this piece of the code or not, as most of the stuff described will likely feel kind of obvious. In the end I still decided to keep it to give a more complete picture of how everything fits together. Feel free to skim through it or sit tight and wait for the coming two posts that will dive into the data-driven aspects of the Stingray renderer.

The `RenderInterface`

is responsible for tying together a bunch of rendering sub-systems. Some of which we have covered in earlier posts (like e.g the [ RenderDevice](http://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-5.html)) and a bunch of other, more high-level, systems that forms the foundation of our data-driven rendering architecture.

The `RenderInterface`

has a bunch of various responsibilities, including:

-
Tracking of windows and swap chains.

While windows are managed by the simulation thread, swap chains are managed by the render thread. The

`RenderInterface`

is responsible for creating the swap chains and keep track of the mapping between a window and a swap chain. It is also responsible for signaling resizing and other state information from the window to the renderer. -
Managing of

`RenderWorlds`

.As mentioned in the

[Overview](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-1-overview.html)post, the renderer has its own representation of game`Worlds`

called`RenderWorlds`

. The`RenderInterface`

is responsible for creating, updating and destroying the`RenderWorlds`

. -
Owner of the four main building blocks of our data-driven rendering architecture:

`LayerManager`

,`ResourceGeneratorManager`

,`RenderResourceSet`

,`RenderSettings`

Will be covered in the next post (I’ve talked about them in various presentations before [

[1](https://www.dropbox.com/s/rehpgc9qkzo831k/flexible-rendering-multiple-platforms.pdf?dl=0)] [[2](https://www.dropbox.com/s/rjcjiricpc89362/benefits-of-a-data-driven-renderer.pdf?dl=0)]). -
Owner of the shader manager.

Centralized repository for all available/loaded shaders. Controls scheduling for loading, unload and hot-reloading of shaders.

-
Owner of the render resource streamer.

While all resource loading is asynchronous in Stingray (See [

[3](https://www.youtube.com/watch?v=nIxuGy6Jh-0&index=12&list=UU5XCn51L8rqL3XgZfOQN6qQ)]), the resource streamer I’m referring to in this context is responsible for dynamically loading in/out mip-levels of textures based on their screen coverage. Since this streaming system piggybacks on the view frustum culling system, it is owned and updated by the`RenderInterface`

.

In addition to being the glue layer, the `RenderInterface`

is also the interface to communicate with the renderer from other threads (simulation, resource streaming, etc.). The renderer operates under its own “controller thread” (as covered in the [Overview](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-1-overview.html) post), and exposes two different types of functions: blocking and non-blocking.

Blocking functions will enforce a flush of all outstanding rendering work (i.e. synchronize the calling thread with the rendering thread), allowing the caller to operate directly on the state of the renderer. This is mainly a convenience path when doing bigger state changes / reconfiguring the entire renderer, and should typically not be used during game simulation as it might cause stuttering in the frame rate.

Typical operations that are blocking:

-
Opening and closing of the

`RenderDevice`

.Sets up / shuts down the graphics API by calling the appropriate functions on the

`RenderDevice`

. -
Creation and destruction of the swap chains.

Creating and destroying swap chains associated to a

`Window`

. Done by forwarding the calls to the`RenderDevice`

. -
Loading of the

`render_config`

/ configuring the data-driven rendering pipe.The

`render_config`

is a configuration file describing how the renderer should work for a specific project. It describes the entire flow of a rendered frame and without it the renderer won’t know what to do. It is the`RenderInterface`

responsibility to make sure that all the different sub-systems (`LayerManager`

,`ResourceGeneratorManager`

,`RenderResourceSet`

,`RenderSettings`

) are set up correctly from the loaded`render_config`

. More on this topic in the next post. -
Loading, unloading and reloading of shaders.

The shader system doesn’t have a thread safe interface and is only meant to be accessed from the rendering thread. Therefor any loading, unloading and reloading of shaders needs to synchronize with the rendering thread.

-
Registering and unregistering of

`Worlds`

Creates or destroys a corresponding

`RenderWorld`

and sets up mapping information to go from`World*`

to`RenderWorld*`

.

Non-blocking functions communicates by posting messages to a ring-buffer that the rendering thread consumes. Since the renderer has its own representation of a “World” there is not much communication over this ring-buffer, in a normal frame we usually don’t have more than 10-20 messages posted.

Typical operations that are non-blocking:

-
Rendering of a

`World`

.`void render_world(World &world, const Camera &camera, const Viewport &viewport, const ShadingEnvironment &shading_env, uint32_t swap_chain);`

Main interface for rendering of a world viewed from a certain

`Camera`

into a certain`Viewport`

. The`ShadingEnvironment`

is basically just a set of shader constants and resources defined in data (usually containing a description of the lighting environment, post effects and similar).`swap_chain`

is a handle referencing which window that will present the final result.When the user calls this function a

`RenderWorldMsg`

will be created and posted to the ring buffer holding handles to the rendering representations for the world, camera, viewport and shading environment. When the message is consumed by rendering thread it will enter the first of the three stages described in the[Overview](http://bitsquid.blogspot.se/2017/02/stingray-renderer-walkthrough-1-overview.html)post -*Culling*. -
Reflection of state from a

`World`

to the`RenderWorld`

.Reflects the “state delta” (from the last frame) for all objects on the simulation thread over to the render thread. For more details see [

[4](http://bitsquid.blogspot.com/2016/10/the-implementation-of-frustum-culling.html)]. -
Synchronization.

`uint32_t create_fence(); void wait_for_fence(uint32_t fence);`

Synchronization methods for making sure the renderer is finished processing up to a certain point. Used to handle blocking calls and to make sure the simulation doesn’t run more than one frame ahead of the renderer.

-
Presenting a swap chain.

`void present_frame(uint32_t swap_chain = 0);`

When the user is done with all rendering for a frame (i.e has no more

`render_world`

calls to do), the application will present the result by looping over all swap chains touched (i.e referenced in a previous call to`render_world`

) and posting one or many`PresentFrameMsg`

messages to the renderer. -
Providing statistics from the

`RenderDevice`

.As mentioned in the

post, we gather various statistics and (if possible) GPU timings in the`RenderContext`

`RenderDevice`

. Exactly what is gathered depends on the implementation of the`RenderDevice`

. The`RenderInterface`

is responsible for providing a non blocking interface for retrieving the statistics. Note: the statistics returned will be 2 frames old as we update them after the rendering thread is done processing a frame (GPU timings are even older). This typically doesn’t matter though as usually they don’t fluctuate much from one frame to another. -
Executing user callbacks.

`typedef void (*Callback)(void *user_data); void run_callback(Callback callback, void *user, uint32_t user_data_size);`

Generic callback mechanics to easily inject code to be executed by the rendering thread.

-
Creation, dispatching and releasing of

`RenderContexts`

and`RenderResourceContexts`

.While most systems tends to create, dispatch and release

and`RenderContexts`

from the rendering thread there can be use cases for doing it from another thread (e.g. the resource thread creates`RenderResourceContexts`

`RenderResourceContexts`

). The`RenderInterface`

provides the necessary functions for doing so in a thread-safe way without having to block the rendering thread.

The `RenderInterface`

in itself doesn’t get more interesting than that. Something needs to be responsible for coupling of various rendering systems and manage the interface for communicating with the controlling thread of the renderer - the `RenderInterface`

is that something.

In the next post we will walk through the various components building the foundation of the data-driven rendering architecture and go through some examples of how to configure them to do something fun from the `render_config`

file.

Stay tuned.

Excellent series of posts! Really learned a lot! But i've got one question. Can the engine have multiple Worlds active at once? for example, have the Level in one World and an Overlay GUI in another World?

ReplyDeleteReally appreciate the great and inspirational reading of the series,





ReplyDeleteeagerly waiting for the next post!

I have some questions about memory management though.

After reading the older referenced post "State Reflection" I found myself wondering: who actually owns the RenderMeshObject? I can see that the

WorldRenderInterface allocates RenderMeshObjects and in the end the pointer ends up in the RenderWorld.

The real question is then: In which order are Worlds destroyed and how do you

deallocate the memory if the WorldRenderInterface who allocated the resource does not have pointers to all its allocated RenderMeshObjects (the RenderWorld have all the pointers, but it does not know which allocator the memory belongs to)?

Is the missing piece here that both WorldRenderInterface and RenderWorld

are using the same allocator?

Sorry if it was wrong to ask these questions here and not in the actual article about "State Reflection".

@Dihara Yes, you can have any number of worlds active at once. It's up to the user to decide how she wants to render them.


ReplyDelete@esse Yup, correct. The WorldRenderInterface has a reference to the RenderWorld allocator. Memory for all objects associated with a RenderWorld comes from the same allocator. Next post will be up in an hour or so. Stay tuned. :)

Thanks for your reply, everything makes sense now :)

DeleteWoho post #7 has arrived, this will be a great evening!

This article is very much helpful and i hope this will be an useful information for the needed one. Keep on updating these kinds of informative things...


ReplyDeleteAndroid App Development Company

You have provided an nice article, Thank you very much for this one. And i hope this will be useful for many people.. and i am waiting for your next post keep on updating these kinds of knowledgeable things...


ReplyDeletePHP training in chennai

This comment has been removed by the author.

ReplyDeleteBest Valuable Information check this Latest Modapkbooster









ReplyDeleteAOS TV

Thoptv Apk

blackmart

Ac market

Live Net Tv

King root Apk

Apk's

APTRON offers amazon web services training with decision of numerous training areas crosswise over Gurgaon. Our aws training focuses are outfitted with lab offices and amazing framework. We have the best Amazon Web Services (AWS) Training Institute in Gurgaon and furthermore give amazon cloud aws certification training way for our understudies in Gurgaon.


ReplyDeleteFor More Info:- AWS course in Gurgaon

Thanks for amazing information. The post is about Render Interface which is added value to my knowledge. There are few more information about Render Interface that can be covered here.




ReplyDeleteHire software developers

Hire Full Stack Developers

Hire OpenCart Developer

hire opencart developers

hire virtual assistants in india

best digital marketing company in India

Hire Magento Developer

Hire FrontEnd Developer

Sky HD(DailyNewsScoop)






ReplyDeleteSky HD (not connected to UK TV channel) only works on Android and is essentially a copy of PlayBox HD. It doesn't have a lot of originality, but it works very well and seems to be reliable.

CinemaBox

CinemaBox is basically another Showbox clone. Add the ability to watch content offline, which is great if you don't always have WiFi access or are planning a long vacation in the woods but want to take some movies with you. CinemaBox is available on both Android and iOS.

WOW! I Love it...


ReplyDeleteand i thing thats good for you >>

LISA BLACKPINK คว้าที่ 1 สวยสุดในเอเชีย 2020

Thank you!

If you are the one looking for technical help in AOL mail then call us today at AOL Mail Support Number and get connected with our award-winning team of AOL Mail Services. They are capable of resolving the technical bugs and issues.


ReplyDeleteAOL Mail Support Number

Recover Hacked AOL Mail Account

Forgot AOL Mail Password

Change AOL Email Password

Recover AOL Password

Reset AOL Mail Password

Install AOL Desktop Gold

Download AOL Desktop Gold

AOL Desktop Gold Update Error

AOL Shield Pro Support

I have been on your site quite often but have not gone through this stuff. I like the information and want to speak about the same over my social channels. Hope you don't mind sharing your piece on my social network.


ReplyDeleteOffshore Software Development

app development

Front End Developer

Such a great Information. Thanks for sharing with us.

ReplyDeleteAkshi Engineers Pvt. Ltd. is a major producer, exporter, and retailer of bar separating shears in India. The

Bar Dividing Shearmachine is easy to use and maintain. It is specially designed for shearing and cutting in steel rolling mills.google 1861

ReplyDeletegoogle 1862

google 1863

google 1864

google 1865

google 1866

A new type of investment That is ready to make money continuously With the best casino services.

ReplyDeleteเว็บสล็อตแตกง่าย

หวยออนไลน์ 2021

เว็บบาคาร่า อันดับ 1

Trade Stocks, Forex, And Bitcoin Anywhere In The World:tradeatf Is The Leading Provider Of Software That Allows You To Trade On Your Own Terms. Whether You Are Operating In The Forex, Stock, Or Cryptocurrency Markets, Use tradeatf Software And Anonymous Digital Wallet To Connect With The Financial World.: tradeatf Is A Currency Trading Company That Allows You To Trade Stocks, Forex, And Cryptocurrency.


ReplyDeleteMcafee has a configuration issue due to which it starts stopping chrome from functioning. But mcafee blocking chrome is easily fixable.

ReplyDeleteI think this article is useful to everyone.

ReplyDeleteป๊อกเด้ง ออนไลน์ เงินจริง

เกมป๊อกเด้ง เล่นเกมส์

วิธีเล่นคาสิโน

หวยรายวัน

Thank you for posting such a great article. Keep it up mate.


ReplyDeleteUP URise Portal

This is my first time pay a visit at here and i am in fact pleassant to read all at single place.



ReplyDelete스포츠토토

먹튀검증

토토 대표 사이트

I love seeing blog that understand the value of providing a quality..




ReplyDelete카지노사이트

카지노사이트홈

홈카지노

카지노사이트



ReplyDelete바카라사이트

안전카지노사이트

These are genuinely enormous ideas in regarding blogging .

Muhammadi Exchange is one of the fastest growing money exchange companiesin Pakistan, providing services such as foreign exchange, money transfer and payment solutions to thousands of customers

ReplyDeletesending money broad

To view the real-time Fxit Stock price and to get an overview of the key fundamentals, simply visit Our Servlogin Webpage. You'll get access to revenue, earnings, valuation, predictors, and technical analysis from experts, news, historical data and Much More.


ReplyDeleteExcellent article. The writing style which you have used in this article is very good and it made the article of better quality.


ReplyDeleteTop Gun Bomber Jacket Costume

Cyprus Airways cancellation policy is one of the greatest in the world. The airline cancellation rules are rather basic, and you can get your money returned in a variety of ways. I'll go over the airline's cancellation methods, refund policies, cancelled flight compensation, penalty, and everything else you need to know before cancelling your ticket.

ReplyDeleteThis article will help raise money for everyone .


ReplyDeleteรีวิวอุปกรณ์กีฬา

สมัครเว็บพนันบาคาร่า

แทงบอล-สูง-ต่ำ

หวยรัฐบาล-เล่นยังไง

ufaslot

Thank you for your support

Good Morning!

ReplyDeleteThank you for your help. I frequently visit Vegas, but it never occurs to me to venture off the strip for a day excursion like this. I'll surely check them out next time - whenever that may be, it'll be this location, as it was the last time I used > Lufthansa manage my booking. If anyone has any better suggestions, please let me know.

According to Expert Market Research latest report, titled “Semiconductor Manufacturing Equipment Market: Global Industry Trends, Size, Share, Opportunity, Growth, and Forecast 2022-2028”, the global Semiconductor Manufacturing Equipment Market reached a value of US$ 84.17 Billion in 2021. The semiconductor manufacturing equipment market is primarily driven by the significant growth in the electronics industry across the globe. Furthermore, semiconductors are widely utilized to manufacture consumer electronics along with various hybrid and electronic vehicles. The major players covered in the semiconductor manufacturing equipment market report are Inpria Corp, JEOL Ltd., AM Lithography Corporation, Energetiq Technology, Inc., evgroup.in., Gigaphoton Inc., Mapper Lithography, Nikon Corporation, ASML, Canon Inc., NIL Technology, Raith GmbH, Rudolph Technologies., NuFlare Technology Inc., Qoniac, S-Cubed, SCREEN Semiconductor Solutions Co., Ltd., Vistec Electron Beam GmbH, ZEISS International; among other domestic and global players.

ReplyDeleteslot auto wallet เว็บเกม สล็อต ฝาก-ถอน ทรูวอลเล็ต ไม่มี ขั้นต่ำเว็บ พีจี สล็อต ออนไลน์ รูปแบบใหม่ พร้อม เกมมันส์ๆ สล็อต แตกง่าย ที่ทำเงินให้มากมาย ที่คุณไม่ควรพลาด ณ ตอนนี้

ReplyDeleteRelationship Counseling

ReplyDelete진안출장안마

ReplyDelete무주출장안마

장수출장안마

임실출장안마

순창출장안마

고창출장안마

부안출장안마

서울출장안마

The lender will deposit your Guaranteed Approval Payday Loans amount directly to your bank account by the end of the next working day. It may happen earlier if you apply and get Same Day Short Terms Loans Unsecured approved on the morning of a business day.

ReplyDeleteGreat blog, thank for sharing with us. With expertise in Impurity Research, our scientific team specializes in the custom Synthesis of Impurity standards including Nitrosamines Impurities, Oncology Impurities, and Peptide Impurities.

ReplyDeletePaschim Vihar, a bustling locality in Delhi, houses a state-of-the-art Nandi IVF Centre dedicated to helping couples achieve their dream of parenthood. This cutting-edge facility combines advanced reproductive technologies with compassionate care, offering a comprehensive range of fertility treatments. The highly skilled team of fertility specialists at the IVF Centre in Paschim Vihar employs the latest medical advancements to provide personalized solutions for infertility challenges.


ReplyDeleteFrom in vitro fertilization (IVF) to intrauterine insemination (IUI), the center employs a holistic approach, ensuring individualized care for each patient. With a commitment to excellence, the

IVF centre in paschim viharstrives to make the journey towards parenthood a positive and successful experience.고흥콜걸

ReplyDelete구례콜걸

곡성콜걸

광양콜걸

담양콜걸

나주콜걸

순천콜걸

여수콜걸

Thanks for sharing the information keep updating, looking forward to more post.



ReplyDeleteableton-live-crack-license-key

Paragon NTFS Crack

ReplyDeleteWow, this walkthrough is incredibly detailed and helpful! The way you broke down the Stingray Renderer makes it so much easier to understand. Thanks for sharing such valuable insights! Also, if anyone ever finds themselves in need of expert legal help, feel free to check out this, It’s always great to have reliable professionals on your side!


ReplyDeleteabogado dui dinwiddie virginiaadd tag

abogado dui southampton virginiaadd tag

abogados de lesiones personales de hampton virginiaadd tag

mejores abogados de divorcio en nueva jerseyadd tag

abogado de accidentes de motocicleta virginiaadd tag

abogado de patrimonioadd tag

abogado dui new kent virginiaadd tag

abogado testamentario y testamentarioadd tag

buen abogado de accidentes automovilísticos

abogado de accidentes de camiones

Just as the Stingray Renderer Walkthrough #6: RenderInterface reveals clarity behind complex visuals, a portable nebulizer brings clear relief to congested airways with every breath.

ReplyDeleteStay connected effortlessly with FM WhatsApp Auto Reply, a smart feature that automates responses using keywords, schedules, and custom rules. Perfect for personal use or businesses, it ensures you never miss a message.

ReplyDeleteIf you enjoy decorating your home with natural materials, then wcspk is a store you shouldn’t miss. They offer trays, bowls, and handcrafted pieces that add a traditional yet stylish touch to any home. Their ongoing discounts make it even more tempting to place an order.

ReplyDeleteThis article covers some valuable insights about apparel quality control. I recently came across a reliable brand in this space — click here to check out their work. They specialize in manufacturing custom sportswear, gym wear, and sublimated kits for international teams and retailers

ReplyDeleteI recently reviewed several companies before finalizing Shiv Shanker Techno, and I’m glad I chose them. Their experience clearly reflects in their work quality and execution. While looking for trusted pre engineered building manufacturers their solutions seemed more refined and well thought out. The entire process felt organized and transparent, which gave me complete confidence. Highly recommended for anyone planning modern industrial or warehouse projects.

ReplyDelete