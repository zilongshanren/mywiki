---
title: The Metal by Example Book is Now Available!
url: https://metalbyexample.com/book-now-available/
published: '2015-11-01'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

*Metal by Example* is now a book! You can [buy it here](https://gum.co/metalbyexample) as a DRM-free PDF.

Since I started this site, I’ve been wanting to turn Metal by Example into a book. Although the blog format is good for quickly publishing techniques one at a time, a book is necessarily a more cohesive experience. For the past month or so, all of my energy has been directed at revising, rewriting, expanding, and editing my Metal content to turn it into a book.

Of course, this project would never have been possible without you, the reader. Thank you for your support over the last year.

If you want to support the work I’ve done here and benefit from the more streamlined, consistent experience of the book, please consider buying it. Thanks again!—Warren

**Update** (September 13, 2016): Thanks to everyone for the support over the past year! The book is now available on a pay-what-you-want basis. A lot has changed in the world of Metal since I started writing two years ago, and it doesn’t make sense to keep charging full-price for this material, some of which has grown out-of-date. I hope even more people can find it useful, even as it ages, now that price isn’t a factor.

Nathan YoungmanCongrats Warren.

For sample code, the book just links to your blog right now. It took me a minute to discover the link to the repo under http://metalbyexample.com/the-book/

Jeroen RansijnHi Warren,

Great to see your book is now available! Will definitely check it out. Wish you the best of luck with the sales 🙂

Warren MooreThanks, J! Sales have been great so far.

JaredWarren you should sell this on Amazon so that you make more money. The reason I’d like you to make more money is so that you create for us even more content! The way you explain things and how you explain them is beyond phenomenal!

Nathan YoungmanSelling a Kindle book on Amazon or ePub on Apple iBooks could give you a (much) smaller piece of a (potentially) bigger pie. In both cases with DRM.

If you want to self-publish a print version, check out Ingram Spark. They do print-on-demand and distribute through Amazon and other popular (online) retailers.

http://gameprogrammingpatterns.com/ is a good example of self-publishing through pretty much every channel there is.

Francesco PavoniI am new to study Metal. I am interested in buying the book, later there will be a version for Swift?

Can with Metal Shaders, through its building of paths vectors, recognize objects in the image in real-time?

I read articles on OpenCV and OpenGL, whereas I start from zero, I would like to learn with Metal seems more powerful in its use of the GPU. I apologize if I said nonsense, it would be driven in the most convenient route.

Thank you

Warren MooreI’m not planning to release a Swift edition of the book. The concepts transfer pretty readily from Obj-C to Swift, though. As far as computer vision is concerned, any task you can do with GLSL or OpenCL kernels can be done with Metal, and there are a lot of common concepts among them. If you’re developing for Apple’s platform, Metal is, in my opinion, the best choice.

Basel FaragWarren may not be working on a Swift version but…. *eh ehm* I am!

Warren MooreEager to see what you come up with, Basel!

JaapHave you come up with anything? I’ve tried some myself but there are a few swift specific differences in the setup I can’t get to work. Would love to work together on porting the whole book to swift or something!

Harshil ChokshiThank you. I bought your book and it was great. Helped a lot. I would like to learn Open GL ES 2.0 for iOS now. Can you recommend a good book for that?

BaselThis one’s a classic: http://amzn.to/1QKLfhR

What are you working on specifically, Harshil? (If you don’t mind me asking)

RamyHello. I purchased the book but I can’t find the source code. Can I get the link?

Warren MooreSure, the source is available here!

Eduardo AndresHi Warren ..

Can u help me.

I want build the chapter 3 example as a Mac App but i have 2 issues.

1. My nextDrawable always is setting as Null

2. Always the appear “failed assertion `No textures set.'”

can u help me?

https://github.com/edthereaper/MTLEngine

LukeBasel Farag said “Warren may not be working on a Swift version but…. *eh ehm* I am!”

So anything is ready now? I’m really interested.

reader from chinaPlease provide more payment method, I can’t use PayPal(in China) and have no Visa card.I already got a copy of this book with the link you provide and purchased it in free price! It’s a valuable book,I hope I can just buy a coffee for you.

AlexHello. What does the array MBEIndex indices[] in Drawing 3D example really does??? Can you send link on any tutorial about it?

KaanWhat part of the book is out-of-date as of 2022? A general answer would be okay, thanks! Just bought the book btw looking forward to reading it 🙂

Warren MooreI think the chief thing I would do differently today is use MTKView to manage interfacing with the window manager, rather than CAMetalLayer. MTKView didn’t exist at the time of writing, but it greatly simplifies things like setting up a render loop, managing render attachment resources, configuring the drawable size, and so on. I’d also like to place greater emphasis on MSAA, which I’ve never written about here; vertex descriptors, which I have, and resource synchronization.

As the years have gone on, I’ve tried to keep the sample code running on newer iOS versions, but this means that the sample code you download today is somewhat out-of-sync with the book.

I’m planning to alleviate all of these issues with a new book on Metal in Swift this year.

Jared JonesMy wallet is ready!

Nathan YoungmanThat’s great news. Looking forward to it!

KaanThanks for the prompt answer Warren. I will keep these in my as I go through the book. I love the fact that the book is in Objective-C because that’s what I’m planing to use mostly.

Looking forward to your new book!