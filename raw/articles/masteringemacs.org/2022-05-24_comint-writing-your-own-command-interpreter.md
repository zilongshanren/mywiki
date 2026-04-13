---
title: 'Comint: Writing your own Command Interpreter'
url: https://www.masteringemacs.org/article/comint-writing-command-interpreter
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

One of the hallmarks of Emacs is its ability to interface with external processes and add to the user experience with the full coterie of Emacs functionality like syntax highlighting, macros, command history, and so on. This functionality has been in Emacs since time immemorial, yet few people make their own *command interpreters* – also known as *comint* – in Emacs, fearing that it is either really difficult or not possible. It’s a concept used across Emacs: [Running Shells and Terminal Emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) is perhaps the most common example.

It’s not surprising people feel this way when you consider how woefully underdocumented this functionality is. Emacs’s comint infrastructure assumes you’re familiar with a diverse set of things, like font locking, code completion, command history and more. It’s at the heart of what powers so many things in Emacs.

So here’s a quick guide to building your own comint interpreter complete with rudimentary syntax highlighting and more.

## The Theory

Before I demonstrate how you use comint, a quick briefing – but rough, as I’m leaving out a few boring steps – on how it works.

At its core, you are spawning a process and either redirecting the stdin, stdout and stderr pipes to Emacs; or you use a pseudo-terminal. You can choose between them with `process-connection-type`

, but it’s unlikely that you would ever want to change that manually. Emacs is smart enough to determine the best tool for your platform.

The fundamental building blocks for interacting with processes are `start-process`

, for kinda-sorta-asynchronous process calls; and `call-process`

, for synchronous process calls.

One layer above that and we get to comint with its very pared-down, basic interpreter framework. This is what things like `M-x shell`

and the various REPL modes like Python build on. Comint takes care of the nitty-gritty stuff like sending and receiving data from the process; the command history; basic input/output filter hooks, so you can apply filters before sending or after receiving; signals and prompt handling.

In other words, it’s the perfect thing to build on if you want something interactive but want more than just what comint has to offer. To use comint is simple: `comint-run`

takes one argument, `PROGRAM`

, and nothing else. You can run it with a filepath to your favourite program and watch it fly. You don’t even need to code anything: `M-x comint-run`

is all you need. For even greater configurability, you can use `make-comint-in-buffer`

, as I’ll show you below.


Important caveat about pipe redirection:Most programs detect that you are redirecting its pipes to a dumb terminal or file. When they catch you doing that, they hide the user-facing prompts (as you generally don’t want them in your output if you’re piping stuff to a file.)It’s really very frustrating.

Not all programs detect that they are running inside Emacs by looking for Emacs-specific environment variables:

`EMACS`

and`INSIDE_EMACS`

. If they don’t check for them, you may get lucky and find a flag you can set to force the program to run in “interactive” mode – for example, in Python it’s`-i`

.

One layer above that and we get to things like `M-x shell`

and `M-x compile`

. I’ve written about both shells and [compiling and running scripts in Emacs](https://www.masteringemacs.org/article/compiling-running-scripts-emacs) if you want to know more.

Finally, as it’s useful to know about, you can list all running/open processes by typing `M-x list-processes`

.

## Writing a Comint Mode

With that out of the way, let’s write some code. I’ve chosen Cassandra, but you can substitute that for your favorite program.

The most important thing about writing a comint mode is that it’s very easy to get 80% of the way there, but getting those remaining 20 percentage points is the really difficult part! I’m only doing the 80% here! If you want pitch-perfect syntax highlighting and code completion, then you’ll have to work for it.

To start the Cassandra CLI you run the program `cassandra-cli`

and you’re presented with output similar to this:

```
$ ./cassandra-cli
Connected to: "Test Cluster" on 127.0.0.1/9160
Welcome to Cassandra CLI version 1.2.8
Type 'help;' or '?' for help.
Type 'quit;' or 'exit;' to quit.
[default@unknown]
```


If you run `cassandra-cli`

with `comint-run`

– you already have a working, interactive process. It’s barebones and simple, but its defaults are reasonable and it will work well enough. If you want to extend it, you have to write your own wrapper function around `make-comint-in-buffer`

and write a major mode also. So let’s do just that.

### The Comint Template

```
(defvar cassandra-cli-file-path "/opt/cassandra/bin/cassandra-cli"
"Path to the program used by `run-cassandra'")
(defvar cassandra-cli-arguments '()
"Commandline arguments to pass to `cassandra-cli'.")
(defvar cassandra-mode-map
(let ((map (nconc (make-sparse-keymap) comint-mode-map)))
;; example definition
(define-key map "\t" 'completion-at-point)
map)
"Basic mode map for `run-cassandra'.")
(defvar cassandra-prompt-regexp "^\\(?:\\[[^@]+@[^@]+\\]\\)"
"Prompt for `run-cassandra'.")
```


The first thing we need to do is capture user-facing options in variables so you can change the settings without having to edit the code. The first one is obvious: we need to store a path to `cassandra-cli`

, the program we want to run.

The next variable, `cassandra-cli-arguments`

, holds an (empty) list of commandline arguments.

The third is an empty and currently disused mode map for storing our custom keybindings. It is inherited from `comint-mode-map`

, so we get the same keys exposed in `comint-mode`

.

Finally, we have `cassandra-prompt-regexp`

, which holds a regular expression that matches the prompt style Cassandra uses. It so happens that by default it sort-of works already, but I recommend you write your own.

If you’re unsure of how to best test that your regular expression matches the prompt, then you should try Emacs’s regexp builder [re-builder](https://www.masteringemacs.org/article/re-builder-interactive-regexp-builder). It’s interactive and you can point it at a buffer with all the different flavors of prompts you must support.

```
(defvar cassandra-buffer-name "*Cassandra*"
"Name of the buffer to use for the `run-cassandra' comint instance.")
(defun run-cassandra ()
"Run an inferior instance of `cassandra-cli' inside Emacs."
(interactive)
(let* ((cassandra-program cassandra-cli-file-path)
(buffer (get-buffer-create cassandra-buffer-name))
(proc-alive (comint-check-proc buffer))
(process (get-buffer-process buffer)))
;; if the process is dead then re-create the process and reset the
;; mode.
(unless proc-alive
(with-current-buffer buffer
(apply 'make-comint-in-buffer "Cassandra" buffer
cassandra-program nil cassandra-cli-arguments)
(cassandra-mode)))
;; Regardless, provided we have a valid buffer, we pop to it.
(when buffer
(pop-to-buffer buffer))))
```


The next thing we need is a variable that determines the name of the buffer we want to use. By all means change that to something else.

The main entrypoint is `run-cassandra`

and there’s two parts to it:

- Dealing with existing Cassandra Buffers
If the process tied to a buffer exits, then we need to check for that so we can restart its process automatically the next time you run

`M-x run-cassandra`

. That’s what`proc-alive`

is for.This is also true if we already have an existing Cassandra buffer

*and*the process is still running.- Spinning up a new comint instance
If we don’t have a Cassandra buffer – and by extension no Cassandra process – then we must first create the

`buffer`

with our preferred name.By then checking if we have a process (we don’t) we can now create one with

`make-comint-in-buffer`

. I’m using`apply`

to invoke the function as we support variadic arguments in`cassandra-cli-arguments`

.

At the end of it all, we `pop-to-buffer`

so we always – whether it’s new or an existing instance – jump to the buffer when we call `M-x run-cassandra`

. I must point out that you can use other forms of buffer display; `pop-to-buffer`

is not the only one. See [Demystifying Emacs’s Window Manager](https://www.masteringemacs.org/article/demystifying-emacs-window-manager) for more information.

```
(defun cassandra--initialize ()
"Helper function to initialize Cassandra."
(setq comint-process-echoes t)
(setq comint-use-prompt-regexp t))
(define-derived-mode cassandra-mode comint-mode "Cassandra"
"Major mode for `run-cassandra'.
\\<cassandra-mode-map>"
;; this sets up the prompt so it matches things like: [foo@bar]
(setq comint-prompt-regexp cassandra-prompt-regexp)
;; this makes it read only; a contentious subject as some prefer the
;; buffer to be overwritable.
(setq comint-prompt-read-only t)
;; this makes it so commands like M-{ and M-} work.
(set (make-local-variable 'paragraph-separate) "\\'")
(set (make-local-variable 'font-lock-defaults) '(cassandra-font-lock-keywords t))
(set (make-local-variable 'paragraph-start) cassandra-prompt-regexp))
(add-hook 'cassandra-mode-hook 'cassandra--initialize)
(defconst cassandra-keywords
'("assume" "connect" "consistencylevel" "count" "create column family"
"create keyspace" "del" "decr" "describe cluster" "describe"
"drop column family" "drop keyspace" "drop index" "get" "incr" "list"
"set" "show api version" "show cluster name" "show keyspaces"
"show schema" "truncate" "update column family" "update keyspace" "use")
"List of keywords to highlight in `cassandra-font-lock-keywords'.")
(defvar cassandra-font-lock-keywords
(list
;; highlight all the reserved commands.
`(,(concat "\\_<" (regexp-opt cassandra-keywords) "\\_>") . font-lock-keyword-face))
"Additional expressions to highlight in `cassandra-mode'.")
```


The previous snippet of code dealt with creating and maintaining the buffer and process, and this piece of code enriches it with font locking and mandatory setup. Namely `comint-process-echoes`

which, depending on the mode and the circumstances, may result in prompts appearing twice. Setting it to `t`

is usually a requirement, but do experiment.

We also tell comint to use our prompt regular expression, and we additionally set a couple of common defaults, like the paragraph (`M-{`

and `M-}`

) commands, and where comint can find our customized font lock settings.

Font locking is a messy subject, and I do the bare minimum, which is highlighting a list of reserved words that I extracted from Cassandra’s `help;`

command.

One way to enrich font locking is by copying the rules from other comint modes. Most programs follow the same rhythm, and you can definitely take inspiration from existing comint modes that way.

### Intercepting Input and Output

Comint has a large range of functions that trigger at certain points in the lifecycle of a program. If you want to intercept input (or output) then you can do so with these variables. Note they work much like hooks, so you can (and should) use `add-hook`

to modify them.


NOTE: Don’t forget to make them buffer-local, like I’ve done for other variables in the`define-derive-mode`

form, by putting your own settings in`cassandra--initialize`

.

`comint-dynamic-complete-functions`


List of functions called to perform completion.


`comint-input-filter-functions`


Abnormal hook run before input is sent to the process.


`comint-output-filter-functions`


Functions to call after output is inserted into the buffer.


`comint-preoutput-filter-functions`


List of functions to call before inserting Comint output into the buffer.


`comint-redirect-filter-functions`


List of functions to call before inserting redirected process output.


`comint-redirect-original-filter-function`


The process filter that was in place when redirection is started


`completion-at-point-functions`


This is the preferred method for building completion functions in Emacs.


Another useful variable is `comint-input-sender`

, which lets you alter the input string mid-stream. Annoyingly its name is inconsistent with the filter functions above.

### Wrapping up

And there you go: a simple, comint-enabled Cassandra CLI in Emacs. As always, there is more to do.

Completion, although outside the scope of this simple tutorial, is also possible. Check out my article on [PComplete: Context-Sensitive Completion in Emacs](https://www.masteringemacs.org/article/pcomplete-context-sensitive-completion-emacs) for more information.