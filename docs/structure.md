# Project structure

* `docs/`  
  Project-level documentation needs to be stored here and be written in Markdown. Module-specific documentation may be located only in source files.
* [`bundles/`](webpack/structure.md)
* `assets/`  
  Project-level CSS and JS scripts. For documentation on the bundling process, check [here](webpack/index.md).
* `etc/`  
  Extra files that accompany the project, such as configuration of external tools etc.
* `project/`
    * [`about/`](about/index.md)
    * [`home/`](home/index.md)
    * [`partners/`](partners/index.md)
    * [`program/`](program/index.md)
    * [`team/`](team/index.md)
    * `static/`  
      Project-level static files (e.g. logo) live here.
    * `settings/`  
      Settings module that reads from *.env* and exports configuration parameters to Django.
    * `urls.py`  
      Top-level routing instructions.
* `media/`  
  User-generated media files will be stored here. More info [here](static_management/index.md).
* `static/`  
  Static files (CSS, JS, images, etc.) from `STATICFILES_DIRS` are gathered here. **Do not** place or edit any files in it, since all the management is done automatically by Django's `collectstatic` command. More info [here](static_management/index.md).
* `manage.py`  
  Django command-line tool.
* `env.sample`  
  Example of a *.env* configuration file.
* `_version.py`  
  Contains a `__version__` variable to indicate the current version of the website. Calendar versioning is used.
* `setup.py`  
  Setup script. Dependencies must also be included here.
* `requirements.txt`  
  Pinned production dependencies.
* `requirements-dev.txt`  
  Pinned development dependencies.
