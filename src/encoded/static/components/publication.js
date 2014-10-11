/** @jsx React.DOM */
'use strict';
var React = require('react');
var globals = require('./globals');
var dbxref = require('./dbxref');
var search = require('./search');

var DbxrefList = dbxref.DbxrefList;
var Dbxref = dbxref.Dbxref;


var Publication = module.exports.Panel = React.createClass({
    render: function() {
        var context = this.props.context;
        var itemClass = globals.itemClass(context, 'view-item');
        return (
            <div className={itemClass}>
                <h2>{context.title}</h2>
                {context.authors ? <div className="authors">{context.authors}.</div> : null}
                <div className="journal">
                    {this.transferPropsTo(<Citation />)}
                </div>

                {context.abstract || context.data_used || (context.datasets && context.datasets.length) || (context.references && context.references.length) ?
                    <div className="view-detail panel">
                        {this.transferPropsTo(<Abstract />)}
                    </div>
                : null}

                {context.supplementary_data && context.supplementary_data.length ?
                    <div>
                        <h3>Related data</h3>
                        {context.supplementary_data.map(function(data, i) {
                            return <SupplementaryData data={data} key={i} />;
                        })}
                    </div>
                : null}
            </div>
        );
    }
});

globals.content_views.register(Publication, 'publication');


var Citation = module.exports.Citation = React.createClass({
    render: function() {
        var context = this.props.context;
        return (
            <span>
                {context.journal ? <i>{context.journal}. </i> : ''}{context.date_published ? context.date_published + ';' : ''}
                {context.volume ? context.volume : ''}{context.issue ? '(' + context.issue + ')' : '' }{context.page ? ':' + context.page + '.' : ''}
            </span>
        );
    }
});


var Abstract = React.createClass({
    render: function() {
        var context = this.props.context;
        return (
            <dl className="key-value">
                {context.abstract ?
                    <div data-test="abstract">
                        <dt>Abstract</dt>
                        <dd>{context.abstract}</dd>
                    </div>
                : null}

                {context.data_used ?
                    <div data-test="dataused">
                        <dt>Consortium data used in this publication</dt>
                        <dd>{context.data_used}</dd>
                    </div>
                : null}

                {context.datasets && context.datasets.length ?
                    <div data-test="datasets">
                        <dt>Datasets</dt>
                        <dd>
                            {context.datasets.map(function(dataset, i) {
                                return (
                                    <span key={i}>
                                        {i > 0 ? ', ' : ''}
                                        <a href={dataset['@id']}>{dataset.accession}</a>
                                    </span>
                                );
                            })}
                        </dd>
                    </div>
                : null}

                {context.references && context.references.length ?
                    <div data-test="references">
                        <dt>References</dt>
                        <dd><DbxrefList values={context.references} className="multi-value" /></dd>
                    </div>
                : null}
           </dl>
        );
    }
});


var SupplementaryData = React.createClass({
    render: function() {
        var data = this.props.data;
        return (
            <div className="view-detail panel">
                <dl className="key-value" key={this.props.key}>
                    {data.supplementary_data_type ?
                        <div data-test="availabledata">
                            <dt>Available data</dt>
                            <dd>{data.supplementary_data_type}</dd>
                        </div>
                    : null}

                    {data.file_format ?
                        <div data-test="fileformat">
                            <dt>File format</dt>
                            <dd>{data.file_format}</dd>
                        </div>
                    : null}

                    {data.url ?
                        <div data-test="url">
                            <dt>URL</dt>
                            <dd><a href={data.url}>{data.url}</a></dd>
                        </div>
                    : null}

                    {data.data_summary ?
                        <div data-test="datasummary">
                            <dt>Data summary</dt>
                            <dd>{data.data_summary}</dd>
                        </div>
                    : null}
                </dl>
            </div>
        );
    }
});


var SupplementaryDataListing = React.createClass({
    render: function() {
        var data = this.props.data;
        var columns = this.props.columns;

        var summary = (data.data_summary && (data.data_summary.length > 100) ? globals.truncateString(data.data_summary, 100) : undefined);
        var seeMoreClass = 'btn btn-link' + (summary ? '' : ' collapsed');

        return (
            <div className="list-supplementary" key={this.props.key}>
                <strong>{columns['supplementary_data.supplementary_data_type']['title']}</strong>: {data.supplementary_data_type}<br />
                <strong>{columns['supplementary_data.file_format']['title']}</strong>: {data.file_format}<br />
                <strong>{columns['supplementary_data.url']['title']}</strong>: <a href={data.url}>{data.url}</a><br />
                <strong>{columns['supplementary_data.data_summary']['title']}</strong>: {summary ?
                    <span>{summary}<button type="button" className={seeMoreClass} data-toggle="collapse" onClick={this.handleClick} /></span>
                : data.data_summary}
            </div>
        );
    }
});


var Listing = React.createClass({
    mixins: [search.PickerActionsMixin],
    render: function() {
        var result = this.props.context;
        var columns = this.props.columns;
        var authorList = result.authors ? result.authors.split(', ', 4) : [];
        var authors = authorList.length === 4 ? authorList.splice(0, 3).join(', ') + ', et al' : result.authors;

        // Calculate data_summary excerpts if needed
        var summaries = [];
        if (result.supplementary_data && result.supplementary_data.length) {
            result.supplementary_data.forEach(function(data, i) {
                summaries[i] = (data.data_summary && (data.data_summary.length > 100) ? globals.truncateString(data.data_summary, 100) : undefined);
            });
        }

        return (
            <li>
                {this.renderActions()}
                <div className="pull-right search-meta">
                    <p className="type meta-title">Publication</p>
                    <p className="type meta-status">{' ' + result.status}</p>
                </div>
                <div className="accession"><a href={result['@id']}>{result.title}</a></div>
                <div className="data-row">
                    {authors ? <p className="list-author">{authors}.</p> : null}
                    <p className="list-citation">{this.transferPropsTo(<Citation />)}</p>
                    {result.references.length ? <div><DbxrefList values={result.references} className="list-reference" /></div> : '' }
                    {result.supplementary_data && result.supplementary_data.length ?
                        <div>
                            {result.supplementary_data.map(function(data, i) {
                                return <SupplementaryDataListing data={data} columns={columns} key={i} />;
                            })}
                        </div>
                    : null}
                </div>
            </li>
        );
    }
});
globals.listing_views.register(Listing, 'publication');
