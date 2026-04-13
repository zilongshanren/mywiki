---
title: Angular, Caddy, Gunicorn and Django
url: https://anteru.net/blog/2023/angular-caddy-and-django
published: '2023-10-21'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This took me way more time than I anticipated, so here’s the summary in case any of you (or future me) runs into the same situation. The stage: I have a [Django](https://www.djangoproject.com/) application which provides a [GraphQL](https://graphql.org/) endpoint, and an [Angular](https://angular.io/) frontend using it. Everything is hosted via [Caddy](https://caddyserver.com/), and Django is served through [Gunicorn](https://gunicorn.org/). So far so good. Now, I was using Django (via some plugins) to serve the Angular web application, so the typical request would be:

- Caddy gets the requests and forwards it to Gunicorn
- Gunicorn invokes Django
- Django reads the static file and serves it

All of this mostly because I was too lazy to set this up correctly; Django has a static files module which seemed like it could do the trick, and it somewhat works, but the correct way to do this is as following:

-
Caddy serves

*all*static files -
If the path is

`/static/*`

, it serves from the Django`STATIC_ROOT`

-
Otherwise, if the file exists, it serves from the Angular root

-
If the path is unknown, it redirects it to the Angular root (as we assume this is an Angular route)


How do we achieve that? It’s actually not that complicated. On the Django side, there’s nothing to do really. Just set the `STATIC_ROOT`

and remember what you set it to. Now comes the `Caddyfile`

:

```
my.host.url {
tls /srv/certs/caddy/cert.crt /srv/certs/caddy/cert.key
@angular {
not path /graphql
not path /admin/*
not path /account/*
}
handle_path /static/* {
root * /srv/app/django/static
file_server
}
handle {
reverse_proxy unix//run/gunicorn.sock
}
handle @angular {
root * /srv/app/angular
try_files {path} {path}/ /index.html
file_server
}
}
```


What this does is:

- Defines a
[named matcher](https://caddyserver.com/docs/caddyfile/matchers#named-matchers)to exclude all paths that should be handled by Angular (`@angular`

) – this matches the paths that should*not*go to Django - Sends all
`/static/*`

requests to a[file server](https://caddyserver.com/docs/caddyfile/directives/file_server#file-server)(note: You can configure that path in case it conflicts with your Angular app via)`STATIC_URL`

- Connects Caddy to Gunicorn/Django – everything that is not handled by Caddy will go here. This is important so we can run the admin console.
- Sends the remaining requests to Angular:
tries to serve a local file, and if that fails, it will serve`try_files`

`index.html`


Voilà, that’s it. It’s easier if you don’t care about the Django admin page and so on, but in my case, I do want to keep the ability to open that. With this configuration, you get the optimal performance serving any static file (as both the Django and Angular static files get served by Caddy), while retaining all the usual Django goodness, without any additional build time complexity.