---
title: Evaluating Lisp Forms in Regular Expressions
url: https://www.masteringemacs.org/article/evaluating-lisp-forms-regular-expressions
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

One of the oft-repeated complaints about Emacs is its antiquated regular expression engine: that it’s GNU-style regex and not PCRE; and that you have to liberally slather everything in backslashes. There is some truth to this, but its detractors overlook the features it *adds* that you won’t find in most other editors or regexp implementations.

I recently did a [VimGolf challenge](https://www.masteringemacs.org/articles/2013/01/14/fun-vimgolf-3-swapping-words-sorting/) where I abused `sort-regexp-fields`

so I could swap two different words. I decided to do it in the most obtuse way possible so I could demonstrate the flexibility of Emacs’s sort commands, and solve what would be a banal challenge in any editor – swapping exactly two elements, once, in a two-line file – using an “eclectic” feature.

But there’s a better way: a “scalable” way that works with an arbitrary number of elements to swap, and it uses.. regular expressions!

## Evaluating Forms

Due to the pervasive nature of Elisp in Emacs, you can invoke elisp from within a call to `replace-regexp`

. That is to say, in the `Replace with:`

portion of the call, you can tell Emacs to evaluate a form and return *its* output in lieu of (or in combination with) normal strings. The syntax is `\,(FORM)`

.

Let’s say you have the following file:

```
INITECH.TXT
----------------------------
Peter Gibbons $15000
Milton Waddams $12500
Bill Lumbergh $90000
```


And you want to give everybody a raise; well, you don’t *reaally* want to give Lumbergh a raise, but ho hum, right?

The simplest method is to use `[query-]replace-regexp`

with the following parameters.

`Replace regexp: \$\([0-9]+\)`


Here we search for the salary; we store the dollar amount in a capturing group.

`Replace regexp with: $\,(* \#1 2)`


And here we replace the salary with the output from an elisp form that multiplies the result from capturing group `\1`

– but in this case represented as `\#1`

, as we want Emacs to convert the result to an integer first – by two.

And now the output looks like:

```
INITECH.TXT
---------------------------
Peter Gibbons $30000
Milton Waddams $25000
Bill Lumbergh $180000
```


Neat.

## Conditional Replace

Let’s refactor some random Java code into CamelCase:

```
public class application_runner {
public static void main(String[] args) {
new Application(create_os_specific_factory());
}
public static GUIFactory create_os_specific_factory() {
int sys = read_from_config_file("OS_TYPE");
if (sys == 0) return new WinFactory();
else return new OSXFactory();
...
```


`Replace regexp: _\([[:lower:]]+\)`


Replace underscore and all lowercase characters, which we capture for use later.

`Replace regexp with: \,(capitalize \1)`


Here I use an elisp form to capitalize each match from capturing group `\1`

. The underscore is removed also, so `create_os_specific_factory`

becomes `createOsSpecificFactory`

, and so on.

And now it looks like this:

```
public class applicationRunner {
public static void main(String[] args) {
new Application(createOsSpecificFactory());
}
public static GUIFactory createOsSpecificFactory() {
int sys = readFromConfigFile("OS_TYPE");
if (sys == 0) return new WinFactory();
else return new OSXFactory();
...
```


Unfortunately, the word `Os`

should probably be written like this, `OS`

. Let’s change the form so that certain words are treated differently.

`Replace regexp: _\([[:lower:]]+\)`


Same as before.

`Replace regexp with: \,(cond ((member \1 '("os")) (upcase \1)) (t (capitalize \1)))`


This time I’ve use a `cond`

form – basically a case statement – to check that *if* the capturing group is a member of the list `("os")`

, we call the function `upcase`

which, you guessed it, uppercases `\1`

; if that condition fails, fall through to the second clause which, because its conditional is `t`

, always returns true and, therefore, we call `capitalize`

on `\1`

. I could’ve used an `if`

statement and saved a bit of typing, but `cond`

is more flexible if you want more than one or two conditionals.

The end result is that we now uppercase `OS`

and leave the rest capitalized.

## Swapping Elements

Going back to what I said in the beginning about swapping text. It is perfectly possible, as I’m sure you can imagine now, to swap two items – you don’t even need a cond element for that!

Consider this trivial Python function.

```
def foobar():
x = 10
y = 42
if x > 10 and y < 40:
return y + y
else:
return x + x
```


Let’s say we want to swap `x`

and `y`

. That is, of course, a *no-op*, but there’s nothing stopping you from extending the example here and using it for something more meaningful, such as reversing `>`

and `<`

.

`Replace: \(x\)\|y`


This is the most simple way of swapping two values. You only need one capturing group, because we only need to compare against one capturing group, hence why `y`

isn’t captured.

`Replace with: \,(if \1 "y" "x")`


Next, we test for existence; if `\1`

is not `nil`

– that is to say, we actually have something IN the capturing group, which would only happen if we encounter `x`

– we fall through to the `THEN`

clause (`"y"`

) in the `if`

form; if it is `nil`

, we fall through to the `ELSE`

clause (`"x"`

).

The result is what you would expect:

```
def foobar():
y = 10
x = 42
if y > 10 and x < 40:
return x + x
else:
return y + y
```


The variables are swapped. But let’s say you want to swap more than two elements: you’d need to nest `if`

statements (ugly) or use `cond`

(less ugly, but equally verbose.)

### More Cond Magic

Consider the string `1 2 3`

. To turn it into `One Two Three`

you have two ways of doing it:

One, you can use `N`

capturing groups like so: `\(1\)\|...\|\(N\)`

and in a `cond`

check for the existence of each capturing group to determine if it is the “matched” one. There’s no reason why you couldn’t use just one capturing group and then string match for each item, but it’s swings and roundabouts: you’re either grouping each match you care about in the *search* bit, or you’re checking for the existence of the elements you care about in a form in the *replace* bit.

Let’s go with the first option.

`Replace: \(1\)\|\(2\)\|\(3\)`


Look for, and capture, the three integers.

`Replace with: \,(cond (\1 "One") (\2 "Two") (\3 "Three"))`


Using `cond`

, if any of the three capturing groups are non-`nil`

, the body of that conditional is returned.

Not unsurprisingly, the result is `One Two Three`

.

If you change the capturing groups to this `\(1\|2\)\|\(3\)`

and if you then change the replacement string to `\,(cond (\1 "One") (\2 "Two"))`

, you end up with `One One Two`

. So as you can see, it’s very easy to create rules that merge multiple different strings into one using `cond`

.

## More ideas?

I think I’ve amply demonstrated the power of mixing regular expressions and lisp. I know a few more tricks, but I’m always keen to find more, so if you have a novel application I’d love to hear about it.

There’s nothing stopping you from invoking elisp functions that *don’t* return anything useful; that is, you’re free to call functions just for their side effects, if that is what you want. For instance, if you want to open a list of files in a buffer, use `\,(find-file-noselect \1)`

. Another useful application is formatting strings using `format`

. Check out the help file (`C-h f format RET`

) for more information. And lastly, you can use Lisp lists to gather matches for use programmatically later: `M-: (setq my-storage-variable '())`

then `\,(add-to-list 'my-storage-variable \1)`

.

Know any useful regexp hacks? Post a comment!