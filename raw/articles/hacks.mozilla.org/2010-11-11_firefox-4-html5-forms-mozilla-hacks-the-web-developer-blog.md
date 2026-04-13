---
title: 'Firefox 4: HTML5 Forms – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2010/11/firefox-4-html5-forms/
author: Anthony Ricaud
published: '2010-11-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Firefox 4 will come with better support for HTML5 forms. In the latest beta we are experimenting with a set of new features: more inputs types (email, url, tel, search), new attributes (placeholder, autofocus, list), decoupled forms and different validation mechanisms. This is thanks mostly to the hard work of Mounir Lamouri.*

*Some examples will work in other browsers, but you’ll need Firefox 4 beta to see all of them.*

## New input field types

In the same fashion as new HTML5 elements, we have new field types to better express what kind of input we want. The look and feel of many of these elements is the same as a text field, but they carry a different semantic meaning. This means that browsers can optimize the experience for users. For example, a mobile browser can provide a specific keyboard for a field. Or the browser can pre-fill phone number fields based on people in your address book. And extensions may even provide some features based on those types.

In this beta, Firefox comes with four new kind of inputs :

```
```

Of the four new input types, `url`

and `email`

will also validate their content. We’ll talk about that later.

We also have support for a new kind of field:

```
```

You can use this element to represent an area of the page that reacts to the interaction with a form. Think about the total price in a cart after you’ve changed the quantity of items or the shipping options. It won’t compute anything, you’ll need to do that with JavaScript, but it will give hints to accessibility technologies. The `for`

attribute is a list of IDs of the fields that intervene into the calculation.

Text fields have been improved with `<datalist>`

support. You can easily provide a list of suggestions for a field as the user is typing. You bind the field and the datalist by using the `list`

attribute. It will use every `option`

element inside `datalist`

to populate the list. And for browsers without `datalist`

support, they will display the content of the `datalist`

element. So be sure to provide some valid markup to get a nice fallback.



```
```

## New input attributes

### Autofocus

When you add this to a field, it will receive focus as soon as possible. The direct advantage for the user is that all sites will have the same algorithm for autofocus instead of relying on different JavaScript code. And browsers or extensions could disable this behavior if a user is not interested in it.

```
```

### Placeholder

The value of this attribute will be displayed inside the form when it is empty and not focused. You can put an example of the kind of expected value.

```
```

## Decoupled forms

You have more options to define the interaction between fields and forms.

### form attribute

**<input> elements don’t need to be children of a <form> element anymore.** You can define them anywhere you want and bind them to a form using the new `form`

attribute. It takes the ID of the form it should bind to.

Here’s an example. Let’s say you’re working on a search engine for some blogging software. You want a very simple form for the general use case and some advanced options if the user needs more control.

At the top of the page you could put:

```
```

And at the bottom:

```
```

This will behave as if the search field was part of the form. And you get the freedom of placing it wherever you want in your HTML.

### Form options on fields

All the options that can be defined at the form level can be overridden at the field element. All submit fields (<button> and input type=”submit”) accept four new attributes : **formenctype**, **formaction**, **formmethod** and **formtarget**.

One use case could be a form with a preview and post buttons. Each one needs all the fields of the form but they perform a different action.

```
```

When the user clicks on the Preview button, its attributes will override the form’s attributes. In this case, instead of a POST request to new_post.php, the whole form will be sent to the preview.php script with a GET method.

## Validation mechanisms

One of the big area of improvements for forms is validation. To give the best experience, we need to give feedback as soon as possible to the user. So people have written a lot of JavaScript code to do that. Wouldn’t it be nicer if browsers handled that?

### required

By adding this attribute, you’ll mark this field as required. For text fields, it means that it shouldn’t be left empty. For checkbox buttons, it means it should be checked. And for radio buttons, it means one of the button for a group should be selected.

Try each of the examples below and you’ll see that they change color when you interact with them.

```
```



```
```



```
```



### url

URL fields are automatically validated.

```
```




Emails are also automatically validated. By passing the multiple attribute ([also valid on type=”file”](http://hacks.mozilla.org/2009/12/multiple-file-input-in-firefox-3-6/)), you can also validate a list of mails separated by commas.

```
```




```
```




### pattern

Urls and emails will not be the only type of data you’ll want to validate. Therefore, the pattern attribute will allow you to provide a JavaScript regular expression. This will be matched against the value of the field to determine if it’s valid. You should also provide a title attribute explaining the pattern to the user.

In the example below, try hovering over the text field. You should see a popup that tells you how to fill out the form.

```
```



### The constraint validation API

If you need even more control over the validation, you can use the `setCustomValidity`

method. If you provide an empty string to this method, the element will be considered valid. Otherwise, it will be marked as invalid and the string will be used as a tooltip to help your user understand the problem.

```
```




If one of the field of a form is not valid, then submitting the form will be blocked and the first invalid field will be focused with a message explaining the problem. If you want to override this behaviour and send the form anyway, you can add a `novalidate`

attribute on the form or the `formnovalidate`

attribute on the appropriate submit button.

If you want more details on the validation mechanisms, check out [Mounir’s blog post](http://blog.oldworld.fr/index.php?post/2010/11/17/HTML5-Forms-Validation-in-Firefox-4).

## New CSS selectors

And to go with all this goodness are a few new CSS selectors.

`:required`

, `:optional`


All fields are marked as `:optional`

by default. If they have the required attribute, they’ll match the `:required`

pseudo-class instead.

`:valid`

, `:invalid`


These pseudo-classes represent the state of the field regarding validation. You can use `:invalid`

to override the default styling that Firefox 4 provides.

Here’s an example of a text box where the default style has been overridden.

`:-moz-placeholder`


This pseudo-class targets input fields displaying a placeholder. This is not yet part of CSS, so you’ll need to use a pseudo-element for WebKit based browsers.

```
```

## Conclusion

Form features in HTML5 are very new, and there’s still a wide difference between browsers. Opera implemented part of the spec (it was called Webforms2 at that time) so it has decent support for HTML5 Forms, along with some quirks since the spec evolved since that implementation. WebKit-based browsers are currently implementing some parts of the spec so you’ll also find some early support there as well.

We will not be adding more form features in Firefox 4, and there is clearly still some work to get full support for HTML5 forms. New field types (numbers, colors, dates), new attributes (step, min, max), new events (onforminput, onformchange) and so on. We’ll be adding support for more of HTML5 forms in later releases.

This was just a rough introduction. To get all the details, you should go to the [documentation on Mozilla Developer Network](https://developer.mozilla.org/en/HTML/HTML5/Forms_in_HTML5).

## 35 comments

mmcNovember 11th, 2010 at 12:19Anthony RicaudNovember 12th, 2010 at 05:09Jeff WaldenNovember 15th, 2010 at 03:07JoshNovember 11th, 2010 at 12:24PeterNovember 11th, 2010 at 12:27FredNovember 11th, 2010 at 16:38RyanNovember 11th, 2010 at 17:41Anthony RicaudNovember 12th, 2010 at 05:17SchizoDuckieNovember 11th, 2010 at 20:13Eli GreyNovember 12th, 2010 at 00:08Richard MilewskiMarch 17th, 2011 at 11:44Eli GreyNovember 12th, 2010 at 00:12fflorentNovember 12th, 2010 at 00:30jpvincentNovember 12th, 2010 at 01:57alexander farkasNovember 12th, 2010 at 03:11GenixonNovember 12th, 2010 at 06:52MarzNovember 15th, 2010 at 00:51Vitaliy KupetsNovember 22nd, 2010 at 07:59fflorentNovember 15th, 2010 at 03:54JO TosoniNovember 19th, 2010 at 06:41Anthony RicaudJanuary 15th, 2011 at 06:25sarmenDecember 15th, 2010 at 15:29Anthony RicaudJanuary 15th, 2011 at 06:11JonJanuary 1st, 2011 at 12:30Muhammad IrfanJanuary 15th, 2011 at 02:32gradeFebruary 12th, 2011 at 09:15leeMarch 4th, 2011 at 01:50Andrea BarghigianiMarch 31st, 2011 at 00:42Anthony RicaudMarch 31st, 2011 at 06:55Andrea BarghigianiMarch 31st, 2011 at 07:55Andrea BarghigianiMarch 31st, 2011 at 07:58Brian LePoreMarch 31st, 2011 at 11:17Si GradyApril 5th, 2011 at 13:37florianApril 27th, 2011 at 07:58RyanApril 27th, 2011 at 16:19