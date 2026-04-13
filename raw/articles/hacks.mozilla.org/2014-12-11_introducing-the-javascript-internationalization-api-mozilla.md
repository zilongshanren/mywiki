---
title: Introducing the JavaScript Internationalization API – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2014/12/introducing-the-javascript-internationalization-api/
author: Jeff Walden
published: '2014-12-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 29 issued half a year ago, so this post is *long* overdue. Nevertheless I wanted to pause for a second to discuss the Internationalization API first shipped on desktop in that release (and passing all [tests](http://test262.ecmascript.org/testcases_intl402.html)!). [Norbert Lindenberg](http://norbertlindenberg.com/) wrote most of the implementation, and I reviewed it and now maintain it. (Work by [Makoto Kato](https://twitter.com/makoto_kato/) should bring this to Android soon; b2g may take longer due to some b2g-specific hurdles. Stay tuned.)

## What’s internationalization?

Internationalization (i18n for short — i, eighteen characters, n) is the process of writing applications in a way that allows them to be easily adapted for audiences from varied places, using varied languages. It’s easy to get this wrong by inadvertently assuming one’s users come from one place and speak one language, especially if you don’t even *know* you’ve made an assumption.

```
function formatDate(d)
{
// Everyone uses month/date/year...right?
var month = d.getMonth() + 1;
var date = d.getDate();
var year = d.getFullYear();
return month + "/" + date + "/" + year;
}
function formatMoney(amount)
{
// All money is dollars with two fractional digits...right?
return "$" + amount.toFixed(2);
}
function sortNames(names)
{
function sortAlphabetically(a, b)
{
var left = a.toLowerCase(), right = b.toLowerCase();
if (left > right)
return 1;
if (left === right)
return 0;
return -1;
}
// Names always sort alphabetically...right?
names.sort(sortAlphabetically);
}
```

## JavaScript’s historical i18n support is poor

i18n-aware formatting in traditional JS uses the various `toLocaleString()`

methods. The resulting strings contained whatever details the implementation chose to provide: no way to pick and choose (did you need a weekday in that formatted date? is the year irrelevant?). Even if the proper details were included, the format might be wrong e.g. decimal when percentage was desired. And you couldn’t choose a locale.

As for sorting, JS provided almost no useful locale-sensitive text-comparison (collation) functions. [ localeCompare()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare) existed but with a very awkward interface unsuited for use with

[. And it too didn’t permit choosing a locale or specific sort order.](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)

`sort`

These limitations are bad enough that — this surprised me greatly when I learned it! — serious web applications that need i18n capabilities (most commonly, financial sites displaying currencies) will box up the data, *send it to a server, have the server perform the operation, and send it back to the client*. Server roundtrips just to format amounts of money. Yeesh.

## A new JS Internationalization API

The new [ECMAScript Internationalization API](http://www.ecma-international.org/ecma-402/1.0/) greatly improves JavaScript’s i18n capabilities. It provides all the flourishes one could want for formatting dates and numbers and sorting text. The locale is selectable, with fallback if the requested locale is unsupported. Formatting requests can specify the particular components to include. Custom formats for percentages, significant digits, and currencies are supported. Numerous collation options are exposed for use in sorting text. And if you care about performance, the up-front work to select a locale and process options can now be done once, instead of once every time a locale-dependent operation is performed.

That said, the API is not a panacea. The API is “best effort” only. Precise outputs are almost always deliberately unspecified. An implementation could legally support *only* the [ oj](https://en.wikipedia.org/wiki/Ojibwe_language) locale, or it could ignore (almost all) provided formatting options. Most implementations will have high-quality support for many locales, but it’s not guaranteed (particularly on resource-constrained systems such as mobile).

Under the hood, Firefox’s implementation depends upon the [International Components for Unicode](http://site.icu-project.org/) library (ICU), which in turn depends upon the [Unicode Common Locale Data Repository](http://cldr.unicode.org/) (CLDR) locale data set. Our implementation is [self-hosted](https://en.wikipedia.org/wiki/Self-hosting): most of the implementation atop ICU is written in JavaScript itself. We hit a few bumps along the way (we haven’t self-hosted anything this large before), but nothing major.

## The `Intl`

interface

The i18n API lives on the global `Intl`

object. `Intl`

contains three constructors: `Intl.Collator`

, `Intl.DateTimeFormat`

, and `Intl.NumberFormat`

. Each constructor creates an object exposing the relevant operation, efficiently caching locale and options for the operation. Creating such an object follows this pattern:

```
var ctor = "Collator"; // or the others
var instance = new Intl[ctor](locales, options);
```

`<var>locales</var>`

is a string specifying a single [language tag](http://www.w3.org/International/articles/language-tags/) or an arraylike object containing multiple language tags. Language tags are strings like `en`

(English generally), `de-AT`

(German as used in Austria), or `zh-Hant-TW`

(Chinese as used in Taiwan, using the traditional Chinese script). Language tags can also include a “Unicode extension”, of the form `-u-key1-value1-key2-value2...`

, where each key is an “extension key”. The various constructors interpret these specially.

`<var>options</var>`

is an object whose properties (or their absence, by evaluating to `undefined`

) determine how the formatter or collator behaves. Its exact interpretation is determined by the individual constructor.

Given locale information and options, the implementation will try to produce the closest behavior it can to the “ideal” behavior. Firefox supports 400+ locales for collation and 600+ locales for date/time and number formatting, so it’s very likely (but not guaranteed) the locales you might care about are supported.

`Intl`

generally provides no guarantee of particular behavior. If the requested locale is unsupported, `Intl`

allows best-effort behavior. Even if the locale is supported, behavior is not rigidly specified. *Never assume that a particular set of options corresponds to a particular format.* The phrasing of the overall format (encompassing all requested components) might vary across browsers, or even across browser versions. Individual components’ formats are unspecified: a `short`

-format weekday might be “S”, “Sa”, or “Sat”. The `Intl`

API isn’t intended to expose exactly specified behavior.

### Date/time formatting

#### Options

The primary options properties for date/time formatting are as follows:

`weekday`

,`era`

`"narrow"`

,`"short"`

, or`"long"`

. (`era`

refers to typically longer-than-year divisions in a calendar system: BC/AD, the[current Japanese emperor’s reign](https://en.wikipedia.org/wiki/Japanese_era_name), or others.)`month`

`"2-digit"`

,`"numeric"`

,`"narrow"`

,`"short"`

, or`"long"`

`year`

`day`

`hour`

,`minute`

,`second`

`"2-digit"`

or`"numeric"`

`timeZoneName`

`"short"`

or`"long"`

`timeZone`

- Case-insensitive
`"UTC"`

will format with respect to UTC. Values like`"CEST"`

and`"America/New_York"`

don’t have to be supported, and they don’t currently work in Firefox.

The values don’t map to particular formats: remember, the `Intl`

API almost never specifies exact behavior. But the intent is that `"narrow"`

, `"short"`

, and `"long"`

produce output of corresponding size — “S” or “Sa”, “Sat”, and “Saturday”, for example. (Output may be ambiguous: Saturday and Sunday both could produce “S”.) `"2-digit"`

and `"numeric"`

map to two-digit number strings or full-length numeric strings: “70” and “1970”, for example.

The final used options are largely the requested options. However, if you don’t specifically request any `weekday`

/`year`

/`month`

/`day`

/`hour`

/`minute`

/`second`

, then `year`

/`month`

/`day`

will be added to your provided options.

Beyond these basic options are a few special options:

`hour12`

- Specifies whether hours will be in 12-hour or 24-hour format. The default is typically locale-dependent. (Details such as whether midnight is zero-based or twelve-based and whether leading zeroes are present are also locale-dependent.)

There are also two special properties, `localeMatcher`

(taking either `"lookup"`

or `"best fit"`

) and `formatMatcher`

(taking either `"basic"`

or `"best fit"`

), each defaulting to `"best fit"`

. These affect how the right locale and format are selected. The use cases for these are somewhat esoteric, so you should probably ignore them.

#### Locale-centric options

`DateTimeFormat`

also allows formatting using customized calendaring and numbering systems. These details are effectively part of the locale, so they’re specified in the Unicode extension in the language tag.

For example, Thai as spoken in Thailand has the language tag `th-TH`

. Recall that a Unicode extension has the format `-u-key1-value1-key2-value2...`

. The calendaring system key is `ca`

, and the numbering system key is `nu`

. The Thai numbering system has the value `thai`

, and the Chinese calendaring system has the value `chinese`

. Thus to format dates in this overall manner, we tack a Unicode extension containing both these key/value pairs onto the end of the language tag: `th-TH-u-ca-chinese-nu-thai`

.

For more information on the various calendaring and numbering systems, see [the full DateTimeFormat documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DateTimeFormat).

#### Examples

After creating a `DateTimeFormat`

object, the next step is to use it to format dates via the handy `format()`

function. Conveniently, this function is a *bound* function: you don’t have to call it on the `DateTimeFormat`

directly. Then provide it a timestamp or [ Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) object.

Putting it all together, here are some examples of how to create `DateTimeFormat`

options for particular uses, with current behavior in Firefox.

```
var msPerDay = 24 * 60 * 60 * 1000;
// July 17, 2014 00:00:00 UTC.
var july172014 = new Date(msPerDay * (44 * 365 + 11 + 197));
```

Let’s format a date for English as used in the United States. Let’s include two-digit month/day/year, plus two-digit hours/minutes, and a short time zone to clarify that time. (The result would obviously be different in another time zone.)

```
var options =
{ year: "2-digit", month: "2-digit", day: "2-digit",
hour: "2-digit", minute: "2-digit",
timeZoneName: "short" };
var americanDateTime =
new Intl.DateTimeFormat("en-US", options).format;
print(americanDateTime(july172014)); // 07/16/14, 5:00 PM PDT
```

Or let’s do something similar for Portuguese — ideally as used in Brazil, but in a pinch Portugal works. Let’s go for a little longer format, with full year and spelled-out month, but make it UTC for portability.

```
var options =
{ year: "numeric", month: "long", day: "numeric",
hour: "2-digit", minute: "2-digit",
timeZoneName: "short", timeZone: "UTC" };
var portugueseTime =
new Intl.DateTimeFormat(["pt-BR", "pt-PT"], options);
// 17 de julho de 2014 00:00 GMT
print(portugueseTime.format(july172014));
```

How about a compact, UTC-formatted weekly Swiss train schedule? We’ll try the official languages from most to least popular to choose the one that’s most likely to be readable.

```
var swissLocales = ["de-CH", "fr-CH", "it-CH", "rm-CH"];
var options =
{ weekday: "short",
hour: "numeric", minute: "numeric",
timeZone: "UTC", timeZoneName: "short" };
var swissTime =
new Intl.DateTimeFormat(swissLocales, options).format;
print(swissTime(july172014)); // Do. 00:00 GMT
```

Or let’s try a date in descriptive text by a painting in a Japanese museum, using the Japanese calendar with year and era:

```
var jpYearEra =
new Intl.DateTimeFormat("ja-JP-u-ca-japanese",
{ year: "numeric", era: "long" });
print(jpYearEra.format(july172014)); // 平成26年
```

And for something completely different, a longer date for use in Thai as used in Thailand — but using the Thai numbering system and Chinese calendar. (Quality implementations such as Firefox’s would treat plain `th-TH`

as `th-TH-u-ca-buddhist-nu-latn`

, imputing Thailand’s typical Buddhist calendar system and Latin 0-9 numerals.)

```
var options =
{ year: "numeric", month: "long", day: "numeric" };
var thaiDate =
new Intl.DateTimeFormat("th-TH-u-nu-thai-ca-chinese", options);
print(thaiDate.format(july172014)); // ๒๐ 6 ๓๑
```

Calendar and numbering system bits aside, it’s relatively simple. Just pick your components and their lengths.

### Number formatting

#### Options

The primary options properties for number formatting are as follows:

`style`

`"currency"`

,`"percent"`

, or`"decimal"`

(the default) to format a value of that kind.`currency`

- A three-letter currency code, e.g. USD or CHF. Required if
`style`

is`"currency"`

, otherwise meaningless. `currencyDisplay`

`"code"`

,`"symbol"`

, or`"name"`

, defaulting to`"symbol"`

.`"code"`

will use the three-letter currency code in the formatted string.`"symbol"`

will use a currency symbol such as $ or £.`"name"`

typically uses some sort of spelled-out version of the currency. (Firefox currently only supports`"symbol"`

, but this will be fixed soon.)`minimumIntegerDigits`

- An integer from 1 to 21 (inclusive), defaulting to 1. The resulting string is front-padded with zeroes until its integer component contains at least this many digits. (For example, if this value were 2, formatting 3 might produce “03”.)
`minimumFractionDigits`

,`maximumFractionDigits`

- Integers from 0 to 20 (inclusive). The resulting string will have at least
`minimumFractionDigits`

, and no more than`maximumFractionDigits`

, fractional digits. The default minimum is currency-dependent (usually 2, rarely 0 or 3) if`style`

is`"currency"`

, otherwise 0. The default maximum is 0 for percents, 3 for decimals, and currency-dependent for currencies. `minimumSignificantDigits`

,`maximumSignificantDigits`

- Integers from 1 to 21 (inclusive). If present, these override the integer/fraction digit control above to determine the minimum/maximum
[significant figures](https://en.wikipedia.org/wiki/Significant_figures)in the formatted number string, as determined in concert with the number of decimal places required to accurately specify the number. (Note that in a multiple of 10 the significant digits may be ambiguous, as in “100” with its one, two, or three significant digits.) `useGrouping`

- Boolean (defaulting to
`true`

) determining whether the formatted string will contain grouping separators (e.g. “,” as English thousands separator).

`NumberFormat`

also recognizes the esoteric, mostly ignorable `localeMatcher`

property.

#### Locale-centric options

Just as `DateTimeFormat`

supported custom numbering systems in the Unicode extension using the `nu`

key, so too does `NumberFormat`

. For example, the language tag for Chinese as used in China is `zh-CN`

. The value for the Han decimal numbering system is `hanidec`

. To format numbers for these systems, we tack a Unicode extension onto the language tag: `zh-CN-u-nu-hanidec`

.

For complete information on specifying the various numbering systems, see [the full NumberFormat documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NumberFormat).

#### Examples

`NumberFormat`

objects have a `format`

function property just as `DateTimeFormat`

objects do. And as there, the `format`

function is a bound function that may be used in isolation from the `NumberFormat`

.

Here are some examples of how to create `NumberFormat`

options for particular uses, with Firefox’s behavior. First let’s format some money for use in Chinese as used in China, specifically using Han decimal numbers (instead of much more common Latin numbers). Select the `"currency"`

style, then use the code for Chinese renminbi (yuan), grouping by default, with the usual number of fractional digits.

```
var hanDecimalRMBInChina =
new Intl.NumberFormat("zh-CN-u-nu-hanidec",
{ style: "currency", currency: "CNY" });
print(hanDecimalRMBInChina.format(1314.25)); // ￥ 一,三一四.二五
```

Or let’s format a United States-style gas price, with its peculiar thousandths-place 9, for use in English as used in the United States.

```
var gasPrice =
new Intl.NumberFormat("en-US",
{ style: "currency", currency: "USD",
minimumFractionDigits: 3 });
print(gasPrice.format(5.259)); // $5.259
```

Or let’s try a percentage in Arabic, meant for use in Egypt. Make sure the percentage has at least two fractional digits. (Note that this and all the other RTL examples may appear with different ordering in RTL context, e.g. ٤٣٫٨٠٪ instead of ٤٣٫٨٠٪.)

```
var arabicPercent =
new Intl.NumberFormat("ar-EG",
{ style: "percent",
minimumFractionDigits: 2 }).format;
print(arabicPercent(0.438)); // ٤٣٫٨٠٪
```

Or suppose we’re formatting for Persian as used in Afghanistan, and we want at least two integer digits and no more than two fractional digits.

```
var persianDecimal =
new Intl.NumberFormat("fa-AF",
{ minimumIntegerDigits: 2,
maximumFractionDigits: 2 });
print(persianDecimal.format(3.1416)); // ۰۳٫۱۴
```

Finally, let’s format an amount of [Bahraini dinars](https://en.wikipedia.org/wiki/Bahraini_dinar), for Arabic as used in Bahrain. Unusually compared to most currencies, Bahraini dinars divide into thousandths ([fils](https://en.wikipedia.org/wiki/Fils_%28currency%29)), so our number will have three places. (Again note that apparent visual ordering should be taken with a grain of salt.)

```
var bahrainiDinars =
new Intl.NumberFormat("ar-BH",
{ style: "currency", currency: "BHD" });
print(bahrainiDinars.format(3.17)); // د.ب. ٣٫١٧٠
```

### Collation

#### Options

The primary options properties for collation are as follows:

`usage`

`"sort"`

or`"search"`

(defaulting to`"sort"`

), specifying the intended use of this`Collator`

. (A`search`

collator might want to consider more strings equivalent than a`sort`

collator would.)`sensitivity`

`"base"`

,`"accent"`

,`"case"`

, or`"variant"`

. This affects how sensitive the collator is to characters that have the same “base letter” but have different accents/diacritics and/or case. (Base letters are locale-dependent: “a” and “ä” have the same base letter in German but are different letters in Swedish.)`"base"`

sensitivity considers only the base letter, ignoring modifications (so for German “a”, “A”, and “ä” are considered the same).`"accent"`

considers the base letter and accents but ignores case (so for German “a” and “A” are the same, but “ä” differs from both).`"case"`

considers the base letter and case but ignores accents (so for German “a” and “ä” are the same, but “A” differs from both). Finally,`"variant"`

considers base letter, accents, and case (so for German “a”, “ä, “ä” and “A” all differ). If`usage`

is`"sort"`

, the default is`"variant"`

; otherwise it’s locale-dependent.`numeric`

- Boolean (defaulting to
`false`

) determining whether complete numbers embedded in strings are considered when sorting. For example, numeric sorting might produce`"F-4 Phantom II", "F-14 Tomcat", "F-35 Lightning II"`

; non-numeric sorting might produce`"F-14 Tomcat", "F-35 Lightning II", "F-4 Phantom II"`

. `caseFirst`

`"upper"`

,`"lower"`

, or`"false"`

(the default). Determines how case is considered when sorting:`"upper"`

places uppercase letters first (`"B", "a", "c"`

),`"lower"`

places lowercase first (`"a", "c", "B"`

), and`"false"`

ignores case entirely (`"a", "B", "c"`

). (Note: Firefox currently ignores this property.)`ignorePunctuation`

- Boolean (defaulting to
`false`

) determining whether to ignore embedded punctuation when performing the comparison (for example, so that`"biweekly"`

and`"bi-weekly"`

compare equivalent).

And there’s that `localeMatcher`

property that you can probably ignore.

#### Locale-centric options

The main `Collator`

option specified as part of the locale’s Unicode extension is `co`

, selecting the kind of sorting to perform: phone book (`phonebk`

), dictionary (`dict`

), and [many others](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Collator).

Additionally, the keys `kn`

and `kf`

may, optionally, duplicate the `numeric`

and `caseFirst`

properties of the `options`

object. But they’re not guaranteed to be supported in the language tag, and `options`

is much clearer than language tag components. So it’s best to only adjust these options through `options`

.

These key-value pairs are included in the Unicode extension the same way they’ve been included for `DateTimeFormat`

and `NumberFormat`

; refer to those sections for how to specify these in a language tag.

#### Examples

`Collator`

objects have a `compare`

function property. This function accepts two arguments `<var>x</var>`

and `<var>y</var>`

and returns a number less than zero if `<var>x</var>`

compares less than `<var>y</var>`

, 0 if `<var>x</var>`

compares equal to `<var>y</var>`

, or a number greater than zero if `<var>x</var>`

compares greater than `<var>y</var>`

. As with the `format`

functions, `compare`

is a bound function that may be extracted for standalone use.

Let’s try sorting a few German surnames, for use in German as used in Germany. There are actually two different sort orders in German, phonebook and dictionary. Phonebook sort emphasizes sound, and it’s as if “ä”, “ö”, and so on were expanded to “ae”, “oe”, and so on prior to sorting.

```
var names =
["Hochberg", "Hönigswald", "Holzman"];
var germanPhonebook = new Intl.Collator("de-DE-u-co-phonebk");
// as if sorting ["Hochberg", "Hoenigswald", "Holzman"]:
// Hochberg, Hönigswald, Holzman
print(names.sort(germanPhonebook.compare).join(", "));
```

Some German words conjugate with extra umlauts, so in dictionaries it’s sensible to order ignoring umlauts (except when ordering words differing *only* by umlauts: *schon* before *schön*).

```
var germanDictionary = new Intl.Collator("de-DE-u-co-dict");
// as if sorting ["Hochberg", "Honigswald", "Holzman"]:
// Hochberg, Holzman, Hönigswald
print(names.sort(germanDictionary.compare).join(", "));
```

Or let’s sort a list Firefox versions with various typos (different capitalizations, random accents and diacritical marks, extra hyphenation), in English as used in the United States. We want to sort respecting version number, so do a numeric sort so that numbers in the strings are compared, not considered character-by-character.

```
var firefoxen =
["FireFøx 3.6",
"Fire-fox 1.0",
"Firefox 29",
"FÍrefox 3.5",
"Fírefox 18"];
var usVersion =
new Intl.Collator("en-US",
{ sensitivity: "base",
numeric: true,
ignorePunctuation: true });
// Fire-fox 1.0, FÍrefox 3.5, FireFøx 3.6, Fírefox 18, Firefox 29
print(firefoxen.sort(usVersion.compare).join(", "));
```

Last, let’s do some locale-aware string searching that ignores case and accents, again in English as used in the United States.

```
// Comparisons work with both composed and decomposed forms.
var decoratedBrowsers =
[
"A\u0362maya", // A͢maya
"CH\u035Brôme", // CH͛rôme
"FirefÓx",
"sAfàri",
"o\u0323pERA", // ọpERA
"I\u0352E", // I͒E
];
var fuzzySearch =
new Intl.Collator("en-US",
{ usage: "search", sensitivity: "base" });
function findBrowser(browser)
{
function cmp(other)
{
return fuzzySearch.compare(browser, other) === 0;
}
return cmp;
}
print(decoratedBrowsers.findIndex(findBrowser("Firêfox"))); // 2
print(decoratedBrowsers.findIndex(findBrowser("Safåri"))); // 3
print(decoratedBrowsers.findIndex(findBrowser("Ãmaya"))); // 0
print(decoratedBrowsers.findIndex(findBrowser("Øpera"))); // 4
print(decoratedBrowsers.findIndex(findBrowser("Chromè"))); // 1
print(decoratedBrowsers.findIndex(findBrowser("IË"))); // 5
```

### Odds and ends

It may be useful to determine whether support for some operation is provided for particular locales, or to determine whether a locale is supported. `Intl`

provides `supportedLocales()`

functions on each constructor, and `resolvedOptions()`

functions on each prototype, to expose this information.

```
var navajoLocales =
Intl.Collator.supportedLocalesOf(["nv"], { usage: "sort" });
print(navajoLocales.length > 0
? "Navajo collation supported"
: "Navajo collation not supported");
var germanFakeRegion =
new Intl.DateTimeFormat("de-XX", { timeZone: "UTC" });
var usedOptions = germanFakeRegion.resolvedOptions();
print(usedOptions.locale); // de
print(usedOptions.timeZone); // UTC
```

## Legacy behavior

The ES5 `toLocaleString`

-style and `localeCompare`

functions previously had no particular semantics, accepted no particular options, and were largely useless. So the i18n API reformulates them in terms of `Intl`

operations. Each method now accepts additional trailing ` locales` and

`arguments, interpreted just as the`

`options`

`Intl`

constructors would do. (Except that for [and](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleTimeString)

`toLocaleTimeString`

[, different default components are used if options aren’t provided.)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString)

`toLocaleDateString`

For brief use where precise behavior doesn’t matter, the old methods are fine to use. But if you need more control or are formatting or comparing many times, it’s best to use the `Intl`

primitives directly.

## Conclusion

Internationalization is a fascinating topic whose complexity is bounded only by the varied nature of human communication. The Internationalization API addresses a small but quite useful portion of that complexity, making it easier to produce locale-sensitive web applications. Go use it!

(And a special thanks to Norbert Lindenberg, Anas El Husseini, Simon Montagu, Gary Kwong, Shu-yu Guo, Ehsan Akhgari, the people of [#mozilla.de](ircs://irc.mozilla.org:6697/mozilla.de), and anyone I may have forgotten [sorry!] who provided feedback on this article or assisted me in producing and critiquing the examples. The English and German examples were the limit of my knowledge, and I’d have been completely lost on the other examples without their assistance. Blame all remaining errors on me. Thanks again!)

## About
[
Jeff Walden ](http://whereswalden.com/)

Mozillian since ~2003, SpiderMonkey hacker since ~2006. Dabbler in all areas of Gecko. General standards wonk.

## 14 comments

VincentDecember 12th, 2014 at 00:12ToniDecember 12th, 2014 at 09:21Jeff WaldenDecember 12th, 2014 at 11:32VincentDecember 15th, 2014 at 00:20JamonDecember 14th, 2014 at 12:04Jeff WaldenDecember 14th, 2014 at 14:06JamonDecember 14th, 2014 at 14:32Jeff WaldenJanuary 23rd, 2015 at 05:39Claudio CicaliDecember 18th, 2014 at 00:52Hao Anh LeDecember 19th, 2014 at 10:43Thiago FDecember 20th, 2014 at 06:00adJanuary 4th, 2015 at 09:43Jeff WaldenJanuary 23rd, 2015 at 05:34JSJanuary 8th, 2015 at 07:48