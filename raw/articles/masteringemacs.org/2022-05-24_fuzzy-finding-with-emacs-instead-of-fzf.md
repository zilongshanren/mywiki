---
title: Fuzzy Finding with Emacs Instead of fzf
url: https://www.masteringemacs.org/article/fuzzy-finding-emacs-instead-of-fzf
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Filtering long lists of output on the command line usually involves taking the list of items – maybe the output of `ls`

, `git`

or `find`

– and doing something with it. If you’re lucky you can mechanically filter the list with pipes and `grep`

. If you’re unlucky and you can’t think of a heuristic, you’ll have to sift through the output with a pager like `less`

and remember the items you want to keep.

![fzf filtering output from apt-cache search intended for apt-get](../../assets/a9410df394857a88.png)

`fzf`

filtering output from `apt-cache search`

intended for `apt-get`

Typically you do this because you want to cherry pick a subset of the items and feed them into another command, like `rm`

, `cat`

or `apt-get`

as the picture above illustrates.

But the manual way is tedious and slow. And that’s the problem [fzf](https://github.com/junegunn/fzf) tries to solve. The premise is simple: you feed it (via stdin) a list of items, and it displays a curses-like window where you can “fuzzy find” and select the items you care about. It’s designed to slot into command substitutions and pipes — like an interactive `grep`

.

So that got me thinking. There’s no reason why you can’t use Emacs to do this instead of `fzf`

! Emacs has better fuzzy finding and it’s the text editor you’re already using, so why not use Emacs?

Another reason to ditch `fzf`

is that you might be using [a shell and not a terminal emulator in Emacs](https://masteringemacs.org/article/running-shells-in-emacs-overview). It’s not impossible to run curses apps in `shell-mode`

, but it is harder.

## EZF: Emacs Fuzzy Finder

![Fuzzy matching with Helm](../../assets/bc5a37fa5cc1df60.gif)

`ezf`

filtering output from `apt-cache`

before passing it back to the shellSo the game plan is simple:

- Build a shell script
This is the shell-facing part that we feed into pipes and command substitution sub-shells.

It must talk to

`emacsclient`

, the client in the Emacs client-server duo. That way it’ll run in your existing Emacs instance and it won’t interrupt your workflow if you also use – as you well should! – Emacs as your shell or terminal emulator.- Write some Elisp glue code
We’ll need a few functions capable of letting you filter and select the match candidates you like. Luckily this is generally very easy.

- Return the picked candidates
After matching and selecting the candidates we want to keep, we must return them from whence they came. We’ll need to be mindful of annoying bagatelles like proper quoting.

- Make it easy to extend
It should be easy to extend or modify to suit individual tastes.

We’ll add a few command switches to

`ezf`

to highlight how easy it is to pass customizable switches through bash into Emacs.

### Sending to Emacs’s standard input

Let’s start with the shell script. I’ve done it in `bash`

. There’s a number of little gotchas and workarounds required for this to work well. So the script’s freighted with one or two annoying hacks.

Chiefly, it’s not possible to ask `emacsclient`

or even `emacs`

to read directly from a file descriptor device. So process substitution with `<(ls ...)`

is out. I don’t know why, as Emacs is absolutely 100% capable of *doing* it inside Emacs. So I’m chalking it up to oversight.

That means we have to work around that problem with real files. I’m using `mktemp`

to `cat`

standard input to a temporary file. To avoid clobbering your `tmpfs`

with junk files, there’s a `trap`

to clean up when the script exits.

Now all we need to do is add a little command argument parsing: I want `-c`

to let us choose the completion tool to invoke in Emacs; and `-f`

is there to pick the field offset to return. The latter is particularly useful if you have a line of text and you want just the first word, for example.

After that, there’s a little bit of house keeping in case you exit out of the selection process without picking anything. Oh, when you tell `emacsclient`

to evaluate elisp it’ll use `prin1`

to emit the representation of the Lisp object to standard output, and that forces quote symbols around strings, even if we don’t really want that. Sieving the output from Emacs through a pipe to `xargs`

cunningly strips the quotes.

```
#!/usr/bin/env bash
set -o nounset -o errexit -o pipefail
field=nil
# the elisp function to use for completing read
candidate_fn=ezf-default
while getopts c:f: OPT; do
case $OPT in
c)
candidate_fn=$OPTARG
;;
f)
field=$OPTARG
;;
*)
echo "usage: ${0##*/} [-f field] [-c candidate-fn]"
exit 2
esac
done
shift $(( OPTIND - 1 ))
OPTIND=1
ezftmp="$(mktemp)"
trap 'rm -f -- "$ezftmp"' EXIT
> "$ezftmp" cat -
# xargs is there to strip the "" from the beginning and end of the output from Emacs.
selection=$(emacsclient -e "(ezf \"$ezftmp\" $field #'$candidate_fn)" | xargs)
if [[ "$selection" == "nil" ]]; then
exit 1
else
echo "$selection"
fi
```


I’ve named it `ezf.sh`

(symlinked to `ezf`

) so all you need to do is put it somewhere on your `PATH`

.

### Filtering in Emacs

Completion in Emacs is a complex subject matter and one soused in bike shedding and personal opinion. So I’ve kept things open and made it work with `completing-read`

– well, specifically `completing-read-multiple`

so you can pick multiple items.

If you’re unsure how that fits into *your* completion framework, then my article on [understanding Minibuffer Completion](https://www.masteringemacs.org/article/understanding-minibuffer-completion) is a good place to start. If you want IDO to work with it, you’ll have to tweak the code yourself. Luckily I have [an example here](https://www.masteringemacs.org/article/find-files-faster-recent-files-package) to get you started.

I’ve also made it work out of the box with Helm which, as we all know, is awesome. Helm in particular is perfect for this as it comes with great fuzzy matching, multiple selection *and* it’s easy to add custom actions like returning matches to the shell *and* opening them as files in Emacs, for example.

There’s three parts: two completion mechanisms and a generic wrapper that turns lists of candidates into usable output.

```
(defun ezf-default (filename)
"EZF completion with your default completion system."
(completing-read-multiple
"Pick a Candidate: "
(with-temp-buffer
(insert-file-contents-literally filename nil)
(string-lines (buffer-string) t))))
```


`completing-read-multiple`

takes a prompt and a list of strings. And that’s all you need to get Emacs’s completion system to work. I create a temporary buffer to hold the file contents before it’s split up into lines. If you want NULL-separated output, this is the place to change it.

If you’re wondering why I’m using a buffer, you should read my article [Why Emacs has Buffers](https://www.masteringemacs.org/article/why-emacs-has-buffers).

```
(defun ezf-helm (filename)
"EZF completion with `helm'."
;; Uncomment if you want Helm to full screen.
;; (helm-set-local-variable 'helm-full-frame t)
(helm :sources
(helm-build-in-file-source "EZF Completion" filename
:action (lambda (_) (helm-marked-candidates)))))
```


For Helm the solution is similar. I’m using Helm’s ability to build candidates directly from a file. If you want to add more than one action then I recommend you use `helm-make-actions`

to build the alist.

Now for the generic wrapper. Its job is to take a list of strings you picked from a candidate function and turn it into something the shell can properly read. If you specified `-f`

to `ezf`

then it’ll also split the string and only use the field index you chose.

```
;; If you start Emacs's server some other way, you can remove this.
(server-start)
(defvar ezf-separators " "
"Regexp of separators `ezf' should use to split a line.")
(defun ezf (filename &optional field completing-fn)
"Wrapper that calls COMPLETION-FN with FILENAME.
Optionally split each line of string by `ezf-separators' if FIELD
is non-nil and return FIELD.
If COMPLETING-FN is nil default to `ezf-default'."
(when-let (candidates (funcall (or completing-fn 'ezf-default) filename))
(mapconcat (lambda (candidate)
(shell-quote-argument
(if field
(nth (1- field) (split-string candidate ezf-separators t " "))
candidate)))
candidates
" ")))
```


Here the goal is simply to take a `filename`

containing our candidates; an optional `completing-fn`

, as set by passing `-c`

to `ezf`

; and an optional `field`

index.

`ezf-separators`

is a regular expression to split each line by. So if you want NULL-delimited support then you can easily add that and a switch to go along with it.

Because we’re taking unsanitized candidates and passing them through our completion system, it’s good form to ensure the filtered candidates are properly escaped when we hand them back to the shell. That’s what `shell-quote-argument`

does. `mapconcat`

merely ensures the quoted candidates are space-separated as that’s what shells expect. (And if you want NULL separation you should change this also.)

Because the last value is by convention the value that is returned from a function in Lisp, we know that the output of `emacsclient`

is the result of the `mapconcat`

form if we selected any matches, and `nil`

otherwise.

With all this in place it’s time to test it:

`ezf`

Yep. Looks good.

This tool is able to do most of the things you’d use `fzf`

for, and all from within the comfort of your Emacs. It’ll work just fine in Eshell also if you don’t push it too hard. Eshell’s support for pipes and redirection is not as good as regular shells, but with a little bit of work it could be made to work there too, with or without the bash script. And of course you can use it from Terminals also: the ones you run from inside Emacs, and external ones also.

## Example Use Cases

Here’s a few examples of how you can use the tool. It goes without saying that it’s a bit threadbare compared to `fzf`

, but I think it’s easy enough to extend to suit your own needs. This is also a great way to get your hands dirty with elisp if you have never done any before.

I’m going to point out that `M-x helm-locate`

already does this, but you can use GNU `locate`

to track down files matching a regex pattern and then open them in `emacsclient`

:

`$ emacsclient $(locate -r '[.]py$' | ezf)`


GNU `locate`

works by querying a database that updates whenever you call `updatedb`

. It’s probably the one of fastest cached file searchers available today. You can have multiple databases with different configurations (one for your home directory and another for the whole file system) to further speed it up. I highly recommend you look into using it if you regularly sweep your file system looking for files.

Finding and installing packages with `apt-get`

and `apt-cache`

:

`$ apt-get install $(apt-cache search <term> | ezf -f 1)`


Change directories. Try playing around with the arguments to `find`

, or use something simpler like `ls`

:

`$ cd $(find . -maxdepth 3 -type d | ezf)`


## Next Steps

I think this is a pretty good example of how you can combine the power of Emacs and a little bit of gnarly shell script magic. And this is really just the beginning. You can take the shell script and hook it up to all manner of crazy Emacs stuff: `M-x dired`

; sending stuff to a buffer for editing; and more.

You can also find it on Github here: [EZF](https://github.com/mickeynp/ezf).