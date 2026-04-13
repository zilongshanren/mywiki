---
title: Building a persistent Notes app for Firefox OS – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/03/building-a-persistent-notes-app-for-firefox-os/
author: Louis Stowasser
published: '2014-03-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In this tutorial we will be building a notes app (like Evernote) from scratch and deploy it to Firefox OS! See a [live demo](http://notes.sproute.io).

A persistent notes app needs a place to store all the notes for a user (so no one else can read it). For this we will use my own backend solution called [Sproute](http://getsproute.com). Sproute is a hosted web framework for quickly building dynamic webapps.

First [create an account](http://getsproute.com/signup) with a unique subdomain then access the Dashboard through `http://<mysubdomain>.sproute.io/admin`

. You must login with the same details used to signup to Sprotue.

## Models

In Sproute there is a concept called [Models](http://getsproute.com/docs/models). A model defines the dynamic data in our app with properties for data integrity. Create a new model called `notes`

with the following fields and properties:

`body`

: Text, Required, Min:`1`

`sharing`

: Text, Allowed Values:`public, private`

, Default Value:`private`


The `body`

field will store the contents of the note. The `sharing`

field will specify whether the note can be viewed by others (with a direct link) or just the owner. This is all the data we need to define, everything else is covered by [built-in fields](http://getsproute.com/docs/rest#built-in-fields).

## List notes

We need a way to list the available notes for a user. This can be done with Pages. A page is HTML with embedded [template tags](http://getsproute.com/docs/pages) for retrieving and processing data.

Open the `index`

page. This is the home page when people view your space. We will list the notes here. Add the following:

`{{ get /data/notes?sort=_lastUpdated,desc as notes }}`


All data is retrieved through an [HTTP interface](http://getsproute.com/docs/rest) so the `{{ get }}`

tag must take a URL. The request above is retrieving all notes for the logged in user and stores the results in a variable called `notes`

. We use a query parameter to sort the results by last modified first (An underscore denotes a built-in field).

Let’s display each note in a list:

-
{{ each notes as note }}
[{{ word note.body 0 5 }}](https://hacks.mozilla.org/view/{{note._id}})
{{ / }}

The `{{ word }}`

template tag will extract the first 5 words from the body content. We link to a not-yet-made page with the URL `/view/<id>`

. `note._id`

is a built-in unique identifier.

## Create a note

Before creating the `view`

page for a note, let’s make a new page for creating a note. Create a new page called `create`

. Add the following HTML:

Simple! As mentioned above, all data is retrieved and modified through an HTTP interface. This means we can use a simple HTML form to create a new note. The `goto`

query parameter will redirect the user to that URL.

Because this is a new page we need to create a new route so the page is accessible. A [route](http://getsproute.com/docs/routes) is a pattern for a requested URL that will render a page if matched. There will already be a route for the index page. Click Routes and create a new one with the following:

- Route:
`/create`

, Page:`create`

.

## User login and registration

User accounts are built into Sproute but we still need to create a Register and Login page. Thankfully this is also a simple HTML form so create a new page called `users`

and add the following:

## Login


You may add the Register form on the same page by copying the login form and replace the action attribute to `/api/register`

. Create two new routes with the following:

- Route:
`/login`

, Page:`users`

- Route:
`/register`

, Page:`users`


## View and update a note

Previously we created a link to view a note. This will also be where we let users modify the note. Create a new page called `view`

and add the following:

```
{{ get /data/notes/_id/:params.id?single=true admin as note }}
{{ if note.sharing eq private }}
{{ if note._creator neq :session.user._id }}
{{ error This note is private }}
{{ / }}
{{ / }}
```

We make a request to get the note data for the note that was passed into the URL (through the `params`

object). The query parameter `single=true`

will return just the object instead of a one item collection. `admin`

will run the request with the specified user-type. Next we check whether the note is private. If so throw an error if the user is not the creator.

The update form is very similar to the create form. We only need to change the action to update notes where the `_id`

matches the one in the URL.

This page requires a slightly complex route. We need to use a placeholder in the route so that `/view/anything`

will still match the `view`

page and store `anything`

in a variable.

Create a route with the following:

- Route:
`/view/:id`

, Page:`view`


Now you can see where `params.id`

comes from. `params`

is an object for all placeholders in the route and the matched values.

## Permissions

The last important concept of Sproute is [permissions](http://getsproute.com/docs/permissions). Permissions are just like routes where a requested URL matches a pattern but instead of pointing to a page, it validates against a required [user type](https://getsproute.com/docs/permissions#user-types).

Click Permissions and add the following:

- Method:
`GET`

, Route:`/data/notes`

, User:`Owner`

- Method:
`GET`

, Route:`/data/notes/*`

, User:`Owner`


This will make sure the only notes listed will be ones the user has created (i.e. the owner). Because of the second permission, we needed to run the `{{ get }}`

request as `admin`

otherwise it would fail for everyone (except for admins and the creator) even if the note is public.

## Firefox OS support

Sproute can very easily support [hosted apps](https://developer.mozilla.org/en-US/Marketplace/Publishing/Publish_options#Hosted_apps) on Firefox OS by creating a page with the [manifest JSON data](https://developer.mozilla.org/en-US/Apps/Developing/Manifest) and the route: `/manifest.webapp`

.

Create a new page called `manifest`

with the following:

```
{
"name": "{{self.name}}",
"description": "A persistent notes app",
"launch_path": "/",
"icons": {
"128": "/absolute/path/to/icon"
}
}
```

Create a Route with the pattern `/manifest.webapp`

pointing to the manifest page.

We’re done! Test this in the [app manager](https://developer.mozilla.org/en-US/Firefox_OS/Using_the_App_Manager) by using the link to the manifest (`http://notes.sproute.io/manifest.webapp`

). [Sproute is open-source and on GitHub](http://github.com/sproute/sproute) under the Mozilla Public License v2 so you may clone the repo for private hosting.

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

yuktarthApril 1st, 2014 at 23:05Louis StowasserApril 2nd, 2014 at 02:02