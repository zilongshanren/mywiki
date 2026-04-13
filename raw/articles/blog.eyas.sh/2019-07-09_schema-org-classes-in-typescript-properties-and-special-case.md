---
title: 'Schema.org Classes in TypeScript: Properties and Special Cases'
url: https://blog.eyas.sh/2019/07/schema-org-classes-in-typescript-properties-and-special-cases/
author: Eyas Sharaiha
published: '2019-07-09'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

In our quest to model Schema.org classes in TypeScript, we’ve so far managed to
model the
[type hierarchy](https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/),
[scalar](https://blog.eyas.sh/2019/07/schema-org-datatype-in-typescript-structural-typing-doesnt-cut-it/)`DataType`

[values](https://blog.eyas.sh/2019/07/schema-org-datatype-in-typescript-structural-typing-doesnt-cut-it/),
and [enums](https://blog.eyas.sh/2019/05/schema-org-enumerations-in-typescript/). The big piece that
remains, however, is representing what’s actually *inside* of the class: it’s
properties.

After all, what it means for a JSON-LD literal to have `"@type"`

equal to
`"Person"`

is that certain properties — e.g. `"birthPlace"`

or `"birthDate"`

,
among others — can be expected to be present on the literal. More than their
potential presence, Schema.org defines *a meaning* for these properties, and the
range of types their values could hold.

### The easy case: Simple Properties

You can download the entire vocabulary specification of Schema.org, most of
which describes properties on these classes. For each property, Schema.org will
tell us it’s *domain* (what classes have this property) and *range* (what types
can its *values* be). For example, the `name`

property specification shows that
it is available on the class `Thing`

, and has type `Text`

. One might represent
this knowledge as follows:

```
interface ThingBase {
name: Text;
}
```


Linked Data, it turns out, is a bit richer than that, allowing us to express situations where a property has multiple values. In JSON-LD, this is represented by an array as the value of the property. Therefore:

```
interface ThingBase {
name: Text | Text[];
}
```


### Multiple Property Types

Often times, however, the *range* of a particular property is any one of a
number of types. For example, the property `image`

on `Thing`

can be an
`ImageObject`

or `URL`

. Note, also, that nothing in JSON-LD necessitates that
all potential values of `image`

have the same type.

In other words, if we want to represent `image`

on `ThingBase`

, we have:

```
interface ThingBase {
name: Text | Text[];
image: ImageObject | URL | (ImageObject | URL)[];
}
```


### Properties are Optional

In JSON-LD, all properties are optional. In practice Schema.org cares about
`"@type"`

being defined for all *classes*, but does not otherwise define any
other properties as being required. This is sometimes complicated as specific
*search engines* require some set of properties on a class.

```
interface ThingBase {
name?: Text | Text[];
image?: ImageObject | URL | (ImageObject | URL)[];
}
```


### Properties Can Supersede Others in the Vocabulary

As Schema.org matures, it’s vocabulary changes. Not all of these changes will be
additive (adding a new type, or a new type on an existing property). Some will
involve adding a new type or property intended to *replace* another.

For example, `area`

was a property on `BroadcastService`

describing a `Place`

the service applies to. Turns out, a lot of other businesses also apply to a
specific area. `serviceArea`

replaced `area`

, and instead of applying to
`BroadcastService`

, it applied to its parent, `Service`

. In addition,
`serviceArea`

can also apply to `Organization`

and `ContactPoint`

(something
`area`

never did). In addition to being just a `Place`

, `serviceArea`

can be an
`AdministrativeArea`

or an arbitrary `GeoShape`

.

Later on, `serviceArea`

was replaced by `areaServed`

, which also included a
freeform `Text`

as a possible value, and applied to a few more objects.

When a property replaces another, it *supersedes* it (inversely, the other
property is *superseded by* the new one). These changes keep existing Schema.org
JSON-LD backwards-compatible. A property `p2`

superseding `p1`

will generally
imply:

`p2`

is available on all types`p1`

was available on. (`p2`

’s domain is strictly*wider*).

This includes (a) additional types in the domain, or (b) the domain changing to a parent class, for example.`p2`

includes all possible types of`p1`

(`p2`

’s range is strictly*wider*).

Typically, new data will be written with `p2`

, but the intention is that any old
data written using `p1`

continues to be valid.

In TypeScript, we can use the `@deprecated`

JSDoc annotation to recommend using
a new property instead. We can go further and simply skip all deprecated
properties (properties that are superseded by one or more properties) if we
wanted to.

The story of `area`

, `serviceArea`

, and `areaServed`

can be partially summarized
as follows:

```
interface BroadcastServiceBase extends OrganizationBase {
/** @deprecated Superseded by serviceArea */
"area"?: Place | Place[];
}
interface OrganizationBase {
/** @deprecated Superseded by areaServed *
"serviceArea"?: AdministrativeArea | GeoShape | Place |
(AdministrativeArea | GeoShape | Place)[];
"areaServed"?: AdministrativeArea | GeoShape | Place | Text |
(AdministrativeArea | GeoShape | Place | Text)[];
}
```


### Things Fall Apart

#### Multiple Types

`"@type"`

is just another property (albeit it has speical meaning).

JSON-LD permits a node to have multiple `"@type"`

s as well, and search engines
are happy to accept multiple types (at least for some nodes). In practice, a
node having two types means that it can have properties on both types. For
example, this is valid:

```
{
"@type": ["Organization", "Person"],
"birthDate": "1980-01-01",
"foundingDate": "2000-01-01"
}
```


In TypeScript, discriminating a union on an array seems to be hard, and it
becomes a bit clunky to define. For now, our TypeScript definitions will not
allow multiple `@type`

values.

#### Sub-Properties

Schema.org takes advantage of the RDF concept of a sub-property:

If a property P is a subproperty of property P’, then all pairs of resources which are related by P are also related by P’


Simply put, a sub-property is *a more specific version* of a property.

For example, `image`

exists on `Thing`

, but has two sub-properties: `logo`

,
which exists on `Brand`

, `Organization`

, and a few other types, and `photo`

,
which exists on a `Place`

.

One thing I expected is *not* to be able to specify a super-property on a node
whose type has the sub-property available. I.e., if I’m describing a `Brand`

,
it’s `logo`

will sufficiently describe `image`

, thereby serving no meaning to
specify `image`

.

That’s not *quite* true, though, a sub-property *implying* a property still
leaves room for the property itself to be available (an `Organization`

can have
multiple `image`

s, one of which is its `logo`

).

And while that *should be* true (by the RDF specification), turns
[even that isn’t true](https://github.com/schemaorg/schemaorg/issues/1896) in
Schema.org. Some sub-properties have more general types than their
super-properties, e.g. `photo`

can be a `Photograph`

, but it’s super-property,
`image`

cannot.

So here, we simply punt.

### Special Cases

Reading Schema.org documentation, you might expect as I did that there are two
distinct hierarchies of data: `Thing`

(aka classes/node types) and `DataType`

(aka values/scalars/primitives). That’s definitely not true in JSON-LD in
general, where many values are untyped to begin with, specified using an `"@id"`

reference, or a string. Schema.org implies it imposes a tighter requirement, and
describes these hierarchies dis-jointly, but that turns out not to be true.

Turns out, some types, like `Distance`

are in the `Thing`

hierarchy, but expect
string values (in the case of `Distance`

, those would take the form `"5 in"`

or
`"2.3 cm"`

, etc.).

We might consider having our typings include `string`

(or `Text`

?) for all of
our classes. To encourage semantically specifying properties, however, I decided
to only allow `string`

on a subset of our nodes.

```
type Distance = DistanceLeaf | string;
```


## Conclusion

Schema.org is a vocabulary designed in an inherently human way. This sometimes have repercussions of being thoughtful. Yet, just as often, it means that the semantics have evolved in a way that is inconsistent. The result is often dissatisfying: relations that are defined but don’t hold in practice, objects that are described with textual comments but have no formal relations specifying them, distances that are described as nodes, and many others. These inconsistencies often lead to hacks when trying to represent the vocabulary in TypeScript.

Yet, it’s important not to lose track of *why* modeling Schema.org in TypeScript
to begin with. The lack of tooling around Schema.org (specifically in IDEs when
writing out a specific piece of data), is precisely the need we’re filling in.
But ultimately, adding *structure* to an ontology that is largely decided by a
loose set of *guidelines* will be lossy.

The question remains: is the trade-off worth it?

For my purposes, [schema-dts](https://github.com/google/schema-dts) has helped
me tremendously over the past several months.