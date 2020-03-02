const path = require('path')

const merge = require('webpack-merge')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')

const base = require('./webpack.base.conf')


module.exports = merge(base, {
  output: {
    path: path.resolve('./dist/'),
    filename: '[name]-[hash].js',
  },
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader' },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: '[name]-[hash].css' }),
    // Don't keep old bundles
    new CleanWebpackPlugin([ 'dist/*' ], {
      root: path.resolve('../bundles')
    }),
    new BundleTracker({ filename: './webpack-stats.prod.json' }),
  ],
})
