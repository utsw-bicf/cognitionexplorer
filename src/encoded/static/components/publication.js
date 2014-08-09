/** @jsx React.DOM */
'use strict';
var React = require('react');
var globals = require('./globals');
var dbxref = require('./dbxref');
var search = require('./search');
var StatusLabel = require('./antibody').StatusLabel;

var DbxrefList = dbxref.DbxrefList;
var Dbxref = dbxref.Dbxref;

var Citation = module.exports.Citation = React.createClass({
    render: function() {
        var context = this.props.context;
        return (
            <span>
                {context.journal ? <i>{context.journal}. </i> : ''}{context.date_published ? context.date_published + ';' : ''}{context.volume ? context.volume : ''}{context.issue ? '(' + context.issue + ')' : '' }{context.page ? ':' + context.page + '.' : ''}
            </span>
        );
    }
});


var Panel = module.exports.Panel = React.createClass({
    render: function() {
        var context = this.props.context;
        var itemClass = globals.itemClass(context);
        return (
            <div className={itemClass}>
                <div className="characterization-status-labels">
                    <StatusLabel title="Status" status={context.status} />
                </div>
                {context.authors ? <div className="authors">{context.authors}.</div> : null}
                <div className="journal">
                    {this.transferPropsTo(<Citation />)}
                </div>

                {context.abstract || context.data_used || context.references.length ?
                    <div className="view-detail panel">
                        {context.abstract ?
                            <div className="abstract">
                                <h2>Abstract</h2>
                                <p>{context.abstract}</p>
                            </div>
                        : null}

                        <dl className="key-value-left">
                            <div>
                                {context.references && context.references.length ?
                                    <div>
                                        <dt>References</dt>
                                        <dd><DbxrefList values={context.references} className="multi-value" /></dd>
                                    </div>
                                : null}
                                {context.data_used ?
                                    <div>
                                        <dt>Consortium data referenced in this publication</dt>
                                        <dd>{context.data_used}</dd>
                                    </div>
                                : null}
                            </div>
                        </dl>
                    </div>
                : null}
            </div>
        );
    }
});

globals.panel_views.register(Panel, 'publication');


var Listing = React.createClass({
    mixins: [search.PickerActionsMixin],
    render: function() {
        var context = this.props.context;
        var authorList = context.authors ? context.authors.split(', ', 4) : [];
        var authors = authorList.length === 4 ? authorList.splice(0, 3).join(', ') + ', et al' : context.authors;
        return (<li>
                    <div>
                        {this.renderActions()}
                        <div className="pull-right search-meta">
                            <p className="type meta-title">Publication</p>
                            <p className="type meta-status">{' ' + context['status']}</p>
                        </div>
                        <div className="accession"><a href={context['@id']}>{context.title}</a></div>
                    </div>
                    <div className="data-row">
                        {authors ? <p className="list-author">{authors}.</p> : null}
                        <p className="list-citation">{this.transferPropsTo(<Citation />)}</p>
                        {context.references.length ? <div><DbxrefList values={context.references} className="list-reference" /></div> : '' }
                    </div>
            </li>
        );
    }
});
globals.listing_views.register(Listing, 'publication');
