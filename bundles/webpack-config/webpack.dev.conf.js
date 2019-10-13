const path = require('path')

const merge = require('webpack-merge')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const base = require('./webpack.base.conf')


module.exports = merge(base, {
  output: {
    path: path.resolve('./build-dev/'),
    filename: '[name].js',
  },

  plugins: [
    new MiniCssExtractPlugin({ filename: '[name].css' }),
    new BundleTracker({ filename: './webpack-stats.dev.json' }),
  ],
})