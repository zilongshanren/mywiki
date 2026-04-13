---
title: ActionScript 3.0 Event Listener Delegates | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/07/actionscript-3-0-event-listener-delegates/
author: Allen Chou
published: '2012-07-16'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

After some research on [C++ delegates](http://allenchou.net/2012/04/easy-c-delegates/), I’ve also tried to build delegates in ActionScript 3.0. It’s extremely easy compared to C++, which is not a surprise at all!

Conveniently, when you refer to a method through an object reference with the “dot (.) syntax”, the evaluated

object reference already acts somewhat like a delegate, in that the value used for the [Function](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/Function.html)`this`

keyword is stored within the `Function`

object. This saves us a lot of work!

We can make use of this convenient feature to create “event listener delegates” to pass in extra arguments to listener functions without having to use multiple listeners or using the [Dictionary](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/utils/Dictionary.html) class.

Here I’ll show you how we would solve the same problem using multiple listeners, dictionaries, and finally, event listener delegates.


### The Multiple-Listener Approach

Suppose we have three display objects called `obj1`

, `obj2`

, and `obj3`

. We’d like to trace out 1, 2, and 3, when we click the display objects, respectively.

This is the most naive and straightforward approach. You’d just create a different listener function for each of the display object.

function listener1(e:Event):void { trace(1); } function listener2(e:Event):void { trace(2); } function listener3(e:Event):void { trace(3); } obj1.addEventListener(MouseEvent.CLICK, listener1); obj2.addEventListener(MouseEvent.CLICK, listener2); obj3.addEventListener(MouseEvent.CLICK, listener3);

So what’s wrong with this approach? Imagine you have 10000 objects and you’re adding listeners using a loop and the [associative array syntax](http://www.adobe.com/devnet/actionscript/learning/as3-fundamentals/associative-arrays.html):

for (var i:int = 0; i < 10000; ++i) { this["obj" + i].addEventListener ( MouseEvent.CLICK, this["listener" + i] ); }

In order for this code to work, you’ll have to declare 10000 different functions!

### The Dictionary Approach

It’s clear that we could solve the problem if we can **associate** a value with each display object. That’s it! We can use the `Dictionary`

class to do that!

var mapping:Dictionary = new Dictionary(); function listener(e:Event):void { //look up our dispatcher trace(mapping[e.target]); } for (var i:int = 0; i < 10000; ++i) { var obj:DisplayObject = this["obj" + i]; //associate the display object with an integer mapping[obj] = i; //just use the only listener and we'll be fine obj.addEventListener(MouseEvent.CLICK, listener); }

There we have it. We no longer need to declare 10000 different listeners. But the code is still not perfect: dictionaries use the [binary search algorithm](http://en.wikipedia.org/wiki/Binary_search_algorithm) to look up mappings, which is not a [constant time](http://en.wikipedia.org/wiki/Time_complexity#Constant_time) operation. In other words, as the number of dictionary entries increases, it takes longer to look up each entry.

This leads to our final solution to this problem, delegates.

### The Delegate Approach

A delegate is an object that acts as an indirect agent between the function being invoked (callee) and the code that invokes the function (caller). We can design a `Delegate`

class that contains a `Fucntion`

reference to the callee and a custom array of arguments to be passed when invoking the callee. In this case, the callee is the `trace`

function and the arguments are the different integers.

class Delegate { private var func_:Function; private var args_:Array; public function Delegate(func:Function, ...args) { func_= func; args_= args; } public function invoke(e:Event):void { func_.apply(null, args_); } }

This gives us the following client code:

for (var i:int = 0; i < 10000; ++i) { this["obj" + i].addEventListener ( MouseEvent.CLICK, new Delegate(trace, i).invoke ); }

We basically “wrap” a `Function`

object reference and the arguments into a `Delegate`

object, and use the delegate’s `invoke`

method as the “indirect agent”. This approach is constant-time, because each call to the delegate involves exactly one indirect function call.

To make the code even cleaner (getting rid of “`.invoke`

” in the code), we can create a helper function:

function delegate(func:Function, ...params):Function { return new Delegate(func, params).invoke; }

This gives us our final client code:

for (var i:int = 0; i < 10000; ++i) { this["obj" + i].addEventListener ( MouseEvent.CLICK, delegate(trace, i) ); }

That’s it! Way simpler than C++ delegates 🙂

Hi

It was very usful in AS2 🙂

I’d use something like that:

public static function create(o:Object, f:Function, … args):Function

{

return function():* { return f.apply(o, args); };

}

super.stage.addEventListener(MouseEvent.CLICK, Delegate.create(null, trace, “asdf”));

super.stage.addEventListener(MouseEvent.CLICK, Delegate.create(null, trace, “qwe”));

沒有讚可以按

推文也OK啊XD