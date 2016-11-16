import React from 'react';
import moment from 'moment';
import { Panel, PanelHeading, PanelBody } from '../libs/bootstrap/panel';
import globals from './globals';
import { AuditIndicators, AuditDetail, AuditMixin } from './audit';
import { DbxrefList } from './dbxref';
import { ProjectBadge } from './image';
import { StatusLabel } from './statuslabel';


const File = React.createClass({
    propTypes: {
        context: React.PropTypes.object, // File object being displayed
    },

    mixins: [AuditMixin],

    render: function () {
        const { context } = this.props;
        const itemClass = globals.itemClass(context, 'view-item');
        const altacc = (context.alternate_accessions && context.alternate_accessions.length) ? context.alternate_accessions.join(', ') : null;
        const aliasList = (context.aliases && context.aliases.length) ? context.aliases.join(', ') : '';
        const datasetAccession = globals.atIdToAccession(context.dataset);

        // Make array of superceded_by accessions.
        let supersededBys = [];
        if (context.superseded_by && context.superseded_by.length) {
            supersededBys = context.superseded_by.map(supersededBy => globals.atIdToAccession(supersededBy));
        }

        // Collect up relevant pipelines.
        let pipelines = [];
        if (context.analysis_step_version && context.analysis_step_version.analysis_step.pipelines && context.analysis_step_version.analysis_step.pipelines.length) {
            pipelines = context.analysis_step_version.analysis_step.pipelines;
        }

        return (
            <div className={itemClass}>
                <header className="row">
                    <div className="col-sm-12">
                        <h2>{context.accession}{' / '}<span className="sentence-case">{`${context.file_format}${context.file_format_type ? ` (${context.file_format_type})` : ''}`}</span></h2>
                        {altacc ? <h4 className="repl-acc">Replaces {altacc}</h4> : null}
                        {supersededBys.length ? <h4 className="superseded-acc">Superseded by {supersededBys.join(', ')}</h4> : null}
                        <div className="status-line">
                            {context.status ?
                                <div className="characterization-status-labels">
                                    <StatusLabel title="Status" status={context.status} />
                                </div>
                            : null}
                            {context.audit ? <AuditIndicators audits={context.audit} id="file-audit" /> : null}
                        </div>
                    </div>
                </header>
                <AuditDetail audits={context.audit} except={context['@id']} id="file-audit" />
                <Panel addClasses="data-display">
                    <div className="split-panel">
                        <div className="split-panel__part split-panel__part--p50">
                            <div className="split-panel__heading"><h4>Summary</h4></div>
                            <div className="split-panel__content">
                                <dl className="key-value">
                                    <div data-test="term-name">
                                        <dt>Dataset</dt>
                                        <dd><a href={context.dataset} title={`View page for dataset ${datasetAccession}`}>{datasetAccession}</a></dd>
                                    </div>

                                    {context.replicate ?
                                        <div data-test="bioreplicate">
                                            <dt>Biological replicate(s)</dt>
                                            <dd>{`[${context.replicate.biological_replicate_number}]`}</dd>
                                        </div>
                                    : (context.biological_replicates && context.biological_replicates.length ?
                                        <div data-test="bioreplicate">
                                            <dt>Biological replicate(s)</dt>
                                            <dd>{`[${context.biological_replicates.join(', ')}]`}</dd>
                                        </div>
                                    : null)}

                                    {context.replicate ?
                                        <div data-test="techreplicate">
                                            <dt>Technical replicate</dt>
                                            <dd>{context.replicate.technical_replicate_number}</dd>
                                        </div>
                                    : (context.biological_replicates && context.biological_replicates.length ?
                                        <div data-test="techreplicate">
                                            <dt>Technical replicate</dt>
                                            <dd>{'-'}</dd>
                                        </div>
                                    : null)}

                                    {pipelines.length ?
                                        <div data-test="pipelines">
                                            <dt>Pipelines</dt>
                                            <dd>
                                                {pipelines.map((pipeline, i) =>
                                                    <span key={i}>
                                                        {i > 0 ? <span>{','}<br /></span> : null}
                                                        <a href={pipeline['@id']}>{pipeline.title}</a>
                                                    </span>
                                                )}
                                            </dd>
                                        </div>
                                    : null}

                                    <div data-test="md5sum">
                                        <dt>MD5sum</dt>
                                        <dd>{context.md5sum}</dd>
                                    </div>

                                    {context.content_md5sum ?
                                        <div data-test="contentmd5sum">
                                            <dt>Content MD5sum</dt>
                                            <dd>{context.content_md5sum}</dd>
                                        </div>
                                    : null}

                                    {context.read_count ?
                                        <div data-test="readcount">
                                            <dt>Read count</dt>
                                            <dd>{context.read_count}</dd>
                                        </div>
                                    : null}

                                    {context.file_size ?
                                        <div data-test="filesize">
                                            <dt>File size</dt>
                                            <dd>{context.file_size}</dd>
                                        </div>
                                    : null}

                                    {context.mapped_read_length ?
                                        <div data-test="mappreadlength">
                                            <dt>Mapped read length</dt>
                                            <dd>{context.mapped_read_length}</dd>
                                        </div>
                                    : null}
                                </dl>
                            </div>
                        </div>

                        <div className="split-panel__part split-panel__part--p50">
                            <div className="split-panel__heading">
                                <h4>Attribution</h4>
                                <ProjectBadge award={context.award} addClasses="badge-heading" />
                            </div>
                            <div className="split-panel__content">
                                <dl className="key-value">
                                    <div data-test="lab">
                                        <dt>Lab</dt>
                                        <dd>{context.lab.title}</dd>
                                    </div>

                                    {context.award.pi && context.award.pi.lab ?
                                        <div data-test="awardpi">
                                            <dt>Award PI</dt>
                                            <dd>{context.award.pi.lab.title}</dd>
                                        </div>
                                    : null}

                                    <div data-test="submittedby">
                                        <dt>Submitted by</dt>
                                        <dd>{context.submitted_by.title}</dd>
                                    </div>

                                    {context.award.project ?
                                        <div data-test="project">
                                            <dt>Project</dt>
                                            <dd>{context.award.project}</dd>
                                        </div>
                                    : null}

                                    {context.date_created ?
                                        <div data-test="datecreated">
                                            <dt>Date added</dt>
                                            <dd>{moment.utc(context.date_created).format('YYYY-MM-DD')}</dd>
                                        </div>
                                    : null}

                                    {context.dbxrefs && context.dbxrefs.length ?
                                        <div data-test="externalresources">
                                            <dt>External resources</dt>
                                            <dd><DbxrefList values={context.dbxrefs} /></dd>
                                        </div>
                                    : null}

                                    {aliasList ?
                                        <div data-test="aliases">
                                            <dt>Aliases</dt>
                                            <dd className="sequence">{aliasList}</dd>
                                        </div>
                                    : null}

                                    {context.submitted_file_name ?
                                        <div data-test="submittedfilename">
                                            <dt>Original file name</dt>
                                            <dd className="sequence">{context.submitted_file_name}</dd>
                                        </div>
                                    : null}
                                </dl>
                            </div>
                        </div>
                    </div>
                </Panel>

                {context.file_format === 'fastq' ?
                    <SequenceFileInfo file={context} />
                : null}

            </div>
        );
    },
});

globals.content_views.register(File, 'File');


// Display the sequence file summary panel for fastq files.
const SequenceFileInfo = React.createClass({
    propTypes: {
        file: React.PropTypes.object.isRequired, // File being displayed
    },

    render: function () {
        const { file } = this.props;
        const pairedWithAccession = file.paired_with ? globals.atIdToAccession(file.paired_with) : '';

        return (
            <Panel>
                <PanelHeading>
                    <h4>Sequencing file information</h4>
                </PanelHeading>

                <PanelBody>
                    <dl className="key-value">
                        {file.platform ?
                            <div data-test="platform">
                                <dt>Platform</dt>
                                <dd><a href={file.platform['@id']} title="View page for this platform">{file.platform.title ? file.platform.title : file.platform.term_id}</a></dd>
                            </div>
                        : null}

                        {file.flowcell_details && file.flowcell_details.length ?
                            <div data-test="flowcelldetails">
                                <dt>Flowcell</dt>
                                <dd><FlowcellDetails flowcells={file.flowcell_details} /></dd>
                            </div>
                        : null}

                        {file.fastq_signature && file.fastq_signature.length ?
                            <div data-test="fastqsignature">
                                <dt>Fastq flowcell signature</dt>
                                <dd>{file.fastq_signature.join(', ')}</dd>
                            </div>
                        : null}

                        {file.run_type ?
                            <div data-test="runtype">
                                <dt>Run type</dt>
                                <dd>{file.run_type}</dd>
                            </div>
                        : null}

                        {file.read_length ?
                            <div data-test="readlength">
                                <dt>Flowcell</dt>
                                <dd>{file.read_length}</dd>
                            </div>
                        : null}

                        {file.paired_end ?
                            <div data-test="pairedend">
                                <dt>Paired end identifier</dt>
                                <dd>{file.paired_end}</dd>
                            </div>
                        : null}

                        {file.controlled_by && file.controlled_by.length ?
                            <div data-test="controlledby">
                                <dt>Controlled by</dt>
                                <dd>
                                    {file.controlled_by.map((controlFile, i) => {
                                        const controlFileAccession = globals.atIdToAccession(controlFile);
                                        return (
                                            <span>
                                                {i > 0 ? <span>, </span> : null}
                                                <a href={controlFile} title={`View page for file ${controlFileAccession}`}>{controlFileAccession}</a>
                                            </span>
                                        );
                                    })}
                                </dd>
                            </div>
                        : null}

                        {file.paired_with ?
                            <div data-test="pairedwith">
                                <dt>File pairing</dt>
                                <dd><a href={file.paired_with} title={`View page for file ${pairedWithAccession}`}>{pairedWithAccession}</a></dd>
                            </div>
                        : null}
                    </dl>
                </PanelBody>
            </Panel>
        );
    },
});


// Render an array of flow cell details into a <dd>
const FlowcellDetails = React.createClass({
    propTypes: {
        flowcells: React.PropTypes.array, // Array of flowcell_detail objects
    },

    render: function () {
        const { flowcells } = this.props;

        return (
            <div className="flowcell-details">
                {flowcells.map((flowcell) => {
                    return (
                        <Panel addClasses="flowcell-details__panel">
                            <PanelHeading addClasses="flowcell-details__header">
                                {flowcell.machine ? <h5>{flowcell.machine}</h5> : <h5>Unspecified machine</h5>}
                            </PanelHeading>
                            <PanelBody addClasses="flowcell-details__body">
                                {flowcell.flowcell ?
                                    <div className="flowcell-details__item">
                                        <strong>ID: </strong>{flowcell.flowcell}
                                    </div>
                                : null}

                                {flowcell.lane ?
                                    <div className="flowcell-details__item">
                                        <strong>Lane: </strong> {flowcell.lane}
                                    </div>
                                : null}

                                {flowcell.barcode ?
                                    <div className="flowcell-details__item">
                                        <strong>Barcode: </strong> {flowcell.barcode}
                                    </div>
                                : null}

                                {flowcell.barcode_in_read ?
                                    <div className="flowcell-details__item">
                                        <strong>Barcode in read: </strong> {flowcell.barcode_in_read}
                                    </div>
                                : null}

                                {flowcell.barcode_position ?
                                    <div className="flowcell-details__item">
                                        <strong>Barcode position: </strong> {flowcell.barcode_position}
                                    </div>
                                : null}

                                {flowcell.chunk ?
                                    <div className="flowcell-details__item">
                                        <strong>Chunk: </strong> {flowcell.chunk}
                                    </div>
                                : null}
                            </PanelBody>
                        </Panel>
                    );
                })}
            </div>
        );
    },
});
