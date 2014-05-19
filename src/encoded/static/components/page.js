/** @jsx React.DOM */
'use strict';
var React = require('react');
var globals = require('./globals');


var Block = module.exports.Block = React.createClass({

    render: function() {
        var block = this.props.block;
        if (typeof block['@type'] == 'string') {
            block['@type'] = [block['@type'], 'block'];
        }
        var block_view = globals.block_views.lookup(block);
        return <block_view type={block['@type']} data={block.data} />;
    }
});


var Row = module.exports.Row = React.createClass({
    render: function() {
        var auto_col_class = "";
        switch (this.props.blocks.length) {
            case 2: auto_col_class = 'col-md-6'; break;
            case 3: auto_col_class = 'col-md-4'; break;
            case 4: auto_col_class = 'col-md-3'; break;
            default: auto_col_class = 'col-md-12'; break;
        }
        var blocks = this.props.blocks.map(function(block) {
            return (
                <div className={block.className || auto_col_class}>
                    <Block block={block} />
                </div>
            );
        });
        return (
            <div className="row">
                {blocks}
            </div>
        );
    }
});


var Page = module.exports.Page = React.createClass({
    render: function() {
        return <div>{this.props.context.layout.rows.map(row => <Row blocks={row.blocks} />)}</div>;
    }
});


globals.content_views.register(Page, 'page');
