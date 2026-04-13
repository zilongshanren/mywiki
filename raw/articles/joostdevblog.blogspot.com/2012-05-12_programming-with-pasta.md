---
title: Programming with pasta
url: http://joostdevblog.blogspot.com/2012/05/programming-with-pasta.html
author: Joost van Dongen
published: '2012-05-12'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Note that I realise that the food metaphors might be slightly lame, but the point of this post is that I think it is important to think about the implications of various structures and methods of programming, and this blogpost is basically just an analysis of some pitfalls and approaches.

Most programmers know the term

*spaghetti code*. It refers to a larger code base that is so intertwined, that is it impossible to know how the rest of the code reacts when you change something somewhere. Every line of code might be referencing almost any variable anywhere and maintaining the code becomes all but impossible, because the risk of introducing bugs elsewhere is too great.

![](../../assets/8e77f5160baf3755.jpg)

The common solution to spaghetti code is also well known:

*object oriented programming*. By using classes and making them as self-contained as possible, you can make sure that as long as the class behaves the same to the outside world, it doesn't matter if you change how it works internally. Each class is a world of its own. Of course, in practice this is more an ideal than reality, because during development classes often also need to change how they behave towards the outside world. Still, object oriented programming can help a lot to separate large code bases into smaller, more maintainable chunks.

However, there is also the other end of the spectrum. Object oriented programming can be taken too far. Let's have a look at an example from a real part of

[Awesomenauts](http://www.awesomenauts.com). In Awesomenauts, when the player dies, the music fades out and decreases in pitch. The real situation is a bit more complex, but to keep this post readable, I'm simplifying it a bit. An intern was to implement the logic for the music. So he came up with something like this set of classes:

![](../../assets/a426f47acb60af93.gif)

However, due to his internship ending, he didn't finish this set of code and I had to complete it. Problem is, that these are so many classes for such a simple task, that I almost got lost in all all the class management code and could hardly make any sense of what was working and what was not. Because the problem was so simple, I decided to just throw away his code altogether and write

*one*simple class instead. It looks like this (again, simplified for clarity):

![](../../assets/29db8a4cf7873e24.gif)

As you can see, this is actually really simple and understandable. No need for all these classes here. It became a little bit more complicated when shuffle and killing spree music were added, but still, the MusicManager class is short and understandable.

So what the intern did, is an example of

*lasagne coding*: too many layers. Especially programmers who are relatively new to object oriented programming often overreact to its benefits by creating way too many classes. I belive there is something like an

*ideal class size*. This varies per class, but I think in general classes above 500 lines are almost always too long, causing spaghetti within the class, while classes beneath 50 lines are quite often too small and thus part of lasagne. Not always of course: some classes are perfectly fine for doing one clear thing in a small number of lines.

![](../../assets/8f939a134e92dbac.jpg)

Lasagne coding is of course a common term, but I recently discovered that few programmers are aware of this name. Most coders I meet do know that having too many classes is a bad thing, of course, but I think it helps communication and thinking to also have terms for good and bad practices.

To finish this post, I'd like to mention two more food metaphors.

*Pizza code*and

*ravioli code*. Unlike spaghetti code and lasagne code, these are terms I just made up on the spot because I like to talk about food. The concepts are real, though.

When programming large projects, interrelations between classes often become more and more complex. Awesomenauts has around 1,200 classes, which to me is quite a lot. Even if all of those classes are proper self-contained units, adding or changing things can still become very complex, as any number of classes might be using any number of other classes. If care is not taken, the class diagram starts to look like a pizza: a big plate of dough with all kinds of stuff randomly thrown on it and no idea what goes where or why. All the classes just happen to be there.

![](../../assets/fefb5c590c61045a.jpg)

So to make the class diagram more manageable, I think it is better to make it resemble

*ravioli*. Ravioli are little dough wraps with good stuff in them. They are closed off and you put the entire thing in your mouth at once and it tastes good. I'd like my code to be like that. Groups of classes work together, but can be represented to the rest of the code base as a whole. Not all of them need to even be usable outside the group at all.

![](../../assets/f440aecdf45d5377.jpg)

The nicest example of this in Awesomenauts is the input system. This consists of some two dozen classes that together handle input from devices like WiiMotes, keyboards, mice and Xbox 360 controllers. It also handles this for five different platforms (Playstation 3, Xbox 360, Wii, PC, Mac). To the outside, however, only one of the twenty classes is accessible: the InputManager class. All other code that wants to know whether a button is pressed on some device just asks this to simple functions like

*InputManager::getIsMouseButtonDown()*. InputManager is the dough and the two dozen classes that actually handle the hardware on all the various platforms are hidden inside the ravioli ball. If all those 1,200 classes in Awesomenauts were this clearly grouped, you would get a much more manageable 50 groups to understand the relations between, instead of 1,200 separate classes.

This concludes my food series for now. Of course, none of the concepts above are revolutionary, but I think it is really important for

*any*programmer to think about what he thinks is good programming and what is not. In my opinion programmers who never stop coding to take some time to think about whether what they used was a good or a bad method, will never become really good. This post just outlines some of my own thoughts on the matter, and I hope they help you define Good Code (tm) for yourself.

I agree with the greater deal of the char array here, but this last part...?




ReplyDelete" In my opinion programmers who never stop to think about whether what they used was a good or bad method, will never become really pro. "

What the?

1. How do you know, are you pro?

2. So, at some point you must stop thinking otherwise you cannot get pro, whut?

3. Define pro.

Euhm, I guess you misread that one? "Stop to think" is not the same as "stop thinking". "Stop to think" means that one stops working for a moment, and starts to think about what one is doing. :)

DeleteI added a couple of words to that sentence to make it clearer what I meant and avoid confusion.

DeleteThis post brought a big smile to my face. Lasagna code? Brilliant. Can't wait to have to explain the concept to someone xD

ReplyDeleteThe best part is that I didn't even make the term "lasagne code" up myself! :D

DeleteIt makes for a great punchline. Observe:




Delete[...Mention lasagne code...]

- What's that?

- Too many layers. *ba dum tish*

Almost as good as the joke of the mummy!

DeleteLol Ted, how on earth did you arrive here _now_, 9 years later?


DeleteNote that I still regularly tell the joke of the mummy, and the response (once they get the joke) is still always a sigh. :D

Hahaha I figured you'd be surprised. I searched for spaghetti code and this was one of the first hits!

DeleteNice! I also searched for that and I also got an article that mentioned ravioli code as a thing. It didn't mention my article, but I'm pretty sure that that term wasn't in use yet when I wrote this. Maybe I influenced that. :)

DeleteDid you just announce Awesomenauts for PC and Wii? :p


ReplyDeleteRavioli code is of course http://en.wikipedia.org/wiki/Separation_of_concerns, but it sounds tastier :D

Nope, I just announced that Awesomenauts uses the same core engine as Swords & Soldiers. :)

DeleteYou had me at your mouth watering description ravioli code. I just had lunch but would eat again. Also very nice article - I think analogies like ravioli are nice because it's hard to explain to people "too many objects! too many layers!" IMO university teaching (and industry) is still too obsessed with OO so most students don't really learn that there should be a sensible balance.

ReplyDeleteI find that I usually move from system to system within the same code base. You are asked to include a particle effect, so you write a class that can produce an effect. Its pretty small and simple, but then it also not very re-usable.




ReplyDeleteThen you find out: I can use more particle systems in other places, so you start to split up the particle code into more classes so you can have more flexibility, creating more of a lasagna model. Then when you use a lot of that copy pasted all over your game you suddenly realize : I should have made a manager class for this.. At this point it probably looks like the pizza model.

And then I end up with the ravioli model, after making the manager.

Problem is, when you prototype a game and design it as you go, there is no real way to know up front how much a certain piece of code will be reused or how large it will become, ie what model to use.

From what I read, your music manager is accessing the character->IsDead() method... Don't you think that the music manager should probably be at a lower level, agnostic of high level stuff like the character? This sounds like an odd dependency to me. But maybe this was just a simplified example to illustrate your point...

ReplyDeleteThis MusicManager manages music from a gameplay perspective. It decides what to play based on the game situation. So it makes sense that it knows about characters and things like that.


DeleteThe kind of manager that should be more outside the game is our SoundManager, which is an engine class that handles playing sound on specific platforms. The SoundManager is completely agnostic from the actual game.