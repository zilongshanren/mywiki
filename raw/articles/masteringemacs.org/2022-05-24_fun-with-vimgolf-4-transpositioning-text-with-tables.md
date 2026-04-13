---
title: 'Fun with Vimgolf 4: Transpositioning text with Tables'
url: https://www.masteringemacs.org/article/fun-vimgolf-4-transpositioning-text-tables
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Here’s another vim challenge, and one you might actually encounter frequently in real life.

Transpose the original lines in separate columns, one for each line.


Simple, really; a transposition here, some alignment there… but can we do better than the good ole’ brute force approach the Vim guys will invariably use? Can we do it without a call to a shell commands like `column`

and `paste`

? (Psst.. yes we can! It’s Emacs!)

Here’s the original data:

```
ultricies, vehicula, felis, sed, auctor, aenean, euismod, semper, quam, dapibus
nibh, consequat, consequat, maecenas, sit, amet, mauris, justo, quis, porttitor
curabitur, pharetra, euismod, orci, sit, amet, ullamcorper, mi, tincidunt, et
vitae, lorem, at, mi, feugiat, convallis, ac, eget, dui, fusce
blandit, iaculis, nulla, sit, amet, dolor, nec, est, ornare, volutpat
```


… Standard comma-, and newline-delimited data, and we must turn it into this:

```
ultricies nibh curabitur vitae blandit
vehicula consequat pharetra lorem iaculis
felis consequat euismod at nulla
sed maecenas orci mi sit
auctor sit sit feugiat amet
aenean amet amet convallis dolor
euismod mauris ullamcorper ac nec
semper justo mi eget est
quam quis tincidunt dui ornare
dapibus porttitor et fusce volutpat
```


Looking into the challenge, I was already thinking “tables” – Emacs tables. Transposition is a common operation in tables (spreadsheets) and mathematics, and Emacs can do both very well indeed.

So here’s what I did, utilizing our old friend `org-mode`

; or rather, one of its subsidiary libraries. You don’t have to be in `org-mode`

for this trick to work. It echoes an earlier VimGolf challenge I did where I used its hierarchical “sort” function to sort an address book: Fun with Vimgolf 1: Alphabetize the Directory.

`C-x h`


Mark the whole buffer


`M-x org-table-convert-region`


Converts a region into an org table. The defaults use comma and new line separators by default. Bonus.


`M-x org-table-transpose-table-at-point`


As the name implies this will transpose our table as required by the Vimgolf challenge.


`C-x C-x`


Exchange point and mark.


`M-x replace-regexp`


`Replace: ^| \\||`

`With: RET`


Replace the pipe at the beginning of the line and a whitespace,

orany pipe.

`M-x delete-trailing-whitespace`


Delete trailing whitespace. Could also be done with a more sophisticated regexp in the penultimate step.


Done right, and it should look like this:

```
ultricies nibh curabitur vitae blandit
vehicula consequat pharetra lorem iaculis
felis consequat euismod at nulla
sed maecenas orci mi sit
auctor sit sit feugiat amet
aenean amet amet convallis dolor
euismod mauris ullamcorper ac nec
semper justo mi eget est
quam quis tincidunt dui ornare
dapibus porttitor et fusce volutpat
```


Six “keystrokes” (for an arbitrarily large definition of “keystroke”…), but done the Emacs way. The best score on VimGolf is currently **31** (characters). Very impressive, but would it work on a 20x20 or with variable-length rows? “Think Abstract,” the developer cried.

The result above should be identical to that of the Vimgolf output, but done without the hyper-specialized and brittle solutions (most?) of the VimGolfers employ.

I didn’t tweak the cell width (whitespacing between each word) for each column; that it aligns perfectly with VimGolf’s output is dumb luck. Maybe they generated the resultant output in Emacs? :)

Nevertheless, the solution is “typical Emacs” and would scale well to very large datasets, and you don’t have to worry about things like unusually long cells; uneven number of rows and columns; etc.