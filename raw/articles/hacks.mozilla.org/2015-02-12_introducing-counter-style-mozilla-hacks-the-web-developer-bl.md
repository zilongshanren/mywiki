---
title: Introducing @counter-style – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/introducing-counter-styles/
author: Saurabh; Jsx
published: '2015-02-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introduction

The characters that indicate items in a list are called counters — they can be bullets or numbers. They are defined using the [list-style-type](https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type) CSS property. CSS1 introduced a list of predefined styles to be used as counter markers. The initial list was then slightly extended with addition of more predefined counter styles in CSS2.1. Even with 14 predefined counter styles, it still failed to address use cases from around the world.

Now, the [CSS Counter Styles Level 3](http://www.w3.org/TR/css-counter-styles-3/) specification, which reached Candidate Recommendation last week, adds new predefined counter styles to the existing list that should address most common counter use cases.

In addition to the new predefined styles, the spec also offers an open-ended solution for the needs of worldwide typography by introducing the [@counter-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style) at-rule — which lets us define custom counter styles or even extend existing ones — and the [symbols()](https://developer.mozilla.org/en-US/docs/Web/CSS/symbols) function. The latter is a shorthand for defining inline styles and is useful when the fine-grained control that `@counter-style`

offers is not needed.

This article provides a guide to using the new counter features of CSS Level 3.

## @counter-style

A `@counter-style`

at-rule is identified by a name and defined with a set of *descriptors*. It takes a numerical counter value and converts it into a string or image representation. A custom counter style definition looks like this:

```
@counter-style blacknwhite {
system: cyclic;
negative: "(" ")";
prefix: "/";
symbols: ◆ ◇;
suffix: "/ ";
range: 2 4;
speak-as: "bullets";
}
```

The different available descriptors have the following meanings:

– the*system*[system descriptor](https://hacks.mozilla.org#The_system_descriptor)lets the author specify an algorithm to convert the numerical counter value to a basic string representation. For example, the`cyclic`

system cycles repeatedly through the list of symbols provided to create counter representations.– the*negative*[negative descriptor](https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style/negative)provides the ability to specify additional symbols, such as a negative sign, to be appended/prepended to a counter representation if the counter value is negative. If only one symbol is specified, it will be added*in front of*the marker representation. A second value, if specified (as in the example below), will be added*after*the marker.@counter-style neg { system: numeric; symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"; negative: "(" ")"; }

The above counter style definition will wrap negative markers in a pair of parentheses, instead of preceding them with the minus sign.

– specifies a symbol that will be prepended to the final counter representation.*prefix*– specifies a symbol that will be appended to the final counter representation.The default value of the*suffix*`suffix`

descriptor is a full stop followed by a space. If you need to replace the full stop “.” with a parenthesis, you can specify the`suffix`

descriptor:@counter-style decimal-parenthesis { system: numeric; symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"; suffix: ") "; }

–*range*`range`

lets the author define a range of values over which a counter style is applicable. If a counter value falls outside the specified range, then the specified or default fallback style is used to represent that particular counter value, for example:@counter-style range-example { system: cyclic; symbols: A B C D; range: 4 8; }

The above rule will apply the style only for counter values starting from 4 to 8. The fallback style,

`decimal`

, will be used for the rest of the markers.– as the name suggests, the*pad*`pad`

descriptor lets the author specify a padding length when the counter representations need to be of a minimum length. For example, if you want the counters to start at 01 and go through 02, 03, 04, etc., then the following`pad`

descriptor should be used:@counter-style decimal-new { system: numeric; symbols: "0" "1" "2" "3" "4" "5" "6" "7" "8" "9"; pad: 2 "0"; }

(For a better way to achieve the same result, but without specifying the counter symbols, see the section below about

[extending existing systems](https://hacks.mozilla.org#Extending_systems).)– the fallback specifies a style to fall back to if the specified system is unable to construct a counter representation or if a particular counter value falls outside the specified range.*fallback*and**symbols**– specify the symbols that will be used to construct the counter representation. The**additive-symbols**`symbols`

descriptor is used in most cases other than when the system specified is ‘*additive*.’ While`symbols`

specifies individual symbols, the`additive-symbols`

descriptor is composed of what are known as*additive tuples –*, which each consist of a symbol and a non-negative weight.Symbols specified can be strings, images in the form*url(image-name)*or identifiers. The below example uses images as symbols.@counter-style winners-list { system: fixed; symbols: url(gold-medal.svg) url(silver-medal.svg) url(bronze-medal.svg); suffix: " "; }

– specifies how a counter value should be spoken by speech synthesizers such as screen readers. For example, the author can specify a marker symbol to be read out as a word, a number, or as an audio cue for a bullet point. The example below reads out the counter values as numbers.**speak-as**@counter-style circled-digits { system: fixed; symbols: ➀ ➁ ➂; suffix: ' '; speak-as: numbers; }

You can then use a named style with

`list-style-type`

or with the`counters()`

function as you normally would use a predefined counter style.ul { list-style-type: circled-digits; }

On a supported browser, the counter style above will render lists with markers like this:

![@counter-style demo image](../../assets/1946f2106312ce4b.png)


### The system descriptor

The [system descriptor](https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style/system) takes one of the predefined algorithms, which describe how to convert a numerical counter value to its representation. The system descriptor can have values that are *cyclic*, *numeric*, *alphabetic*, *symbolic*, *additive*, *fixed* and *extends*.

If the system specified is *cyclic*, it will cycle through the list of symbols provided. Once the end of the list is reached, it will loop back to the beginning and start over. The fixed system is similar, but once the list of symbols is exhausted, it will resort to the fallback style to represent the rest of the markers. The symbolic, numeric and alphabetic systems are similar to the above two, but with their own subtle differences.

The additive system requires that the `additive-symbols`

descriptor be specified instead of the `symbols`

descriptor. `additive-symbols`

takes a list of additive tuples. Each additive tuple consists of a symbol and its numerical weight. The additive system is used to represent “[sign-value](http://en.wikipedia.org/wiki/Sign-value_notation)” numbering systems such as the Roman numerals.

We can rewrite the Roman numerals as a @counter-style rule using the additive system like this:

```
@counter-style custom-roman {
system: additive;
range: 1 100;
additive-symbols: 100 C, 90 XC, 50 L, 40 XL, 10 X, 9 IX, 5 V, 4 IV, 1 I;
}
```

### Extending existing or custom counter styles

The *extends* system lets authors create custom counter styles based on existing ones. Authors can use the algorithm of another counter style, but alter its other aspects. If a `@counter-style`

rule using the `extends`

system has any unspecified descriptors, their values will be taken from the extended counter style specified.

For example, if you want to define a new style which is similar to decimal, but has a string “Chapter ” in front of all the marker values, then rather than creating an entirely new style you can use the *extends* system to extend the decimal style like this:

```
@counter-style chapters {
system: extends decimal;
prefix: 'Chapter ';
}
```

Or, if you need the decimal style to start numbers from 01, 02, 03.. instead of 1, 2, 3.., you can simply specify the *pad* descriptor:

```
@counter-style decimal-new {
system: extends decimal;
pad: 2 "0";
}
```

A counter style using the `extends`

system should not specify the `symbols`

and `additive-symbols`

descriptors.

See the [reference page](https://developer.mozilla.org/en-US/docs/Web/CSS/@counter-style/system) on MDN for details and usage examples of all system values.

## A shorthand – The symbols() function

While a `@counter-style`

at-rule lets you tailor a custom counter style, often such elaborate control is not needed. That is where the [symbols()](https://developer.mozilla.org/en-US/docs/Web/CSS/symbols) function comes in. `symbols()`

lets you define inline counter styles as function properties. Since the counter styles defined in this way are nameless (anonymous), they can not be reused elsewhere in the stylesheet.

An example anonymous counter style looks like this:

```
ul {
list-style-type: symbols(fixed url(one.svg) url(two.svg));
}
```

## Even more predefined counter styles

CSS Lists 3 vastly extends the number of predefined styles available. Along with the predefined styles such as `decimal`

, `disc`

, `circle`

and `square`

that existed before, additional styles such as `hebrew`

, `thai`

, `gujarati`

, `disclosure-open`

/`close`

, etc. are also added to the predefined list. The full list of predefined styles enabled by the spec can be seen [here](https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#Values).

## Browser support

Support for `@counter-style`

and the symbols() function along with the new predefined styles landed in [Firefox 33](https://developer.mozilla.org/en-US/Firefox/Releases/33). Google Chrome hasn’t implemented `@counter-styles`

or the `symbols()`

function yet, but most of the new numeric and alphabetic predefined styles have been implemented. There is no support in IE so far. Support has already landed in the latest releases of Firefox for Android and in the upcoming Firefox OS 2.1, which has support for `@counter-style`

. Support for `symbols()`

will land in Firefox OS 2.2.

## Examples

Check out this [demo page](https://mdn.github.io/css-examples/counter-style-demo/) and see if `@counter-style`

is supported in your favorite browsers.

## About
[
Saurabh / Jsx ](http://rebugged.com)

Saurabh is a free software and web standards enthusiast. More info is available in his blog below.

## 3 comments

Wes JohnstonFebruary 12th, 2015 at 12:32Saurabh / JsxFebruary 13th, 2015 at 00:00jperrier@mozilla.comFebruary 15th, 2015 at 02:12