var path = require('path');
var webpack = require('webpack');
var env = process.env.NODE_ENV;

var PATHS = {
	static: path.resolve(__dirname, 'src/encoded/static'),
	build: path.resolve(__dirname, 'src/encoded/static/build'),
}

var plugins = [];
// don't include momentjs locales (large)
plugins.push(new webpack.IgnorePlugin(/^\.\/locale$/, [/moment$/]));
var chunkFilename = '[name].js';

if (env === 'production') {
	// uglify code for production
	plugins.push(new webpack.optimize.UglifyJsPlugin({minimize: true}));
	// add chunkhash to chunk names for production only (it's slower)
	chunkFilename = '[name].[chunkhash].js';
}

var preLoaders = [
	// Strip @jsx pragma in react-forms, which makes babel abort
	{
		test: /\.js$/,
		include: path.resolve(__dirname, 'node_modules/react-forms'),
		loader: 'string-replace',
		query: {
			search: '@jsx',
			replace: 'jsx',
		}
	}
];

var loaders = [
	// add babel to load .js files as ES6 and transpile JSX
	{
		test: /\.js$/,
		include: [
			path.resolve(__dirname, 'src/encoded/static'),
			path.resolve(__dirname, 'node_modules/react-forms'),
		],
		loader: 'babel',
		query: {
			presets: ['es2015', 'react'],
			plugins: ["transform-object-rest-spread"],
		}
	},
	{
		test: /\.json$/,
		loader: 'json',
	}
];

module.exports = [
	// for browser
	{
		context: PATHS.static,
		entry: {
			inline: './inline',
			bundle: [
				'./libs/compat.js', // The shims should execute first
				'./browser.js',
			],
		},
		output: {
			path: PATHS.build,
			publicPath: '/static/build/',
			filename: '[name].js',
			chunkFilename: chunkFilename,
		},
		module: {
			preLoaders: preLoaders,
			loaders: loaders,
		},
		devtool: 'source-map',
		plugins: plugins,
		debug: true
	},
	// for server-side rendering
	{
		entry: {
			renderer: './src/encoded/static/server.js',
		},
		target: 'node',
		// make sure compiled modules can use original __dirname
		node: {
			__dirname: true,
		},
		// avoid bundling babel, which is not used at runtime
		externals: ['babel-core/register'],
		output: {
			path: PATHS.build,
			filename: '[name].js',
			libraryTarget: 'commonjs2',
			chunkFilename: chunkFilename,
		},
		module: {
			preLoaders: preLoaders,
			loaders: loaders,
		},
		devtool: 'source-map',
		plugins: plugins,
		debug: true
	}
];
