---
title: 'Schema.org DataType in TypeScript: Structural Typing Doesn''t Cut It'
url: https://blog.eyas.sh/2019/07/schema-org-datatype-in-typescript-structural-typing-doesnt-cut-it/
author: Eyas Sharaiha
published: '2019-07-02'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Schema.org has a concept of a `DataType`

, things like `Text`

, `Number`

, `Date`

,
etc. In JSON-LD, we represent these as strings or numbers, rather than array or
object literals. This data could describe the name of a `Person`

, a check-in
date and time for a `LodgingReservation`

, a URL of a `Corporation`

, publication
date of an `Article`

, etc. As we’ll see, the Schema.org `DataType`

hierarchy is
far richer than TypeScript’s type system can accommodate. In this article, we’ll
go over the `DataType`

hierarchy and explore how much type checking we *can*
provide.

We saw in the first installment how
[TypeScript’s type system makes expressing JSON-LD describing Schema.org class structure very elegant](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/).
The story got slightly more clouded when we
[introduced Schema.org Enumerations](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/).

### Schema.org Data Types

Let’s take a look at the
[full](https://schema.org/docs/full.html#datatype_tree)`DataType`

[tree according Schema.org](https://schema.org/docs/full.html#datatype_tree):

Boolean’s look quite similar to enums, with `http://schema.org/True`

and
`http://schema.org/False`

as it’s two possible IRI values (depending on
`@context`

, those can of course be represented as relative IRIs instead) or
their HTTPS equivalents.

`Number`

and descendants are just JSON / JavaScript numbers. `Float`

indicates
the JSON number will have a floating point precision, whereas `Integer`

tells us
to expect a whole number. On its own right, JavaScript does not distinguish
floats and integers as separate types, and neither does TypeScript. While
TypeScript supports the idea of
* literal types*,
specifying a type as

*all possible integers*or

*all possible floating point numbers*isn’t expressible.

`Text`

and descendants are just JSON / JavaScript strings. Similar to above,
TypeScript does not support more specific string types based on their pattern
(RegEx or otherwise).

`Date`

, `DateTime`

, and `Time`

are all expressed as JSON / JavaScript strings as
well. Those are expected to be formatted in
[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date or time formats, or
similar.

Simply put, TypeScript lacks a cohesive type hierarchy under `string`

and
`number`

that can sufficiently express `Date`

, `DateTime`

, `Time`

, and the
sub-classes of `Number`

and `Text`

. Only `Number`

, `Text`

, and Booleans are
sufficiently represented by the type system.

### Biting the Bullet

So far, the invariant we have tried to maintain with our TypeScript definition
is that: *Every JSON literal matching the Schema type is valid Schema.org
JSON-LD literal*
([In the case of enums, we even accepted a](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/)[subset](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/)[of legal literals](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/).)

One option is to introduce factories, e.g. a `date(2019, 01, 01)`

or similar to
create a matching `Date`

type. Part of the original goal of these type
definitions, however, is to allow the developer to write literals as they would
in regular JSON-LD, and just have schema-dts function as a type checker on top
of these.

With that, I decided that it is more desirable to bite the bullet (hoping at
least that the Integer and Float case to be
[resolved by the TypeScript team](https://github.com/Microsoft/TypeScript/issues/15480))
and leave my typings *more* permissive than valid Schema.org, for once.

The implication, here, is that the typings for the basic data types are equivalent to something like this:

```
// Text and Derivatives:
export type Text = string;
export type CssSelectorType = Text;
export type URL = Text;
export type XPathType = Text;
// Number and Derivatives:
export type Number = number;
export type Integer = Number;
export type Float = Number;
// Date, etc.
export type Date = string;
// Booleans:
export type Boolean {
True = "https://schema.org/True",
False = "https://schema.org/False",
}
```


While run-time behaviors can give us nicer properties, with TypeScript, this is the best we can do compile-time.