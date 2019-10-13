# Webpack: Usage

## Creating an asset file

Assets are created in `assets` directories, either globally (in `assets/`) or on a per-application basis (e.g. in `project/partners/assets/`).

The `assets` directories contain `css/` and `js/` subdirectories (or more if needed).

### Aliases/Resolving

#### Referencing NPM modules
To import code from modules installed through NPM, simply use the module's name.

For example:
```javascript
import "bootstrap"
```

#### Custom aliases
For imports in asset files, you can use the `@` alias that is defined in `webpack.base.conf.js` and points to the `project/` folder.

For example:
```javascript
import "@/partners/assets/js/main.js"
```

#### Aliases in SCSS
The above imports can also work in SCSS files, but they need to be prepended by a tilde (`~`). Read sass-loader's [docs](https://github.com/webpack-contrib/sass-loader#imports) for more information:

```javascript
import "~@/partners/assets/css/main.css";
```

## Supported features

Our setup currently supports vanilla JS and for stylesheets, CSS and [Sass](https://sass-lang.com/guide).

## Linking the assets to Webpack

There are two ways to include an asset file in Webpack's bundling process:

#### Using an existing entry point

Scripts that will be used globally in the project are usually imported in the main entry point (`assets/js/index.js`).

This also applies to CSS stylesheets, which are additionally splitted to their own files by the [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin).

#### Creating a new entry point

If your asset is to be separated from the rest of the bundles and become its own bundle, you just need to list it as an entry point in Webpack's configuration.

Let's take for example a script `assets/js/auth.js` that is necessary only in authorized pages.

In order to create an entry point for it, edit `webpack.base.conf.js` and add the following in the entry object:

```javascript
module.exports = {
  ...
  entry: {
    main: fromRoot('assets/js/index.js'),
    ...,
    auth: fromRoot('assets/js/auth.js')
  },
  ...
}
```

> **Note:**
> 
> `fromRoot` is a utility function defined in `webpack.base.conf.js`. It simply generates a <u>relative</u> path that points to the root of the repository.

Now when Webpack is run, an `auth.js` (or `auth-[hash].js`) will be generated in `bundles/build-dev/` (or `bundles/dist/`). The `auth` filename comes from `auth` being the corresponding key in `entry`, similar to `main.js` being the bundle that results from `main: fromRoot('assets/js/index.js')`.

## Bundling

The bundling process is simplified by the npm scripts defined in `package.json`. Along with the bundles, the `webpack-stats` files are also generated.

### Development mode

Generates and stores the bundles in `bundles/build-dev/`:

```bash
cd bundles
npm run build:dev
```

> **Note**:
>
> `bundles/build-dev/` and `webpack-stats.dev.json` are not to be committed to the repository and thus they are listed in `bundles/.gitignore`.

To avoid running `npm run build:dev` everytime you make a change you can use the *watch mode* that does this automatically, by running:
```bash
cd bundles
npm run watch
```

### Production mode

Generates and stores the bundles in `bundles/dist/`:

```bash
cd bundles
npm run build
```

Read [static files management docs](../static_management/index.md) on how to deploy static files when in production mode.

## Referencing a Webpack bundle in Django templates

For the simplest case:

```HTML+Django
{% load render_bundle from webpack_loader %}

<html>
  <head>
    {% render_bundle 'main' 'css' %}
  </head>
  <body>
    ....
    {% render_bundle 'main' 'js' %}
  </body>
</head>
```

Check [here](https://github.com/owais/django-webpack-loader#templates) for extensive examples.