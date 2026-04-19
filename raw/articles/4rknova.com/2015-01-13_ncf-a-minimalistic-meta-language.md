---
title: NCF, A Minimalistic Meta-Language
url: https://www.4rknova.com/blog/2015/01/13/ncf
author: Nikolaos Papadopoulos
published: '2015-01-13'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Overview

A few years back, I was working on my offline renderer and I needed a way to describe simple scenes in a human readable format. I created NCF to serve that purpose and wrote a handy parser for it. What follows is a description of the language format. The parser is written in c++ and is available at [github](https://github.com/4rknova/libncf)

NCF is a data serialization language (DSL) like YAML, XML and JSON. It provides the mechanics to implement complex hierarchy descriptors. Each line constitutes a separate entry. All entries are stripped of leading and trailing whitespace characters. Empty lines are ignored.

# Specification

## Comments

Strings following the sign “#” are treated as comments and are ignored at the parsing stage.

```
# This line is a comment
property = value # This is a comment as well
```


## Local File Inclusion

Local files can be inlined with the use of the “%include” directive.

```
%include common_set.ncf
```


## Properties

The simplest type of instruction is the property definition:

```
property = value
```


## Blocks

Blocks are used to group properties together. They can contain other blocks to create a hierarchy. A block definition begins with:

```
block name = {
}
```


The property scope is local to each block and the bottom-most redefinition within the same block prevails. Redefinition of groups within the same level adds the new properties to the existing ones.

```
root = /
server A = {
root = ./
root = ./sandbox/
# After parsing, the local property "root" will be equal to "./sandbox"
# Note that the global property "root" is not the same as the local
# property "path.root"
}
server B = {
}
server A = {
# The following property will be added to the existing set of "server A".
allow edit = true
}
```


## References

References can be used to substitute values with previously defined properties higher in the hierarchy.

```
# Character sheet
version = 1.0
character = {
name = John
surname = Doe
statistics = {
level = 10
}
dialogue = {
# In the following property, the string "<name>" will be
# substituted with the string "John".
msg01 = Some call me <name>, the wizard king.
msg02 = Greetings traveller!
}
}
inventory = {
}
```