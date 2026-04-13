---
title: 'TypedArray or DataView: Understanding byte order – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2017/01/typedarray-or-dataview-understanding-byte-order/
author: Martin Splitt
published: '2017-01-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

### TL;DR

Depending on how you access an `ArrayBuffer`

you get different byte order on the same machine. So long story short: it makes a difference if you use a [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Typed_arrays) or the setters from a [DataView](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView).

`ArrayBuffer`

is there to give efficient and fast access to binary data, such as data that is needed by [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Getting_started_with_WebGL), [Canvas 2D](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API) or [Web Audio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API). In these instances, you generally want to store data in a way that is most efficiently consumed by your hardware or most easily streamed over the network.

Read on to find out how that works in detail.

### A primer on TypedArrays and the ArrayBuffer

With ES6 we got three nice new things:

- The
[ArrayBuffer](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer), a data structure designed to hold a given amount of binary data. [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray), a*view*into an ArrayBuffer where every item has the same size and type.- The
[DataView](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView), another*view*into an ArrayBuffer, but one which allows items of different size and type in the ArrayBuffer.

Having a data structure that can take a bunch of bytes to work with binary data makes sense, if we want to work with things such as images or all sorts of files.

Without going into much more detail on how binary data works, let’s have a look at a small example:

```
var buffer = new ArrayBuffer(2) // array buffer for two bytes
var bytes = new Uint8Array(buffer) // views the buffer as an array of 8 bit integers
bytes[0] = 65 // ASCII for 'A'
bytes[1] = 66 // ASCII for 'B'
```


Now we can turn that into a [Blob](https://developer.mozilla.org/en-US/docs/Web/API/Blob),

make a [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) from it and open it as a new text file:

```
var blob = new Blob([buffer], {type: 'text/plain'})
var dataUri = window.URL.createObjectURL(blob)
window.open(dataUri)
```


This will display the text ‘AB’ in a new browser window.

### Which way is up? Byte order, part one:

So we wrote two bytes (or 16 bit) one after the other, but as there are TypedArray constructors for larger numbers, we could also write the two characters using a single 16-bit number – writing two bytes with a single instruction.

This helpful table from the [typed arrays article](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Typed_arrays) on the Mozilla Developer Network should illustrate the idea:

![TypedArrays group one or multiple bytes in an ArrayBuffer](https://mdn.mozillademos.org/files/8629/typed_arrays.png)


You can see that in the previous example we wrote the byte for ‘A’ and then the byte for ‘B’, but we could also write two bytes at once using a `Uint16Array`

instead, and putting both bytes into a single 16-bit number:

```
var buffer = new ArrayBuffer(2) // array buffer for two bytes
var word = new Uint16Array(buffer) // views the buffer as an array with a single 16 bit integer
var value = (65 << 8) + 66 // we shift the 'A' into the upper 8 bit and add the 'B' as the lower 8 bit.
word[0] = value // write the 16 bit (2 bytes) into the typed array
// Let's create a text file from them:
var blob = new Blob([buffer], {type: 'text/plain'})
var dataUri = window.URL.createObjectURL(blob)
window.open(dataUri)
```


But wait? We see “BA” instead of “AB” as we did before! What’s happened?

Let’s have a closer look at the value we wrote into the array:

```
65 decimal = 01 00 00 01 binary
66 decimal = 01 00 00 10 binary
// what we did when we wrote into the Uint8Array:
01 00 00 01 01 00 00 10
<bytes[0]-> <bytes[1]->
// what we did when we created the 16-bit number:
var value = (01 00 00 01 00 00 00 00) + 01 00 00 10
= 01 00 00 01 01 00 00 10
```


You can see that the 16 bit we wrote to the Uint8Array and the 16 bit we wrote to the Uint16Array are the same, so why does the result differ?

The answer is that the order of bytes in a value that is longer than one byte differs depending on the [endianness](https://en.wikipedia.org/wiki/Endianness) of the system. Let’s check that:

```
var buffer = new ArrayBuffer(2)
// create two typed arrays that provide a view on the same ArrayBuffer
var word = new Uint16Array(buffer) // this one uses 16 bit numbers
var bytes = new Uint8Array(buffer) // this one uses 8 bit numbers
var value = (65 << 8) + 66
word[0] = (65 << 8) + 66
console.log(bytes) // will output [66, 65]
console.log(word[0] === value) // will output true
```


When looking at the individual bytes, we see that the value of `B`

has indeed been written into the first byte of the buffer, instead of the value for `A`

, but when we read back the 16-bit number, it is correct!

This is due to the fact that the browser has defaulted to using *little endian* numbers.


What does this mean?


Let’s imagine that a byte could hold a single digit, so the number 123 would take three bytes: `1`

, `2`

and `3`

. Little endian means, that the lower digits of the multi-byte number are stored first so in memory it would be stored as `3`

, `2`

, `1`

.

There is also the *big endian* format where the bytes are stored in the order we would have expected, starting with the highest digits first, so in memory it would be stored as `1`

, `2`

, `3`

.

As long as the computer knows which way around the data is stored, it can do the conversion for us and get the right number back from memory.

That isn’t really a problem. When we do the following:

```
var word = new Uint16Array(buffer)
word[0] = value // If isLittleEndian is not present, set isLittleEndian to either true or false.
```


The choice is implementation dependent. Choose the alternative that is most efficient for the implementation.


An implementation must use the same value each time this step is executed and the same value must be used for the corresponding step in the`GetValueFromBuffer`

abstract operation.

Okay, that’s alright then: We leave `isLittleEndian`

out, the browser decides on a value (in most cases `true`

, because most of the systems are little endian), and sticks to it.

This is a pretty reasonable behaviour. As Dave Herman points out in [his blog post from 2012](http://calculist.org/blog/2012/04/24/the-little-endian-web/), it’s either “fast-mode or correct-mode” when picking one choice of endianness in the spec.

Most of the systems these days are little endian, so it is a reasonable assumption to pick little endian. When the data is in the format that the system consumes, we get the best performance because our data does not need to be converted before it can be processed (for instance by the GPU via WebGL). Unless you explicitly need to support some rare hardware, you are safe to assume little endian and reap the speed benefits.

However, what if we want to transfer this data over the network in chunks or write to a structured binary file?

It would be nice to have the data so that we can just write byte by byte as the data come in from the network. For this, we would prefer big endian, because the bytes can then be written sequentially.

Luckily, the platform has us covered!

### Another way of writing to ArrayBuffers: the DataView

As I mentioned in the beginning, there are times when it could come in handy to write different types of data into an ArrayBuffer.

Imagine you want to write a binary file that requires some file header like this:

| Size in byte | Description |
|---|---|
| 2 | Identifier “BM” for Bitmap image |
| 4 | Size of the image in byte |
| 2 | Reserved |
| 2 | Reserved |
| 4 | Offset (in bytes) between the end of the header and the pixel data |

By the way: This is the structure of the [BMP file header](https://en.wikipedia.org/wiki/BMP_file_format#Bitmap_file_header).

Instead of juggling a range of typed arrays, we can also use a DataView:

```
var buffer = new ArrayBuffer(14)
var view = new DataView(buffer)
view.setUint8(0, 66) // Write one byte: 'B'
view.setUint8(1, 67) // Write one byte: 'M'
view.setUint32(2, 1234) // Write four byte: 1234 (rest filled with zeroes)
view.setUint16(6, 0) // Write two bytes: reserved 1
view.setUint16(8, 0) // Write two bytes: reserved 2
view.setUint32(10, 0) // Write four bytes: offset
```


Our `ArrayBuffer`

now contains the following data:

```
Byte | 0 | 1 | 2 | 3 | 4 | 5 | ... |
Type | I8 | I8 | I32 | ... |
Data | B | M |00000000|00000000|00000100|11010010| ... |
```


In the example above we used the `DataView`

to write two `Uint8`

into the first two bytes, followed by a `Uint32`

occupying the following four bytes, and so on and so forth.

Cool. Now let’s go back to our simple text example.

We can also write a `Uint16`

to hold our two-character string `'AB'`

using a `DataView`

instead of the `Uint16Array`

we’ve used previously:

```
var buffer = new ArrayBuffer(2) // array buffer for two bytes
var view = new DataView(buffer)
var value = (65 << 8) + 66 // we shift the 'A' into the upper 8 bit and add the 'B' as the lower 8 bit.
view.setUint16(0, value)
// Let's create a text file from them:
var blob = new Blob([buffer], {type: 'text/plain'})
var dataUri = window.URL.createObjectURL(blob)
window.open(dataUri)
```


Wait, what? We are greeted by the correct string ‘AB’ instead of the ‘BA’ we got last time when we wrote a `Uint16`

! Maybe `setUint16`

defaults to big endian?

DataView.prototype.setUint16 ( byteOffset, value [ , littleEndian ] )


1. Let v be the this value.

2. If littleEndian is not present, let littleEndian befalse.

3. Return SetViewValue(v, byteOffset, littleEndian, “Uint16”, value).

(Emphasis mine.)

Gotcha! The specification says an omitted `littleEndian`

should be treated as `false`

and the `SetViewValue`

will pass this on to `SetValueInBuffer`

, but the operation on the `Uint16Array`

was allowed to *choose* the value and decided for `true`

.

This mismatch results in a different byte order and can cause quite some trouble when overlooked.

The now-deprecated [original spec proposal](https://webcache.googleusercontent.com/search?q=cache:b1P8_b65ZE8J:https://www.khronos.org/registry/typedarray/specs/latest/+&cd=1&hl=en&ct=clnk&gl=us) from the Khronos Group even states this explicitly:

The typed array view types operate with the endianness of the host computer.

The DataView type operates upon data with a specified endianness (big-endian or little-endian).


This sounds pretty exhaustive, but there is a significant gap: What if the typed array and the DataView operations leave out the desired endianness? The answer is:

- The TypedArray will use the native endianness of the system.
- The DataView will default to big endian.

### Conclusion

So is this a problem? Not really.

The browser chose little-endian probably because most systems today happen to work with it on the CPU- and memory levels, and that’s great for performance.

Now why the divergent behavior when using `TypedArray`

setters versus `DataView`

setters?

`TypedArray`

s aim to provide a way to compose binary data for consumption on the same system – therefore it’s a good call to pick the endianness ad hoc.

DataView on the other hand is meant to be used to serialise and deserialise binary data for transmission of said binary data. This is why it makes sense to pick the endianness manually. The default for big endian is precisely because big endian is often used in network transmissions (sometimes referred to as the “network endianness”). If the data is streamed, the data can be assembled just by adding the incoming data at the next memory location.

The easiest way to deal with binary data is to use the `DataView`

setters whenever the binary data we’re creating is leaving the browser – whether over the network to other systems or to the user in the form of a file download.

This has always been suggested, for instance in [this HTML5Rocks article from 2012](https://www.html5rocks.com/en/tutorials/webgl/typed_arrays/):

Typically, when your application reads binary data from a server, you’ll need to scan through it once in order to convert it into the data structures your application uses internally.

DataView should be used during this phase.

It’s not a good idea to use the multi-byte typed array views (Int16Array, Uint16Array, etc.) directly with data fetched via XMLHttpRequest, FileReader, or any other input/output API, because the typed array views use the CPU’s native endianness.


So, in summary, here’s what we’ve learned:

- It is safe to assume systems to be little-endian.
- TypedArrays are great for creating binary data, for instance to pass on to Canvas2D ImageData or WebGL.
- DataView is a safe way to deal with binary data that you receive from or send to other systems.

## About
[
Martin Splitt ](http://www.geekonaut.de)

Martin is pretty decent at humaning and pretty good at computering, so he decided to use his computering to improve his and other's humaning. He loves the open web and open source and helps to make things better with, but not limited to, code.

## 5 comments

Jona StubbeJanuary 4th, 2017 at 11:54NoitidartJanuary 4th, 2017 at 11:59voracityJanuary 5th, 2017 at 22:58Gibran MalheirosJanuary 13th, 2017 at 06:16JarrodJanuary 31st, 2017 at 11:56