---
title: git-subrepo Tutorial | Sebastian Schöner
url: https://blog.s-schoener.com/2019-04-20-git-subrepo/
author: Sebastian Schöner
published: '2019-04-20'
source_blog: Hi there! | Sebastian Schöner
source_site: https://blog.s-schoener.com/
category: graphics
fetched: '2026-04-19'
---

In the past, I have used both `git submodules`

and `git subtrees`

until I eventually ran into so many problems with them that I just gave up and started looking for alternatives. I stumbled over `git-subrepo`

([github](https://github.com/ingydotnet/git-subrepo)), so this is the next thing I will try and then most likely give up on in 6 months.
Since I already have trouble remembering what I need to do just to get started, here are some notes for future me.

The setup is as follows: I have a local repository and multiple external repositories that I want to install.

- Ensure that
`git-subrepo`

is installed. Just follow the instructions[here](https://github.com/ingydotnet/git-subrepo); they are actually quite decent. - Go into your local repository.
- In the root directory, execute
`git subrepo clone <remote-url> <subdir>`

where`<remote-url>`

is the url of the remote and`<subdir>`

is the subdir that you want to clone into. Note that the tool will*not*create another subdirectory with the name of the subrepo that you are adding. - Use
`git subrepo pull <subdir>`

and`git subrepo push <subdir>`

to pull and push. - Commit as usual, the tool is smart enough to figure out what goes where.

There is a more elaborate guide available [here](https://github.com/ingydotnet/git-subrepo/wiki/Basics), but I somehow always find it very hard to extract these few basic steps above from that.