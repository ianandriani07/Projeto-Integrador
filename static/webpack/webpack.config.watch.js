const Path = require("path");
const Webpack = require("webpack");
const { merge } = require("webpack-merge");
const StylelintPlugin = require("stylelint-webpack-plugin");
const ESLintPlugin = require("eslint-webpack-plugin");

const common = require("./webpack.common.js");

module.exports = merge(common, {
  target: "web",
  mode: "development",
  devtool: "inline-source-map",
  output: {
    chunkFilename: "js/[name].chunk.js",
  },
  plugins: [
    new Webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("development"),
    }),
    // new StylelintPlugin({
    //   files: Path.resolve(__dirname, "../src/**/*.s?(a|c)ss"),
    // }),
    new ESLintPlugin({
      extensions: "js",
      emitWarning: true,
      files: Path.resolve(__dirname, "../src"),
    }),
  ],
  module: {
    rules: [
      {
        test: /\.html$/i,
        loader: "html-loader",
      },
      {
        test: /\.[mc]?[jt]sx?$/,
        include: Path.resolve(__dirname, "../src"),
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "swc-loader"
        }
      },
      {
        test: /\.s?css$/i,
        use: [
          "style-loader",
          "css-loader",
          "sass-loader",
        ],
      },
    ],
  },
});
