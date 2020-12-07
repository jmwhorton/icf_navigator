const path = require("path");
const exclusions = /node_modules/;

module.exports = [
  {
    entry: {
      app: "./assets/app.js",
    },
    output: {
      path: path.resolve(__dirname, "core/static/"),
      publicPath: "/static/",
      filename: "[name].js",
      chunkFilename: "[id]-[chunkhash].js",
    },
    devServer: {
      port: 8081,
      writeToDisk: true,
    },
    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
              plugins: ['@babel/plugin-proposal-class-properties']
            }
          }
        },
        {
          test: /\.(scss)$/,
          use: [{
            loader: 'style-loader', // inject CSS to page
          }, {
            loader: 'css-loader', // translates CSS into CommonJS modules
          }, {
            loader: 'postcss-loader', // Run postcss actions
          }, {
            loader: 'sass-loader' // compiles Sass to CSS
          }]
        }
      ]
    }
  },
];
