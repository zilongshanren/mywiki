---
title: 'XML Parser Generator :: nklein software'
url: http://nklein.com/2010/03/xml-parser-generator/
author: Pat
published: '2010-03-16'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

A few years back (for a very generous few

), we needed to parse a wide variety of XML strings. It was quite tedious to go from the XML to the native-language representations of the data (even from a DOM version). Furthermore, we needed to parse this XML both in Java and in C++.

I wrote (in Java) an XML parser generator that took an XML description of how you’d like the native-language data structures to look and where in the XML it could find the values for those data structures. The Java code-base for this was ugly, ugly, ugly. I tried several times to clean it up into something publishable. I tried to clean it up several times so that it could actually generate the parser it used to read the XML description file. Alas, the meta-ness, combined with the clunky Java code, kept me from completing the circle.

Fast forward to last week. Suddenly, I have a reason to parse a wide variety of XML strings in Objective C. I certainly didn’t want to pull out the Java parser generator and try to beat it into generating Objective C, too. That’s fortunate, too, because I cannot find any of the copies (in various states of repair) that once lurked in ~/src

.

What’s a man to do? Write it in Lisp, of course.

### Example

Here’s an example to show how it works. Let’s take some simple XML that lists food items on a menu:

<food name="Belgian Waffles" price="$5.95" calories="650">

<description>two of our famous Belgian Waffles with plenty of real maple syrup</description>

</food>

<!-- ... more food entries, omitted here for brevity ... -->

</menu>

We craft an XML description of how to go from the XML into a native representation:

<struct name="food item">

<field type="string" name="name" from="@name" />

<field type="string" name="price" from="@price" />

<field type="string" name="description" from="/description/." />

<field type="integer" name="calories" from="@calories" />

</struct>

<struct name="menu">

<field name="menu items">

<array>

<array_element type="food item" from="/food" />

</array>

</field>

</struct>

</parser_generator>

Now, you run the parser generator on the above input file:

--types-package menu \

--reader-package menu-reader \

--file menu.xml

This generates two files for you: types.lisp

and reader.lisp

. This is what types.lisp

looks like:

(:use :common-lisp)

(:export #:food-item

#:name

#:price

#:description

#:calories

#:menu

#:menu-items))

(in-package :menu)

(defclass food-item ()

((name :initarg :name :type string)

(price :initarg :price :type string)

(description :initarg :description :type string)

(calories :initarg :calories :type integer)))

(defclass menu ()

((menu-items :initarg :menu-items :type list :initform nil)))

I will not bore you with all of reader.lisp

as it’s 134 lines of code you never had to write. The only part you need to worry about is the parse

function which takes a stream for or pathname to the XML and returns an instance of the menu

class. Here is a small snippet though:

;;; food-item struct

;;; =================================================================

(defmethod data progn ((handler sax-handler) (item food-item) path value)

(with-slots (name price description calories) item

(case path

(:|@name| (setf name value))

(:|@price| (setf price value))

(:|/description/.| (setf description value))

(:|@calories| (setf calories (parse-integer value))))))

### Where it’s at

I currently have the parser generator generating its own parser (five times fast). I still have a little bit more that I’d like to add to include assertions for things like the minimum number of elements in an array or the minimum value of an integer. I also have a few kinks to work out so that you can return some type other than an instance of a class for cases like this where the menu

class just wraps one item.

My next step though is to get it generating Objective C parsers.

Somewhere in there, I’ll post this to a public git repository.

Sweet. I think I might have a copy of the old xml parser generator around somewhere.

If you want, I can look for it. 🙂

I keep finding myself rewriting your xml-tagstack interface on every platform where I use XML data these days. hehe.

As you can see with the “path” in the above code snippet, I still use the tagstack approach. In this case, I even extended it to include the text contents of a tag and the attributes into the same handler method.

Oh, and I improved the tagstack so that it’s absolute from the current structure being parsed instead of the whole way to the root.