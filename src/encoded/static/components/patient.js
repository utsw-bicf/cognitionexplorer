import React from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelBody, PanelHeading } from '../libs/bootstrap/panel';
import * as globals from './globals';
import { Breadcrumbs } from './navigation';
import { RelatedItems } from './item';
import { DisplayAsJson } from './objectutils';
import formatMeasurement from './../libs/formatMeasurement';
import { CartToggle } from './cart';
import Status from './status';
import PatientChart from "./PatientChart";
import GermlineTable from './GermlineTable';



/* eslint-disable react/prefer-stateless-function */
class Patient extends React.Component {
    render() {
        const context = this.props.context;
        const itemClass = globals.itemClass(context, 'view-item');

        // Set up breadcrumbs
        const crumbs = [
            { id: 'Patients' },
            { id: <i>{context.accession}</i> },
        ];

        const crumbsReleased = (context.status === 'released');
        console.log(context.accession);
    //     console.log(context.germline);
    //     let germlineFilters= [];
    //    germlineFilters = context.germline;
    //    console.log(germlineFilters);
    //     let germlineGenes=[];
    //     germlineGenes= germlineFilters.filter(i=>{return i.significance==="Positive"||i.significance==="Variant" ||i.significance==="Positive Variant" }).map(i=>{return  [i.target, i.significance]});
    //     // || i.significance==='Variant'
    //     console.log(germlineGenes);
        
        

        //const data = context.germline; 
        //const list= [];
        //let list = data.map(i=>{return i.target});
        //console.log(list);
        // for (let i = 0; i < data.lentgh; i++)
        // {  
        //     console.log (Object.keys(i)[target]);
        // }
        

        return (
            <div className={globals.itemClass(context, 'view-item')}>
                <header className="row">
                <script src="https://cdn.zingchart.com/zingchart.min.js"></script>
                <script src="http://cdn.zingchart.com/modules/zingchart-grid.min.js"></script>
                <script src="https://unpkg.com/axios@0.18.0/dist/axios.min.js" ></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js" ></script>
                    <div className="col-sm-12">
                        <Breadcrumbs root="/search/?type=Patient" crumbs={crumbs} crumbsReleased={crumbsReleased} />
                        <h2>{context.accession}</h2>

                    </div>
                </header>

                <Panel>
                    <PanelHeading>
                        <h4>Patient Information</h4>
                    </PanelHeading>
                    <PanelBody>
                    <dl className="key-value">
                        <div data-test="status">
                            <dt>Status</dt>
                            <dd><Status item={context} inline /></dd>
                        </div>
                        <div data-test="gender">
                            <dt>Gender</dt>
                            <dd>{context.gender}</dd>
                        </div>

                        <div data-test="ethnicity">
                            <dt>Ethnicity</dt>
                            <dd>{context.ethnicity}</dd>
                        </div>

                        <div data-test="race">
                            <dt>Race</dt>
                            <dd>{context.race}</dd>
                        </div>

                        <div data-test="age">
                            <dt>Age at diagnosis</dt>
                            <dd className="sentence-case">
                                {formatMeasurement(context.age, context.age_units)}
                            </dd>
                        </div>

                    </dl>
                    </PanelBody>
                </Panel>
                
                <PatientChart chartId="labsChart" data={context.labs} chartTitle ="Lab Results Over Time"></PatientChart>
                <PatientChart chartId="vitalChart" data={context.vitals} chartTitle="Vital Results Over Time"></PatientChart>
                <GermlineTable tableId="germlineMutation" data={context.germline} tableTitle="Germline mutations " ></GermlineTable>


            </div>
        );
    }
}
/* eslint-enable react/prefer-stateless-function */

Patient.propTypes = {
    context: PropTypes.object, // Target object to display
};

Patient.defaultProps = {
    context: null,
};

globals.contentViews.register(Patient, 'Patient');
