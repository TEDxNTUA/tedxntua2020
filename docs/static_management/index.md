# Static files management

> **Quick usage workflow:**
> 
> When in dev mode, static files are managed automatically for you.
> 
> When in production mode, every time you make a change in static files, run `manage.py collectstatic`.

## Introduction

Some definitions first:
* *Static files* are images, CSS, JS or other files that we as developers create for the website.
* *Media files* are user-generated files that are uploaded through a `FileField`.

## Where do they live?

Static files can be created:
* In each app's `static/` folder (default Django locations).
* In additional locations defined by the `STATICFILES_DIRS` setting. In our project these are:
  * `project/static/` for project-level static files and
  * `bundles/dist/` when in production, or `bundles/build-dev/` when in development (see [bundling docs](../webpack/index.md)).

Media files are stored by default in `MEDIA_ROOT` which for our project is the `media/` folder.

### For example
* The logo –which is a project-level static file– will be stored in `project/static/`.
* The venue photos –that are specific to the homepage– will be stored in `project/home/static/`.
* The team photos –that will be uploaded through a `FileField` of the admin interface– will be stored somewhere in `media/` (e.g. `media/team/`).

## How do we serve them?

This depends on whether we are in development or production mode. When in production mode, serving such files via Django is a major **performance overhead**. That's why [the Django docs encourage us not to](https://docs.djangoproject.com/en/2.2/howto/static-files/deployment/).

## How do we serve them in production mode then?

Serving images, CSS, JS or any other static (and media) files is better handled directly by our web server, if not a separate dedicated server.

We just need to add directives to map `static/` and `media/` URLs to the corresponding folders. Example Apache configuration [here](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/modwsgi/#serving-files).

### Yes, but my static files are split among many directories. Wouldn't it be nicer if all lived in a single folder?

This is where the management command `collectstatic` comes in and does exactly that: it automatically discovers all static files and moves them to the root-level `static/` folder (or whatever `STATIC_ROOT` is).

**WARNING!** Do not place or edit any file directly from the `static/` folder. Use the `STATICFILES_DIRS` instead and run `collectstatic` again to update the contents.

## What about development mode?

Running `collectstatic` every time to gather the static files would be cumbersome while developing. That's why Django's `runserver` does it automatically when `DEBUG` is `True`.

But now we are missing the mapping from URLs to the folders. Django provides the [`static`](https://docs.djangoproject.com/en/2.2/howto/static-files/#serving-static-files-during-development) helper for that, so we can just add to `project/urls.py` the following:

```python
from django.conf import settings
from django.conf.urls.static import static

# ... the rest of your URLconf goes here ...

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This will map `static/` URLs to the `static/` folder and `media/` URLs to the `media/` folder.

**WARNING!** The static helper also only works when `DEBUG` is `True`, otherwise it returns `[]`.
