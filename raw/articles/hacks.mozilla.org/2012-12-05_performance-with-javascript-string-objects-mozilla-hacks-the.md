---
title: Performance with JavaScript String Objects – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/12/performance-with-javascript-string-objects/
author: Panagiotis Tsalaportas
published: '2012-12-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This article aims to take a look at the performance of JavaScript engines towards primitive value Strings and Object Strings. It is a showcase of benchmarks related to the excellent article by Kiro Risk, [The Wrapper Object](http://kiro.me/blog/wrapper_objects.html). Before proceeding, I would suggest visiting Kiro’s page first as an introduction to this topic.

The [ECMAScript 5.1 Language Specification (PDF link)](http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf) states at paragraph 4.3.18 about the String object:

String object member of the Object type that is an instance of the standard built-in String constructor


NOTEA String object is created by using the String constructor in a new expression, supplying a String value as an argument.

The resulting object has an internal property whose value is the String value. A String object can be coerced to a String value

by calling the String constructor as a function (15.5.1).

and David Flanagan’s great book “JavaScript: The Definitive Guide”, very meticulously describes the Wrapper Objects at section 3.6:

Strings are not objects, though, so why do they have properties? Whenever you try to refer to a property of a string s, JavaScript converts the string value to an object as if by calling new String(s). […] Once the property has been resolved, the newly created object is discarded. (

Implementations are not required to actually create and discard this transient object: they must behave as if they do, however.)

It is important to note the text in bold above. Basically, the different ways a new String object is created are implementation specific. As such, an obvious question one could ask is *“since a primitive value String must be coerced to a String Object when trying to access a property, for example str.length, would it be faster if instead we had declared the variable as String Object?”*. In other words, could declaring a variable as a String Object, ie `var str = new String("hello")`

, rather than as a primitive value String, ie `var str = "hello"`

potentially save the JS engine from having to create a new String Object on the fly so as to access its properties?

Those who deal with the implementation of ECMAScript standards to JS engines already know the answer, but it’s worth having a deeper look at the common suggestion *“Do not create numbers or strings using the ‘new’ operator”*.

## Our showcase and objective

For our showcase, we will use mainly Firefox and Chrome; the results, though, would be similar if we chose any other web browser, as we are focusing not on a speed comparison between two different browser engines, but at a speed comparison between two different *versions of the source code* on each browser (one version having a primitive value string, and the other a String Object). In addition, we are interested in how the same cases compare in speed to subsequent versions of the same browser. The first sample of benchmarks was collected on the same machine, and then other machines with a different OS/hardware specs were added in order to validate the speed numbers.

## The scenario

For the benchmarks, the case is rather simple; we declare two string variables, one as a primitive value string and the other as an Object String, both of which have the same value:

```
var strprimitive = "Hello";
var strobject = new String("Hello");
```

and then we perform the same kind of tasks on them. (notice that in the jsperf pages strprimitive = str1, and strobject = str2)

### 1. length property

```
var i = strprimitive.length;
var k = strobject.length;
```

If we assume that during runtime the wrapper object created from the primitive value string **strprimitive**, is treated equally with the object string **strobject** by the JavaScript engine in terms of performance, then we should expect to see the same latency while trying to access each variable’s `length`

property. Yet, as we can see in the following bar chart, accessing the `length`

property is a lot faster on the primitive value string **strprimitive**, than in the object string **strobject**.

Actually, on Chrome 24.0.1285 calling `strprimitive.length`

is **2.5x** faster than calling `strobject.length`

, and on Firefox 17 it is about **2x** faster (but having more operations per second). Consequently, we realize that the corresponding browser JavaScript engines apply some “short paths” to access the length property when dealing with primitive string values, with special code blocks for each case.

In the SpiderMonkey JS engine, for example, the pseudo-code that deals with the “get property” operation looks something like the following:

```
// direct check for the "length" property
if (typeof(value) == "string" && property == "length") {
return StringLength(value);
}
// generalized code form for properties
object = ToObject(value);
return InternalGetProperty(object, property);
```

Thus, when you request a property on a string primitive, and the property name is “length”, the engine immediately just returns its length, avoiding the full property lookup as well as the temporary wrapper object creation. Unless we add a property/method to the String.prototype requesting |this|, like so:

```
String.prototype.getThis = function () { return this; }
console.log("hello".getThis());
```

then no wrapper object will be created when accessing the String.prototype methods, as for example String.prototype.valueOf(). Each JS engine has embedded similar optimizations in order to produce faster results.

### 2. charAt() method

```
var i = strprimitive.charAt(0);
var k = strobject["0"];
```

This benchmark clearly verifies the previous statement, as we can see that getting the value of the first string character in Firefox 20 is substiantially faster in **strprimitive** than in **strobject**, about **x70** times of increased performance. Similar results apply to other browsers as well, though at different speeds. Also, notice the differences between incremental Firefox versions; this is just another indicator of how small code variations can affect the JS engine’s speed for certain runtime calls.

### 3. indexOf() method

```
var i = strprimitive.indexOf("e");
var k = strobject.indexOf("e");
```

Similarly in this case, we can see that the primitive value string **strprimitive** can be used in more operations than **strobject**. In addition, the JS engine differences in sequential browser versions produce a variety of measurements.

### 4. match() method

Since there are similar results here too, to save some space, you can click the source link to view the benchmark.

### 5. replace() method

### 6. toUpperCase() method

### 7. valueOf() method

```
var i = strprimitive.valueOf();
var k = strobject.valueOf();
```

At this point it starts to get more interesting. So, what happens when we try to call the most common method of a string, it’s valueOf()? It seems like most browsers have a mechanism to determine whether it’s a primitive value string or an Object String, thus using a much faster way to get its value; surprizingly enough Firefox versions up to v20, seem to favour the Object String method call of **strobject**, with a **7x** increased speed.

It’s also worth mentioning that Chrome 22.0.1229 seems to have favoured too the Object String, while in version 23.0.1271 a new way to get the content of primitive value strings has been implemented.

A simpler way to run this benchmark in your browser’s console is described in the comment of the jsperf page.

### 8. Adding two strings

```
var i = strprimitive + " there";
var k = strobject + " there";
```

Let’s now try and add the two strings with a primitive value string. As the chart shows, both Firefox and Chrome present a **2.8x** and **2x** increased speed in favour of **strprimitive**, as compared with adding the Object string **strobject** with another string value.

### 9. Adding two strings with valueOf()

```
var i = strprimitive.valueOf() + " there";
var k = strobject.valueOf() + " there";
```

Here we can see again that Firefox favours the `strobject.valueOf()`

, since for `strprimitive.valueOf()`

it moves up the inheritance tree and consequently creates a new wapper object for **strprimitive**. The effect this chained way of events has on the performance can also be seen in the next case.

### 10. for-in wrapper object

```
var i = "";
for (var temp in strprimitive) { i += strprimitive[temp]; }
var k = "";
for (var temp in strobject) { k += strobject[temp]; }
```

This benchmark will incrementally construct the string’s value through a loop to another variable. In the for-in loop, the expression to be evaluated is normally an object, but if the expression is a primitive value, then this value gets coerced to its equivalent wrapper object. Of course, this is not a recommended method to get the value of a string, but it is one of the many ways a wrapper object can be created, and thus it is worth mentioning.

As expected, Chrome seems to favour the primitive value string **strprimitive**, while Firefox and Safari seem to favour the object string **strobject**. In case this seems much typical, let’s move on the last benchmark.

### 11. Adding two strings with an Object String

```
var str3 = new String(" there");
var i = strprimitive + str3;
var k = strobject + str3;
```

In the previous examples, we have seen that Firefox versions offer better performance if our initial string is an Object String, like **strobject**, and thus it would be seem normal to expect the same when adding **strobject** with another object string, which is basically the same thing. It is worth noticing, though, that when adding a string with an Object String, it’s actually quite *faster* in Firefox if we use **strprimitive** instead of **strobject**. This proves once more how source code variations, like a patch to a bug, lead to different benchmark numbers.

## Conclusion

Based on the benchmarks described above, we have seen a number of ways about how subtle differences in our string declarations can produce a series of different performance results. It is recommended that you continue to declare your string variables as you normally do, unless there is a very specific reason for you to create instances of the String Object. Also, note that a browser’s overall performance, particularly when dealing with the DOM, is not only based on the page’s JS performance; there is a lot more in a browser than its JS engine.

Feedback comments are much appreciated. Thanks :-)

## About Panagiotis Tsalaportas

Panagiotis is a Mozilla community member, and contributor to the Mozilla Developer Network and Firefox.

## 31 comments

Nicholas C. ZakasDecember 5th, 2012 at 15:26Panagiotis TsalaportasDecember 6th, 2012 at 08:33Felipe N. MouraDecember 5th, 2012 at 15:33Panagiotis TsalaportasDecember 6th, 2012 at 08:17Daniel LewisDecember 5th, 2012 at 18:13Panagiotis TsalaportasDecember 6th, 2012 at 08:31Dave HermanDecember 5th, 2012 at 23:32Karel JáraDecember 6th, 2012 at 03:23Panagiotis TsalaportasDecember 6th, 2012 at 08:22Alberto ArenaDecember 6th, 2012 at 01:59Panagiotis TsalaportasDecember 6th, 2012 at 08:23Vyacheslav EgorovDecember 6th, 2012 at 02:42Panagiotis TsalaportasDecember 6th, 2012 at 08:25Vyacheslav EgorovDecember 16th, 2012 at 10:41Panagiotis TsalaportasDecember 16th, 2012 at 14:54Vyacheslav EgorovDecember 16th, 2012 at 15:07Arun DavidDecember 6th, 2012 at 03:47Panagiotis TsalaportasDecember 6th, 2012 at 08:26Tomas CorralDecember 6th, 2012 at 06:18Panagiotis TsalaportasDecember 6th, 2012 at 08:26Dylan SchiemannDecember 6th, 2012 at 06:29Panagiotis TsalaportasDecember 6th, 2012 at 08:28Panagiotis TsalaportasDecember 7th, 2012 at 14:24Blaise KalDecember 6th, 2012 at 07:03Mauricio Samy SilvaDecember 6th, 2012 at 12:28Robert Nyman – EditorDecember 7th, 2012 at 02:31Panagiotis TsalaportasDecember 7th, 2012 at 14:22CaesarDecember 6th, 2012 at 18:55Panagiotis TsalaportasDecember 7th, 2012 at 14:22SwaderDecember 17th, 2012 at 00:44Panagiotis TsalaportasDecember 17th, 2012 at 05:32