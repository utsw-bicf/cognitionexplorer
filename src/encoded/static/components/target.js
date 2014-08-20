/** @jsx React.DOM */
'use strict';
var React = require('react');
var _ = require('underscore');
var globals = require('./globals');
var dbxref = require('./dbxref');

var DbxrefList = dbxref.DbxrefList;
var Dbxref = dbxref.Dbxref;

var Target = module.exports.Target = React.createClass({
    render: function() {
        var context = this.props.context;
        var itemClass = globals.itemClass(context, 'view-detail panel key-value');
        var geneLink, geneRef, sep;

        if (context.organism.name == "human") {
            geneLink = globals.dbxref_prefix_map.HGNC + context.gene_name;
        } else if (context.organism.name == "mouse") {
            var uniProtValue = JSON.stringify(context.dbxref);
            sep = uniProtValue.indexOf(":") + 1;
            var uniProtID = uniProtValue.substring(sep, uniProtValue.length - 2);
            geneLink = globals.dbxref_prefix_map.UniProtKB + uniProtID;
        } else if (context.organism.name == 'dmelanogaster') {
            geneRef = _.find(context.dbxref, function(ref) {
                return ref.indexOf('FBgn') != -1;
            });
            if (geneRef) {
                sep = geneRef.indexOf(":") + 1;
                var flybaseName = geneRef.substring(sep, geneRef.length);
                geneLink = globals.dbxref_prefix_map.FlyBase + flybaseName;
            }
        } else if (context.organism.name == 'celegans') {
            geneRef = _.find(context.dbxref, function(ref) {
                return ref.indexOf('WBGene') != -1;
            });
            if (geneRef) {
                sep = geneRef.indexOf(":") + 1;
                var wormbaseName = geneRef.substring(sep, geneRef.length);
                geneLink = globals.dbxref_prefix_map.WormBase + wormbaseName;
            }
        }
        return (
            <div className={globals.itemClass(context, 'view-item')}>
                <header className="row">
                    <div className="col-sm-12">
                        <h2>{context.label} (<em>{context.organism.scientific_name}</em>)</h2>
                    </div>
                </header>

                <dl className={itemClass}>
                    <dt>Target name</dt>
                    <dd>{context.label}</dd>

                    {context.gene_name ? <dt>Target gene</dt> : null}
                    {context.gene_name ? <dd><a href={geneLink}>{context.gene_name}</a></dd> : null}

                    <dt>External resources</dt>
                    <dd>
                        {context.dbxref.length ?
                            <DbxrefList values={context.dbxref} target_gene={context.gene_name} />
                        : <em>None submitted</em> }
                    </dd>
                </dl>
            </div>
        );
    }
});

globals.content_views.register(Target, 'target');
