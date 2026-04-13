---
title: The Ronimo coding style guide
url: http://joostdevblog.blogspot.com/2017/07/the-ronimo-coding-style-guide.html
author: Joost van Dongen
published: '2017-07-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[coding methodology](http://joostdevblog.blogspot.nl/2017/07/the-ronimo-coding-methodology.html)that we use at

[Ronimo](http://www.ronimo-games.com/), which describes our workflow. This week we'll have a look at what our actual code looks like, which is defined in our

*coding style guide*. The idea behind our style guide is that if all code is formatted in a similar manner then it's easier to read and edit each other's code. For example, reading a different bracing style or naming convention usually takes some getting used to, and we avoid that altogether by having a strict style guide that all programmers at Ronimo must follow.

![](../../assets/816b6e04041a8cd8.jpg)

I haven't seen a whole lot of style guides from other companies, but from what I've heard our style guide is quite a lot stricter than what's common elsewhere. I'm not sure whether that's true, but I can totally imagine it is since I'm known for being precise (sometimes maybe overly much). Our style guide isn't set in stone though: there's an exception to every rule. If our style guide really doesn't make sense in a particular situation, then it's okay if a coder ignores it somewhere. Just as long as there's a good reason for it.

Some of the choices in this document are quite arbitrary. Sometimes alternatives would have been equally good, but without clear choices you can't have similar formatting for all programmers. This is especially true for bracing style. I know that this is a heated subject and while I have a clear preference, good arguments can be made for alternative bracing styles. (Still, it would have been nice if advocates of the other major style wouldn't have called it the One True Bracing Style... ;) )

A key element in our style guide is that I want code to read like English wherever possible. Variable and function names should be descriptive and only the most commonly known abbreviations are allowed. Brevity isn't a concern of mine, readability is.

Not all points in our style guide are about formatting though. Others are about actual language constructions. C++ is a rich language with an enormous amount of possibilities, but quite a few are too confusing or have too much risk of bugs to actually use. For example, nesting ternary operators is totally possible in C++, but the result is rarely readable so we disallow it altogether.

![](../../assets/9153691e2600c063.gif)

Our style guide also contains some rules that are intended to make cross platform development easy. On consoles you usually can't choose your compiler, so you have to work with whatever Nintendo, Sony or Microsoft have chosen, including the limitations of their compilers. We've researched what features of C++ each supports and have forbidden some of the newer C++ constructions that we think might not work on one of the consoles. Since we're not currently actively developing on some of the consoles we went by documentation only though, but I'd rather be too strict here than too lenient.

Another thing you can see in our style guide is my dislike for complex language constructions. C++ allows for some highly impressive stuff, especially using templates and macros. While I appreciate that these tricks can sometimes be really useful, I generally dislike them whenever they become too difficult to read. In the rare cases where these tricks are truly needed they are allowed, but usually I prefer if complex language constructions are avoided.

![](../../assets/a0d445d950a3f2f9.gif)

One particularly hotly debated point in coding styles is whether to mark class member variables. If the Car class has a float speed, do we call that speed, mSpeed, _speed or something else still? I've chosen to simply call this speed. Here too the reason is that I want code to be as similar to English as possible. The more prefixes and underscores there are, the further it moves away from natural language and the more difficult it becomes to just read code and understand it like you would text.

However, there's a good reason many programmers mark their member variables: it's very important in code to know whether a variable is a class member, a function parameter or a local variable. This argument is true, but I think we have that covered elsewhere: our style guide contains limitations on how long a class or function can be. If a function is short and fits on one screen, then it's easy to immediately see where variables are coming from. I think if classes and functions are short enough, then markers for member variables aren't really needed.

Note by the way that the rule for how long functions and classes can be is the one broken most internally. Sometimes it's just really difficult to split a class or function in a neat way. In the end the goal of our style guide is to produce clear code, not to hinder that by forcing clumsy splits. Still, there's real skill in figuring out how to neatly split classes and functions into smaller, more maintainable units, so if you're not super experienced yet then more often than not a neat split is possible and you just don't see it. In my opinion the ideal size of a class is anywhere between 200 and 400 lines, but a rule that strict isn't feasible so what's listed in the style guide is more lenient.

Now that I've discussed the reasoning behind our coding style guide, let's finally have a look at what it's actually like!

## The Ronimo Coding Style GuideThere is an exception to every rule. However, keep to these rules as much as possible to maintain a constant layout and style for all the code. A lot of this is taste and a constant code layout requires setting aside one's own taste and keeping to these rules. Once used to it, it's easier to read such code. When working in another language than C++, try to keep as close as possible to the C++ coding standard, but of course within reason. There are some specific notes on C# at the bottom as well. ## C++
## C#
|

That's it, our coding style guide! ^_^ While I imagine you might disagree with a bunch of the specific rules, I think it's useful for any company that does programming to have some form of a style guide. Our style guide can be a good starting point for creating your own. I'm quite curious: what's the style guide like at your own company and how do you like it? Do you have one at all?

nice post, lots of good tips.


ReplyDeleteAbout static members. What if your class/lib is header only (e.g. templated classes often are).

Do you permit this trick for getting static member (it uses local static variable)?

class Bla {

public:

static Stuff& getStuff() {

static Stuff stuff;

return stuff;

}

};

That's a very particular trick, not something that would be commonly used I think. We do allow tricks like that when needed though, but they need to be really really needed since it's also kind of dirty and obscure. Really useful in some cases though. :)

DeleteI've used this trick to formalize singleton access to a class (which I use a lot of).











Deletehttps://github.com/vovoid/vsxu/blob/master/lib/common/include/tools/vsx_singleton.h

Is used like this:

class shot_manager

: public vsx::singleton

{

vsx_nw_vector< shot > shots;

public:

...

};

--

The use case looks like:

shot_manager::get()->is_a_shot_within_rect(my_rect);

There is also the managed one (to control order of creation / destruction which is problematic with static variables, especially in games):

https://github.com/vovoid/vsxu/blob/master/lib/common/include/tools/vsx_managed_singleton.h

you should investigate clang-format for 1/3 of these rules.

ReplyDelete"In constructors, prefer using initialiser lists over setting variables in the body of the constructor. Each initialisation in the initialiser list gets its own line. Make sure variables in the initialiser list are in the same order as in the class definition in the .h-file."



ReplyDeleteThis is not as relevant if you have access to C++11. Then just go:

class foo

{

public:

size_t bar = 0;

...

};

For me at least, not adding things to the initialiser list is my most common error. With C++11 this way I can get rid of most default constructors.

That's a neat feature! I actually didn't even know that one. :)

DeleteYou didn't like it, but initializer lists can go there as well. Useful for some things like color, where you have a fixed number of member variables...



Deletevsx_color my_color = {1.0, 0.5, 0.5, 1.0};

That particular feature is disallowed because one of the console compilers that need to be able to run our code list it as unsupported.

DeleteIt's always interesting to see the code style guide of other companies.

ReplyDeleteBecause I've help write the style guide for Two Tribes I’ve thought about this topic a lot, and I had some feedback on the Ronimo style guide.

So much in fact, that it was too long for the comments here.

I’ve updated my reply here: https://pastebin.com/9fqzaFaw

I agree that this style guide is a mix of things intended for juniors and things that are also relevant to seniors. Even for a senior it's not a problem to read through this once though, so I don't see much use for us in actually splitting it up. Also, some of the things that might seem for juniors are things where seniors might disagree, so I do want them to read them because I am pretty strict on these.




DeleteThe lack of reasons for a lot of the points in this document is to keep it somewhat brief. Good explanations for all the points would at least double the length of the document. When a new coder joins the team I go through this document together with them and give verbal explanations for a lot of these things, so they do get the explanations.

Operator overloading and "so many other things" are mostly not mentioned because the document isn't intended to describe the entire language. We use operator overloading where applicable and we don't have any particular rules for it so it's not in the document.

I won't go into full detail on the other things you mentioned, but it was really interesting to read your reply (although I disagree with half of it ;) ). Thanks for giving such an extensive reply! :)

I don’t understand why it would be a problem to have a longer document. With the right formatting it should be possible to read through just the guidelines while skipping the reasoning, if that’s what the reader wants. Having the reasoning in the document itself also scales way better in bigger teams. I would also not expect anyone who’s just starting out to remember all of that when you’re going through the guidelines with them. And finally it looks less like a “because I told you so” list and could invite feedback based on new insight that might change things for the better. (e.g. “We don’t do this because compiler X doesn’t support it” could change when compiler X suddenly does support it.)


DeleteSpeaking of inviting feedback, I would love to hear what you disagree with. At Two Tribes I always said that nothing in the Guide is set in stone and I tried to encourage feedback from everyone. Especially interns might be shy about such things otherwise.

nice

ReplyDelete