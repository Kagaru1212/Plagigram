const path = require('path');

module.exports = {
  entry: './app/static/insta/js/main.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'app/static/insta/js/dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    alias: {
      'jquery': 'expose-loader?$!jquery',
    },
  },
};
