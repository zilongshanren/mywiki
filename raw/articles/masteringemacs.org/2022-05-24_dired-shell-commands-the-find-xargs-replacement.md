---
title: 'Dired Shell Commands: The find & xargs replacement'
url: https://www.masteringemacs.org/article/dired-shell-commands-find-xargs-replacement
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re a Linux/BSD user you probably do most of your bulk operations on files with the command line tools `find ... -exec`

or `find ... | xargs`

– but there’s a much better way. Dired (`M-x dired`

or `C-x d`

), Emacs’s DIRectory EDitor, can do the same but in a very intuitive way. I’ve talked about Dired before: [how to work with files spread out across many directories](https://www.masteringemacs.org/articles/2011/03/25/working-multiple-files-dired/) and [editable dired buffers](https://www.masteringemacs.org/articles/2013/10/10/wdired-editable-dired-buffers/) that will persist the changes made to filenames and permissions in the buffer.

Of all the hidden gems in Dired, this is one of my favourites: the ability to run arbitrary shell commands on marked files – and if it’s a file extension known to Dired, it will suggest a default action: untarring .tar.gz files; displaying .pdf files; and much more!

## Installing Dired-X

The latter functionality is buried in `dired-x`

, an add-on for Dired that… ships with Emacs but isn’t enabled by default.

To use dired-x you must load it first.

```
(add-hook 'dired-load-hook
(lambda ()
(load "dired-x")))
```


You can also just `(require 'dired-x)`

somewhere in your init file.

## Using Emacs’s Guess Shell Command functionality

To apply a shell command to marked files press `!`

. If you have no marked files Dired will apply the shell command to the file or directory point is on. Dired will suggest a list of defaults (navigate the choices with `M-n`

and `M-p`

) and if Dired-x is loaded it will set a default action so you just press enter to apply it.

Dired-x ships with a fairly large repository of common operations on files and you can add your own by modifying the alist `dired-guess-shell-alist-user`

.

## Running Arbitrary Shell Commands

Another little-known feature of Dired’s shell command functionality is that you can write your own one-off commands but run each command per marked file or collect (and separated by whitespace, like in the shell) them all and pass them to a single instance of the command.

Some shell commands accept many files per command and others just one. You can use two wildcard operators (`*`

and `?`

) in a Dired shell command and that will determine how Dired constructs the external shell command(s).

Let’s say I want to call the external script `foo.py`

. My shell command can be constructed in two ways. And let’s assume I have two files marked in Dired: `hello.txt`

and `world.txt`

.

If the command `foo.py`

only accepts a single file argument I can use `?`

as the substitution variable. So `foo.py ?`

will give us the following expanded commands:

```
foo.py hello.txt
foo.py world.txt
```


If I had used `*`

in lieu of the `?`

substitution variable then the entire list of marked files would have been inserted with whitespaces separating each file, like so:

`foo.py hello.txt world.txt`


**Note:** You must separate the substitution variable with spaces or it won’t work right!

If you want your calling shell to expand the `*`

as a globbing wildcard you must type `*""`

instead.

Finally, you can dictate whether the shell commands should be executed synchronously or asynchronously.

By default the commands are called synchronously unless you append `&`

, `;`

or `;&`

. However, they are not all alike. If you are operating on *multiple files* (that is, you are using the `?`

substitution variable) then `&`

will make the shell commands execute **in parallel as well!** If the command ends in `;`

or `;&`

then the commands are **executed sequentially, one after another** but still asynchronously.

Dired’s shell command functionality is particularly powerful if you want to apply the shell commands on files spread out across multiple directories as it eliminates the need for `find`

in all but the most complex searches. My article on [how to work with files spread out across many directories](https://www.masteringemacs.org/articles/2011/03/25/working-multiple-files-dired/) shows you how you can find files across directories and display them in a “merged” dired buffer. Combined with the Dired shell command I just talked about and you can replace most external `find ... -exec command`

patterns. If you think `find`

is painful to use simply use Dired’s extremely powerful file marking functionality and off you go.