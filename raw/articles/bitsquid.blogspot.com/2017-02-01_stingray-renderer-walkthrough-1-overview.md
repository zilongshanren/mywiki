---
title: 'Stingray Renderer Walkthrough #1: Overview'
url: https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-1-overview.html
author: Tobias
published: '2017-02-01'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

When we started writing Bitsquid back in mid 2009 all platforms we intended to run on were already multi-core architectures. This and the fact that we had some prior experience trying to get our last engine to run efficiently on the PS3 answered the question how *not* to architecture an efficient renderer that scales to many cores. We knew we needed more than functional parallelism, we wanted data-parallelism.

To solve that we divide the CPU view of a rendered frame into three stages:

`Culling`

- Filter out visible renderable objects with respect to a camera from a potentially huge set of different type of objects (meshes, particle systems, lights, etc).`Render`

- Iterate over the filtered result from`Culling`

and “record” an intermediate representation of draw calls/state switches to a command buffer.`Dispatch`

- Take result from`Render`

and translate that into actual render API calls (D3D, OGL, Metal, GNM, etc).

As you can see each stage pipes its result into the next. Rendering is typically very simple in that sense; we tend to have a one way flow of our data: [[user input or time affects state, state propagates into changes of the renderable objects (transforms, shader constants, etc), figure out what need to be rendered, iterate over that and finally generate render API calls. Rinse & Repeat :]]

If we ignore the problem of ordering the final API calls in the rendering backend it’s fairly easy to see how we can achieve data parallelism in this scenario. Just fork at each stage splitting the workload into a *n*-chunks (where *n* is however many worker threads you can throw at it). When all workers are done for a stage take the result and pipe into the next stage.

In essence this is how all rendering in Stingray works. Obviously I’ve glanced over some rather important and challenging details but as you will see they are not too hard to solve if you have good control over your data flows and are picky about when mutation of the data happens.

The rendering code in Stingray tends to be heavily influenced by Data Oriented Programming principles. When designing new systems our biggest efforts usually goes into structuring our data efficiently and thinking about its flow through the systems, more so than writing the actual code that transforms the data from one form to another.

To achieve data-parallelism throughout the rendering code the first thing to realize is that we have to be very picky about when mutation of the renderable objects happens. Multiple worker threads will run over our objects and its not unlikely that more than one thread visits the same object at the same time, hence we must not mutate the state of our objects in its render function. Therefore all of our `render()`

functions are `const`

.

To further guard ourselves from the outer world (i.e gameplay, physics, etc) the renderer operates in complete isolation from the game logics. It has its own representation of the data it needs, and only the data relevant for rendering. While the gameplay logics usually wants to reason about high-level concepts such as game entities (which basically groups a number of meshes, particle systems, lights, etc together), we on the rendering side don’t really care about that. We are much more interested in just having an array of all renderable objects in a game world, in a memory layout that makes it efficient to access.

Another nice thing with decoupling the representation of the renderable objects from the game objects is that it allows us to run simulation in parallel with rendering (functional parallelism). So while simulation is updating frame *n* the renderer is processing frame *n-1*. Some of you might argue that overlaying rendering on top of simulation doesn’t give any performance improvements if the work in all systems is nicely parallelized. In reality though this isn’t really the case. We still have systems that don’t go wide, or have certain sections where they need to do synchronous processing (last generation graphics APIs: e.g DX11, OpenGL are good examples). This creates bubbles in the frame slowing us down.

By overlaying simulation and rendering we get a form of bubble filling among the worker threads which in most cases gives a big enough speed improvement to justify the added complexity that comes from this architecture. More specifically:

- Double buffering of state - since the simulation might mutate the state of an object for frame
`n`

at the same time as the renderer is processing frame`n-1`

any mutable state needs to be double buffered. - Life scope tracking of immutable data - while immutable/read only state such as static vertex and index buffers are safe to read by both simulation and renderer we still need to be careful not pulling the rug under the renderers feet by freeing anything still being in use by the renderer.

Here’s a conceptual graph showing the benefits of overlaying simulation and rendering:

So basically what we got here is two “controller threads”: `simulation`

and `render`

both offloading work to the worker threads. In the case that a controller thread is blocked waiting for some work to finish it will assist the worker threads striving to never sit idle. One thing to note is that to prevent frames from stacking up, we never allow the simulation thread to run more than one frame ahead of the render thread.

As a comparison here’s the same workload with simulation and rendering running in sequence.

As you can see we get significantly more idle time (bubbles) on the worker threads due to certain parts of both the simulation and rendering not being able to go wide.

I think this pretty much covers the high level view of the core rendering architecture in Stingray. Now lets go into some more detail.

Since Andreas Asplund recently covered both how we handle propagation of state from simulation to the renderer (we call this “State reflection” in Stingray): [http://bitsquid.blogspot.se/2016/09/state-reflection.html](http://bitsquid.blogspot.se/2016/09/state-reflection.html) as well as how our view frustum culling system(s) works: [http://bitsquid.blogspot.se/2016/10/the-implementation-of-frustum-culling.html](http://bitsquid.blogspot.se/2016/10/the-implementation-of-frustum-culling.html) I won’t be covering that in this series.

Instead I will jump straight into how creating and destroying GPU resources works, and from there go through all the building blocks needed to implement the second stage `Render`

mentioned above.

Our sap scm mentors are sap production network the board (sap scm) ensured specialists and experienced working experts with hands on ongoing numerous SAP SCM ventures information. We have planned our sap scm course substance and prospectus dependent on understudies necessity to accomplish everybody's profession objective. In our sap scm training program, you will learn request the board, Supply Network Planning Heuristic, SNP Run Using Capable, SNP Configuration, Master Data and Transaction Data in SNP, Demand Planning, Interactive Planning, Safety Stock Planning, sap scm continuous venture and sap store network the board (sap scm) placement training.


ReplyDeleteFor More Info:- SAP SCM Course in Gurgaon

Thanks for sharing the information.


ReplyDeleteAugmented reality application development

Best augmented reality companies

Augmented reality app development company

Augmented reality developers

Augmented reality development companies

What a resourceful piece of information thanks you for sharing. When it becomes hard to manage your resources, you can check this. I am very happy to read your post. I'm also sharing my nice stuff to you guys please go through it and take a review.



ReplyDeleteoutsource digital marketing services

outsource website development

top digital marketing agencies in india

virtual assistant websites

web design and development india

web design and development india

You can get more offers through Lufthansa Airlines Phone Number , which mainly looks for any details that you usually really like your airline. Want to experience with Lufthansa Airlines Phone Number is your personal travel agent who books your plan.

ReplyDeleteGet easy and quick reservations for

ReplyDeleteAmerican Airlines Cancellation. So there is no need to wait in lines now when all your booking can be done on the call of our travel expert.If you wish to cancel your ticket that was purchased from American Airlines, you can contact

ReplyDeleteAmerican Airlines Cancellationthrough an online refund request by communicating customer support.You just have to call

ReplyDeleteSouthwest Airlines Customer Servicefor flight booking our services. Get ready to have a joyful and comfortable journey with us.Plan a journey and contact our travel specialists on

ReplyDeleteUnited Airlines Phone Number. helpline. With us, nothing is unattainable for our esteemed customers. United Phone Number is our toll-free service which takes care of all your booking needs when you want to move across to your destination for business or leisure purposes.If you are looking for reliable and affordable services then visit Spirit Airlines Contact Number . Here you can get best deals and offers on your flight tickets. So, go now book your flight tickets at low-cost. Now you can fulfil your vacation dreams in your budget.

ReplyDeleteIf you are paining your trip by flights and looking to Travel several beautiful places then just visit at


ReplyDeleteAirlines Low Fare Calendarwhere you don’t need to search over dates now and you will find the lowest airfare options for both domestic as well as international flights.. Get comfortable services to reach relaxed to your destination.We provide a detailed update regarding cricket matches on a daily basis. We offer you the best India fantasy information and cricket news and player. So that you Get Best today match prediction and increase your chances of a win.

ReplyDeletewin the 2023 ODI World Cup

Catering Piknik

ReplyDeleteistanbul catering

kokteyl catering

Mevlüt Yemekleri fiyatları

Mevlüt yemek Menüleri

kokteyl catering fiyatları

istanbul kokteyl catering

catering kokteyl menüleri

fuar yemek organizasyon

fuar yemek organizasyo firmaları

fuar için yemek firmaları

düğün yemek organizasyonu

düğün yemek organizasyonu yapan firmalar

istanbul kokteyl catering

istanbul kokteyl catering firmaları

Kokteyl catering fiyatları

kokteyl prolounge menu

kokteyl prolounge düğün

Paketli Mevlüt yemekleri

Düğün ve Mevlüt Yemekleri

Kokteyl Prolounge Menu

Mevlüt yemeği nedir

Pideli Mevlüt menüsü

Cenaze Yemek Organizasyonu

300 kişilik yemek Fiyatları

istanbul fuar yemek organizasyonn

istanbul fuar yemek organizasyo firmaları

istanbul fuar için yemek firmaları

istanbul düğün yemek organizasyonu

istanbul düğün yemek organizasyonu yapan firmalar

istanbul kokteyl prolounge menu

istanbul kokteyl prolounge düğün

istanbul Paketli Mevlüt yemekleri

istanbul Düğün ve Mevlüt Yemekleri

istanbul Kokteyl Prolounge Menu

istanbul Mevlüt yemeği nedir

istanbul Pideli Mevlüt menüsü

We offer more opportunities for great feedback in travel time. So, what are you waiting for now? Dial

ReplyDeleteSouthwest Airlines Phone Numberor grab the amazing plan.Get more mileage, the above facilities combine with

ReplyDeleteSouthwest Customer Servicespecialists. Save your time or money with a toll-free number.Daftar poker online terbaru, hanya di situs pokerwan bossku. Dengan waktu hanya dengan 1 menit saja, anda sudah bisa bermain di agen poker online terpercaya di Indonesia.


ReplyDeletehttp://diamondwajik.com/

Pokerwan sudah dipercaya oleh lebih dari 3000 player poker online bossku, jadi anda tidak usah khawatir dalam hal keuntungan dan pelayanan. Karena agen poker resmi ini senantiasa membayarkan semua keuntungan anda tanpa ada potongan sama sekali. Daftarkan diri anda untuk bermain di situs kami bossku, hanya dengan 10.000 rupiah saja.

Hey, I believe that this is an individual choice of everyone, you should try and understand whether it is yours or not. But I can recommend a site with a review, where there are ratings of different sites. This is paito warna sydney. I hope this makes it easier for you to choose and search, good luck!

ReplyDeletepaito togel

paito warna hongkong

paito warna singapore

After going over a handful of the blog articles on your website, I truly appreciate your technique of writing a blog. I bookmarked it to my bookmark webpage list and will be checking back in the near future. Please check out my website as well and let me know what you think. best-cheap-24-inch-monitors



ReplyDeletePowerful Love spells Guide :- Love spells and not forgetting the amazing and authentic || Love spells that Work Immediately On Facebook


ReplyDelete|| Nothing But the Best Love spells That Work Fast and spells of || Immediate Love Spells

After looking over a few of the articles on your blog, I seriously like your technique of blogging. I saved it to my bookmark site list and will be checking back in the near future. Please check out my web site too and let me know what you think.


ReplyDeletebest-cheap-kitchen-robot

click on one of the sites below to get a variety of the best tips and tricks in life.



ReplyDeletelive draw hk tercepat

click on one of the sites below to get a variety of the best tips and tricks in life.



ReplyDeletelive draw sd

gamelantogel

ReplyDeleteI am very happy after reading this fantastic Article, I appreciate your work.


ReplyDeleteHow to Install Epson Printer DriversWow, Great information shared. I appreciate the persistence you put into your website and detailed information you provided.


ReplyDeleteoutsource website development

freelance website developer

vitual assistant

click on one of the sites below to get a variety of the best tips and tricks in life.



ReplyDeletehasil data sydney

hasil data singapore

hasil data hongkong

hasil data cambodia

hasil data bullseye

hasil data china

hasil data pcso

paito warna sydney

paito warna singapore

paito warna hongkong

I’m amazed. I must say. Rarely do I encounter a blog that’s equally educative and entertaining. and without a doubt. you have hit the nail on the head. The issue is something that not enough folks are speaking intelligently about. I am very happy I came across this in my search for something relating to this.

ReplyDelete5 BANDAR TOGEL TERPERCAYA

Wow! After all I got a webpage from where I know how to truly get useful data concerning my study and knowledge.

ReplyDeleteAGEN TOGEL TERPERCAYA

LIVE HONGKONG

ReplyDeleteKunjungi segera situs Prediksi HK Mbah Sukro yang menyediakan prediksi terjitu angka togel di indonesia

ReplyDeleteThanks for sharing this! I’m delighted with your blog, where such important moments are captured. All the best!

ReplyDeleteShare Market Tips | Stock Market Tips

data hongkong merupakan rangkuman salah satu data pengeluaran togel hongkong atau juga sering disebut live draw hk yang di sajikan atau kami tampilkan dalam bentuk tabel, Keluaran Hongkong atau Result HK yang kami tampilkan di situs ini merupakan hasil keluaran hk yang kami berikan diambil langsung dari Hongkongpools.com sebagai situs resmi dari Togel Hongkong.





ReplyDeleteDengan berbagai aspek yang sudah kami pertimbangkan, kami membuat situs atau link ini guna membantu para pemain Togel Hongkong dalam mengetahui Data Pengeluaran HK hari ini secara tepat dan cepat, disini kami akan memberikan Keluaran HK Terbaru untuk sobat pecinta Toto Hongkong setiap harinya.

Groww is one of India’s fastest growing online investment platforms. It offers paperless investing options by letting you buy and sell stocks and mutual funds online. Through this


ReplyDeleteGroww App Review, we will talk about the Groww brokerage charges and commissions for stocks.Plan for Jio tower installation 2022 - Apply Now For Jio Tower | Apply Reliance Jio Tower Installation Online | Jio tower installation monthly rent | Jio Tower Complaint Helpline Number - Jio Tower Helpline Number | Reliance Jio Tower Installation Process Steps To Install | Reliance Jio Tower Installation Apply Online and Contact Number 2022 | Jio tower installation customer care number and contact number | Jio tower installation apply online 2021 & jio advance amount

ReplyDeleteThe process to set up PIXMA ts3122 starts from ij.start.canon/ts3122 and download the latest full driver & software package for PIXMA TS3122. You can learn to set up this multifunction printer model.

ReplyDelete



ReplyDeleteThis is very good blog post, I like the way you pointed all stuff, must follow below useful links

POS Systems

point of sale systems

pos solution dubai

restaurant pos

retail software dubai

saloon software

inventory management software

warehouse management software

barcode printer dubai

barcode solutions dubai

thanks bro


ReplyDeletebandar togel terpercaya 2022

Stay In Touch With Clii Stock Price? Every Move With Our Live, Real Time Stock Market Overview. Here You Will Always Be One Of The First To Know When Clii Stock Price Is Increasing Or Decreasing. Our Live Information Is Delivered Right To Your Browser, Giving You All The Data You Need To Make An Informed Trading Decision. With This Information At Your Fingertips You Will Be Able To Make Quick And Educated Decisions While Keeping Track Of All The Latest Clii Stock Price Changes!


ReplyDeleteThanks for elaborating on this sensitive topic. Even today most online public platforms do not publish or discuss this topic. I also want you to give a little comment on my perspective to follow the organic diet for better health and environmental safety. I am so obsessed with it that you will find everything in my kitchen and refrigerator is organic even I use whole green moong dal in my diet for better health.

ReplyDeleteYour writing is so impressive and informative that now I am able to understand the importance of blogging. But here still I am confused about the topic on which I should do blogging. I also want to share some information about organic food that I am using for a long time. I would also suggest others try organic moong dal whole from a certified organic food producer. And what do you think to start an informative blog on organic food consumption?

ReplyDeleteBaca Dan Cermati





ReplyDeleteforum syair hk

live sdy

prediksi syair hk

forum syair sdy

website sangat cocok untuk dibaca dan menyenangkan





ReplyDeletelive draw cambodia

data sydney terbaru

result cambodia tercepat

live macau hari ini

live draw china


ReplyDeletelive draw sgp

Result Sdy

ReplyDeletelive draw sdy




ReplyDeletelive draw hk

prediksi hk

prediksi sdy

Live Draw Cambodia






ReplyDeleteSyair Macau

Syair Hk

Syair Cambodia

Syair Taiwan

Angka Keramat

Dr. Vincent A stands out as one of the


ReplyDeleteBest cataract surgeon in austin texas. With over two decades of experience, Dr. Vincent A combines expertise with cutting-edge technology to deliver exceptional results to his patients. He is known for his meticulous approach, personalized care, and commitment to staying abreast of the latest advancements in cataract surgery techniques.Patients consistently praise his professionalism, compassion, and ability to achieve remarkable vision improvements. Dr. Vincent A reputation as the best cataract surgeon in Austin is well-deserved, making him the top choice for those seeking high-quality eye care and optimal surgical outcomes.

GyFTR is a top digital gifting platform offering instant e-gift vouchers for brands across categories like fashion, travel, and electronics. Partnered with

ReplyDeleteHDFC SmartBuy Flipkart, it provides exclusive deals on Flipkart and more. Enjoy seamless redemption, instant delivery, and secure transactions. Explore more at GyFTR.Looking for reliable


ReplyDeletewindow installation near me? Our expert team provides professional window installation services tailored to your home or business. Whether you need energy-efficient windows, stylish replacements, or custom designs, we ensure top-quality craftsmanship and durability.Our licensed and insured professionals handle everything from measurement to installation with precision and care. Enjoy enhanced curb appeal, better insulation, and long-term savings with our high-quality windows. Contact us today for a free consultation and estimate—your perfect windows are just a call away!