---
title: Busted! Eight Reasons not to use ARC
url: http://www.learn-cocos2d.com/2012/06/mythbusting-8-reasons-arc/
author: Paul says
published: '2012-06-28'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

So, you’ve heard about Objective-C automatic reference counting (ARC). And you’ve read about it [here](http://www.learn-cocos2d.com/2011/11/everything-know-about-arc/) and [there](http://www.mikeash.com/pyblog/friday-qa-2011-09-30-automatic-reference-counting.html) and [every](http://longweekendmobile.com/2011/09/07/objc-automatic-reference-counting-in-xcode-explained/) [where](http://stackoverflow.com/questions/6385212/how-does-the-new-automatic-reference-counting-mechanism-work). But you’re not using it.

Guess what? You’re not alone. There are developers out there who refuse to use ARC, who delay using it, who believe they just can’t use it or expressly decided against using ARC for the time being. They all have their reasons.

**Most of them are wrong.**

Here’s a summary of reasons I’ve heard (repeatedly) in the past months from developers who aren’t using ARC, or have tried it but gave up using it. And I’ll tell you why these rationalizations are wrong, or at least over-inflated.


#### ARC takes away control

The control-freak angst. Completely irrational. Very common among code monkeys.

So you’re afraid that you lose control if you have to turn this:

|
1 2 3 4 5 6 |
-(void) someMethod { Object* o = [[Object alloc] init]; … [o release]; } |

… into this:

|
1 2 3 4 5 |
-(void) someMethod { Object* o = [[Object alloc] init]; … } |

Where you believe you are losing control, you’re actually gaining 100% reliability. That’s more than you could ever hope to achieve. Or have you never forgotten to release an object before? ARC doesn’t forget to release your objects, and it does so consistently at the same point in time that you would have to release it anyway.

This is just a basic example. There are really only very obscure, rare, on-the-fringes reasons where having manual control over retain/release *may* be helpful. But I guarantee that yours is not one of them, and never do you actually require full reference counting control to do anything. Not even to optimize performance - ARC code is typically faster anyway thanks to internal optimizations.

Take, for example, the autoreleasing many objects loop which you can tweak and control to not trash the autorelease pool regardless of whether you use ARC or not:

|
1 2 3 4 5 6 7 8 |
-(void) someMethod { for (int i = 0; i < 1234567; i++) { Object* o = [Object objectWithSomeInt:i]; … } } |

If you understand reference counting and autorelease, you know that this is going to grow the autorelease pool to over a million objects. Because according to naming conventions, objectWith… methods return an autorelease object. These objects will be released eventually, but until then they all sit in memory.

This is a situation where you would normally either enclose the loop with an NSAutoreleasePool or switch to using alloc/init followed by release, to ensure that there’s only one object in memory during each loop iteration. But …

The same can be done with ARC, only enclosing a loop in an autorelease pool is now done by enclosing it in @autoreleasepool { } and you can still use the init/alloc method instead of the autoreleasing objectWith… method - you just omit the release because that’s inserted automatically by ARC.

You may think you need the control, but you really don’t. I have yet to see an example where manual reference counting code is cleaner, faster, or otherwise better than ARC code. If you only want to feel like you’re in control, you may be subject to perform [micromanaging](https://en.wikipedia.org/wiki/Micromanagement).

Please, let go. There’s **real** work to be done.

#### ARC hasn’t proven to be reliable yet

You have only proven that [you don’t understand what ARC is](http://www.abbreviations.com/ARC).

Put simply: ARC removes the burden laid on you to perfectly manage the memory of your objects and puts it in the compiler’s hands, which knows more about object lifetime than you do. There’s nothing inherently unreliable about ARC whatsoever. In fact it produces more reliable (and also faster) memory management code than you ever could.

ARC is not a new framework, it’s not a rewrite, it doesn’t break backwards compatibility, ARC and non-ARC code can be mixed, ARC doesn’t have irrational behavior or any serious defects, it’s been available for almost a year and probably thousands of apps have already been built and shipped with ARC enabled.

ARC is fully supported by Apple, and they encourage you to use it. Consider it having the same impact on your project as upgrading Xcode. You just do it when it’s available. (*)

(*) At least that’s what I’m doing. I’m frequently aghast at how many developers don’t upgrade (or install side-by-side) the tool that’s most important for their work (D’oh!). Then again, so many dive right into using beta software without even considering the flipside; like not being able to submit their apps (D’oh!), not being allowed to ask questions about it in public should you run into problems (D’oh!), not getting support from library developers either (D’oh!) and not being able to downgrade the device if the beta iOS causes important apps to crash (D’oh!).



Hey, did you really watch the whole thing?

#### ARC isn’t worth learning so many new things

The stick-with-tried-and-true method. Blind-folds on. Sigh.

This one kind of makes me angry. And sad. Because as programmers, we sort of love technology, don’t we? Aren’t we open-minded and eager to learn new things? Isn’t solving technical problems part of what we like about programming?

It turns out that apparently some of us don’t. They can become very defensive when it comes to using new technologies such as ARC. Without actually using it no less, because ARC really doesn’t introduce many new things - it takes away a lot more superfluous old things than it does add new ones. Like bridge casting, which you may not even need. Or the handful of new keywords like strong (retain), weak (like assign) and __unsafe_unretained (like it says: unretained and unsafe, just as it were before but expressly stated in the declaration of the variable).

Here’s a reminder: learning new things is fun. It’s liberating. It gives you power. It frees you from clutches. Especially if it’s such a promising new technology that erradicates the need to write perfect memory management code.

Of course, while you’re learning you may feel intimidated at first, you may be less productive for a time, you may become frustrated because some things just don’t work the way they used to anymore. You may even lose some self-worth because there’s things you just can’t figure out. But this trough of adaptation gives way quickly to new lands where the grass actually **is** greener.

Come on over here, it’s fun! And since so many are here already, there’s plenty of people to help you up if you do run into a problem. [Just go ahead and ask.](http://stackoverflow.com/questions/tagged/automatic-ref-counting)

#### ARC is not supported by (insert library name here)

Maybe just a cheap excuse, repeating what others have said, or simply bridge-casting-confusion. But it can also be true so I let this one slide under some circumstances.

From my experience, most source code or prebuilt-binary libraries are compatible with ARC. Some source code libraries (like cocos2d) require some extra effort to build them as a static library instead of just plucking the code into your project. That way, the source code library can be built with ARC disabled and linked to your ARC enabled project. You can then use it safely, there’s no issues with mixing ARC and non-ARC code if it is cleanly separated and follows Apple’s guidelines.

For example, an Objective-C property whose name begins with new or init or possibly other reserved keywords like create, copy, alloc will cause errors. A simple rename will fix this.

If the library in question uses C or C++ code, then you may need to [learn about bridge casting](http://stackoverflow.com/questions/7036350/arc-and-bridged-cast). But that’s not very difficult - personally I had a harder time understanding blocks. In most cases it is sufficient to just apply __bridge because the other two variants are used almost exclusively when interfacing with the Core Foundation library, or other C libraries that follow the same Core Foundation memory management rules with CFRelease and all that.

There are some reasons why source code libraries may be unfit for use with ARC. Some source code just won’t compile because of the Apple LLVM Compiler detecting a greater number of potential issues not directly related to ARC. For example variations of NSLog(object) need to be changed to NSLog(@”%@”, object). Some header files may also cause errors when imported in an ARC enabled class, often times due to inline functions (move them to an actual .m implementation file) or structs with id types (change them to void* and cast to (__bridge id) where applicable).

In any case I strongly urge you to contact the developer(s) and express your need for an ARC compatible version of the library. We all need more ARC-ready libraries. In some cases you may be able to find a fix yourself, since the [changes revolving around ARC are well documented](http://developer.apple.com/library/ios/#releasenotes/ObjectiveC/RN-TransitioningToARC/index.html) and many compiler issues are simply encouraging good (better) coding style rather than being actual ARC-related issues.

This can also reveal how well supported the library is for the iOS platform. If you have alternatives, consider using the alternative if it works better with ARC. In other cases you may be able to find a wrapper of sorts that allows you to interface with the library in question from ARC-ready code. Or write one yourself, it can be as simple as a single non-ARC class containing only class methods which merely forwards all the calls to the library code.

#### You still need to know how memory management works before you can use ARC

The everyone-needs-to-know-assembler attitude. Here’s my answer to that:

**Yes, we can all drive cars perfectly fine, thank you. We don’t need to understand how the engine works.**

You can write ARC code without ever having written manual reference counted code, or even understanding reference counting. That’s one of the beauties of ARC - it just works the way most people would expect it to work.

To understand the difference between strong and (zeroing) weak references you don’t need to understand reference counting. [Retain cycles are still a possibility](http://stackoverflow.com/questions/6260256/what-kind-of-leaks-does-automatic-reference-counting-in-objective-c-not-prevent/6388601#6388601) and understanding [how to avoid retain cycles](http://cocoawithlove.com/2009/07/rules-to-avoid-retain-cycles.html) doesn’t require understanding of reference counting either. Whether alloc/init or autorelease is practically of no concern to ARC users. Due to the behind the scenes optimizations [autorelease initializers are actually preferred when writing ARC code](http://stackoverflow.com/questions/6776537/objective-c-with-arc-whats-better-alloc-or-autorelease-initializers), so learning the old rules first also means learning the wrong things first which then have to be unlearned again.

Especially as a new Objective-C user, **you have nothing to gain from learning how to use retain/release/autorelease**. In fact, it will slow down your progress and present you with a plethora of ugly issues that you can’t even begin to understand, nor would you want to. It’s ok to defer that learning to the situation when you might actually benefit from it. For most people, that probably means: never. And that’s perfectly ok.

At a later time, you can always come back and learn the underlying basics of reference counted memory management if that grabs your interest. It can be helpful but it’s not nearly as relevant as some people say it is. I’ve heard the same argument when C# and Java were new. Blah blah you should still learn proper memory management before using C#/Java with garbage collection. No, you didn’t.

#### I’m in the middle of a project right now

So what?

Give it a spin, I dare you. Take a day to try and convert a copy of your project and learn from the process, whether you succeed or not. You’ll be thankful you did. Besides, a half-way completed project with code that you wrote is a perfect playground to experiment. If it works, you’re using ARC, so: yay! If it doesn’t, well then you didn’t waste much time.

Sure, you’ll run into “ARC readiness issues”. Google them. Understand what the compiler is trying to tell you. Then fix them. Most ARC readiness issues are dead simple to fix. And making one fix can make hundreds of other issues go away, too.

Of course, if your project is a blend of code from various places, includes C or C++ code or generally lots of code from all over the web and has only a single target, then you’re looking at a lot of work. It may even be just not worth trying in your case.

But please be sure you don’t dismiss ARC just because it wouldn’t work with your current project. Next time, start with ARC right away.

#### After converting successfully to ARC, my project keeps crashing

This can happen. It’s not an issue of ARC itself. It doesn’t mean that ARC is buggy, it’s still your code that crashes now that it has been converted to ARC.

There are a few subtle but important differences in an ARC enabled project. For example, if you have an autorelease object in manual reference counting, and you assign this autorelease object to an instance variable, you will be able to access the object for some time via the instance variable before the object is actually released.

Now under ARC, this behavior may change. The object may be released as soon as the method where the object was allocated and autoreleased exits. Then the instance variable points to a released object, and accessing it, say, from the calling method, will cause a crash. This happens if the instance variable is set to __unsafe_unretained. This is an example of bad coding practice that is considered dangerous and very bad practice but it may still have worked before ARC.

Autoreleased object lifetime issues are probably the most common causes of what I call **Post-ARC-Conversion-Crashes**.

Once you have converted your project to ARC successfully and you have eliminated all compiler warnings as well, you’re very close to the finish line, so don’t give up now. Keep in mind that compiler warnings may or may not be potentially harmful issues, so be sure to check and eliminate all of them without prejudice! Repeatedly developers complained about crashes yet ignored all compiler warnings. Always consider that warnings and crashes may be related.

Then go on to check where exactly the crashes are coming from. In most cases you’ll find they are dangling pointer issues. Those are relatively easy to pinpoint [by enabling Zombie objects](http://stackoverflow.com/questions/2190227/how-do-i-setup-nszombieenabled-in-xcode-4). Enabling zombie objects is highly recommended before you convert your project to ARC and for some time after you have converted it. You want to be sure you have no such dangling pointer issues, and without zombie objects these issues will not always or immediately cause a crash.

Once you found the dangling pointer respectively the variable storing a reference to the already released object, it’s just a matter of figuring out why that object wasn’t held on to. Maybe it was set to __unsafe_unretained respectively assign but it really needs to be a strong reference, or a zeroing weak reference.

Other reasons are more subtle. For example I’ve had the static singleton instance variables vanish on me because I used a Singleton pattern that did not follow the [Apple-approved Singleton pattern](http://stackoverflow.com/questions/5720029/create-singleton-using-gcds-dispatch-once-in-objective-c).

All of these issues are solvable. In a fairly complex project, fixing all those crashes was a day’s work. Interestingly, the app proved to run a lot more reliable with ARC than it used to. There’s a good chance that the things that cause ARC to crash right away were the rare and seemingly random crashes you’ve noticed before but were never able to reproduce.

I suppose some people blamed ARC because of these imminent crashes, but I believe they should be thankful for ARC to crash right in their faces. It tells you there’s a problem that needs fixing that’s very likely to have existed even before the code was converted to ARC - it just happened to work sort of kinda hopefully maybe.

#### ARC isn’t available in my project templates. It didn’t seem worth the trouble.

Cocos2D is a good example. Even though it is deemed compatible with ARC it does not provide ARC-enabled template projects. That’s where [tutorials will help you out](http://www.learn-cocos2d.com/2012/04/enabling-arc-cocos2d-project-howto-stepbystep-tutorialguide/). Or in general the development community.

Not having ARC handed to you on a silver plate doesn’t mean you can’t or shouldn’t use it. It really **is** worth all the trouble!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen

Blinders, so true! The tried and true methods are a crutch for so many coders. ARC also cleans up your code immensely. It’s definitely worth adopting. Also I heard somewhere OS X is dropping GC (garbage collection) in favour of ARC too. That’s how reliable it is.

BTW you mentioned you don’t need to understand manual reference counting (MRC) to avoid circular references. I wish it were true. You can of course just use “recipes” when declaring properties as strong or weak, but to understand what’s going on you need to know how MRC works, after all ARC is just inserting retains/releases for us.

It’s also worth noting any Core Foundation classes are a major PITA when used with ARC. I’d avoid that if you can and stick to MRC for those kinds of classes.

Paul

ps: thanks for the link to our article!

You’re welcome. I agree that ARC + CF is terrible. But then again you can a) either use the Cocoa versions of the same functionality or b) write (or find) a simple Objective-C with ARC wrapper for CF, which will make your life easier ARC or not.

You do not need to understand MRC to avoid strong reference cycles.

You simply have to understand that a strong reference keeps an object alive (and as a corollary an object is only deallocated when there are no strong references to it).

If A has a strong reference to B has a strong reference to C has a strong reference to A, then they’re in a mutual embrace of eternity. To ensure this doesn’t happen, you need to break one of the references, or make one of the references weak.

No need to understand reference counts.

Exactly. You need to understand (strong) references keep objects alive, you don’t have to understand there’s something counting these references by which the compiler determines when it is safe to deallocate the object.

A good read, I have recently started to convert a lot of older projects to ARC (with iOS6 around the corner, it seemed like the perfect time).

Ok, I just made my shooter project ARC compatible following your tutorial (thanks for this awesome blog).

I made it because I like to use the latest technologies (when possible), but I was pretty happy with MRC (no memory leaks at all). Now with ARC my code looks almost the same as before, but with lots of “unsafe_unretained”, and also I feel like having less control on what’s going on. I suppose it’s the change from MRC to ARC. It seems that is working well with ARC, the Leaks Instruments doesn’t found anything.

In my opinion, I recommend to use ARC if you have done MRC before. It’s important to understand the basics of memory management. And the conversion process is not trivial for advanced projects. Believe me, it’s not like converting a cocos2d template.

Anyway, all seem to work fine at the moment. Does using ARC improves performance?

Thanks for your in deep tutorials and blog posts man!

Many of the __unsafe_unretained can actually be removed. But this requires careful consideration because you might create a retain cycle. You could also use __weak if you’re targeting iOS 5 or newer.

The feeling of having less control is just that, a feeling. There’s less code, something must be gone. Consider ARC merely hiding the retain/release etc messages from your source code view.

ARC is typically faster but it varies from app to app. For games you’re probably spending a significant amount of time rendering stuff to the screen so that it doesn’t really make a difference in terms of framerate.

“and puts it in the compiler’s hands, which knows more about object lifetime than you do” -> if you’ve been programming for longer than 10 years you’ve seen the compiler be wrong enough times to know this is fantasy. This is true *most* of the time (99+%), but it isn’t true 100% of the time and that’s the rub.

“ARC is fully supported by Apple, and they encourage you to use it. ” -> you could have said that about Objective C garbage collection, now couldn’t you? And what a nightmare *that* was! (so bad Apple abandoned it and now tells us not to use it). Again, if you’ve been programming for Apple platforms for more than 10 or 20 years you know how many times they release *new* technology that doesn’t turn out quite right and then abandon it (AOCE anyone? ha!).

“There are a few subtle but important differences in an ARC enabled project” -> told you so.

“The object may be released as soon as the method where the object was allocated and autoreleased exits.” -> this is a significant change of behavior and it was NOT a bug in manual retain/release/autorelease to understand the autorelease pool lifetime and use and object such. The new behavior actually breaks some of the utility of autorelease, but maybe ARC decreases the need for autorelease.

You left off the biggest two reasons:

a) ARC and CoreFoundation is a drag. If you use a lot of core foundation and you’ve already mastered retain/release usage then ARC doesn’t seem like much of a “win”.

b) the interaction & changes to blocks and block retained memory are a bit obscure.

c) doesn’t work for code that has to support older runtimes. In particular you lock out 32 bit runtime (there are still a lot of relatively new, fully working macs that have this environment).

d) if there’s a bug in your retain/release/autorelease code, you can fix it. IF there’s a bug in ARC you are SOL because you have to wait until Apple fixes it.

e) ARC is an unholy marriage of runtime and compiler dancing that by it’s design must make assumptions. We’re still finding out just how insidious this is.

In the end, I’ll switch to ARC, but I’m definitely not in a hurry to suffer that pain. Longer I wait, the more bugs in ARC Apple will have fixed.![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I think ARC really appeals to people who grew up on scripting languages and never had to learn about memory management and who thus felt that having to deal with memory management was so hard. If instead you grew up on C or the like you’ll have been doing memory management for so long that ObjectiveC is nice and works fine. It would be nice not to have to deal with memory management and I’m looking forward to that, but v1.0 isn’t necessarily the time to do that.![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


In any case the compiler gets it right more often (99%) than a regular human being does (anywhere from zero to 99%). I haven’t heard of a single case where ARC failed to do it correctly.

True that. But I don’t see any signs of failure when it comes to ARC. ARC is practically Apple’s v2 of garbage collection. Look what we’ve learned.

Not a bug, but very bad design to rely on an autorelease object being around for longer than the variable’s scope. There’s a reason why modern compilers stopped allowing this:

I agree with you on ARC + CoreFoundation. But CoreFoundation is a drag in itself. I bet many have already wrapped whatever they needed often in an Objective-C class.

Has that every happened to anyone thus far? I haven’t heard of such a case but then again I’m not closely following the Apple or LLVM bug trackers.

If something like that were to happen, you don’t have to wait for Apple to fix it. You can always extract the code in question to a method or class that isn’t compiled with ARC and apply whatever retain/release/autorelease is necessary. ARC is a per-class / per-object file setting.

The only reference to an ARC compiler bug I could find is this one.

I wager that you’ll have more bugs in manual reference counting code just because you’re human than Apple has in its implementation of ARC and the LLVM compiler right now.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Btw, I programmatically grew up with C/C++ and Turbo Pascal in the 90s. Only when I started using C# did I began to understand and enjoy programming, because it freed me of having to consider memory management all the time and focus on getting things done. Memory management is nothing but a distraction from creativity.

Memory management isn’t something you need to learn, it’s something that ought to “just work” for 99% of use cases. There are a few scenarios where actually being aware what you’re doing with memory can significantly speed up certain algorithms, but that’s just not really important for the large majority - someone has already written that algorithm so you can just use that implementation. It’s somewhat akin to command line vs GUI operating systems. A higher level system that’s more user friendly opened up computers to a whole new range of users.

Don’t let other that U can do yourself…..

Long live to retain/release.

Ur are responsible to free the memory that U allocate.

Java tried in past with GC, we know now that the java heap is limited to avoid memory swapping….

NeXTStep developer programmer since the begin.

don’t do yourself what the computer can do for you (and more reliably so)

First off, this point is funny to me:

“I think ARC really appeals to people who grew up on scripting languages and never had to learn about memory management”

I never thought of Java as a scripting language, but ok. However, this point is ultimately a “back in the old days, we had to push the cars around like the Flintstones.” So what? The question is, what do you gain with ARC, and what do you lose?

ARC is really the single most important advance for Objective-C since properties (and there are still people arguing against dot-syntax, of couse). Why? Because it makes your code more concise and focused on what it does instead of how it does it.

What do you lose? Really, empirically? Nothing.

That said, the transition is a serious PITA in some cases, and needs to be taken quite seriously. Is it worth it? Yes.

ARC really worth you time studying it, not just learning it. Yes you did mention some “disadvantages”. However in my opinion that just show your weakness that you have not taken enough time to read the documents of Apple related to ARC. After getting arc fully understood, it will save you a lot of time. So, I will just suggest you to take more time on ARC^_^

I see one very important point that is always overlooked in discussions about memory management, which is that while not having to worry about how the memory is managed is fine, not _knowing_ and _understanding_ how memory is managed is very bad.

Just because your memory is “auto-managed” (via some type of garbage collector, an ARC type solution, etc) does not mean the programmer is then freed from being smart about actually using that memory.

Basically what these solutions typically provide is a safety net against a crash, or other bad behavior, from using data (ie, an object) that no longer exists (was freed, released, etc). What they don’t provide is automatic “smart” memory management. The programmer is still free to perform gratuitous allocation cycles, perform allocations that are never freed, overwrite memory, and in general perform all types of abuse upon the memory they use.

As someone who hires programmers and has seen uncounted programmers who extolled the virtuous of these systems, I’ve seen the majority of these same programmers who could not understand that you can run out of memory, even in a Windows application with a backing VM store, or that memory allocations can be extremely expensive in terms of application performance.

If you understand memory management, and how the memory is handled for the platform you are developing on, then GC, ARC, etc. can help you develop better applications faster. Otherwise, they only help you develop buggy applications faster.

I agree with your point but disagree with your conclusion. What is worse to the end user: an app that uses memory less efficiently or one that crashes more frequently? And what is better for the (beginning) developer: an app that uses memory inefficiently or one that crashes and you don’t understand why?

ARC and other automatic memory management systems make the entry level easier, and it leads to more stable apps from all developers - minus the few cases where developers haven’t understood memory usage. Btw, this is not only related to memory management, frequently I come across new developers who wonder why their 20 image files, each less than 200 KB, lead to a memory usage of over 100 MB. This is not related to how memory is allocated, but other technical facts that developers simply need to learn as they encounter them.

The problem with inefficient memory usage is far less significant than unsafe use of pointers and mismatched alloc/retain/release in manual memory management. The memory management issues can also be taught easier compared to safe use of pointers and references - there’s just a lot more that can go wrong in manual reference counting.

For example I once lead a team of Lua scripters. Teaching them the issue of thrashing the garbage collector by appending strings in a loop, and instead using table.concat to minimize the impact of immutable string concatenation was more or less a simple tip. Teaching them pointers and references and manual memory management would have been a far greater challenge.

I agree that ARC is a real improvement over manually releasing memory and the reasons for not using ARC you listed are indeed lame. However, you left out one important reason for not using ARC, which is it isn’t supported on older devices like the iPhone 3G that can’t run iOS 5. If you want to continue to support pre-3GS phones you can’t use ARC.

That’s not quite correct. ARC works with iOS 4.0 and above, so you really only can’t deploy ARC apps to the first generation of devices. The 2nd generation like iPhone 3G can be upgraded to iOS 4.2, and run ARC code just fine.

If you target iOS 4 the only thing you lose are zeroing weak references. You can use zeroing weak references (__weak keyword) only if you set the deployment target to iOS 5.0 or higher.

Good post, and good points all. However the biggest point, and in fact the only point, which has held me back from ARC is a need to support OS X platforms going back to 10.6 This is actually pretty common among Mac developers. You’ll notice that many of the big titles, both big time and independent, continue to support 10.6. Snow Leopard was a great, stable, lean release and it still has a pretty devout following.

You know that ARC is supported on Snow Leopard, right? It’s just not supported on machines with a 32-bit CPU, ie machines that can’t run 64-Bit apps. These machines install Snow Leopard in 32-Bit mode where ARC is unavailable. Those machines and their users will probably make a very, very minor subset of the market given that these machines haven’t been running SL very well to begin with.

A similar myth exists for iOS: contrary to what some developers believe ARC is available beginning iOS 4.0, not just in iOS 5. Though on 10.6 / 4.x you can’t use weak references.

[…] you still aren’t convinced of the benefits of ARC, check out this article on eight myths about ARC to really convince you why you should be using […]

Thank you for yet another article jam-packed with information and solid reasoning. I fit in the “I’m in the middle of a project” camp. I’m new to coding, and have been working on an iPhone game after reading your book on Cocos2d iPhone games for beginners. I thought I was close to finishing the game, and then realized I know absolutely nothing about proper memory management, and my game is leaking memory like rusty frozen pipes leaking water after an earthquake. I’ve been banging my head against Instruments for the past week, and now I think I’m ready to throw in the towel and try ARC. I’ll be coming back for more knowledge later. Thanks again for all the informative blog entries, I really enjoy your writing style.

Good job! Hopefully by now everyone’s gotten the message. I can’t imagine coding without ARC.

Now you’ll have to convince people to use Swift, too.

-W