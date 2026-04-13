---
title: 'Modeling Schema.org Schema with TypeScript: The Power and Limitations of the
  TypeScript Type System'
url: https://blog.eyas.sh/2019/05/modeling-schema-org-schema-with-typescript-the-power-and-limitations-of-the-typescript-type-system/
author: Eyas Sharaiha
published: '2019-05-09'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Recently, I published
[ schema-dts](https://opensource.google.com/projects/schema-dts)
(

[npm](https://www.npmjs.com/package/schema-dts),

[GitHub](https://github.com/google/schema-dts)), an open source library that models JSON-LD Schema.org in TypeScript. A big reason I wanted to do this project is because I knew some TypeScript type system features, such as discriminated type unions, powerful type inference, nullability checking, and type intersections, present an opportunity to both model what Schema.org-conformant JSON-LD looks like, while also providing ergonomic completions to the developer.

In a series of posts, I’ll go over some of the Structured Data concepts that lent themselves well to TypeScript’s type system, and those concepts that didn’t. First up: the type hierarchy of JSON-LD Schema.org Schema, and how can be represented in TypeScript.

## Modeling the Schema.org class structure with the TypeScript Type System

Schema.org JSON-LD node objects are always *typed* (that is, they have a `@type`

property that points to some IRI–a string–describing it). Given a `@type`

you
know all the properties that are defined on a particular object. Object types
inherit from each other. For example, `Thing`

in Schema.org has a property
called `name`

, and `Person`

is a subclass of `Thing`

that defines additional
properties such as `birthDate`

, and inherits all the properties of `Thing`

such
as name. `Thing`

has other sub-classes, like `Organization`

, with it’s own
properties, like `logo`

.

Let’s use this minimal example to try a few approaches:

### 1. Modeling each with inheritance

```
interface Thing {
name: string;
}
```


```
interface Person extends Thing {
"@type": "Person";
birthDate: string;
}
```


```
interface Organization extends Thing {
"@type": "Organization";
logo: string;
}
```


If we had a `const something: Thing`

, then we could assign it to a `Thing`

,
`Person`

, or `Organization`

. So that’s a start! But there are a few problems:

- Using type
`Thing`

on it’s own isn’t quite right, as it is missing a`@type`

annotation.*More broadly*, non-leaf types (types that a super-class of another) are not representible this way. - Writing object literals inline will cause TypeScript’s excess property
checks to complain that
`"@type"`

,`"birthDate"`

, and`"logo"`

are not a known property of`Thing`

. - Lacking completions for
`"@type"`

. If I was filling in a complex nested object whose property had some type, it would be great if I can look for helpful completions on`"@type"`

and see what allowed types exist for a certain property.

### 2. Modeling each object individually

```
interface Thing {
"@type": "Thing";
name: string;
}
```


```
interface Person {
"@type": "Person";
name: string;
birthDate: string;
}
```


```
interface Organization {
"@type": "Organization";
name: string;
logo: string;
}
```


Another approach altogether is to fully roll all parent types of each object separately. This solves the first problem, where types that are a superclass of other types can still be represented, but introduces (and exacerbates) the existing problems.

- “Sub-classes” are not assignable to their parent types. For example, an
object of type
`Person`

cannot be assigned to a variable of type`Thing`

. It also cannot be used as the value of a property of a super-class type.

### 3. Modeling super-classes as discriminated unions

```
type Thing = Person | Organization;
```


```
interface Person {
"@type": "Person";
name: string;
birthDate: string;
}
```


```
interface Organization {
"@type": "Organization";
name: string;
logo: string;
}
```


By defining `Thing`

(or, generally, a parent class) as a union of it’s
sub-classes, it’ll behave like a discriminated union. It’s *discriminated*
because each possible type within the union has a property (`@type`

) that is
sufficient to tell the compiler which type of the union that object is.

Discriminated unions allow us to achieve assignability, completions (typing
’`"@type": "`

’ inside of a `Thing`

will suggest `"Person"`

or `"Organization"`

),
and proper type checking without tripping up excess property checking when
writing properties of a sub-class.

The problem? We’re back to not being able to individually express a type with
sub-classes (e.g. `Thing`

) individually. Back to the drawing board.

### 4. Hybrid Approach: Modeling parent classes within unions

When we think of the `Thing`

Schema.org class, three separable concepts come to
mind. It could be a node

- with the actual
`"@type": "Thing"`

- that has all the properties of
`Thing`

- that has a
`"@type"`

equal to that of any of the (direct or indirect) sub-classes of`Thing`

.

(1) can be represented as a specific object literal; (2) can be represented as some type to be extended (or intersected); and (3) can be represented as a discriminated union.

![Graph illustration of TypeScript interfaces described in the nest 4 code blocks.](../../assets/61c890bee21c95ef.img)

```
interface ThingBase {
name: string;
}
```


```
interface ThingLeaf extends ThingBase {
"@type": "Thing";
}
```


```
interface Person extends ThingBase {
"@type": "Person";
birthDate: string;
}
```


```
interface Organization extends ThingBase {
"@type": "Organization";
logo: string;
}
```


```
type Thing = ThingLeaf | Person | Organization;
```


Here, `Thing`

, `Person`

, and `Organization`

can all be used independently. And
we have the properties we want:

- A
`Person`

or`Organization`

is assignable to a`Thing`

. - A
`Thing`

can exist with`"@type": "Thing"`

. `Thing`

is a discriminated union and can suggest`"Thing"`

,`"Person"`

, or`"Organization"`

when typing a`"@type"`

value.

TypeScript will also type check our deeply nested properties according to their types.

Best thing about this approach, it’s recursive. Consider, for example, two
sub-types of `Organization`

: `Airline`

and `Corporation`

. Those can be modeled
recursively as the graph shows below.

![The class hierarchy is composable by making sure "Base" types extend other "Base" types, and union types aggregate all "complete" types, in addition to leaf types.](../../assets/10d50d66880aca31.img)

### Getting to a Working System

When schema-dts generates types, it uses a very similar model as described
above. Notably different, is that I use type intersections (`A & B`

) instead of
interfaces (`interface B extends A`

) to simplify some of the nested expressions
that show up.

In schema-dts, every “node” type is represented like `Thing`

in that it has a
“base” type, and represents the “real” type as a union of a leaf and other
sub-classes.

In future articles, I’ll discuss how to represent “enums”, the limitations of the TypeScript type system with data types, and how to represent properties.