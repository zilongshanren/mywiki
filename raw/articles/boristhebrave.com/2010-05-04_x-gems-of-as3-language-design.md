---
title: X Gems of AS3 Language Design
url: https://www.boristhebrave.com/2010/05/04/x-gems-of-as3-language-design/
author: Boris
published: '2010-05-04'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Ok, so AS3 has its fair share of problems. It is slow, it has next to no support for templates/generics and somewhat sparse standard library. And yet still I love using it.

Why? It has managed to pull together some of the rarer features that I think every language should have. Language designers, take note of the following.



## Easy to parse

**Better known in:** Pascal, Ada

**Worst offenders:** C++, Java

A lot of languages fall into the C trap of declaring variables, function parameters, members, like this:

Type myInstance;

This is a *horrible* convention. When the parser comes across the “Type” token, it doesn’t know what it is until later, and in some languages, needs higher level semantic information to decide. It gets even worse when declaring functions. It is also not so readable imho. AS3’s

var myInstance:Type;

is much simpler.

Same thing goes for templates, using `Template<templateArg>` is a recipe for parsing nightmares, as it is just to easy for those angle brackets to be comparison operators. The addition of a dot, `Template.<templateArg>`, and it is suddenly easy. (though still not perfect)

## Modern Primitives

**Better known in:** Javascript

**Worst offender:** Lua

AS3 has regexps and XML as basic primitives. These are so commonly used in languages, and yet working with them is frequently cumbersome. Regexps require escaping, and often don’t mesh with the standard library, while XML becomes huge fests of method calls and nested loops, or (*shudder*), visitor patterns.

AS3 has regex literals, which can slot into most string manipulation functions, XML literals that can be escaped back to AS3 code to embed variables and the like, and most importantly, [E4X](http://en.wikipedia.org/wiki/E4x), which I cannot do justice in a quick synopsis.

First class functions and lambdas are also a needed primitive, but I think most language designers have caught onto that one now.

Actions speak louder than louder than words, so here is some AS3 versus Strawmania, a language I just made up for comparison. It’s actually being generous, there are languages out that that fail far harder at these toy examples.

| Actionscript | Strawmania |
function upper(c){return c.toUpperCase();} "the quick brown fox".replace(/\b./g, upper); // The Quick Brown Fox |
text = "the quick brown fox"; atStart = true; for(i in 0...text.length()) { if(atStart) text[i] = text[i].toUpperCase(); atStart = text[i]==" "; } // The Quick Brown Fox |
function toXML(circle) { var x = <circle radius={circle.radius}> <color> {circle.color.toString()} </color> </circle>; } |
function toXML(circle) { var x = XML.makeElement("circle"); x.setAttribute("radius", circle.radius); var color = XML.makeElement("color"); color.appendChild(XML.makeText( circle.color.toString()); x.appendChild(color); } |
var maleMiddleNamesStartingWithJ = familyTree..person.(@gender == 'M'). (middleName.toString().match(/^J/)); |
results = []; for(var p in familyTree.descendantsByName("person")) { if(p.getAttribute("gender")!="M") continue; var middleName = p.getElement("middleName").text(); if(middleName[0]!="J") continue; results.push(p); } |

AS3 actually takes XML integration one step further that all members of a class are associated with a namespace, which is cool, but not imho useful enough to merit this list.

## Implicit method binding

**Better known in:** Python?

**Worst offender:** C++98

This one is so simple I don’t know why more languages don’t do it. If you get a method from a instance of a class, it is implicitly bound to that instance.

var a:Array = [1,2,3]; var f:Function = a.join; f(","); // 1,2,3 f(" "); // 1 2 3

This turns out to be vitally useful for event systems. Want to connect button A to oojamaflip B?

buttonA.addEventListener(Event.PRESS, oojamaflip.flipOut); // Later... buttonA.removeEventListener(Event.PRESS, oojamaflip.flipOut);

No bind statements, no lambdas, just what you need. Note how I didn’t need store a variable during the add phase that I needed to pass to the remove phase.

## Optional Static Typing

**Better known in:** Implicitly typed languages

**Worst offender:** Java

AS3 (& [haXe](http://haxe.org)) seems to be more or less unique in this feature. Variables etc can be either typed or untyped, with casts added for you beneath the hood. I really like the way you can write something quickly, with that untyped scripting language feel, and then neaten it up by adding static typing, to enhance readability, code completion and documentation.

Once again, AS3 falls down in practice – I statically type everything for the performance gain, except the areas where you are forced into dynamic typing – mainly when using Function.

## Conclusion

I’m not saying AS3 is an amazing language. I’m not saying your language sucks (though it does – the perfect language has yet to be made). I am saying there are some under-appreciated ideas here, which I hope to see more of in the future. I’m looking at you, Javascript and Python.

## Post Script

I don’t know much about Ecmascript, but I’m guessing that the designers of it are responsible for many if not all of the inovations seen here, so props to them.

Also, sorry if I didn’t represent your language, I appreciate there are many so alien from the “common set” that a lot of the points here are irrelevant. Who needs weak typing when you have Haskell’s all powerful type inference, or regexp literals when you have Scheme’s reader macros?