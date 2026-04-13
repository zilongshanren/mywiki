---
title: What most young programmers need to learn
url: http://joostdevblog.blogspot.com/2015/01/what-most-young-programmers-need-to.html
author: Joost van Dongen
published: '2015-01-04'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo](http://www.ronimo-games.com)and have seen hundreds of portfolios of students and graduates. In almost all of those I saw the same things that they needed to learn. One might expect that I think they need to learn specific techniques, algorithms or math, or other forms of specific knowledge. And of course they do, but in my opinion that is never the main thing. The main thing they need to learn is

*self discipline*. The discipline to always write the clearest code you can, the discipline to refactor code if it becomes muddy through changes later in development, the discipline to remove unused code and add comments.

Most of the time I spend supervising programming interns is spent on these topics. Not on explaining advanced technologies or the details of our engine, but on making them write better code in general. I always ask applicants what they think is important in being a good programmer and they usually answer that code should be clear, understandable and maintainable. That is indeed what I want to hear, but it is very rare for a young programmer to actually consistently follow through with that.

Keeping this in mind requires self discipline, because it means not stopping "when it works". If all the variables would have the wrong name the code could still function perfectly, but the code would be super confusing. The step from functional code to clear code brings very little reward in the short term: it worked already and after cleaning it up it still works. That is why discipline is required to take this step. That is also why doing an internship is so useful: a good supervisor is vigilant on code quality (even though the definition of "good code" might of course differ per programmer) and thus forces the intern or junior to always take that next step.

Let me give a few examples of the kinds of things I often see in code written by starting programmers:

**Liar functions/variables/classes**

These are functions, classes or variables that do something else than their name suggests. Their name is a lie. It is very obvious that names should be correct, but to my surprise it is quite common for names to be completely off.

An example I recently encountered in code written by a former intern was two classes: EditorGUI and EditorObjectCreatorGUI. This is code that handles the interface in our editors. To my surprise it turned out that the code that handled the button for creating new objects was in EditorGUI, while EditorObjectCreatorGUI only handled navigating through different objects. The exact opposite of what the naming suggests! Even though the code was relatively simple, it took me quite a while to understand it, simply because I started with a completely wrong assumption based on the class names. The solution in this case is really simple: rename EditorObjectCreatorGUI to EditorObjectNavigationGUI and it is already much, much more understandable.

This is something I see a lot: names that are simply incorrect. I think this often happens because code evolves while working on it. When the name was chosen it might have been correct, but by the time the code was finished it had become wrong. The trick is to constantly keep naming in mind. You have to always wonder whether what you are adding still fits the name of the function or class.

**Muddy classes**

Another problem I see is muddy classes: classes that do a lot of unrelated things. Again this is something that happens as you keep working on the same code. New features are added in the easiest spots and at some point classes become bloated with all kinds of unrelated behaviour. Sometimes the bloating is not even in the size of the classes: a class might be only a few hundred lines but still contain code that does not belong there.

An example of how this can happen is if for some reason a GUI class needs to analyse what textures are available (maybe because there is a button to select a texture). If the GUI class is the only class that needs the results of this analysis, then it makes sense to do that in the GUI class. However, then some totally unrelated gameplay class for some reason also needs that info. So you pass the GUI class to that gameplay class to query the texture information. At this point the GUI class has grown to be something more: it is also the TextureAnalyser class. The solution is simple: split off the TextureAnalyser class into a separate class that can be used by both the GUI class and the gameplay class.

The general rule of thumb to avoid this problem is to always wonder: does the functionality that I am adding here still fit the name of the class? If not, then the class either needs to be renamed, or it needs to be split into separate classes or the code needs to go into a different class.

It is usually a Bad Smell if you cannot come up with a fitting name for your class. If you cannot describe what a class does in its name, then maybe what it does is too muddy. It might need to be split into parts that make more sense and can actually be described with a proper name.

**Oversized classes**

This one is really similar to the muddy classes above: over time more and more is added to a class and it gets bloated. In this case however it all still makes sense to be in one class, but the class simply grows too big. Gigantic classes are cumbersome to work with. Bugs slip in easily as there is a lot of code manipulating the same private member variables, so there are a lot of details one can easily overlook.

Splitting a class that has grown too big is quite boring work. It can also be a challenge if the code in the class is highly intertwined. Add to this that it already works and that fixing it adds no new functionality. The result is again that it requires serious self discipline to split a class whenever it becomes too big.

As a general rule of thumb at Ronimo we try to keep classes below 500 lines and functions below 50 lines. Sometimes this is just not feasible or sensible, but in general whenever a class or function grows beyond that we look for ways to refactor and split it into smaller, more manageable pieces. (This makes me curious: where do you draw the line? Let me know in the comments!)

**Code in comments**

Almost all sample code that applicants send us contains pieces of code that have been commented out, without any information on why. Is this broken code that needs to be fixed? Old code that has been replaced? Why is that code there? When asked applicants are usually well aware that commented-out-code is confusing, but somehow they almost always have it in their code.

**Parallel logic and code duplication**

Another problem that I often see occurring is to have similar logic in several spots.

For example, maybe the name of a texture gives some information as to what it is intended for, like “TreeBackground.dds”. To know whether a texture can be used for a tree we check the filename to see whether it starts with the word “Tree”. Maybe with the SDK being used we can check that really quickly by just using

*filename.beginsWith(”Tree”)*. This code is so short that if we need it in various spots, we can just paste it there. Of course this is code duplication and everyone knows that code duplication should be avoided, but if the code being duplicated is so short, then it is tempting to just copy it instead. The problem we face here is obvious: maybe later the way we check whether a texture is fit for a tree changes. We then need to apply shotgun surgery and fix each spot separately.

A general rule of thumb here is that if code is very specific, then it should not be copied but put in a function. Even if it is super short and calling a function requires more code than doing it directly.

All of the things discussed in this blogpost are really obvious. Most of these things are even taught in first year at university. The challenge is to make the step from knowing them to actually spending the time to always follow through with them, to always keep them in mind. This is why the most important thing that all programming interns learn at Ronimo is not

*knowledge*, but

*self discipline*.

Really nice post, thank you! In Unity3d C# we at Little Chicken try to keep our classes below 400 lines of code.. no real conventions for methods, but they should fit in a landscaped monitor in my opinion ^^

ReplyDeleteyeah but over splitting is equaly wrong and annoying!


DeleteIndeed, over splitting is also a problem and results in lasagne code (the opposite of spaghetti code). I actually wrote a post with a really nice example of crappy lasagne code a couple of years ago:



Deletehttp://joostdevblog.blogspot.nl/2012/05/programming-with-pasta.html

400 lines per class sounds very reasonable though, I wouldn't call that "over splitting". :)

400 lines seems arbitrary. Classes need to do what it is they need to do. I agree that few classes approach 400 lines but lines-of-code should not be the criteria for class size, purpose and function should be. If you keep your classes focused on the object they represent then lines of code will take care of itself.


DeleteMethod size, on the other hand, I do generally set line limits as a guideline because it makes me focus on keeping my methods single-purpose. Landscape screen is generally too big. In the old 24x80 green-screen days, a screen size was a good limit. Not only did it allow you to see the entire method, it kept them small enough to allow you to easily follow the flow. A method that fills a full landscape screen today still is likely doing too much and has too much complexity to quickly comprehend. Of course, if the single purpose actually does take even more than the full screen then that's what it takes - I just very, very, rarely ever see a single-purpose method that takes that much space - especially if refactored to make it self-documenting and easily read and understood.

Thank you for this. As a programmer who started full-time six months ago, this resonated so much with me. The transition was hard (and still is). Projects become more and more bloated and deadlines come closer and closer. I've been rushing and refactoring at the end when I should be doing it throughout my workflow. Self discipline sums it up very well. Correct does not mean done.

ReplyDeleteYeah, deadlines make this much more difficult. In the long run it is better to write good code even when facing deadlines, but it can be really difficult to find the time for it.


DeleteAt Ronimo we have the rule that code always needs to be good. We value this more than meeting deadlines. However, this is a luxury that not everyone can afford.

This is why tools such as Resharper are very useful for me personally. I can refactor as I go and change my mind frequently about what I'm doing and how I'm structuring the code.

DeleteJoost:




DeleteI disagree that it is a luxury. Allowing code that has issues is exactly how trojans and other malware get a foothold. If you cannot write a clear prose description (and you absolutely should) then your code is not maintainable and is suspect.

Another way to describe your discipline admonition is:

Software is *NOT* the same as code. Software requires thought, design, clear execution, and adequate testing against requirements. Coding is only about 10% of 'software'.

Ray M

Anyone beginning to write professional code should read "Clean Code" by C. Martin. It would make all code so much simpler.





ReplyDeleteI've actually written a blog post recently about clean code. It's targeted to beginners and advanced programmers as well.

http://yourcodesucksexception.blogspot.com/2014/11/your-code-sucks.html

You didn't mention testing. Tests first, wild implementation later. If we don't emphasise the importance of this we're going to be dealing with a lot of untested code handling our private information in the future.

ReplyDeleteThanks for this very good post. I especially like your insight that "knowledge" is not the the problem, but "self discipline". This did not occurred to me so far but I think you're right.


ReplyDeleteI made similar observations and came up with the "10 commandments" :-)

https://larsxschneider.github.io/2013/08/25/ten-commandments/

You're forgetting thorough input validation. Otherwise regardless of your layout and functions, your program will do something else than it was intended to do.

ReplyDeleteRegarding code duplication, you could use symbolic names (not sure what they are called) so long as the scheme stays the same, ie.



ReplyDeleteDefine a name for the substring you check against and declare it's actual value just once, if you simply change your scheme from Tree... to Foliage... you can then change what substring you're checking against.

Of course this approach doesn't work if you change from startswith to endswith, but it's up to the programmer to declare such a change valid and/or necessary.

What if the way you check is not a substring any more?

DeleteOften, young programmers startet with fixing bugs. They are anxious to change the code of their "masters". They want to fix the bugs with minimal changes and impact. They are socialized and rewarded for not refactoring.


ReplyDeleteOver time, the code becomes messy.

I am surprised you mention this: if there is one thing I wouldn't let a junior do initially, it is fixing bugs. Fixing bugs in other people's code is much more difficult to do well than building something new from scratch, especially when working in a large codebase. I once let an intern do random bugfixing/improving instead of giving one big clear assignment. Years later we are still regularly bumping into the mess he left throughout our codebase...

DeleteDisagree, fixing bugs is the fastest way to get a junior up to speed with your code base, coding style and general architectural approach. You should be reviewing their code to prevent any mess and guide them in learning their trade. You're short-changing yourself and the junior if you're leaving them to their own devices. Besides, you're going to run into the same issues with their code, but just in a whole other area, if you let them crack on with something new.

DeleteThe point is that bugs can be anywhere and I cannot quickly see whether a bug is fixed in the correct way. With a new subsystem however I can much more easily check the entire code the intern made and really understand what it all does.

DeleteI agree with Anonymous that bug fixing the fastest way to get your hands dirty on a code.


DeleteAs for verifying the correctness of the bug fix, I suppose you will have units tests to help you out. You can even tryout TDD for bug fixes

As Joost said, I wouldn't get a junior programmer or new starter to fix a master programmers bugs. That would only lead to confusion. Besides, the master programmer must fix their bugs and fix them early. Junior programmers or new starters ought to start at either the top of the stack(front end) of the bottom of the stack(DAL & database) and be educated to the more complex middleware. Of course Interfaces and TDD for these must be written first

DeleteHow timely, I've been preparing a talk on this very subject. The reason behind this phenomenon, I think, is not a fault of inexperience but our lack of ability to teach programming well. Programmers, young and old, have a difficult time recognizing what good code looks like... much as writers once did (and still do when they're just starting out). The solution that William Burroughs took up in teaching good writing is to teach comprehensive reading in the hopes that students could recognize and internalize good writing. The same could be true for programming as well.

ReplyDeleteHmm, interesting point, I indeed don't remember ever having received an assignment to read code (when I was still in school).



DeleteI think part of the burden for this is the internship though. Writing clean code is learned very much in practice. In the Netherlands most computer science students need to do a four month internship at a company and this is the ideal spot to learn this. If only all companies wrote clean code...

One thing schools could do is spend more time reviewing student's code instead of just checking whether the assignment was completed.

"As a general rule of thumb at Ronimo we try to keep classes below 500 lines and functions below 50 lines."



ReplyDeleteIt depends what language/environment you're using, but these limits seem pretty big to me. On a 15" laptop (not an ideal working environment but a common one), it means you won't be able to see more than one function at a time.

Besides, unless you're writing in a low-level language, 50 lines is a lot of work -- it's hard to imagine a single un-decomposible function needing that many lines.

What? The FFT function (pure mathematics) that most people use is over 100 lines. You wouldn't want to decompose it.

DeleteOne screen height is my absolute maximum for functions. Classes are a bit harder to pin down to a maximum other than "is this code still relevant".



ReplyDeleteHonorable mention for this list: code organization. This applies to both the source code itself (arrangement of methods, etc) and project folder/file structure. It's much easier to debug/grok someone else's code if it reads as you would expect without a lot of guessing/jumping around.

Yeah, I totally agree that code organization can help a lot. At Ronimo we have a much stricter coding standard than at any other company I know simply because it helps a lot if everyone puts things in the same order and with the same layout (for example, member variables always come after member functions in our coding standard).

Delete"Member variables after member functions"


DeleteDouble thumbs up for this.

Someone explain to me the advantage of putting the functions above the variables. In every language I've ever coded, the variables come before the functions.

DeleteBoth can be at the top, it just helps readability to be consistent with it.


DeleteWe put functions at the top because variables are usually all private (or protected) so the public things are all functions. The public things is what users of the class need to see, so to me it makes most sense to put those at the top.

"All of the things discussed in this blogpost are really obvious. Most of these things are even taught in first year at university."




ReplyDeleteAren't these statements contradictory? People don't go to universities to be taught things which are obvious. I studied computer science at an American university (which is consistently rated in the top 10 in the world) and none of these was ever taught to me.

I think these things fall into an intersection of "courtesy" and "memory". A lot of programmers have a mind for remembering and dealing with 1000 tiny details all at once. A lot of programmers haven't worked with other people enough to know that other people can't. Together, these mean that many programmers simply don't appreciate that they need to document their work, not lie with their naming, write functions that are readable, etc.

Unfortunately, at the organizational level, this is a latch. Once an organization is infected with extremely technical people who don't think of others, it's virtually impossible for anyone different to join the organization. But if an organization begins with people who write clean code, it's very easy for people to join who will mess it up.

Heh, good point, obvious things don't need to be taught. :) I meant that what is taught in the first year seems really obvious by the time you graduate.

DeleteI don't think they're contradictory at all. The points mentioned are obvious *once you've spent some time working with code*. Which, unfortunately for a lot of people, isn't until they start attending university.

DeleteExcellent advice - for new programmers and old ones alike. While there are millions of "how to code" pointers out there, it's always useful to see one that has real life examples, both of how you got to that point, and why it's important to step beyond the "it finally works" checkin and checking in the updates to make it right.



ReplyDeleteI humbly suggest your next blog post: How entry level engineers can work productively with management to ensure these steps get recognized and instilled in corporate culture. That's the really hard part - both for engineers as well as managers.

Thanks!

That is a post I would not be able to write: I co-founded Ronimo right out of university, so I have never worked under management. My entire professional career was as lead programmer. I have the luxury of never having had to deal with bad management. Except when I did bad management myself, of course... ;)

DeleteI think I can share my experience here! When I started, I was introduced to a major (ugly) code base that had been developed on for over 3 years by a few seniors and a lot of different interns without any reviewing whatsoever. Syntax of naming was all over the place and public members were literally named by single characters, so you'd get pm.g.d = 5.



DeleteWhat I did (as an entry level engineer) was convincing the other programmers that the code should be cleaner and we should do code reviews. But before doing code reviews we needed conventions, so we (asked management and) set up a meeting with all senior programmers to discuss conventions that we could display in a wiki site. After a few long discussions and setting up the wiki we slowly started doing code reviews every now and then. We're still bound by deadlines, but we focus more on writing clean code since then.

I think starting with the conventions is most important, to get all seniors and newcomers on the same line. Then, if management is OK with it, slowly work towards code reviewing :D

Yeah, conventions are really important. I intend to do a post about the coding standard document at Ronimo in the future, might be interesting to compare it to yours then and hear your opinion on ours. :)

DeleteVery interesting indeed :D

DeleteYou never stop getting supriced :-)



ReplyDeleteAfter this "new" knowledge, how do you handle new recruits? If so, did it have any affect?

Great post anyway.

For new recruits I make sure to come up with a very specific subsystem that they need to build. Something where they can keep working on the same topic for several months, so that they don't have to learn our entire big codebase right away and can get to know a part really well. I then make sure to check all their code to make sure it is up to our coding standard. Our coding standard is very strict and I hand it to them on the first day and discuss our approach to coding.

DeleteHelpful post. Self discipline is indeed one of the greatest skills for us who belong to IT sector. Recently I read 'Applying UML and Patterns' by Craig Larman, who emphasizes some of the points you mentioned through his GRASP and the Design Patterns of OOP.

ReplyDeleteTake a look at just about any Git repo, written by anyone between the ages of 5 and 95. And soon you will realize that these young kids are lacking these disciplines because there's a whole lot of older programmers out their that are failing to teach them these disciplines!

ReplyDeleteReally neat post, unfortunately I recognize myself quite a bit in this as a student getting closer and closer to graduation. Most of these points get taught in university but rarely put to the test. Code that has been commented out and class size are probably the things from this list that get checked the most often, but your view on code duplication isn't even taught that strictly at all.


ReplyDeleteYour post has actually gotten me pretty interested in doing my final internship at Ronimo.

We have an internship position for a C++ programmer every half year, so you are welcome to apply when the time comes. :) Note that our internal communication language is Dutch, so only people who understand Dutch well can apply.

DeleteJoost, so you guys at Ronimo talk to each other in Dutch and code in English? If that is the case, then that really sows how Software is the total idea/implementation and Code(English) is just syntax in a file.

DeletePersonally I tend to tolerate much larger functions than that, if they are clearly divisible. For example, I have some functions in my personal codebase that are over a thousand lines long- except it's 30 individual pieces that don't interact with each other (registering many related event handlers where each handler is totally independent).

ReplyDeleteGoogle SOLID principles in software development. There's no good reason for any method to be that long. If you're a hobbyist and don't care then I suppose it is your choice but if you are a professional or expect anyone else to work on your code then you practice is very bad.


DeleteAs Fowler states, we write code for other developers, not for computers.

Really good advice, Joost van Dongen. I myself am an (almost) 14 year old game developer, and the Parallel logic and code duplication part in your post really makes sense. Since I work alone, I don't really keep my code that clean, but now since I have started selling Unity3D assets, it is forcing me to maintain coding conventions and clean code, which I think is a good thing ;)

ReplyDeleteI'm not young but I'm starting out in coding. I am not naturally good at math or physics, will this be a big problem for me to start a career in coding or software testing? Thanks.

ReplyDeleteThere are many topics within coding and most don't require serious math or physics. All programming requires a really good mind for logic and structure, that is the most important 'talent' I suppose. To me math and coding are closely related but I know lots of programmers who dislike math.

DeleteIt is good to document standard coding practices with examples and pass it to all Junior - Senior programmers.so they will verify with their code like a checklist. this practice of verifying will make them more self disciplined.

ReplyDeleteI've walked into a group a few years ago after being with a software developer for 18 years. I was a Sr Project Lead at my previous company but walked into this group that had no documented standards and standards were; his way, my way or whichever way the developer wanted to go. Most of this group were Sr in their minds but had about 2-3 years experience as this was their entry level into software development. Only myself and the manager had 10 or more years experience developing software but these "Young" programmers knew everything there was to know about software development. Within a year the manager left and the next in line with I think 3 1/2 years experience took over. Well, if there were standards, they left with the prior manager and I left about 6 months later. Self discipline, they had it. Comments were actually removed from code as well as dead code that was left in for specific commented reasons was removed as well.

DeleteI m very bad at programming.

ReplyDeleteIt would be great if you guide me till i can write good programs on my own!

I agree with this topic ,I am Sr programmer and all the programmers , including Experienced programmers do not have self discipline another words put rules on yourself, there are patterns to find and sometimes those patterns are hard to find or see..in time code becomes more separated (concerns) more flexible, robust and maintainable


ReplyDeleteand 80 percent of the programmers I come involved with don't understand the concept of core libraries (System level and business level libraries) they have code all over the place and keep building on top of bad code

Joost:




ReplyDeleteThis is spot on. If I ever get the chance to teach at university again, I believe I need to make the discipline aspect a major part of the lessons.

The worst example I ever saw came from code my manager's manager wrote several years before I inherited the code. Unfortunately, he was a EE with little formal software engineering training. He implemented what was actually a state machine using if-elseif-elseif-else constructs over 2000 lines. My manager later inherited the code and ended up getting a couple of very bad performance reviews because the code just simply could not be fixed without refactoring and simplifying.

Your limits of 500 and 50 are reasonable. The number is a little arbitrary, but the description is correct. If you have to scroll back and forth through the file endlessly to try to see things, then it is way too large. This is a human factors issue. The human brain can only handle what it sees all at once. Once it has to do several operations, you loose the effectiveness. In the "old days" we basically set the limit to what could be printed on an 8.5x11 piece of paper (turns out to be about 50 lines). Today that translates to what you can see on a screen in landscape mode.

This is hilarious. Of course you are spot on in all your points. And most of the commenters agree more or less. But reality is quite different at most places I've worked in the past 20+ years. I have people even now that argue vehemently for "no break no fix" (if it isn't broken, don't fix it). The best way for a new programmer to get chewed out or dressed down is to make any kind of "unnecessary" code changes. I wish i was joking but I'm not. Ask around, many if not most places follow this atrocious policy.

ReplyDeleteA terrible policy that I love to ignore.

DeleteI agree with you. However, I believe the author's emphasis is on classes or applications developed by the interns from inception. I wouldn't suggest that you just start to alter existing and working (or even legacy) code without the need for this.

DeleteI have never worked as a programmer at another company: we started Ronimo right out of school. So I am quite baffled by how many replies this post has been getting (also on Reddit and y-combinator) that are all about how bad the programming practices at many companies are. Really painful to see so many programmers complain about how crappy the practices at most jobs are...

Delete"The step from functional code to clear code brings very little reward in the short term". This is very correct. In fact sometimes refactoring can stop the original code from working and this brings more work but it will prevent code rot in the long term.

ReplyDeleteI'm very surprised to hear these comments, especially from seasoned programmers. 500 lines in a class only - really. I've worked on classes that were huge. Very well organized, very well written, but very large doing very specific business logic routines. Sure we could have thousands of little classes running around. Sooner or later that becomes a major problem. We have all seen the little single function call shoved into a class that should have been put together in one utility class. Writing clean good code is truly something to aspire to and most seasoned programmers will try their best to do it. Time, pressure, reality of job demands, may make code less than ideal for new programmers and seasoned ones alike. Personally my entire 25+ years coding has been in the business area. No game programming. You would not believe the incredible amount of pressure that can be put on the programmers to get something out the door because a marketer or sales person promised something that realistically could not/should not have been done. I’ve seen this so many times now in the electronic area, medical field, warehousing field, you name it, that it’s ridiculous. It would be great to take as much time as necessary to make the code very clean, elegant, and fast. It’s a serious balancing act.

ReplyDeleteThat argument predates OO languages, anonymous. it was wrong-headed back then, and it's wrong headed today.

DeleteI disagree that job demands and time pressures or schedule excuse writing bad code. When you know how to write good code and writing good code is your habit then writing good code is always faster than writing bad code. Writing unit tests is always faster than not writing unit tests.



DeleteWhen developers write bad code because of pressure and schedule it is the developer's skills that are the cause, not the schedule. Needing to update your skills is not a bad thing so please don't get defensive when I say this but needing to update your skills and not updating them is a bad thing - and it's indefensible so no worries about readers getting defensive on that point.

So, even if you've been writing code for 25 years, if you are writing bad code because of tight deadlines, get Fowler's Refactoring, read it cover to cover at least twice, and start practicing turning your bad code into good code - at home, and not just at work, until you find it easier to write good code than it is to write bad code.

I agree that with the right habits and skills one writes much better code than without. For example, I personally try to write code cleanly right away, so that I do not need to do a cleaning step at the end.


DeleteHowever, refactoring is still sometimes optional. We had a case last week where a class had grown beyond 1000 lines of code and we expected it to grow further. All the code in the class was clean and nice, and the class had a clear purpose. Yet at some point a class just becomes too big to handle and you need to split it. This splitting is extra work (in this case at least a day because the split is also a real restructuring) and fully optional. Good habits could not have avoided this because we didn't know we were going to nee this many features there when we first made that class.

Good article!! One minor nit: when you write: " Their name is a lie. It is very obvious that names should be correct, but to my surprise it is quite uncommon for names to be completely off," I believe you mean "quite common" rather than "quite uncommon".

ReplyDeleteAh, yes, thanks, fixed! :)


Delete(Surprising that no one mentioned this before with over 100k views on this one blogpost!)

Nice post I agree. Nevertheless, I would like to excuse two "bad" habits:



ReplyDeleteOld commented out code can stay until I'm convinced the new code has proven to be better, until it is not needed anymore, or until I forgot why its there (whatever happens first). Hopefully it gets removed fast.

Size is not an issue. Clearness is. Function-size becomes an issue only when clearness suffers, or function-headers are scrolled out of view. For modules, coherency matters and not the number of functions and certainly not the size.

This comment has been removed by the author.

DeleteChris, on you 2 points:


DeleteWith comments, I hope you use some type of comment identifier so that you can find all those comment blocks that might need removing, such as //TODO or //REMOVE

With class size, size might not matter but high cohesion does. A class' methods must be relevant to that classes purpose. Or if you still code in a non-OOP language(script or Cobol), methods in a file must be relevant to the purpose of that file.

I once saw a Cobol file that was 30k lines, all relevant to the file name.

So if you call a class/file "Admin", it doesn't mean you put all administration methods for an enterprise into that class/file.

What it means is that your naming convention is incorrect as it is not specific enough to be able to break out the various "Admin" methods.

As far as function size is concerned, atomicity is important. So ensure a large method only has one purpose. A easy mistake to mix the manager code with the worker code. Try to identify which is which. Manager code and worker code really belong in two different classes.

If the method size is getting large ( > 50 lines), then examine the code to see if parts can be refactored into smaller methods. Candidates are code blocks in loops or branching code(if/else or Switch/case).

Large methods can also have logical breaks so that code between these logical breaks can be broken out in separate methods, or even separate classes.

That is what Refactoring is about.

Remember, the general rule is small is best as it will be more manageable and lead to class/method reuse.

old commented code never has value. That's what version control is for. No commented out code should ever be checked into the main branch or trunk. It's ok, I supposed, in your working branch but no further.

DeleteIf code is commented out, it is not needed anymore. Therefore, you're safe to delete it. If you want that code back at a later time, use source control.

ReplyDeleteany of that, but learn new things and be different,

ReplyDeleteAm one of those young programmers interesting article. Check out an application 've been building on and tell me what you think http://mbithy.blogspot.com/2014/12/music-sounds-better-if-you-made-player.html

ReplyDeleteI didn't look at your code for very long, but a couple of small things that I noticed right away:







DeleteIn Settings.cs starts with a bunch of comments that are so obvious that it would be better not to write those in comments. For example:

"//The SettingsLoaded event is raised after the setting values are loaded."

The variable name already communicates that.

Some of the other comments there are a bit more informative, but could still be removed:

"//The SettingChanging event is raised before a setting's value is changed."

If you change the event name to "BeforeSettingChanged" then you don't need this comment at all. The main concept of Self Documentating Code is that if you can explain things through code and naming, then you don't need comments. Comments don't raise compile warnings when they are wrong, so comments should only be used when they are actually useful. If possible, clearer code is preferable over comments (or both if needed, of course).

Another thing I noticed: MusicAccessData is a static class, but why? Is it inherently impossible to play two songs at once? If this were a normal class instead of a static class then the class would not be more complex, but it would be more flexible since it would be much easier to stream two songs at once (useful for cross-fades, if you ever want to add those).




DeleteIn general my opinion on making code more flexible and generic is that it should only be done if either you need the extra functionality, or it does not make the code more complex. Adding complexity to add a flexibility that you don't need is a bad idea, but if it is just as much work to build and the code is just as simple, then there is no reason to not be flexible.

Also, in general static classes should only be used when this actually makes sense. In most cases normal classes are better, so you should always wonder why you are using static and only use it if there is good reason for it.

Do note that I did not look at the code for too long, so maybe there are really good reasons why you made this class static and I just didn't notice it. With all comments anyone gives on code: always wonder whether you are agree, or whether there are further arguments that the commenter (me, in this case) did not realise.

Overall, let me say I agree with this article but rather than self-discipline, I think it is a question of habit. Is that the same as self-discipline? Perhaps; it depends on point of view, I suppose.


ReplyDeleteI always teach developers who have problems with writing good code to follow Fowler's Refactoring. Proper refactoring, as Fowler describes, allows developers to be productive while learning to be better OO programmers. Over time, you have to refactor much less because you think to yourself, "If I type this this way now, I just have to refactor it in 5 minutes." You soon find yourself stopping the bad code and writing so you don't have to refactor in the first place. Keep writing code but keep improving the code you already wrote and the code you're writing now by practicing and repeated refactoring until you find you're refactoring less and less.

To me "habit" is often something the starts with "discipline". If you discipline yourself to always keep Good Code in mind, then at some point it comes automatically and then it is a habit.

DeleteThis is a really good blog and I did send it to one of the interns on my team. Before I had even seen this blog, I basically told him the same thing about what it takes to be a good coder/developer. Consistency is the main thing and I've read a log of code in my career as much as producing code for others to maintain. The thing I noticed most is reading through a lot of crap that makes no sense or are very hard to figure out. Good code is very easy to follow and does not require very much thought process to figure out. When code is formulated, I learned a long time ago from one very intelligent senior developer (while I was a junior), that a line of code should be a singular execution. If a line of code contains multiple execution, it requires the mind to wander and the person to figure out what that line of execution is doing. Also, time and time over the years, you hear others expressing simplicity in implemenation. How true can that be, but it is hard to do than it sounds. To keep things simple, you definitely have to do just that - keep each line of code simple and self documenting. You can document the hell out of the code you want, but if the line of code still doesn't make sense and requires a huge amount of comment, it means that the code should be re-written to make it more simple.



ReplyDeleteAs for huge classes, I really don't agree on limitation on the size of any code. Like what the blog has stated, it is impossible to enforce the size of a function and class length to 50 lines or less for methods or 500 lines for classes. The best ways to look at it is to make things simple and make sure a method does only one task and not multiple tasks. The method can be unit tested this way. The unit of code can be a big as you want or as small as you want; and the smallest unit of code is a one line of code, which can be tested. For classes, an intern or a junior developer is likely not going to be able to do this very well or at all in terms of true object orientation. This takes time and experience until that concept is shown over the course of several projects. This is because OO's practicality is transpaarent in a framework and not developed by anyone other than the architect or a senior tech lead. I've seen in so many projects that even senior developers often use static global implementations rather than true OO for code re-usability. This is a bad approach as it is simple and direct; however, over time, you see similar code popping up in different files across the whole system.

I totally agree with developing a good sense of coding with consistency through self discipline and good mentoring. It is important for any senior developers to train the intern and junior developers early and make sure coding standards are adhered at all times. It would be totally wrong to either through the person to the fire immediately leave the person to learn things on his/her own. It is also wrong to also ignore the intern and give that person nothing to do during the whole term. I just want to mention these is because I know some companies do that kind of crap and it makes no sense except to claim research grant money from the government.

To further clarify your point on "Code in comments", I would suggest that a remedy for that situation is version control. Go ahead and kill that code, you can always go back and see what was there before.

ReplyDeleteIt is obvious that proper , clear and simple comments make us understand any code clearly

ReplyDeleteMost of the juniors I met doesn't know about OOP apart from definition of class, object, abstraction ... even though they know definition they don't understand it, forget about using it on their code. We teach them these basic things by asking them write games like Tetris, Ping Pong etc

ReplyDelete