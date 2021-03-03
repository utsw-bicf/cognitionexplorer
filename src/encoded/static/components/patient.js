import React from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelBody, PanelHeading } from '../libs/ui/panel';
import * as globals from './globals';
import { Breadcrumbs } from './navigation';
import { RelatedItems } from './item';
import { ItemAccessories } from './objectutils';
import formatMeasurement from './../libs/formatMeasurement';
import { CartToggle } from './cart';
import Status from './status';
import CollapsiblePanel from './collapsiblePanel';
import FormsTable from './formsTable';
import { valueOnly } from './objectutils';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleDoubleUp } from "@fortawesome/free-solid-svg-icons";


/* eslint-disable react/prefer-stateless-function */
class Patient extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showButton: false
    }
    this.topFunction = this.topFunction.bind(this);
    this.listenToScroll = this.listenToScroll.bind(this);
  }

  topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }

  listenToScroll() {
    let mybutton = document.getElementById("scrollUpButton");
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }

  }

  componentDidMount() {
    window.addEventListener('scroll', this.listenToScroll)
  }

  componentWillUnmount() {
    window.removeEventListener('scroll', this.listenToScroll)
  }

  createPathPanel() {
    let list = [];
    let surgeryData = this.props.context.surgery;
    if (surgeryData.length > 1) {
      surgeryData.sort((a, b) => Date.parse(a.date) - Date.parse(b.date));
    }
    for (let i = 0; i < surgeryData.length; i++) {
      list.push(<div data-test="surgery"><dt>Surgery Date</dt><dd>{surgeryData[i].date}</dd> </div>)
      if (surgeryData[i].pathology_report && surgeryData[i].pathology_report.length > 0) {
        for (let j = 0; j < surgeryData[i].pathology_report.length; j++) {
          list.push(<div data-test="surgery.pathology_report"><dt>pathology_report</dt><dd><a href={surgeryData[i].pathology_report[j]['@id']}>{surgeryData[i].pathology_report[j].accession}</a></dd> </div>)
          list.push(<div data-test="surgery.pathology_report"><dt>Histologic Subtype</dt><dd>{surgeryData[i].pathology_report[j].histology}</dd> </div>)
          list.push(<div data-test="surgery.pathology_report"><dt>pT stage</dt><dd>{surgeryData[i].pathology_report[j].t_stage}</dd> </div>)
          list.push(<div data-test="surgery.pathology_report"><dt>pN stage</dt><dd>{surgeryData[i].pathology_report[j].n_stage}</dd> </div>)
          list.push(<div data-test="surgery.pathology_report"><dt>pM stage</dt><dd>{surgeryData[i].pathology_report[j].m_stage}</dd> </div>)
        }
      }
      if (i != surgeryData.length - 1) {
        list.push(<div className="row" style={{ borderTop: "1px solid #151313" }}></div>)
      }


    }
    return list

  }
  render() {

    const context = this.props.context;
    const itemClass = globals.itemClass(context, 'view-item');
    // Set up breadcrumbs
    const crumbs = [
      { id: 'Patients' },
      { id: <i>{context.accession}</i> },
    ];
    const crumbsReleased = (context.status === 'released');
    let hasForms =false;
    if (this.props.context.ivp_a1.length > 0) {
        hasForms = true;
    }
    const NACCFormsPanelBody = (
      <FormsTable data={context} ></FormsTable>

    );





    return (
      <div className={globals.itemClass(context, 'view-item')}>
        <header className="row">
          <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <script src="https://unpkg.com/axios@0.18.0/dist/axios.min.js" ></script>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js" ></script>
          <div className="col-sm-12">
            <Breadcrumbs root="/search/?type=Patient" crumbs={crumbs} crumbsReleased={crumbsReleased} />
            <div className="cart__toggle--header">
                <CartToggle element={context} />
            </div>
            <h2>{context.accession}</h2>
            <ItemAccessories item={context}/>
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
              {context.pic &&<div data-test="pic">
                <dt>Patient Initial Category</dt>
                <dd>{valueOnly(context.pic)}</dd>
              </div>}
              {context.gender && <div data-test="gender">
                <dt>Gender</dt>
                <dd>{valueOnly(context.gender)}</dd>
              </div>}
              { context.racial && <div data-test="racial">
                <dt>Race</dt>
                <dd>{valueOnly(context.racial)}</dd>
              </div>}
              { context.ethn && <div data-test="ethn">
                <dt>Spanish, Hispanic or Latino</dt>
                <dd>{valueOnly(context.ethn)}</dd>
              </div>}
              { context.tribe && <div data-test="tribe">
                <dt>Tribe</dt>
                <dd>{valueOnly(context.tribe)}</dd>
              </div>}
              { context.edu && <div data-test="edu">
                <dt>Years of education</dt>
                <dd>{context.edu}</dd>
              </div>}
              { context.retard && <div data-test="retard">
                <dt>Exclude Mental Retardation</dt>
                <dd>{valueOnly(context.retard)}</dd>
              </div>}
              {context.occ && <div data-test="occ">
                <dt>Occupation</dt>
                <dd>{valueOnly(context.occ)}</dd>
              </div>}

            </dl>
          </PanelBody>
        </Panel>
        {hasForms && <CollapsiblePanel panelId="NACCFormsTable" title="NACC Forms" content={NACCFormsPanelBody} />}
        <button onClick={this.topFunction} id="scrollUpButton" title="Go to top"><FontAwesomeIcon icon={faAngleDoubleUp} size="2x" /></button>

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
