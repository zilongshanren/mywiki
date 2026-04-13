---
title: Object Oriented Programming doesn't need Encapsulation
url: https://dewitters.com/object-oriented-programming-doesnt-need-encapsulation/
published: '2010-04-10'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

*Note: I use the term ‘Encapsulation’ as a language mechanism for restricting access to some of the object’s components. Others might call this ‘information hiding’. *

### Traditional Object Oriented Programming

In every object orientend programming course or book that I know, you get introduced to a concept called encapsulation. Encapsulation is a technique that allows you to protect implementation details while exposing only the interface. The advantage is that the rest of the code can only use the interface, and therefore is not dependent on the hidden implementation.

The thought behind the whole idea of encapsulation is that when implementing a class, you protect it against misuse. You make sure that the user can’t break it. You have total control over your class, and the user can only use that what you allow him to use. Another advantage is that providing a stable interface will protect implementation details that are likely to change, and therefore limiting interdependencies between software components. That is, it forces the users to do so.

Most Object Oriented programmers totally agree with all of the above, and I used to too. But that was until I met python.

### OOP without Encapsulation?

Python supports Object Oriented Programming, but it doesn’t support encapsulation. Now how is that possible? Various OO programmers asked the same question in the python user group, and the end conclusion is pretty simple: you don’t need encapsulation for OO. In python everything is public, you just put and underscore before members or methods that are not part of the interface. If the user is going to use them, it’s at their own risk. Python programmers refer to it as “encapsulation by convention rather than enforcement”. But essentially it’s not encapsulation or data hiding at all. If you ask yourself why this would be an improvement, you probably don’t know that in some rare cases, it is necessary to access the implementation. Let me explain below.

### Using the ‘computer’ metaphor

I have this computer on my desk, and it’s a nice piece of engineering. It has a public interface which is clean and simple; On the front it has 2 buttons “Power” and “Reset”, and a few leds to show if it’s on or if the hard disk is accessed. On the back it has connectors where I can plug in the power, network, keyboard, mouse, screen, etc. .

When it’s broken or I want to upgrade, I can just buy a new one and it will provide me with the same interface.

What my computer doesn’t use, is proper encapsulation. Remember that encapsulation is restricting access to some of the underlying components. But with my computer, I can pop open the hood and do anything I want. The hardware manufacturer didn’t restrict my access to the underlying components, and I’m glad he didn’t. The thing is, when I open the computer case, I know 2 things:

- I might break stuff
- Components inside the computer will probably change when I buy a new one.

This is exactly what encapsulation is trying to prevent. But you know what, I want to have a choice. I want to be able to put a new hard drive or silent fan in there, and yes, I know the risks, and know a new computer probably won’t support them anymore. But as a user, it’s my responsibility to make the correct decisions for solving my problems.

So what would happen when the hardware manufacturer did use encapsulation. Well, then he would make it extremely difficult for you to open the case, and anytime you want something changed you need to go back to the shop.

Encapsulation restricts access to implementation details. While I’m not saying you should access implementation details, sometimes it might be handy to do so. With hardware I’m glad they don’t restrict me opening up the hood, so why would I like it in software?

### Abstraction instead of Encapsulation

One definition of abstraction states: ‘the act of considering something as a general quality or characteristic, apart from concrete realities, specific objects, or actual instances.’. In programming terms this means that you provide an interface on top of an implementation, but the user only needs to know the interface (abstraction), and not care about the implementation details.

The difference with encapsulation is that when the user wants to, he can still access the underlying details.

Most hardware uses abstraction instead of encapsulation. They provide an interface that’s not likely to change, but still allow “power users” to pop open the hood and access the implementation.

When using abstraction instead of encapsulation, the user can clearly see the interface, and use it in the same manner as with encapsulation. Users are encouraged to use the public interface, but are not restricted to it. When only using the interface, abstraction has the same benefits of encapsulation. But when needed he can also access the implementation behind it. And because of the clear distinction between interface and implementation, he is aware of the risks involved (ie breaking things and future incompatibility).

### A real world programming example

Let me show you how this might work in the real world of programming. Suppose I’m writing an application that uses a multiplatform GUI library. Multiplatform libraries are great because they make porting really easy. Their public interface is the same across platforms, and so the method calls don’t need to be adapted when switching platforms.

Now suppose the Windows users of our application are requesting a certain feature. That features is not supported by the GUI library, but it is available in the underlying Windows implementation of that library (because MFC supports it for example).

At that point you must take a decision: If you respect encapsulation, you are limited to the following things:

- Implement it yourself on top of the GUI library, but this could mean rewriting a whole GUI control yourself (duplicating both the code of the GUI control, and the code of the MFC feature you want).
- Contact the GUI library vendor to make it available in their public interface, but this also means they have to implement it themselves on all non-Windows platforms. In other words, you won’t have it available soon.
- Switch your windows code over to a Windows specific GUI library. This will cost you some serious time, money and headaces.

What if you would drop encapsulation and use abstraction? Well, in that case you still have the options above, but also an extra one. You’re able to access implemenation details, but then you will have to consider the risks:

- Accessing it is risky for breaking other parts of the GUI Library
- Updates of that library might change the way they use MFC, so you will have to double check it every time you upgrade
- Probably no official support for that from the Library Vendor

The thing is, by using abstraction instead of encapsulation, you do have a choice whether the benefits outweigh the risks. And in this case, that’s probably correct. But remember, I’m not encouraging anyone to use implementation details, but in specific cases, it might be the best solution.

### How I do it

Because Python doesn’t support encapsulation, I don’t have to do anything specific to use abstraction instead of encapsulation. I follow the conventions of putting underscores in front of methods and members, to make the distinction clear between interface and implementation. My users should only use my public interfaces, but if they really need to, they can ‘pop open the hood’ pretty easily.

In more traditional object oriented languages, I use ‘public’ for my public interface, and ‘protected’ for my implementation details. You probably know the following expression from the ‘Gang of Four’: “Because inheritance exposes a subclass to details of its parent’s implementation, it’s often said that ‘inheritance breaks encapsulation'”. That last part is exaclty what I need for my abstraction :). My users use the public interface, but if they really want to, they can access all implementation details by deriving their own version from it.

This also speeds up my development, because I don’t have to break my head over whether I should use private, package-private, protected or public. I use public for my interface, and protected for implementation details. I love to *Keep It Stupid Simple*.

### Encapsulation is not Security

Sometimes it *is* necessary to protect or hide some data from the user. But in this case we are talking about security, and the worst way to implement security is through Object Oriented encapsulation.

### Conclusion

Depending on implementation details is a bad idea. Therefore you should only use the public interface of a class. But for specific or unforeseen needs, it might be useful to be able to access implementation details. It’s the responsibility of the class to be as useful as possible, and the responsibility of the user to use it in a professional manner. Don’t treat your users like idiots, but treat them like professionals who make use of your class the best way possible, to solve their specific problems. If they to need access the implementation details, they probably have a good reason to do so, because else they wouldn’t. So don’t treat them like idiots by using encapsulation.

Koen Witters

## 10 Comments

## Ed Kirwan · April 11, 2010 at 04:12

Hi, Koen,

Thank you for your well-written and thoughtful article; it was most interesting and raises an important question.

I hope you don’t mind if I disagree with you on two points.

I largely agree with your definition of encapsulation, though I usually adhere to the International Organization for Standardization’s definition, whereby encapsulation is defined as being, “The property that the information contained in an object is accessible only through interactions at the interfaces supported by the object.”*

I disagree with you, however, about what encapsulation’s benefit is. You write, “The thought behind the whole idea of encapsulation is that when implementing a class, you protect it against misuse. You make sure that the user can’t break it.”

There are two issues here.

The first concerns ripple effect.

Back in 1974, Messrs Stevens, Myers and Constantine produced a paper in which were written two of the most important, consecutive sentences in the history of computing literature**:

“The fewer and simpler the connections between modules, the easier it is to understand each module without reference to other modules. Minimizing connections between modules also minimizes the paths along which changes and errors can propagate into other parts of the system, thus eliminating disastrous, “Ripple effects,” where changes in one part causes errors in another, necessitating additional changes elsewhere, giving rise to new errors, etc.”

There are two types of source code dependency in a software system: a direct dependency (class A’s calling a method on class B realizes a direct dependency from A to B) and an indirect dependency (if class A calls a method on class B, and class B calls a method on class C, then A has an indirect dependency on class C).

When a change is made to a class, that there exists a probability that this change may trigger a ripple effect to those classes that depend (either directly or indirectly) on it, that is, if we change class C above then there is a probability that the change will propagate to class A, and there is a probability that the change will propagate to class B.

It can be proved that, given a change to any class X, the probability of this change’s propagation to classes indirectly dependent on class X cannot be greater than the probability of the change’s propagation to classes directly dependent on X. In almost all computer systems, furthermore, the probability of change propagation to indirectly-dependent classes is less that the probability of change propagation to directly-dependent classes.

Sounds obvious, but there it is.

The second issue is more subtle, and concerns potential.

Encapsulation, strange as it sounds, isn’t about the dependencies in a software system.

That is, it isn’t about the actual dependencies in a software system. The actual dependencies in a software system are simply a given. They exist and there’s nothing you can do about them. That they exist is merely evidence that encapsulation was powerless to prevent their existence.

Encapsulation, instead, is about potential dependencies: those dependencies that don’t yet exist in a system. Over these potential dependencies, encapsulation holds enormous sway: encapsulation makes potential dependencies probable or improbable. The point being, of course, that future, actual dependencies are more likely to be a subset of probable potential dependencies than they are to be a subset of the improbable potential dependencies.

Putting these two issues together we arrive at the benefit of encapsulation: encapsulation minimizes the number of potential, direct dependencies. In doing so, it minimizes the number of potential dependencies which carry the highest probability of change propagation. Given, furthermore, that every such potential change propagation is associated potential cost, then encapsulation minimizes the potential cost of ripple effect.

And that’s it.

Encapsulation, as described above, does not entail a means of encapsulation. How you implement your encapsulation is irrelevant, whether you use a compiler-enforced mechanism such as public/private accessors or a non-compiler-enforced mechanism such as leading underscores makes no difference, in theory, to the benefit of encapsulation. Despite the title, your article seems not present a case against encapsulation per se, rather it presents a case against compiler-enforced encapsulation and for non-compiler-enforced encapsulation (please correct me if I’m wrong).

Here, I have find my second disagreement with your writing.

You write of that, “If you ask yourself why this [non-compiler-enforced encapsulation] would be an improvement [over compiler-enforced encapsulation], you probably don’t know that in some rare cases, it is necessary to access the implementation.”

I would argue that you are correct: in rare cases, non-compiler-enforced encapsulation is superior; it lowers the cost of development by reusing some functionality that otherwise would have had to have been designed from scratch; let’s call this the Duplication Reduction case. Being superior in rare cases, however, does not mean that non-compiler-enforced encapsulation is outright superior. We must attempt to evaluate the costs and benefits of non-compiler-enforced encapsulation before we can claim that it is an, “Improvement,” over compiler-enforced encapsulation.

Admitting the superiority of non-compiler-enforced encapsulation in rare cases is admitting at least equivalence with compiler-enforced encapsulation in the overwhelming majority of cases.

Consider, also, those rare cases when a designer incorrectly forms a dependency towards an encapsulated class and that class then changes, incurring a ripple-effect cost that would not have been incurred had compiler-enforced encapsulation been used and the designer had been forced to use the correct class; let’s call this the Inappropriate Dependency case.

The question perhaps boils down to the whether the probability of the Duplication Reduction case outweighs that of the Inappropriate Dependency case, or more particularly, if the cost-saving of the former outweighs the cost-increase of the latter, then non-compiler-enforced encapsulation is superior to compiler-enforced encapsulation. I’d like to show that this hypothesis is false.

We don’t, of course, have such probability figures available, but we can examine how we might expect such probabilities to behave as software systems scale, presuming the systems are well-encapsulated (either compiler-enforced or non-compiler-enforced) to begin with.

We note firstly that using non-compiler-enforced encapsulation does not guarantee that the Duplication Reduction case will be avoided. It is still possible, even in a system of non-compiler-enforced encapsulation, for a designer to simply overlook that some functionality he needs is encapsulated in the platform on which he’s working, causing him to write the same functionality again. There are two ways to prevent this. Either the designer must perform an exhaustive search of all the encapsulated functionality of the platform, or he must perform a random, non-exhaustive search. Both of these strategies fail to scale: for a large software system, the cost of an exhaustive search may quickly outweigh the cost of the duplicate development; and a random search will necessarily prove increasingly unsuccessful as the size of the system grows.

Furthermore, there is a limited subset of successful targets from which a designer may chose to benefit from the Duplication Reduction case: basically, there is a limited number of encapsulated classes which the designer could use instead of reproducing functionality, and this limited subset cannot grow as fast as the system itself grows (otherwise the designer end up with no product himself and just have the system). This successful subset decreases as a proportion of the system’s overall increasing size.

Thus as systems scale it seems the probability of the Duplication Reduction case falls.

On the contrary, as systems scale, the probability of the Inappropriate Dependency case does not seem to fall. Given that the Inappropriate Dependency case is essentially a failure case (in that it costs more money) then the target space from which the unwary designer may chose classes on which to form inappropriate dependencies scales precisely with the system size: as the system’s size increases, so too does the space of available, encapsulated classes towards which costly dependencies may be formed. (Indeed there is a wealth of evidence from poorly encapsulated systems that such inappropriate dependencies lead to Big-Ball-Of-Mud syndrome and hopelessly expensive maintenance cycles.)

So it seems that, for increasingly large systems, there must come a point when the probability of the Duplication Reduction case does not outweigh that of the Inappropriate Dependency case, and thus non-compiler-enforced encapsulation is not an improvement over compiler-enforced encapsulation.

Yours sincerely,

Ed Kirwan.

* “Information technology – Open Distributed Processing,” ISO/IEC 10746, 1998.

** “Structured design,” W. P. Stevens, G. J. Myers, and L. L. Constantine SD 13-2 p. 115ff, 1974.

## fernando trasviña · April 30, 2010 at 15:56

amazing description of the current concerns about software design!

This show that as a community we are all getting smarter and we might not need to be protected, but we are mature enough to take responsibility for our own development practices.

## JJ · June 10, 2010 at 07:50

I just wanted to say that, if Hardware used encapsulation and offered a good interface, you wouldn’t need to open your computer. Instead, you would do Computer->upgrade( Ram( “32GB” ) ) and the computer would do the upgrade for you 😉

PS: Ed’s comment was very interesting. And if you check his website you can see he’s a bit of an “encapsulation nerd” 🙂

## Chris · July 8, 2010 at 02:59

Hey Koen, I do not find your examples convincing at all.

The computer metaphor doesn’t translate all that well into OOP.

Like JJ said, as a class in your code, the computer would provide an upgrade method itself, without the need for you to mess with internals. Another possibility would be to have a helper for upgrading. For example, if a computer object would be created via the builder pattern, the builder might as well be the one to ask for upgrades. No need to get rid of encapsulation.

The GUI example:

This case is similar to one I encounter from time to time in programming forums.

The usual situation where someone asks for help is as follows: There is a BaseClass, and SubClass1 and SubClass2 derive from it.

Now, that someone creates a container for objects of BaseClass, containing both objects of the concrete classes SubClass1 and SubClass2. He then asks, for example, how to iterate over the container’s contents and execute specific actions depending on the concrete subtype.

In summary: Abstracting from the concrete classes, and then asking how to break the abstraction again. This can be solved in clean ways – double dispatch and visitor pattern come to mind, so you’re still fine using encapsulation. However, in my experience, most of the time someone does something like this, his/her concept is faulty somewhere.

Now back to the GUI example. Cross-platform GUI toolkits abstract away from the concrete operating systems. By their nature, they must thus provide the lowest common denominator. Now asking how to access an OS-specific function means “you’re doing it wrong” in my opinion. But as I said, this can be solved without breaking encapsulation.

## Niriel · June 15, 2011 at 12:56

I love that, with Python, I don’t need to write getters and setters if these are dumb. And properties allow me to write them later if I realize I need non-dumb getters and setters after all, without having to change anything but the class itself. Sweet. It just saves me some time.

The article made me think about something… In Python, you can choose to have one or two underscores in front of your variable of method name. Two underscores makes it more annoying than one underscore for the guy who’s trying to access the internals of your class. I’ve never found a use for it. Has anybody ?

## Esailija · August 9, 2013 at 02:48

There is no language I know of where access control is enforced. In Java, C#, C++, PHP, Ruby etc it’s always possible to access private if you want. The only thing they do is to prevent you from doing that by accident.

But you don’t really need complicated mechanics to prevent those “accidents”. Underscore prefix is enough for it.

## DXM · January 14, 2014 at 21:06

I’ve been a C++/C# developer for a long time but for a little more than a year Python has been my primary development language. I came across this article because the whole thing of encapsulation was bugging me. In fact, before I read this article, I shared a lot of views with Ed Kirwan who left a reply higher up the page. Why is it so ingrained into C++ developers to make as much as possible hidden, yet Python takes the opposite view? But everything you wrote makes a lot of sense. Just like in C++, Python fully supports the notion of “here’s a concise, simple to use, public interface” and that really is the key basic building block in any language. If consumer crosses that boundary, that’s consumers problem but it’s also consumer’s choice.

I think the only gripe I have left is that there’s still no convention to mark members as truly internal vs. accessible to deriving classes (i.e. private vs protected). In the past, I used double underscore but seems a lot of people frown on that as well, so now everything non-public gets a single underscore which still feels a bit weird. I guess that’s where docstrings come in.

## massau · June 3, 2016 at 11:34

after reading this and the first comment it seems that encapsulation is necessary to avoid people from ‘misusing’ and relaying on implementation details. But it makes a strong case for the usage of a protected field.

The public field should only contain functions and trivial data.

the private field should contain most internal functions and all non specific data for example if you have an image class the image should be protected and the load function should be protected.

The os dependent and environment specific things should be private.

A in most C++ programs they use ether private or public but almost never protected.

So they end up making a getter that returns a reference to an internal member variable (and thus creating a ball of mud). This function is actually still useful for the inherited class. but if you do that then you could as well make the variable protected.

Since an inherited class tend to know about the implementation details of the super class to extend it. Or they hack some way to get to the data one way or the other.

I would really like it if classes had another modifier in there encapsulation level.

It would be useful to have a “const public” and “const protected” identifier to the data members. This would allow you to read the data members but not to write.

For the image example it could be useful to do operations on the image and then read the result without a getter. Or you could easily create an other observer class that looks at the image. It would be a bit like a window into a class thus making it possible to have data as an interface.

## Tim · May 28, 2019 at 10:07

To readers.

This sounds like an attempt of a code nerd who like slapping few lines of code together to get to software architecture and industry standards level. Pretty pathetic and empty.

Summary of the whole article.

Python doesn’t have some inbuilt feature which other languages have. Doesn’t matter which one exactly. And, somehow, this is a good thing deserving a fully fledged article.

## Jo · March 10, 2020 at 18:12

You almost had me on the “encapsulation isn’t needed” bandwagon, until you tried to make it analogous to a personal computer. If computer systems were only (analogously) as small a PC. your analogy would make sense. But instead of a PC, use a a vast network of interconnect CNC machines and you’d be fired from your job. At my work, access to modifying a machine’s underlying mechanics/controls/software is tightly regulated. One mess up can cost millions of dollars and the possible replacement of part of or the whole of a machine. Before access was tightly controlled a change by a mechanic or technician caused unknown degradation. It becomes known only when the system crashed and the fault had to be reconstructed. In terms of your analogy, encapsulation isn’t needed in small programs, but imperative in large scale applications.