var path = require('path');
var webpack = require('webpack');


var entry= {
    index: './src/index.js'
};

var webpack_module= {
    loaders: [
        {
            test: /\.js$/,
            loaders: [ 'babel' ],
            exclude: /node_modules/,
            include: __dirname
        }
    ]
};

var externals= {
    'electron': 'electron'
    // 'react': 'React',
    // 'react-dom': 'ReactDOM',
    // 'redux': 'Redux',
    // 'react-redux': 'ReactRedux',
    // 'echarts': 'echarts',
    // 'moment': 'moment',
    // 'react-router': 'ReactRouter',
    // 'react-router-redux': 'ReactRouterRedux',
    // 'redux-thunk': 'ReduxThunk'
};

module.exports = {
    devtool: "source-map",
    entry: entry,
    output: {
        path: path.join(__dirname, 'dist'),
        filename: "[name].entry.js",
        sourceMapFilename: '[file].map'
    },
    module: webpack_module,
    externals: externals
};