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
    publicPath: "/",  // Certifique-se de que o Webpack serve os arquivos no root
  },
  devServer: {
    static: {
      directory: Path.resolve(__dirname, '../static/dist'),  // Diretório para servir os arquivos compilados
      publicPath: "/static/",  // Alinhado com o Flask (garante que ele serve como o Flask espera)
    },
    hot: true,
    liveReload: true,  // Ativa o live-reload para alterações HTML
    watchFiles: [
      Path.resolve(__dirname, "../templates/**/*.html"),
      Path.resolve(__dirname, "../src/**/*")
    ],  // Observa mudanças nos templates e nos arquivos de fonte
    host: "0.0.0.0",
    port: 9091,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
    devMiddleware: {
      writeToDisk: true,  // Garante que as alterações sejam escritas no disco para sincronização
    },
  },
  plugins: [
    new Webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("development"),
    }),
    new StylelintPlugin({
      files: Path.resolve(__dirname, "../src/**/*.s?(a|c)ss"),
    }),
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
        test: /\.js$/,
        include: Path.resolve(__dirname, "../src"),
        loader: "babel-loader",
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