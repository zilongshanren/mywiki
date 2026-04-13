---
title: Implications of Rewriting a Browser Component in Rust – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/02/rewriting-a-browser-component-in-rust/
author: Diane Hosfelt
published: '2019-02-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*The previous posts in this Fearless Security series examine memory safety and thread safety in Rust. This closing post uses the Quantum CSS project as a case study to explore the real world impact of rewriting code in Rust.*

The style component is the part of a browser that applies CSS rules to a page. This is a top-down process on the DOM tree: given the parent style, the styles of children can be calculated independently—a perfect use-case for parallel computation. By 2017, Mozilla had made two previous attempts to parallelize the style system using C++. Both had failed.

*Quantum CSS* resulted from a need to improve page performance. Improving security is a happy byproduct.

![Rewrites code to make it faster; also makes it more secure](../../assets/82e60d110a9fcd74.jpg)


There’s a large overlap between memory safety violations and security-related bugs, so we expected this rewrite to reduce the attack surface in Firefox. In this post, I will summarize the potential security vulnerabilities that have appeared in the styling code since [Firefox’s initial release in 2002](https://en.wikipedia.org/wiki/Firefox_version_history). Then I’ll look at what could and could not have been prevented by using Rust.

Over the course of its lifetime, there have been 69 security bugs in Firefox’s style component. If we’d had a time machine and could have written this component in Rust from the start, 51 (73.9%) of these bugs would not have been possible. While Rust makes it easier to write better code, it’s not foolproof.

## Rust

Rust is a modern systems programming language that is type- and memory-safe. As a side effect of these safety guarantees, Rust programs are also known to be thread-safe at compile time. Thus, Rust can be a particularly good choice when:

✅ processing untrusted input safely.

✅ introducing parallelism to improve performance.

✅ integrating isolated components into an existing codebase.

However, there are classes of bugs that Rust explicitly does not address—particularly correctness bugs. In fact, during the Quantum CSS rewrite, engineers accidentally reintroduced a critical security bug that had previously been patched in the C++ code, regressing the fix for [bug 641731](https://bugzilla.mozilla.org/show_bug.cgi?id=641731). This allowed global history leakage via SVG image documents, resulting in [bug 1420001](https://bugzilla.mozilla.org/show_bug.cgi?id=1420001). As a trivial history-stealing bug, this is rated security-high. The original fix was an additional check to see if the SVG document was being used as an image. Unfortunately, this check was overlooked during the rewrite.

While there were automated tests intended to catch `:visited`

rule violations like this, in practice, they didn’t detect this bug. To speed up our automated tests, we temporarily turned off the mechanism that tested this feature—tests aren’t particularly useful if they aren’t run. The risk of re-implementing logic errors can be mitigated by good test coverage (and actually running the tests). There’s still a danger of introducing new logic errors.

As developer familiarity with the Rust language increases, best practices will improve. Code written in Rust will become even more secure. While it may not prevent all possible vulnerabilities, Rust eliminates an entire class of the most severe bugs.

## Quantum CSS Security Bugs

Overall, bugs related to memory, bounds, null/uninitialized variables, or integer overflow would be prevented by default in Rust. The miscellaneous bug I referenced above would not have been prevented—it was a crash due to a failed allocation.

### Security bugs by category

All of the bugs in this analysis are related to security, but only 43 received official security classifications. (These are assigned by Mozilla’s security engineers based on educated “exploitability” guesses.) Normal bugs might indicate missing features or problems like crashes. While undesirable, crashes don’t result in data leakage or behavior modification. Official security bugs can range from low severity (highly limited in scope) to critical vulnerability (might allow an attacker to run arbitrary code on the user’s platform).

There’s a significant overlap between memory vulnerabilities and severe security problems. Of the 34 critical/high bugs, 32 were memory-related.

### Security rated bug breakdown

## Comparing Rust and C++ code

[Bug 955914](https://bugzilla.mozilla.org/show_bug.cgi?id=955913) is a heap buffer overflow in the `GetCustomPropertyNameAt`

function. The code used the wrong variable for indexing, which resulted in interpreting memory past the end of the array. This could either crash while accessing a bad pointer or copy memory to a string that is passed to another component.

The ordering of all [CSS properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Properties_Reference) (both longhand and custom) is stored in an array, `mOrder`

. Each element is either represented by its CSS property value or, in the case of custom properties, by a value that starts at `eCSSProperty_COUNT`

(the total number of non-custom CSS properties). To retrieve the name of a custom property, first, you have to retrieve the custom property value from `mOrder`

, then access the name at the corresponding index of the `mVariableOrder`

array, which stores the custom property names in order.

### Vulnerable C++ code:

```
void GetCustomPropertyNameAt(uint32_t aIndex, nsAString& aResult) const {
MOZ_ASSERT(mOrder[aIndex] >= eCSSProperty_COUNT);
aResult.Truncate();
aResult.AppendLiteral("var-");
aResult.Append(mVariableOrder[aIndex]);
```


The problem occurs at line 6 when using `aIndex`

to access an element of the `mVariableOrder`

array. `aIndex`

is intended for use with the `mOrder`

array not the `mVariableOrder`

array. The corresponding element for the custom property represented by `aIndex`

in `mOrder`

is actually `mOrder[aIndex] - eCSSProperty_COUNT`

.

### Fixed C++ code:

```
void Get CustomPropertyNameAt(uint32_t aIndex, nsAString& aResult) const {
MOZ_ASSERT(mOrder[aIndex] >= eCSSProperty_COUNT);
uint32_t variableIndex = mOrder[aIndex] - eCSSProperty_COUNT;
aResult.Truncate();
aResult.AppendLiteral("var-");
aResult.Append(mVariableOrder[variableIndex]);
}
```


### Equivalent Rust code

While Rust is similar to C++ in some ways, idiomatic Rust uses different abstractions and data structures. Rust code will look very different from C++ (see below for details). First, let’s consider what would happen if we translated the vulnerable code as literally as possible:

```
fn GetCustomPropertyNameAt(&self, aIndex: usize) -> String {
assert!(self.mOrder[aIndex] >= self.eCSSProperty_COUNT);
let mut result = "var-".to_string();
result += &self.mVariableOrder[aIndex];
result
}
```


The Rust compiler would accept the code, since there is no way to determine the length of vectors before runtime. Unlike arrays, whose length must be known, the [ Vec type](https://doc.rust-lang.org/std/vec/struct.Vec.html) in Rust is dynamically sized. However, the standard library vector implementation has built-in bounds checking. When an invalid index is used, the program immediately terminates in a controlled fashion, preventing any illegal access.

The [actual code](https://dxr.mozilla.org/mozilla-central/source/servo/ports/geckolib/glue.rs#5735) in Quantum CSS uses very different data structures, so there’s no exact equivalent. For example, we use Rust’s powerful built-in data structures to unify the ordering and property name data. This allows us to avoid having to maintain two independent arrays. Rust data structures also improve data encapsulation and reduce the likelihood of these kinds of logic errors. Because the code needs to interact with C++ code in other parts of the browser engine, the new `GetCustomPropertyNameAt`

function doesn’t look like idiomatic Rust code. It still offers all of the safety guarantees while providing a more understandable abstraction of the underlying data.

## tl;dr;

Due to the overlap between memory safety violations and security-related bugs, we can say that Rust code should result in fewer critical [CVEs](https://cve.mitre.org/) (Common Vulnerabilities and Exposures). However, even Rust is not foolproof. Developers still need to be aware of correctness bugs and data leakage attacks. Code review, testing, and fuzzing still remain essential for maintaining secure libraries.

Compilers can’t catch every mistake that programmers can make. However, Rust has been designed to remove the burden of memory safety from our shoulders, allowing us to focus on logical correctness and soundness instead.

## 16 comments

stillDreaming1February 28th, 2019 at 12:29Diane HosfeltFebruary 28th, 2019 at 12:57AkyFebruary 28th, 2019 at 12:47D DMarch 6th, 2019 at 19:43timFebruary 28th, 2019 at 13:20Rune K. SvendsenMarch 6th, 2019 at 08:47tekiFebruary 28th, 2019 at 19:53Tom GeeMarch 1st, 2019 at 17:28Carl RashMarch 4th, 2019 at 04:38Jonathan AdamsMarch 7th, 2019 at 12:14D DMarch 8th, 2019 at 09:39jcdyerMarch 19th, 2019 at 06:57Dan NeelyMarch 4th, 2019 at 05:46Diane HosfeltMarch 5th, 2019 at 10:45Javier SánchezMarch 7th, 2019 at 09:24Wellington Torrejais da SIlvaMarch 8th, 2019 at 06:40