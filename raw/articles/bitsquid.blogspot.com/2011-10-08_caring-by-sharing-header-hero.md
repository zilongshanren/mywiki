---
title: 'Caring by Sharing: Header Hero'
url: https://bitsquid.blogspot.com/2011/10/caring-by-sharing-header-hero.html
author: Niklas
published: '2011-10-08'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Compile times get worse over time, that is the second law of C++ programming dynamics. There are many small day-to-day changes that each exacerbate the problem slightly: The project grows. New header files get included. Clever templates get written. And so on. There are comparatively few forces that work in the other direction. Once an

*#include*has been added, it stays.

The only exception is when some hero steps up, says

*Enough!*and starts to crunch down on those header files. It is thankless menial work that offers few rewards, save the knowledge that you are contributing to the public good.

Today, I want to give something back to these unsung heroes, so I’ve made a small tool to make their drudgery a bit less... drudgery-ish? It is called

*Header Hero*:

To run

*Header Hero*you specify the directories where your

*.cpp*files can be found as well as the directories to search for included headers. The program scans your

*.h*and

*.cpp*files to find all the include links. It presents the result in a summarized report that shows you what the worst headers are. You can think of it as a header file profiler.

You don’t need to specify all your include directories, but only the ones you have specified will be scanned.

I’ve focused on making the tool

*fast*by caching as much information as possible and using a simple parser that just looks for

*#include*patterns rather than running the real C preprocessor. The downside is that if you are using any fancy preprocessor tricks, they will most likely be missed. On the other hand, the tool can scan a huge project in seconds. And after the initial scan, new scans can be done in a fraction of that time.

The program produces a report that looks something like this:

At the top are some statistics, such as the total number of files and lines in the project.

*Total Parsed*counts how many lines that would actually be parsed in a full recompile of the project. So, a header that is included by several

*.cpp*files adds to that number every time. The

*Blowup Factor*are the last two items divided. It specifies how many times, on average, each line gets parsed. A value of 35 means that on average, each line in our project is parsed 35 times. That seems quite a lot.

Below the summary are a list of the header files sorted by how many lines they contributed to the

*Total Parsed*number. In other words, the size of that file multiplied by the number of times it was included.

Looking at the sample report above, it seems pretty reasonable. At the top we find big templated collection classes (

*map, set, string, vector*) that have big header files and are used in a lot of places. Math (

*matrix4x4, vector3*) and utility (

*critical_section, file_system*) files also end up high on the list.

But when you dig into it, there are also things that seem a bit fishy.

*Set<T>*is not a very popular collection class. Sets are used less than maps, and

*HashSet*is usually preferable to

*Set*. Why does it end up so high on the list? What is

*shader.h*doing there? That seems too specialized to end up so high. And

*file_system.h*? There shouldn’t be that much code that directly accesses the file system, only the resource loader needs to do that.

To answer those questions, you can click on any file in the report to get a detailed view of its relations:

In the middle we find the file we are looking at. To the left are the files that directly include it. The number after each file name specifies how many files that directly or indirectly include

*that*file. To the right are the files included by the file. The numbers are all the files directly or indirectly included by

*those*files. You can double click on any file name in the view to refocus on it.

Here we clearly see that the main culprit is

*data_compiler.h*. It includes

*set.h*and is in turn included by 316 other files. To fix the compile times we can make

*data_compiler.h*not include

*set.h*or we can try to reduce the number of files that include

*data_compiler.h*(that number also seems high). If we also fix

*scene_graph.h*we can really make a difference.

Breaking dependencies is a whole topic in itself, especially when it comes to templates and inlined code. Here are some quick tips though:

1) Predeclare the structs and classes that you use instead of including the header file. Don’t forget that you can predeclare templates and typedefs as well as regular classes:

```
class MyClass;
typedef int Id;
template <class T> class Vector;
```

2) Predeclared types can only be used as pointers and references. You can’t have a member variable of a type whose actual size is unknown. So you may have to change your member variables to pointers in order to get rid of the header dependency. You can also use the

[pimpl idiom](http://en.wikipedia.org/wiki/Opaque_pointer), if you can live with the extra indirection and lack of inlining.

3) Switching from in-place variables to pointers can lead to bad memory access patterns. One way of fixing that is to placement new the object directly into a raw memory buffer.

```
// a.h
class B;
class A {
A();
B *_b;
static const int SIZE_OF_B = 20;
char _b_storage[SIZE_OF_B];
};
// a.cpp
#include ”b.h”
A::A()
{
XASSERT(sizeof(B) == SIZE_OF_B);
_b = new (_b_storage) B();
}
```

With this technique, you get the data for

*B*stored inside

*A*, without having to include the

*b.h*header in

*a.h*. But the code isn’t exactly easy to read, so you should only use this in desperate situations.

4) For files with small type definitions, but lots of inlined methods (e.g.,

*matrix4x4.h*), a good strategy is to split the file, so you have just the type in one file and all the methods in the other. Header files can then include just the type definition, while

*.cpp*files pull in the whole shebang.

Using these techniques you can get rid of the header dependencies one by one, until you are back at reasonable compile times. Since a rescan takes just a fraction of a second it is easy to see how your changes affect the compile time. Just make sure you have your integration test running, it is easy to break build configurations when you are fiddling around with the headers.

Here is the result of about a day and a half of header optimization in our code base:

From 6 million to 4.3 million lines, that’s not too shabby. We can now do a complete rebuild in 37 seconds on a reasonably modern machine. With this tool we can hopefully keep that number.

You can download the C# source code here. Feel free to do whatever you like with it:

Interesting tool, thanks.

ReplyDeleteBut FYI after a very simple test I've just made where I commented few #include lines to sse the changes, it seems that those lines are still taken into account, at least for the right column of the detailed view (while it also seems that stats like blowup factor are correctly updated).

Yes, Header Hero's simple parser doesn't understand comments, so delete the lines completely instead of commenting them out.


ReplyDeleteCommenting out code is

bad form anyway ;)

Great stuff. A few things it doesn't handle the way I'd expect:




ReplyDeleteFirstly, if there's a header and one .cpp file that includes it, that header seems to be counted twice.

Generally, a header file will have include guards around it so will only be parsed once per translation unit. So you should really be only counting, for each header file, how many different .cpp files it is transitively included by.

Of course, neither are showstoppers. I'm looking forward to trying this out!

Yes, I assume include guards and only count the files once per translation units. If you see a file doubly counted, there must be something else going on. I'll investigate.

ReplyDeleteI tested it. Made a small project with just one header and one .cpp file and the count was correct. If you have something where it counts badly, perhaps you can zip it up and send it to me.

ReplyDeletesmall suggestion. Dont expect "#include". A lot of boost and others use 'pretty printing' in includes. So something like


ReplyDeletestring line = inputLine.Trim();

if (line.StartsWith("#") && line.Contains("include"))

will show blowup not 35 but 67 :)

And to be useful the thing probably should read build system instructions for sources/includes - when company starts to separate 'common' libs the src/include filesystem locations start to become quite hairy.

Ah, right! I'll add some better #include-parsing.


ReplyDeleteI don't think I'll add project parsing though. That's too messy, with different build systems, configurations, etc.

Thx, it's a simple great tool. I am also a game dev and it can be really boring to wait for a build.





ReplyDeleteI did a clean up few month ago on our engin by using PIMPL idiom and cleaning includes at hand, but without your tools it's much more easier to find some little miss.

Do you know the D language? That make me dream of instantaneous build.

What is your machine because I build this (i7 2600 under Visual Studio 2010) in 54seconds :

Files: 419

Total Lines: 79 102

Total Parsed: 1 732 757

Blowup Factor: 21,91

Those numbers are without standard headers.

Yes, it's crazy that we even have to deal with this stuff. We are still paying the price for the fact that 60's computers couldn't fit both a compiler and a linker in main memory. In modern languages such as D and Go, this isn't even a problem.


ReplyDeleteThe numbers are from an i7 with lots of memory, compiler set to use all cores. But I don't think you can compare across projects... there are many other things that could affect compile time then the raw line count, such as amount of templates, etc.

I just can suppose our engine is much more simple as yours. We only realize some adventure games ports. We are just adding some real 3D features for a new kind of game, but there is no dynamics, all scenes are precalculated.


ReplyDeleteVS 2010 Compiler use all core of our CPU, mine have 4 and 8Go of RAM, but I think your right it's hard to compare without a real analyse of code and compiler work around.

I've wanted to write this tool for a while now, but haven't had the time. Here's what I would do different.




ReplyDeleteFlame graphs!!!

http://www.brendangregg.com/flamegraphs.html

I think a flame graph visualization would make it easier to find the intermediate include that is dragging in tons of unwanted stuff. You could get good visualization results even if your tool just emitted an .svg that could then be opened in a browser.

I liked your post and I am waiting for your new update.if you are an obsessive gamer also check this out

ReplyDeleteJohnny Silverhand Vest

African Mango Seed Extract Market is often combined with other ingredients such as green tea and marketed as a fat-burning supplement. Because of the weight-loss properties associated with the seed extract, along with the rising fears about health problems such as obesity, the market for African mango seed extract is expected to be further propelled forward. The industry is also being driven by the rising demand for foods made from natural ingredients.

ReplyDeleteChlorine is a greenish-yellow gas. It has a pungent, suffocating odour. It is slightly soluble in water. It liquefies at -35C.


ReplyDeleteChlorine Production

Are you looking for stylish, trendy, comfortable, easy to carry, best quality jackets and coats? But find it difficult to get one with all your demands? Not anymore! Buy premium quality, super stylish attires at hiltonsky.

ReplyDeleteWe produce high quality trendy products, available at our website christmas apparel at the best possible prices. Buy your favorite jackets and coats to look stylish and classy like your favorite celebrities.

ReplyDeleteIndulge in the quality and style you have never experienced before! pink ladies jacket brings you the most trendy and stylish product line this season. Visit pink ladies jacket and grab your favorite superstar attires!

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteGreat Article. You have beautifully articulated it. Readers revisit only if they found something useful. Oujeer - Men Vest

ReplyDeleteThe PhD students need to do low maintenance occupations to monetarily uphold their families and accordingly have an extremely brief time frame to provide for their examinations and dissertation writing service is such an extensive undertaking that no understudy can do it in one go.

ReplyDeletePretty good post. I just stumbled upon your blog and wanted to say that I have really enjoyed reading your blog posts. Any way I'll be subscribing to your feed and I hope you post again soon. Grease Trap Cleaning Houston TX Big thanks for the useful info.


ReplyDeleteYour Pet Planet - Treat animals with care, it's only fair


ReplyDeleteGreat Article! I appreciate your effort. Well done and thank you.

Best Regards:

Your Pet Planet

Your Pet Planet



ReplyDeleteBrown Cat Breed

Blogs

It's great to have you here. I really like the colours and theme.

ReplyDeleteIs this your website? I'd like to start working on my project as soon as possible.

If you don't mind, I was curious to know where you got this or what theme you're using.

Thank you..

Final Cut Pro X Ios Mac Torrents Full Download

Really Good Work Done By You...However, stopping by with great quality writing, it's hard to see any good blog today.

ReplyDeleteCRACKPEDIA

Nsauditor Network Security Auditor Crack

Crack Softwares Free Download

InPage Download is one of the high-quality software typing software for Urdu that Urdu wants to bring huge numbers of people on the market around the world.



ReplyDeleteView More:

cc2018 クラック

ms project free download with crack

element 3d v2.2 kickass

videoscribe crack

xforce keygen rar download 64 bit

acid pro 7 download + crack

Autocad 2013 Activation Code Generator

Delite Cleaning Services is Australia’s fastest growing Commercial cleaning Company that provides steady work for thousands of people throughout Australia. The work is what you do in your own home every day. The only difference is you get paid for it!

ReplyDeleteI adore your websites way of raising the awareness on your readers. ลิงค์รับทรัพย์

ReplyDeleteThank you very much. Thank you for sharing this wonderful article with us.


ReplyDeletehttps://softhound.net/idm-crack-download/

This is a great post. Thank you.

ReplyDeletehttps://windowsactivators.org/internet-download-manager-crack/

what a best type of article which is really great, thanks for sharing the most beautiful post of the blog with useful information which is really amazing. Scott Callum

ReplyDeleteWhat a fantastic article; thank you for giving the most beautiful blog post with important information; it's truly awesome.top gun jacket

ReplyDeleteWow! Great blog, I really liked your post. Keep Posting. We provide the technical support for the email related issues like how to Recover Spectrum Email Password

ReplyDeleteWe offer a wide variety of used cars with hundreds of choices, while holding zero interest rates on our new and used car loans. Car Dealers Mississauga

ReplyDeleteIt's wonderful to see that some people can still craft an outstanding post! Not only is your blog helpful, but it's also really imaginative. I looked over and thought about what you said. Seeing your article makes me happy. Pelle Pelle Jacket

ReplyDeleteTruly awesome! for the best type of site sharing beautiful post with best information that I had learned properly. Atty Pete

ReplyDeletewhat a best type of article that I really appreciated, sharing best info update that looks very impressive. click here to view

ReplyDeleteIt's wonderful to see that some people can still write excellent posts! Your blog is not only informative, but also very creative. I looked over and considered what you said. I'm delighted to see your article.Tom Cruise Outfit

ReplyDeleteJSM offers Premium and affordable Luxury Limo Services in Toronto. We offer services for weddings, proms, corporate, and special events. JSM Black Limousine easily handles your event transportation demands and less celebratory logistics, such as any last-minute errands or special-needs transportation for your wedding guests.

ReplyDeleteLimo service hamilton

limo services toronto

SEO Content Writing Very welled explained. Great Pro Tips! Thank you very much for taking the time to make this great video. I found it extremely helpful.


ReplyDeleteI feel extremely cheerful to have seen your post. I found the most beautiful and fascinating one. The Batman Bomber Jacket

ReplyDeleteGood Work, keep it up. Get the latest Garmin Map Updates and updated Garmin Express

ReplyDelete"Caring by Sharing: Header Hero" reflects the essence of community and support, akin to the stylish kaley cuoco flight attendant outfits. Just as her wardrobe showcases warmth and professionalism, sharing our talents and kindness can elevate others, creating a supportive environment where everyone feels valued and cared for.





ReplyDeleteMaxon CINEMA 4D Studio Crack is a strong 3D mock-up, the formation of graphics as well as compositing developer all through the movement image, the standard, with betting division.

ReplyDeleteMaxon CINEMA 4D Studio Crack

A beach wedding in Maui sounds like an absolute dream! The combination of stunning ocean views, golden sunsets, plecak 40x25x20

ReplyDeletezaino donna mandarina duckzaino donna mandarina duck

ReplyDeletesombrero blanco sombrero blanco

ReplyDeletebransoletka meskabransoletka meska

ReplyDeletecappellocappello

ReplyDeleteabrigo beige mujerabrigo beige mujer

ReplyDeleteski truiski trui

ReplyDeletesciarpa uomo cashmeresciarpa uomo cashmere

ReplyDeletedlugi kardigandlugi kardigan

ReplyDeletecolgante rosa de los vientoscolgante rosa de los vientos

ReplyDeleteniebieski szalik damski A beach wedding in Maui sounds like an absolute dream! The combination of stunning ocean views, golden sunsets

ReplyDeletearmband damenThis is really an amazing article

ReplyDeleteohrringe silberThank You so much

ReplyDeleteI feel extremely cheerful to have seen your post. I found the most beautiful and fascinating onecardigan uomo

ReplyDelete

ReplyDeletewhat a best type of article that I really appreciated, sharing best info update that looks very impressiveschoenen heren

I feel extremely cheerful to have seen your post.heren bodywarmer

ReplyDeleteI feel extremely cheerful to have seen your post.josh v vest

ReplyDeleteI feel extremely cheerful to have seen your post.stivaletti estivi donna

ReplyDeleteI feel extremely cheerful to have seen your post.schiebermutze

ReplyDeleteI feel extremely cheerful to have seen your post.zapatillas para hombre

ReplyDeleteA beach wedding in Maui sounds like an absolute dream!hardshelljacke damen

ReplyDeleteI feel extremely cheerful to have seen your post.norweger pullover damen

ReplyDeleteIt's wonderful to see that some people can still write excellent posts!sandaly na obcasie

ReplyDeleteTruly awesome!teddy vest dames

ReplyDeleteThis is a great post.sac bash

ReplyDeleteDeep Freeze Standard Crack is free through ‘faronics business’. In agreement to their first name, it disembark to acquire frozen your plan. No matter what adjustment are happening.

ReplyDeleteDeep Freeze Standard Crack

I assume include guards and only count the files once per translation units.gilet femme coton

ReplyDeleteI tested it.armband herren

ReplyDeleteMade a small project with just one header and one .trajes hombre

ReplyDeleteit's crazy that we even have to deal with this stuff.casa barriguitas

ReplyDeleteI just can suppose our engine is much more simple as yours.converse chuck

ReplyDeleteExcellent post. I really enjoy reading and also appreciate your work. This concept is a good way to enhance knowledge. Keep sharing this kind of articles, Thank yousweat capuche carhartt

ReplyDeleteI liked your post and I am waiting for your new update excellent platform for sharing your knowledge with otherzadig en voltaire trui

ReplyDeleteI appreciate you sharing this article with us, I really enjoyed reading it.sciarpe

ReplyDeleteGreat Post! after so long I have spent time on any post, but you deserve itdlugi kardigan

ReplyDeleteI appreciate the effort you put into your blogcover iphone 11

ReplyDeleteI assume include guards and only count the files once per translation units.gefutterte gummistiefel

ReplyDeleteMade a small project with just one header and one .sweat capuche boss

ReplyDeleteit's crazy that we even have to deal with this stuff.bershka kurtka puchowa

ReplyDeleteI just can suppose our engine is much more simple as yours.halskette damen

ReplyDeleteYou have beautifully articulated it.skarpety kapcie antyposlizgowe

ReplyDeleteI've heard a lot about this festival before.cardigan alanui

ReplyDeleteThe data transferred over the platform secured with a binding connection protocol.oversized t shirt heren

ReplyDeleteI must say you have written very nice article.sciarpa cashmere uomo loro piana

ReplyDeleteIt is very useful and top articles and i love this article.cappello pescatore uomo

ReplyDeletethank you a lot for sharing this article with us.puma future

ReplyDeleteUn paesaggio incantato che ci lascia incantate!sac a dos cuir homme

ReplyDeleteI found so many interesting stuff in your blog especially its discussion.cowgirl hoed

ReplyDeleteI guess I am not the only one having all the enjoyment here!gorro bebe

ReplyDeleteNice guide thanks for sharing and talking about these homemade stars.gestreifter pullover damen

ReplyDeleteThe style needs of everyone with a variety of classy attires and innovative designs.ladies laptop backpack

ReplyDeleteThe spring season is warming up those open house events.mochilas 40 litros

ReplyDeletegood to launch the emulator with an app.dzinsy meskie

ReplyDeletewith pages that has no trace mark or hint.zapatillas nike

ReplyDeleteThanks so much for sharing your experience here.chrome hearts hat

ReplyDeleteI found the most beautiful and fascinating onerobe beige

ReplyDeleteTotally loved your article. Looking forward to see more more from you. Meanwhile feel free to surf through my website while i give your blog a read.trajes hombre el corte ingles

ReplyDeleteIt's wonderful to see that some people can still craft an outstanding post! Not only is your blog helpful, but it's also really imaginative. gormiti alfa

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happyspielzeug

ReplyDeleteI assume include guards and only count the files once per translation units.cappello basco

ReplyDeleteThis is wonderful!sam smith adidas

ReplyDeleteI was wanting to try this in my classroom next year as well.fobya swetry

ReplyDeleteThanks so much for sharing!flanell jacke

ReplyDeleteThis is the first time that I visit here.Bottine Femme

ReplyDeleteExcellent post. I really enjoy reading and also appreciate your work. This concept is a good way to enhance knowledge. Keep sharing this kind of articles, Thank youmaglie oversize

ReplyDeleteLearn Java programming easily with Java Assignment Help. Improve your coding skills and complete assignments accurately.

ReplyDeleteYour blog has always attracted me and this particular post left me speechless. It is one of the best pieces of writing I have seen. Good job…..magliette personalizzate

ReplyDeleteI’m grateful for the positive impact your blog has on me. Thank you for sharing your knowledge and motivation. gestreepte trui dames

ReplyDeleteI appreciate you sharing this article with us, I really enjoyed reading it.vestidos para boda de noche

ReplyDeleteI liked your post and I am waiting for your new update excellent platform for sharing your knowledge with otherborsa bianca

ReplyDeleteI feel extremely cheerful to have seen your post. ted baker tas

ReplyDeleteI found the most beautiful and fascinating oneon schuhe

ReplyDeleteI assume include guards and only count the files once per translation units.shein robe

ReplyDeleteI don't think I'll add project parsing though.hush puppies pantoffels heren

ReplyDeleteit's crazy that we even have to deal with this stuff.pantaloncini di pelle

ReplyDeleteI love your blog and your adorable freebies!mutze

ReplyDeleteI really enjoy reading and also appreciate your work.kollektionen nike

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happyzielone kolczyki

ReplyDeleteYour blog has always attracted me and this particular post left me speechless. It is one of the best pieces of writing I have seen. Good job…..ysl bags

ReplyDeleteTotally loved your article.giubbotto di jeans

ReplyDeleteI feel extremely cheerful to have seen your post. pme jas

ReplyDeleteI found the most beautiful and fascinating one ballkleider

ReplyDeleteTotally loved your article. Looking forward to see more more from you. Meanwhile feel free to surf through my website while i give your blog a read.giacca camicia

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happyair jordan 1

ReplyDeleteThanks for sharing this blog with us! kurtka damska wiosenna

ReplyDeleteThis is a really too good post. chapeaux panama

ReplyDeleteVery important and wonderful post here. pantaloni lana donna

ReplyDeleteThanks for sharing this blog with us! bottes camel femme

ReplyDeleteI can’t say, how grateful we are to read this. mochilas 40 litros

ReplyDeleteThank you so much buddy and Keep up the good work.zapatillasfila

ReplyDeleteMuch thanks for sharing this valuable data. zapatillas nike

ReplyDeleteWow, this is very interesting reading. I found a lot of things which I need. Great job on this content. I like itsweter damski kaszmir

ReplyDeleteI’m grateful for the positive impact your blog has on me. Thank you for sharing your knowledge and motivation. pantofole primi passi

ReplyDeleteThe things you share are relevant to my search needs. camisetas de vestir mujer

ReplyDeleteThanks for posting this info. estolas para bodas

ReplyDeleteI truly enjoy reading content like this and look forward to more. damska torebka

ReplyDeleteYou have worked nicely with your insights. hoed

ReplyDeleteThanks for sharing such a wonderful blog about fashion. giubbotto uomo

ReplyDeleteI've heard a lot about this festival before. ysl schuhe

ReplyDeleteThanks for sharing this blog with us! longue doudoune homme

ReplyDeleteThis is a really too good post. mango pantalones mujer

ReplyDeleteVery important and wonderful post here. yoga pants

ReplyDeleteI was doing a task and for that, I was searching for related data. lego ferrari

ReplyDeleteKeep sharing this kind of articles, Thank you.muts wit

ReplyDeleteI appreciate you sharing this article with us, I really enjoyed reading it.samsonite plecak na laptopa

ReplyDeleteYou have performed a great job. plecak damski

ReplyDeleteGreat article! mochilas mujer

ReplyDeleteI'm going to bookmark your site and keep checking for new information about once per week.maglioni uomo firmati scontati

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happymerkal calzados mujer

ReplyDeleteI appreciate the effort you put into your blogamen bracciali

ReplyDeleteI'm grateful for the knowledge you've shared in this postbracciale

ReplyDeleteSo keep it up!strickweste damen

ReplyDeleteThe things you share are relevant to my search needs. trui

ReplyDeleteThanks for posting this info. pull eden park

ReplyDeleteI truly appreciate your efforts and I will be waiting for your next possudaderas hombre

ReplyDeleteThe post was really nice to read. Thanks a lot for sharing that!on schuhe

ReplyDeleteI feel extremely cheerful to have seen your post. strickjacke damen

ReplyDeleteI found the most beautiful and fascinating onereserved sukienki

ReplyDeleteThank you for sharing and be sure to check out my page! spodnie eleganckie

ReplyDeleteI like it. mochila de pesca

ReplyDeleteI’m grateful for the positive impact your blog has on me. sandales hommes cuir

ReplyDeleteI liked your post and I am waiting for your new update excellent platform for sharing your knowledge with other.korte broek name it

ReplyDeleteI will certainly dig it and individually suggest my friends. torebka damska

ReplyDeleteGreat post and nice blog thanks for sharing valuable information Car service ct

ReplyDeleteThanks for wonderful information. Get Limo Service CT, Car Service CT

ReplyDeleteNice Blog This is what I exactly Looking for , Keep sharing more blog


ReplyDeleteBlack Car Service NJ

Keep sharing this kind of articles, Thank you.vans ultrarange

ReplyDelete

ReplyDeleteThe post was really nice to read. Thanks a lot for sharing that!zakelijke rugtas

Wow, this is very interesting reading. I found a lot of things which I need. Great job on this content. I like itvestidos ceremonia mujer

ReplyDeleteIt's a really useful post. nubikk sale

ReplyDeleteYou really do a great job. zwarte winterjas heren

ReplyDeleteI have really enjoyed reading your blog posts. cardigan donna

ReplyDeleteThank you for a wonderful overview of how to clean hardwood floors! t shirt personnalise

ReplyDeleteNice post! giacca bomber

ReplyDeleteExcellent post. hema vest

ReplyDeleteI really enjoy reading and also appreciate your work.short homme

ReplyDeleteGreat Post! casa de munecas

ReplyDeleteYou will find a lot of approaches after visiting your post.shein pullover

ReplyDeleteThanks for such post and please keep it up. superdry hoodie herren

ReplyDeleteI found the most beautiful and fascinating onebolsos y articulos de cuero ofertas outlet

ReplyDeleteTotally loved your article. Looking forward to see more more from you. Meanwhile feel free to surf through my website while i give your blog a read.unoaerre bracciali

ReplyDelete

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happybague fantaisie femme swarovski

I appreciate the effort you put into your blog t shirt donna

ReplyDeleteI found a lot of things which I need. chanclas rip curl hombre

ReplyDeleteGreat job on this content. I like it. lustige kopfbedeckung

ReplyDeleteExcellent post. tn blanche

ReplyDeleteI really enjoy reading and also appreciate your work.new balance 373 herren

ReplyDeleteIt's wonderful to see that some people can still craft an outstanding post! Not only is your blog helpful, but it's also really imaginativepantaloni calzedonia

ReplyDeleteI looked over and thought about what you said. Seeing your article makes me happyrains impermeabile

ReplyDeleteVery nice and unique information you share in this blog. jbl in ear kopfhorer

ReplyDeleteyou can also visit this website for more information about style.plumifero de marca

ReplyDeleteThis is a good way to increase our knowledge.vest heren

ReplyDeleteGreat blog. jas vest dames

ReplyDeleteI have found profitable information from this blog. sandali per uomo

ReplyDeleteThis is my first visit to your blog! mutzen damen

ReplyDeleteLooking forward to see more more from you. salomon zapatillas

ReplyDelete