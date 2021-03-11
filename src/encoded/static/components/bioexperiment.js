import React from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelBody, PanelHeading } from '../libs/ui/panel';
import * as globals from './globals';
import { Breadcrumbs } from './navigation';
import Status from './status';
import _ from 'underscore';
import { FileGallery1 } from './filegallery1';

import { singleTreatment, ItemAccessories, DisplayAsJson, InternalTags } from './objectutils';
import pubReferenceList from './reference';

import { BiosampleSummaryString, BiospecimenOrganismNames, CollectBiosampleDocs, AwardRef, ReplacementAccessions, ControllingExperiments } from './typeutils';


const anisogenicValues = [
    'anisogenic'
];


class Bioexperiment extends React.Component {
    constructor(props) {
        super(props);

    }


    render() {

        const context = this.props.context;
        const itemClass = globals.itemClass(context, 'view-item');
  
        const loggedIn = !!(this.context.session && this.context.session['auth.userid']);
        const adminUser = !!(this.context.session_properties && this.context.session_properties.admin);

        // Determine this experiment's ENCODE version.
        const encodevers = globals.encodeVersion(context);

        // Make list of statuses.
        const statuses = [{ status: context.status, title: 'Status' }];
        if (adminUser && context.internal_status) {
            statuses.push({ status: context.internal_status, title: 'Internal' });
        }

        // Determine whether the experiment is isogenic or anisogenic. No replication_type
        // indicates isogenic.
        const anisogenic = context.replication_type ? (anisogenicValues.indexOf(context.replication_type) !== -1) : false;

        // Get a list of related datasets, possibly filtering on their status.
        let seriesList = [];
        if (context.related_series && context.related_series.length) {
            seriesList = _(context.related_series).filter(biodataset => loggedIn || biodataset.status === 'released');
        }


        // Make a list of reference links, if any.
        const references = pubReferenceList(context.references);

        // Set up breadcrumbs
        // Set up the breadcrumbs.
        const assayTerm = context.assay_term_name ? 'assay_term_name' : 'assay_term_id';
        const assayName = context[assayTerm];
        const assayQuery = `${assayTerm}=${assayName}`;

        const crumbs = [
            { id: 'Bioexperiments' },
            { id: assayName, query: assayQuery, tip: assayName },

        ];


        const crumbsReleased = (context.status === 'released');

        const experimentsUrl = `/search/?type=Bioexperiment&possible_controls.accession=${context.accession}`;

        let biospecimen_summary = [];
        let awards = [];
        let files = context.files;

        for (let i = 0; i < files.length; i++) {
            let biospecimen = files[i].biospecimen;
            let award = files[i].award;
            biospecimen_summary.push(biospecimen);
            awards.push(award)
        }
        let uniqueBiospecimen_summary = Array.from(new Set(biospecimen_summary.map(a => a.accession)))
        .map(accession => {
        return biospecimen_summary.find(a => a.accession === accession)
        });
        biospecimen_summary = uniqueBiospecimen_summary;
        
        let uniqueAwards = Array.from(new Set(awards.map(a => a.uuid)))
        .map(uuid => {
        return awards.find(a => a.uuid === uuid)
        });
        awards = uniqueAwards;

        let show_specimen_summary = (<div>
            <dt>biospecimen_summary</dt>
            <dd><strong>Accession: </strong>{biospecimen_summary[0].accession}</dd>
            <dd><strong>Patient: </strong>{biospecimen_summary[0].patient}</dd>
            <dd><strong>Openspecimen ID: </strong>{biospecimen_summary[0].openspecimen_id}</dd>
            <dd><strong>Sample Type: </strong>{biospecimen_summary[0].sample_type}</dd>
            <dd><strong>Tissue Derivatives: </strong>{biospecimen_summary[0].tissue_derivatives}</dd>
            <dd><strong>Tissue Type: </strong>{biospecimen_summary[0].tissue_type}</dd>
            <dd><strong>Species: </strong>{biospecimen_summary[0].species}</dd>
            <dd><strong>Anatomic Site: </strong>{biospecimen_summary[0].anatomic_site}</dd>
        </div>);


        return (
            <div className={globals.itemClass(context, 'view-item')}>
                <header className="row">
                  <div className="col-sm-12">
                    <Breadcrumbs root="/search/?type=Bioexperiment" crumbs={crumbs} crumbsReleased={crumbsReleased} />
                    <h2>Experiment summary for {context.accession}</h2>
                    <ReplacementAccessions context={context} />
                    <ItemAccessories item={context}/>
                  </div>
                </header>
                <Panel >
                    <PanelBody addClasses="panel__split">
                        <div className="panel__split-element">
                            <div className="panel__split-heading panel__split-heading--experiment">
                                <h4>Summary</h4>
                            </div>
                            <dl className="key-value">
                                <div data-test="status">
                                    <dt>Status</dt>
                                    <dd>
                                        <Status item={context} css="dd-status" title="Experiment status" inline />

                                    </dd>
                                </div>

                                <div data-test="assay">
                                    <dt>Assay</dt>
                                    <dd>
                                        {context.assay_term_name}
                                    </dd>
                                </div>

                                {show_specimen_summary}

                            </dl>
                        </div>
                        <div className="panel__split-element">
                            <div className="panel__split-heading panel__split-heading--experiment">
                                <h4>Attribution</h4>
                               
                            </div>
                            <dl className="key-value">
                                <div data-test="lab">
                                    <dt>Lab</dt>
                                    <dd>{context.lab.title}</dd>
                                </div>

                               

                                <div data-test="project">
                                    <dt>Project</dt>
                                    <dd>{awards[0].project}</dd>
                                </div>


                            
                            </dl>
                        </div>

                    </PanelBody>
                </Panel>
                {/*<BioreplicateTable data={context.bioreplicate} tableTitle="Bioreplicates summary"></BioreplicateTable>*/}
                {/* Display the file widget with the facet, graph, and tables */}
                {/* <FileGallery1 context={context} encodevers={encodevers} anisogenic={anisogenic} /> */}



            </div>
        )
    }

}


Bioexperiment.propTypes = {
    context: PropTypes.object, // Target object to display
};

Bioexperiment.defaultProps = {
    context: null,
};

globals.contentViews.register(Bioexperiment, 'Bioexperiment');





