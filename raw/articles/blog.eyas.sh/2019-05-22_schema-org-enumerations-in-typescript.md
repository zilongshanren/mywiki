---
title: Schema.org Enumerations in TypeScript
url: https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/
author: Eyas Sharaiha
published: '2019-05-22'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Last time, we talked about
[modeling the Schema.org class hierarchy in TypeScript](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/).
We ended up with an elegant, recursive solution that treats any type `Thing`

as
a `"@type"`

-discriminated union of `ThingLeaf`

and all the direct sub-classes of
the type. The next challenge in the journey of building TypeScript typings for
the Schema.org vocabulary is modeling
[Enumeration](https://schema.org/Enumeration)s.

### Learning from Examples

Let’s look at a few examples from the Schema.org website to get a better sense of what Enumerations look like.

First up, I looked at `PaymentStatusType`

, which can take any one of these
values: `PaymentAutomaticallyApplied`

, `PaymentComplete`

, `PaymentDeclined`

,
`PaymentDue`

, or `PaymentPastDue`

. `PaymentStatusType`

is used in the
`paymentStatus`

property on the `Invoice`

class.

Here’s an excerpt from an example of an invoice:

```
{
"@context": "http://schema.org/",
"@type": "Invoice",
// ...
"paymentStatus": "http://schema.org/PaymentComplete",
"referencesOrder": [
// ...
]
}
```


Here, the *value* of an Enumeration appears as an **absolute**
[IRI](https://www.w3.org/TR/json-ld/#iris).

Looking at other examples, however, such as `GamePlayMode`

which appears in
`playMode`

on `VideoGame`

shows up differently:

```
{
"@context": "http://schema.org",
"@type": "VideoGame",
// ...
"playMode": "SinglePlayer"
// ...
}
```


Here, `SinglePlayer`

shows up as an IRI reference relative to the current
`"@context"`

. The exact mechanics of `"@context"`

are a bit cumbersome to
describe inline here, but I’ll be discussing them in a future post. Suffice to
say, *in this example*, if your context is `"http://schema.org"`

then you can
use `"SinglePlayer"`

in contexts where an IRI reference is expected as a
*relative* IRI reference, resolving to `"http://schema.org/SinglePlayer"`

.

Therefore, the *same* enumeration value can be represented by *multiple* strings
that happen to resolve to the same thing. *But*, for us to know the set of all
possible strings we can use to represent an enumeration value, we’ll need to
know the `@context`

used. As a matter of fact, this also applies to the
`"@type"`

property, so we’ve been assuming a context of `http[s]://schema.org`

all along.

The [schema-dts](https://github.com/google/schema-dts) uses a smarter approach:
when using the `schema-dts-gen`

CLI tool, the user can specify exactly what
their `@context`

should be. Then, the `"@type"`

s produced are rendered as the
appropriate relative IRI string literals, if the context allows it, and
otherwise an absolute IRI. The pre-packaged `schema-dts`

package, uses
`"https://schema.org"`

as its context.

#### Choosing our Representation

Say the goal of the typings is to easily allow writing *new* JSON-LD. Then,
clarity might be desirable: choose to only allow absolute IRIs or only allow
relative IRIs (when permitted). This way, redundant but still valid JSON-LD
would be rejected by the type checker, but completions would be much cleaner and
all new code would look the same.

On the other hand, say the goal of the typings is to easily validate existing
JSON-LD. Then, we probably want it to *only* emit type errors on invalid string
literals. That is, we’ll probably want our typings to include all plausible ways
of referencing an enum value, given a @context.

For now, we’ll choose to standardize on just absolute IRIs (like
`http://schema.org/SinglePlayer`

) since those are the most common *and* the
clearest.

So far, one might think of representing enums simply:

```
enum GamePlayMode {
SinglePlayer = "https://schema.org/SinglePlayer",
MultiPlayer = "https://schema.org/MultiPlayer",
CoOp = "https://schema.org/CoOp",
}
```


or perhaps:

```
type GamePlayMode =
| "https://schema.org/SinglePlayer"
| "https://schema.org/MultiPlayer"
| "https://schema.org/CoOp";
```


both of these are equally valid, though using `const enum`

s in the first
approach might more desirable.

### Enumerations can have other values…

If only it were that simple. For example, take `DeliveryMethod`

which,
[in this example](https://schema.org/ReceiveAction#ReceiveAction-gen-162) is
represented as so:

```
"deliveryMethod": {
"@type": "DeliveryMethod",
"name": "http://purl.org/goodrelations/v1#UPS"
},
```


That’s right. `DeliveryMethod`

still extends `Enumeration`

, which *is* a class
type. Enumeration itself extends `Intangible`

which extends `Thing`

.

Our representation will need to change (accounting to the insights learned from
[the class hierarchy article](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/)),
then:

```
const enum GamePlayModeEnum {
SinglePlayer = "https://schema.org/SinglePlayer",
MultiPlayer = "https://schema.org/MultiPlayer",
CoOp = "https://schema.org/CoOp",
}
type GamePlayModeBase = EnumerationBase; // Doesn't extend other properties
interface GamePlayModeLeaf extends GamePlayModeBase {
"@type": "GamePlayMode";
}
type GamePlayMode = GamePlayModeEnum | GamePlayModeLeaf;
```


Here, we allow for a `GamePlayMode`

to be either the Enum value (represented
either as a union of string literals or a const enum) or the Leaf value.

### Enums can have sub-classes

The `DeliveryMethod`

example also shows us sub-types are possible. Note that
`ParcelService`

, for instance, is a class type (albeit not an interesting one;
it adds no properties).

This means we’ll need to include sub-classes in our final type union of the enum, just as we did with Classes in general.

### Enums can extend regular classes

A regular class can have sub-classes that themselves are enumerations. Let’s
take a look at the `PhysicalExam`

, for an example. `PhysicalExam`

is an enum
type that extends a non-enum `MedicalProcedure`

(notice how Schema.org models
that as having two parents: `MedicalEnumeration`

*and* `MedicalProcedure`

).

Using the recursive method defined previously, this means that:

`MedicalProcedure`

is a union of it’s “leaf” class, and all it’s subclasses, which includes “Enums”`PhysicalExam`

and other enum sub-classes are defined as above: a union of a true Enum type, a leaf type, and all direct sub-classes.

### Putting it all Together

Essentially, we can see that Enumerations really are just classes that can also
take a special value (an IRI reference). All of the rules of classes we have
learned before still apply, but now there’s an addition: our final union
contains an `XyzEnum`

type in the union, in addition to `XyzLeaf`

and all
sub-classes.

Take a look at the `Audience`

enum for example, and notice it’s very nested
nature:

![Schema.org Audience has a very nested nature, with 4 direct subclasses, one of which is an enum, with subclasses of it's own.](../../assets/42555f0ac28c340a.img)

The rules provided so far compose nicely to allow us to represent this complex structure. I’ll leave this as an exercise to the reader to see how the TypeScript structure ends up here, but isn’t too different from the final result you’ll see in schema-dts.