---
title: 'Advent 2021: TypeScript'
url: https://anteru.net/blog/2021/advent-2021-typescript
published: '2021-12-06'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Web development is always tied to one language – JavaScript. You may or may not like it, but JavaScript is really all there is and ultimately you need to produce JavaScript to do anything reasonably interesting on your web site. However, I never got the hang of JavaScript, and I struggled and continue to struggle writing anything bigger than a few functions in “plain” JavaScript. Early on in my web development career I used [CoffeeScript](https://coffeescript.org/) which is a nice(r) little language that compiles down to JavaScript. It worked, I was more productive than with JavaScript, but CoffeeScript never ended up being super popular unfortunately.

Fast forward a few years and a new language appeared, from the same language designer who brought us [C#](https://anteru.net/blog/2021/advent-2021-csharp), called [TypeScript](https://www.typescriptlang.org/). I’ve used TypeScript quite early on and it was “love at first sight”. The gradual typing system was *the* genius part of it, as it meant that you could continue to write what looked like JavaScript but with type constraints added. That was however only half of the reason why TypeScript is great. The other half was fantastic tooling from day one. It’s hard to stress how important the tooling is for TypeScript. Thanks to strong typing, you can get good completion, helpful error messages, and clean code, which for me completely changed the way I write web applications.

The short summary of TypeScript is that it’s an object-oriented programming language with a strong but optional type system. It looks and feels like a mix of C# and JavaScript, but it really never gets in your way. If you need to interop with JavaScript there’s always the `any`

escape hatch, and it does compile down to JavaScript so your clients will never notice. However, it does crazy things for you like turning this code:

```
let minValue = parseFloat (element?.getAttribute ('data-filter-range-min') ?? "0");
let maxValue = parseFloat (element?.getAttribute ('data-filter-range-max') ?? "0");
```


and converting it to this JavaScript nobody would write voluntarily:

```
let minValue = parseFloat((_a = element === null || element === void 0 ? void 0 : element.getAttribute('data-filter-range-min')) !== null && _a !== void 0 ? _a : "0");
let maxValue = parseFloat((_b = element === null || element === void 0 ? void 0 : element.getAttribute('data-filter-range-max')) !== null && _b !== void 0 ? _b : "0");
```


It quite literally is JavaScript just without the pain of JavaScript. If you haven’t used it, and you’re doing web development, do yourself a favor and give it a try! For me, TypeScript was a complete game changer and I can’t imagine doing web development without it.