---
title: Evaluating Elisp in Emacs
url: https://www.masteringemacs.org/article/evaluating-elisp-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

There are several ways of evaluating elisp code in Emacs, and picking the right approach will help you get your job done faster and more efficiently. If you’re new to elisp it’s easy to learn about one or two methods and come away disappointed or frustrated because you’re using the wrong tool for the job.

Emacs is capable of evaluating elisp in a variety of ways, each with their own trade-offs and benefits, and all of them serve a distinct but important purpose. Knowing all them is important.

## Evaluating a Region or Buffer

If you want to evaluate a whole file, then `M-x eval-buffer`

is a good place to start.

It’ll re-evaluate everything *except* special forms like `defface`

, `defcustom`

and `defvar`

. The reason is that they’re usually user-facing variables that you may have customized: for instance the fonts and faces you use for text, or the options you’ve picked in the *Customize* interface. Blindly resetting them when you evaluate a whole buffer is a blunderbuss approach that’ll likely cause more harm than good. So, Emacs will happily *set* special forms like `defface`

if they’re undefined; if they’re already set, Emacs leaves them alone.

This also applies when you evaluate a region with `M-x eval-region`

.

I frequently evaluate the current buffer – and rarely regions – when I’m writing elisp. As it’s annoying to type, and because it leaves no visual indication that the evaluation took place, I have a little helper function and key binding I like to use:

```
(defun mp-elisp-mode-eval-buffer ()
(interactive)
(message "Evaluated buffer")
(eval-buffer))
(define-key emacs-lisp-mode-map (kbd "C-c C-c") #'mp-elisp-mode-eval-buffer)
(define-key lisp-interaction-mode-map (kbd "C-c C-c") #'mp-elisp-mode-eval-buffer)
```


Pressing `C-c C-c`

– a common key binding used for this sort of thing in other major modes – now evaluates the whole buffer in both `*scratch*`

(more on that below) and `emacs-lisp-mode`

buffers.

## Evaluating Expressions

### By S-Expression

This is where Emacs starts to shine, for it has special tools available to it to evaluate S-expressions. An S-expression is, put simply, anything Emacs’s Lisp implementation can *read*, which has special meaning in Lisp. In Lisp, first you read; then you evaluate.

In Emacs’s case it’s not just balanced expressions – like `(message "Hello World")`

, though that is most likely what you’ll use it for – but other, more primitive constructs also. Those primitives include numbers such as decimal `42`

, `#x12`

as hexadecimal and `#o44`

as octal; vectors, like `[1 2 3]`

; `"strings"`

or ordinals like `?:`

; and so on.

To evaluate S-expressions, type `C-x C-e`

or run `M-x eval-last-sexp`

.

Although the function is designed for S-expressions, you can ask Emacs to evaluate nearly anything this way: numbers, strings, you name it. If what you’re asking it to evaluate is invalid or malformed, Emacs will tell you.

Its key binding, `C-x C-e`

, is a global key. That means it’s available by default in most of Emacs’s major modes and, thus, buffers. That means you can safely evaluate elisp from an `M-x info`

buffer; an `M-x eww`

web browser session; or indeed anywhere else.

So it’s designed to work in a variety of situations — provided Emacs can guess what it is you’re asking it to evaluate! As its name alludes to, it’s called evaluate *last* S-expression: you must put your point at the *end* of the thing you want to evaluate.

Emacs will backtrack and find the logical beginning – the beginning of a number or string, or the opening `(`

that a `)`

belongs to – so keep that in mind when you evaluate stuff.

The result of the evaluation, if there is one, is printed in your minibuffer.

Prior to Emacs 28 `C-x C-e`

would not re-evaluate special forms like `defvar`

, `defcustom`

and `defface`

. That was actually rather annoying (hence the change) as more often than not you’d selectively evaluate a `defvar`

with `C-x C-e`

*exactly because* you wanted to change it.

So if you’re using older versions of Emacs, beware: you must evaluate by defun (see below) to change them.

### By Form or Defun

Arguably the simplest way to evaluate a form is `eval-defun`

, bound to `C-M-x`

. Unlike `C-x C-e`

(in versions leading up to Emacs 28 anyway) it re-evaluates special forms like `defcustom`

, `defface`

or `defvar`

.

What makes `C-M-x`

useful is that it looks for the outermost form your point is in. So if you’re deep inside a `defun`

form, it’ll eval the whole shebang. And it’s not limited to just `defun`

forms, of course; no, it’ll run anything, despite its name.

One way to determine – until you’re familiar with how it decides what to evaluate – is to type `C-M-u`

repeatedly inside a form until you get an error saying it can’t go up. *That* is the top level form Emacs evaluates when you type `C-M-x`

.

What makes it even better is its built-in support for *edebug*, Emacs’s elisp debugger. Using the universal argument `C-u`

Emacs will evaluate the form as normal, but enable debug instrumentation.

Emacs is clever enough to detect that if you’re edebugging a `defun`

that it’ll trigger the next time you, or any other part of Emacs, executes that function.

To remove debug instrumentation, re-evaluate the form with `C-M-x`

but without `C-u`

.

You should memorize this command. It’s handy as you can evaluate a block of code you’re working on *without* moving point, and without evaluating either the region it’s in, or the whole buffer.

### By Expression

The command `M-x eval-expression`

, bound to `M-:`

, is meant for quick, one-off evaluations. Unlike `C-x C-e`

, an evaluated expression does not have to be a form (like this `(+ 1 2 3)`

) but can instead be anything Emacs is capable of evaluating:

- Variables, like
`default-directory`

- Calling functions, like
`(shell)`

- Evaluating complex forms, like
`(+ (* 3 42) 9)`

- Setting variables, like
`(setq foo 42)`


Evaluated expressions are printed to the echo area and the value prepended to the list variable `values`

.

I use it frequently when I want to quickly change a variable or see its value. Usually because I’m testing or tweaking something.

What is also useful to know is that it evaluates code in the context of the buffer you called `M-:`

. So if you’re curious about the definition of a buffer-local variable like `default-directory`

you can switch to the buffer you want to check and use `M-:`

. It’ll also set variables in the same context.

If you use the universal argument `C-u`

, Emacs will insert the output into the current buffer. In a similar vein, you can tell Emacs to redo the previous command it did and let you edit the command beforehand by invoking `C-x M-:`

.

`C-x M-:`

is especially useful if you don’t know how an interactive command “works”. Try calling it after switching buffers; opening `M-x dired`

; or doing a search and replace. Emacs spits out the elisp code required to repeat the last command. Pretty cool stuff, and it is a great way to [bind complex commands to keys](https://www.masteringemacs.org/article/mastering-key-bindings-emacs) as I explain in my article on mastering key bindings.

One thing you cannot do is invoke multiple expressions. To get around this, you can wrap the expressions in the `progn`

form, like so: `(progn (foo) (bar) (baz))`

.

But if you find yourself in the habit of doing that frequently, you should use Emacs’s scratch buffer.

## Interactive Evaluation

### The Scratch Buffer

The `*scratch*`

buffer is created for you automatically when you launch Emacs. I’m sure you wondered what on *earth* that buffer was about when you first started using Emacs. It does have a few specialized commands and, unlike the major mode (`emacs-lisp-mode`

) you activate when you open a `.el`

elisp file, the `*scratch*`

buffer uses `lisp-interaction-mode`

. It’s got all the features of `emacs-lisp-mode`

– it inherits from that major mode – but with a few sweeteners that make it useful for one-off scripts and commands.

If you put point at the end of an sexp and type `C-j`

Emacs will evaluate the expression and print the result straight into the buffer.

I find it useful. I’ll quite often switch to the scratch buffer – it’s an omnipresent thing in my Emacs, as I never kill it – and store snippets of code I’m working on. If I’m hacking on a third-party library or Emacs’s own code, I will often copy the `defun`

I’m editing into `*scratch*`

and modify and evaluate it there. That way I’m overwriting the old function with my own, but I don’t permanently change the original source file.

But the scratch buffer is a poor substitute for a proper REPL, but thankfully Emacs does come with one of those too.

### IELM: The Interactive Emacs-Lisp Mode

IELM is a hidden gem. No, really: I’ve met Emacs users with decades of experience who’ve never heard of it. It really *is* hidden.

And it’s a proper REPL. Type `M-x ielm`

to launch it. It comes with all the useful features you would expect from an interactive shell:

- Multi-line editing
When you press

`RET`

IELM will check whether you did so at the end of the input, or in the middle. If it’s the latter, it’ll insert a newline and let you continue editing and writing. Great if you want to write multi-line code.In all other instances it’ll evaluate what you wrote.

- Output Variables
The variables

`*`

,`**`

and`***`

contain the last three outputs from the shell.- History
`ielm`

inherits from comint mode, although it talks to no external process. That means it inherits a lot of the core functionality present in comint mode. I’ve written about[comint history commands](https://www.masteringemacs.org/article/shell-comint-secrets-history-commands)before so I won’t repeat myself here.

Another useful feature is the concept of a *working buffer* - a buffer through which your changes are evaluated. If you type `C-c C-b`

you can change ielm’s working buffer to one of your choosing and then all the code you evaluate thereafter is treated as if you executed it in the context of that buffer. So in this sense it works like `M-:`

. Not only is it useful, it’s downright essential as some variables are local to a particular buffer or directory on your file system.

### From the Command Line

Both the `emacs`

and `emacsclient`

binaries support elisp evaluation on the command line. By passing `-e`

to either binary, Emacs evaluates the code you give it and it then returns the result. If you use *several* distinct calls to `-e`

you’ll get the return value (if any) for every single call. If you want to call multiple forms in one go you’ll need special forms like `progn`

or `prog1`

.

I recommend you use `emacsclient`

as it’ll reuse your existing Emacs instance instead of spawning a brand new one.

In fact, I use this approach to good effect in [Fuzzy Finding with Emacs instead of fzf](https://www.masteringemacs.org/article/fuzzy-finding-emacs-instead-of-fzf) where I demonstrate how you can “send” output from pipes into Emacs and back into the shell.

### Honorable Mention: Eshell

You can evaluate elisp in Eshell directly from the prompt, with some limitations. I have covered this in greater detail in my article on [Mastering Eshell](https://www.masteringemacs.org/article/complete-guide-mastering-eshell).

## Conclusion

That just about covers evaluating code in Emacs, from one-liners to entire buffers of code. If you’re hacking elisp you want `C-M-x`

for your everyday editing and quick debugging; if you’re inspecting state or want to change something in Emacs real quick, use `M-:`

; if you want to evaluate a buffer or region, use `eval-buffer`

or `eval-region`

; and if you’re exploring elisp and want an interactive environment, use `ielm`

.