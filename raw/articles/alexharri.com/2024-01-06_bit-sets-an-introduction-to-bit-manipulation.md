---
title: 'Bit Sets: An introduction to bit manipulation'
url: https://alexharri.com/blog/bit-sets
published: '2024-01-06'
source_blog: Personal website | Alex Harri Jónsson
source_site: https://alexharri.com/
category: graphics
fetched: '2026-04-19'
---

# Bit Sets: An introduction to bit manipulation

[Bit sets](https://en.wikipedia.org/wiki/Bit_array) — also known as bit arrays or bit vectors — are a highly compact data structure that stores a list of bits. They are often used to represent a set of integers or an array of booleans.

In addition to their memory-compactness, bit sets support extremely performant boolean operations like [unions](https://en.wikipedia.org/wiki/Union_(set_theory)) and [intersections](https://en.wikipedia.org/wiki/Intersection_(set_theory)), achieved through the use of [bitwise operations](https://en.wikipedia.org/wiki/Bitwise_operation).

In this 2-part series on bit sets, we’ll walk through implementing a `BitSet`

from scratch in JavaScript.

- This post covers the basics of bitwise operators and bit manipulation. We’ll use that knowledge to implement a basic
`BitSet`

class. [In part 2](https://alexharri.com/blog/bit-set-iteration)we’ll add the ability to iterate over bit sets extremely quickly by exploiting[two’s complement](https://en.wikipedia.org/wiki/Two%27s_complement)and[Hamming weights](https://en.wikipedia.org/wiki/Hamming_weight).

The post assumes that you’re somewhat familiar with [binary numbers](https://www.mathsisfun.com/binary-number-system.html), so refresh your memory if you haven’t used them for a while.

With that out of the way, let’s get started!

## Bit masks

[Bit masks](https://en.wikipedia.org/wiki/Mask_(computing)) allow us to compactly store multiple booleans in a single number. You may know bit masks as *bit flags* or *bit fields*.

// This binary number...00001001// ...is equivalent to this array of booleans[ true, false, false, true, false, false, false, false ]

Binary numbers are read right-to-left, following [bit ordering](https://en.wikipedia.org/wiki/Bit_numbering) from least-significant to most-significant

Each bit in the bit mask corresponds to a single boolean — 1 representing true, and 0 representing false.

In the following example, we’ll represent a user’s permissions using a bit mask. Certain positions in the bit mask correspond to specific permissions (e.g. `READ`

or `WRITE`

). If the corresponding bit is set to 1, the user has the permission, otherwise, they don’t.

// The '0b' prefix denotes a binary numbersconst READ = 0b0001;const UPDATE = 0b0010;const CREATE = 0b0100;const DELETE = 0b1000;function canRead(permissions: number) {return (permissions & READ) !== 0;}function canUpdate(permissions: number) {return (permissions & UPDATE) !== 0;}canRead(0b1100);//=> falsecanRead(0b0101);//=> true

`&`

is the [bitwise AND operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_AND). It returns a new number where the bits are set to 1 if both of the input bits are 1.

Input 0101 0101 0101Bit mask & 0001 & 0010 & 0100------------------------------------Output 0001 0000 0100

If the input numbers have no bits in common with the bit mask, the `&`

operation will yield 0.

const BIT_MASK = 0b0010;function secondBitIsSetToOne(input: number) {return (input & BIT_MASK) !== 0;}

`|`

is another operator, representing [bitwise OR](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_OR). It returns a new number where the bits are set to one if either of the input bits is 0.

Input 0101 0101 0101Bit mask | 0001 | 0010 | 0100------------------------------------Output 0101 0111 0101

We can use it to, for example, set specific bits to one.

const READ = 0b0001;function addReadPermission(permissions: number) {return permissions | READ;}addReadPermission(0b0010);//=> 0b0011

We can now add permissions, but what about removing them?

We can set bits to 0 through the use of the [bitwise NOT](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_NOT) operator `~`

, a [unary](https://www.digitalocean.com/community/tutorials/javascript-unary-operators-simple-and-useful) operator that flips all of the bits in the number:

Unary means that it takes a single operand, as opposed to two.

Input ~0101 ~1000 ~0001-------------------------------Output 1010 0111 1110

We can use NOT to create an *inverse bit mask* that passes through all but one bit:

const READ = 0b0001;const UPDATE = 0b0010;console.log(~READ)//=> 0b1110console.log(~UPDATE)//=> 0b1101

Using this in conjunction with AND, we can set specific bits to zero:

const READ = 0b0001;function removeReadPermission(permissions: number) {return permissions & ~READ;}removeReadPermission(0b0011);//=> 0b0010

We can also create groups of permissions using OR:

const OWNER = READ | UPDATE | CREATE | DELETE; // 0b1111const EDITOR = READ | UPDATE | CREATE; // 0b1011const VIEWER = READ; // 0b0001

And use them to see if a user has a set of permissions, or provide a user with a set of permissions:

function isEditor(permissions: number) {return (permissions & EDITOR) === EDITOR;}function addEditorPermissions(permissions: number) {return permissions | EDITOR;}

We can also see which permissions users have in common:

function commonPermissions(a: number, b: number) {return a & b;}

### Limits of bit masks

Bit masks are great, but their capacity is limited. JavaScript only [supports 32-bit integers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#fixed-width_number_conversion), so a bit mask can only store 32 bits.

This is where bit sets come in. Once you need to store more than 32 booleans (or 64, depending on the language) you can use an array of integers to make the number of bits *arbitrarily* large.

[ 0b00010011, 0b01100000, ... ]

## Implementing a bit set

The integers that store the bits of our bit set are called [words](https://en.wikipedia.org/wiki/Word_(computer_architecture)), so we’ll store a `words`

array in our `BitSet`

class.

class BitSet {private words: number[];}

Any set data structure will need a few basic operations:

- Add an element
- Remove an element
- Check for the presence of an element

The elements of a bit set are non-negative integers that correspond to a bit index. If the bit at index `N`

is set to 1, then `N`

is considered to be *in* the set.

Considering that, we can create a skeleton for our `BitSet`

class:

class BitSet {private words: number[];add(index: number) {// Set some bit to '1'}remove(index: number) {// Set some bit to '0'}has(index: number) {// Return true if some bit is set to '1'}}

Each bit will be stored in some individual `word`

in `words`

. Consider how the `words`

array is structured:

[ 00000000, 00000000, 00000000, 00000000 ]// The `0b` prefix is omitted for clarity, and we're using// 8 bits instead of 32 for readability

We can map each bit to an absolute index:

[ 00000000, 00000000, 00000000, 00000000 ]│││││││└ 0 │││││││└ 8 │││││││└ 16 │││││││└ 24││││││└─ 1 ││││││└─ 9 ││││││└─ 17 ││││││└─ 25│││││└── 2 │││││└── 10 │││││└── 18 │││││└── 26││││└─── 3 ││││└─── 11 ││││└─── 19 ││││└─── 27│││└──── 4 │││└──── 12 │││└──── 20 │││└──── 28││└───── 5 ││└───── 13 ││└───── 21 ││└───── 29│└────── 6 │└────── 14 │└────── 22 │└────── 30└─────── 7 └─────── 15 └─────── 23 └─────── 31

Each word is indexed right-to-left, following [bit ordering](https://en.wikipedia.org/wiki/Bit_numbering) from least-significant to most-significant

But to find a single bit in a specific `word`

, we need to convert the input index into two indices:

- The index of the
`word`

in`words`

. - The index of the bit in
`word`

.

// word 0 word 1 word 2 word 3[ 00000000, 00000000, 00000000, 00000000 ]// 76543210 76543210 76543210 76543210

### Parsing an input index

Since JavaScript only supports [32-bit integers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#fixed-width_number_conversion), we’ll define a `WORD_LEN`

constant with the value 32.

const WORD_LEN = 32;

Because `WORD_LEN`

is a power of two, the bit index within the `word`

will be the `log2(WORD_LEN)`

least significant bits of `index`

, which yields a value of 5.

Math.log2(WORD_LEN)//=> 50b00000//=> 0 (1st bit)0b11111//=> 31 (32nd bit)

The rest of the bits in `index`

(leftmost) specify the word index.

00000000000 // word index~~~~~~~~~~~0000000000000000 // input index~~~~~00000 // bit index

When all of the bits in the bit index region are set to 1, we get a word index of 0 and a bit index of 31, corresponding to the 32nd bit.

00000000000 = 0 // word index~~~~~~~~~~~0000000000011111 = 31 // input index~~~~~11111 = 31 // bit index// 32nd bit

If we increment the input index by 1, we get a word index of 1 and a bit index of 0, corresponding to the 33rd bit.

00000000001 = 1 // word index~~~~~~~~~~~0000000000100000 = 32 // input index~~~~~00000 = 0 // bit index// 33rd bit

This works for any input index. An input `index`

of 100 corresponds to `0b1100100`

in binary. Broken down, we get a word index of 3 and a bit index of 4, corresponding to the 101st bit.

00000000011 = 3 // word index~~~~~~~~~~~0000000001100100 = 100 // input index~~~~~00100 = 4 // bit index// 101st bit

We can verify this by computing `(3 * 32) + 4`

:

const wordIndex = 3;const bitIndex = 4;(wordIndex * 32) + bitIndex//=> 100

So to compute the word index, we need to shift the bits in the input index right by 5 (i.e. `log2(WORD_LEN)`

) so that the word index bits become the rightmost (least-significant) bits.

We can do this with the `>>`

operator.

const wordIndex = index >> 5;

`>>`

is the [bitwise right shift](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Right_shift) operator. It returns the input number with its bits shifted right by N places:

const input = 0b01100100;input >> 5//=> 0b00000011

This can be illustrated like so:

// This expression...0b01100100 >> 5// ...corresponds to the following01100100011>>>>>>>>>>01100000011

As we learned earlier, the number 5 corresponds to the base 2 logarithm of 32.

Math.log2(32)//=> 5

Let’s put it in a `WORD_LOG`

constant for readability.

const WORD_LEN = 32;const WORD_LOG = Math.log2(WORD_LEN);

Computing the bit index is quite simple: we take the 5 least-significant bits from `index`

using bitwise AND:

const bitIndex = index & 0b11111;

This sets any bits left of the 5 least significant bits to zero.

And with that, we know how to parse an input `index`

into word and bit indices:

const wordIndex = index >> WORD_LOG;const bitIndex = index & 0b11111;

We can now get to implementing some of the methods of `BitSet`

!

### BitSet.add

The `add`

method should set the bit at `index`

to 1. This bit will live in some individual `word`

, which we can access via `wordIndex`

:

class BitSet {add(index: number) {const wordIndex = index >> WORD_LOG;const bitIndex = index & 0b11111;// ...}}

Given an integer, we can set the bit at a specific index to 1 like so:

function setBitAtIndexToOne(input: number, index: number) {return input | (1 << index);}setBitAtIndexToOne(0b00000000, 2);//=> 0b00000100setBitAtIndexToOne(0b00000000, 5);//=> 0b00100000

`<<`

is the [bitwise left shift](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Left_shift) operator, which returns the input number with its bits shifted left by N places.

The expression `1 << index`

creates a bit mask with the bit at `index`

set to one.

1 << 2;//=> 0b000001001 << 0;//=> 0b000000011 << 6;//=> 0b01000000

Applying this bit mask to our word using bitwise OR will set the bit at `bitIndex`

to 1.

this.words[wordIndex] |= (1 << bitIndex);

With that, we have our implementation:

class BitSet {add(index: number) {const wordIndex = index >> WORD_LOG;const bitIndex = index & 0b11111;this.words[wordIndex] |= (1 << bitIndex);}}

However, there is one simplification we can make. Because the bitwise shift operators `<<`

and `>>`

operate on 32-bit integers, the maximum shift possible is 31 (from 32nd to 1st bit, or 1st to 32nd bit).

The [ECMAScript standard states](https://262.ecma-international.org/14.0/#sec-numeric-types-number-leftShift):

Let shiftCount be ℝ(rnum) modulo 32.


In other words, only read the 5 least-significant bits which represent 0 to 31; all other bits are dismissed. This means that we don’t need to compute `bitIndex`

and can left shift on `index`

directly.

class BitSet {add(index: number) {const wordIndex = index >> WORD_LOG;this.words[wordIndex] |= (1 << index);}}

### BitSet.remove

In implementing `BitSet.remove`

, we want to set a specific bit to zero. We’ve already seen how this was done in a previous example:

const READ = 0b0001;function removeReadPermission(permissions: number) {return permissions & ~READ;}removeReadPermission(0b0011);//=> 0b0010

As we did in `BitSet.add`

, we’ll use `1 << index`

to create a bit mask for a specific bit.

1 << 4//=> 0b00010000

We then invert that bit mask using bitwise NOT:

~(1 << 4)//=> 0b11101111

And then apply this inverse bit mask via bitwise AND:

const word = 0b01111100;word & ~(1 << 4)//=> 0b01101100

With that, our implementation of `BitSet.remove`

looks like so:

class BitSet {remove(index: number) {const wordIndex = index >> WORD_LOG;this.words[wordIndex] &= ~(1 << index);}}

### BitSet.has

The `BitSet.has`

method should return true if a specific bit is set to 1, and false otherwise.

We saw how this is done earlier in this post:

const READ = 0b0001;function canRead(permissions: number) {return (permissions & READ) !== 0;}

As before, we create a bit mask using left shift and apply it using bitwise AND.

const word = 0b11011100;word & (1 << 4)//=> 0b00010000

If the result is non-zero, the bit is set to 1.

class BitSet {has(index: number) {const wordIndex = index >> WORD_LOG;return (this.words[wordIndex] & (1 << index)) !== 0;}}

### Handling edge cases

One easy edge case to run into is `wordIndex`

being out-of-bounds. That problem can be resolved by adding a `resize`

method that ensures that the `words`

array encompasses `wordIndex`

:

class BitSet {set(index: number) {const wordIndex = index >> WORD_LOG;this.resize(wordIndex);// ...}private resize(wordIndex: number) {// Make 'this.words' encompass 'wordIndex'}}

I won’t cover other edge cases in this post. If you’re interested, feel free to explore [my full implementation of BitSet on GitHub](https://github.com/alexharri/bitset-mut).

## Next up: Iteration

We covered a lot of ground in this post!

Next up in our bit set journey is iterating over bits. We’ll learn how exploiting [two’s complement](https://en.wikipedia.org/wiki/Two%27s_complement) and [Hamming weights](https://en.wikipedia.org/wiki/Hamming_weight) enables us to make our iteration extremely fast!

See you in part 2: [Iterating over Bit Sets quickly](https://alexharri.com/blog/bit-set-iteration)

— Alex Harri

To be notified of new posts, subscribe to my mailing list.