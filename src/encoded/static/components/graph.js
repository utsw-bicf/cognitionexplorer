/** @jsx React.DOM */
'use strict';
var React = require('react');
var globals = require('./globals');
var $script = require('scriptjs');


// Constructor for a graph architecture
function GraphArch(id) {
    this.id = id;
    this.children = [];
    this.edges = [];
}

// Add node to the graph architecture
GraphArch.prototype.addNode = function(id, label, cssClass, type) {
    var newNode = {};
    newNode.id = id;
    newNode.type = type;
    newNode.labels[0].text = label;
    newNode.cssClass = cssClass;
    this.children.push(newNode);
};

// Add edge to the graph architecture
GraphArch.prototype.addEdge = function(source, target) {
    var newEdge = {};
    newEdge.id = '';
    newEdge.source = source;
    newEdge.target = target;
};

module.exports.GraphArch = GraphArch;


var Graph = module.exports.Graph = React.createClass({
    getInitialState: function() {
        return {
            infoNode: '' // ID of node whose info panel is open
        };
    },

    // Draw the graph on initial draw as well as on state changes
    drawGraph: function(el) {
        var d3 = require('d3');
        var dagreD3 = require('dagre-d3');
        var svg = d3.select(el).select('svg');

        // Create a new empty graph
        var g = new dagreD3.graphlib.Graph()
            .setGraph({rankdir: "TB"})
            .setDefaultEdgeLabel(function() { return {}; });

        // Call the supplied node assembler, passing it the graph to assemble
        // the nodes into, and the ID of the currently selected node, if any
        this.props.assembler(g, this.state.infoNode);

        // Run the renderer. This is what draws the final graph.
        var render = new dagreD3.render();
        render(svg, g);

        // Dagre-D3 has a width and height for the graph.
        // Set the viewbox's and viewport's width and height to that plus a little extra
        var width = g.graph().width;
        var height = g.graph().height;
        svg.attr("width", width + 20);
        svg.attr("height", height + 20);
        svg.attr("viewBox", "-10 -10 " + (width + 20) + " " + (height + 20));
    },

    // After the graph panel is mounted in the DOM, use D3/Dagre/Dagre-D3 to draw into it
    componentDidMount: function () {
        $script('dagre', this.setupGraph);
    },

    setupGraph: function() {
        var d3 = require('d3');
        var dagreD3 = require('dagre-d3');
        var el = this.getDOMNode();

        // Add SVG element to the graph component, and assign it classes, sizes, and a group
        var svg = d3.select(el).insert('svg', '.graph-node-info')
            .attr('class', 'd3')
            .attr('width', '960px') // Just choose an initial viewport size; we'll resize it later
            .attr('height', '300px')
            .attr('viewBox', '0 0 960 300') // Choose an inital viewbox size; we'll resize it later
            .attr('preserveAspectRatio', 'xMidYMid');
        svg.append('g').attr('class', 'd3-points');

        // Draw the graph into the panel
        this.drawGraph(el);

        // Add hover event listeners to each node rendering. Node's ID is its ENCODE object ID
        var reactThis = this;
        svg.selectAll("g.node").each(function(nodeId) {
            globals.bindEvent(this, 'click', function(e) {
                reactThis.handleMouseClick(e, nodeId);
            });
        });
        this.dagreLoaded = true;
    },

    // State change; redraw the graph
    componentDidUpdate: function() {
        if (!this.dagreLoaded) return;
        var el = this.getDOMNode();
        this.drawGraph(el);
    },

    // Handle mouse clicks in any of the nodes
    handleMouseClick: function(e, nodeId) {
        this.setState({infoNode: this.state.infoNode !== nodeId ? nodeId : ''});
    },

    render: function() {
        return (
            <div className="panel graph-display">
                {this.props.detailer(this.state.infoNode)}
            </div>
        );
    }
});
