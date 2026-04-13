---
title: Getting lively with Firefox 90 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2021/07/getting-lively-with-firefox-90/
author: Ruth John
published: '2021-07-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Getting lively with Firefox 90**

As the summer rolls around for those of us in the northern hemisphere, temperatures are high and unwinding with a cool ice tea is high on the agenda. Isn’t it lucky then that Background Update is here for Windows, which means Firefox can update even if it’s not running. We can just sit back and relax!

Also this release we see a few nice JavaScript additions, including [private fields and methods for classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields), and the at() method for [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/at), [String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/at) and [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/at) global objects.

This blog post just provides a set of highlights; for all the details, check out the following:

**Classes go private**

A feature JavaScript has lacked since its inception,[ private fields and methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields) are now enabled by default In Firefox 90. This allows you to declare private properties within a class. You can not reference these private properties from outside of the class; they can only be read or written within the class body.

Private names must be prefixed with a ‘hash mark’ (#) to distinguish them from any public properties a class might hold.

This shows how to declare private fields as opposed to public ones within a class:

```
class ClassWithPrivateProperties {
#privateField;
publicField;
constructor() {
// can be referenced within the class, but not accessed outside
this.#privateField = 42;
// can be referenced within the class aswell as outside
this.publicField = 52;
}
// again, can only be used within the class
#privateMethod() {
return 'hello world';
}
// can be called when using the class
getPrivateMessage() {
return this.#privateMethod();
}
}
```


Static fields and methods can also be private. For a more detailed overview and explanation, check out the great guide:[ Working with private class features](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_With_Private_Class_Features). You can also read what it takes to implement such a feature in our [previous blog post Implementing Private Fields for JavaScript](https://hacks.mozilla.org/2021/06/implementing-private-fields-for-javascript/).

**JavaScript at() method**

The relative indexing method at() has been added to the [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/at), [String](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/at) and [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/at) global objects.

Passing a positive integer to the method returns the item or character at that position. However the highlight with this method, is that it also accepts negative integers. These count back from the end of the array or string. For example, 1 would return the second item or character and -1 would return the last item or character.

This example declares an array of values and uses the at() method to select an item in that array *from the end*.

```
const myArray = [5, 12, 8, 130, 44];
let arrItem = myArray.at(-2);
// arrItem = 130
```


It’s worth mentioning there *are* other common ways of doing this, however this one looks quite neat.

**Conic gradients for Canvas**

The [2D Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) has a new [createConicGradient()](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/createConicGradient) method, which creates a gradient *around* a point (rather than from it, like [createRadialGradient()](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/createRadialGradient) ). This feature allows you to specify where you want the center to be and in which direction the gradient should start. You then add the colours you want and where they should begin (and end).

This example creates a conic gradient with 5 colour stops, which we use to fill a rectangle.

```
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
// Create a conic gradient
// The start angle is 0
// The centre position is 100, 100
var gradient = ctx.createConicGradient(0, 100, 100);
// Add five color stops
gradient.addColorStop(0, "red");
gradient.addColorStop(0.25, "orange");
gradient.addColorStop(0.5, "yellow");
gradient.addColorStop(0.75, "green");
gradient.addColorStop(1, "blue");
// Set the fill style and draw a rectangle
ctx.fillStyle = gradient;
ctx.fillRect(20, 20, 200, 200);
```


The result looks like this:

![Rainbow radial gradient](../../assets/48f8f67852101fee.png)


**New Request Headers**

Fetch metadata request headers provide information about the context from which a request originated. This allows the server to make decisions about whether a request should be allowed based on where the request came from and how the resource will be used. Firefox 90 enables the following by default:

## About Ruth John

Ruth John works as a Technical Writer at Mozilla. A recent addition to the MDN team, she's a big fan of web technologies, and not only enjoys writing about them, but building demos with them as well.

## 2 comments

satta kingJuly 14th, 2021 at 08:37JesseJuly 19th, 2021 at 10:19