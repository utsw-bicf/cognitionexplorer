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

        const loggedIn = !!(this.context.session && this.context.session['auth.userid']);
        const adminUser = !!(this.context.session_properties && this.context.session_properties.admin);

        // Make list of statuses.
        const statuses = [{ status: context.status, title: 'Status' }];
        if (adminUser && context.internal_status) {
            statuses.push({ status: context.internal_status, title: 'Internal' });
        }
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
        let biospecimen_summary = [];
        let projectSet = new Set();
        let files = context.files;
        if (Object.keys(this.props.context.files).length > 0) {
            for (let i = 0; i < files.length; i++) {
                let biospecimen = files[i].biospecimen;
                let project = files[i].award.project;
                biospecimen_summary.push(biospecimen);
                projectSet.add(project)
            }
            let uniqueBiospecimen_summary = Array.from(new Set(biospecimen_summary.map(a => a.accession)))
                .map(accession => {
                    return biospecimen_summary.find(a => a.accession === accession)
                });
            biospecimen_summary = uniqueBiospecimen_summary;
        }

        let show_specimen_summary = (<div>
            <dt>biospecimen_summary</dt>
            <dd><strong>Accession: </strong>{biospecimen_summary[0].accession}</dd>
            <dd><strong>Patient: </strong>{biospecimen_summary[0].patient}</dd>
            <dd><strong>Openspecimen ID: </strong>{biospecimen_summary[0].openspecimen_id}</dd>
            <dd><strong>Sample Type: </strong>{biospecimen_summary[0].sample_type}</dd>
            <dd><strong>Tissue Derivatives: </strong>{biospecimen_summary[0].tissue_derivatives}</dd>
            <dd><strong>Tissue Type: </strong>{biospecimen_summary[0].tissue_type}</dd>
            <dd><strong>Species: </strong>{biospecimen_summary[0].species}</dd>
            <dd><strong>Anatomic Site: </strong>{biospecimen_summary[0].anatomic_site_display}</dd>
        </div>);

        let hasGenomics = false;
        // if (context.genomic_release.item_status === 'released' && Object.keys(this.props.context.biofile).length > 0) {
        if (Object.keys(this.props.context.files).length > 0) {
            hasGenomics = true;
        }
        return (
            <div className={globals.itemClass(context, 'view-item')}>
                <header className="row">
                    <div className="col-sm-12">
                        <Breadcrumbs root="/search/?type=Bioexperiment" crumbs={crumbs} crumbsReleased={crumbsReleased} />
                        <h2>Experiment summary for {context.accession}</h2>
                        <ReplacementAccessions context={context} />
                        <ItemAccessories item={context} />
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
                                    <dd>{[...projectSet].join(', ')}</dd>
                                </div>



                            </dl>
                        </div>

                    </PanelBody>
                </Panel>
                {/* <BioreplicateTable data={context.bioreplicate} tableTitle="Bioreplicates summary"></BioreplicateTable> */}
                {/* Display the file widget with the facet, graph, and tables */}
                {/* <FileGallery1 context={context} encodevers={encodevers} anisogenic={anisogenic} /> */}
                { hasGenomics && <FileGallery1 context={context} />}



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






