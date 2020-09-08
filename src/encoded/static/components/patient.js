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
import CollapsiblePanel from './collapsiblePanel';
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
  render() {

    const context = this.props.context;
    const itemClass = globals.itemClass(context, 'view-item');
    // Set up breadcrumbs
    const crumbs = [
      { id: 'Patients' },
      { id: <i>{context.accession}</i> },
    ];
    const crumbsReleased = (context.status === 'released');





    return (
      <div className={globals.itemClass(context, 'view-item')}>
        <header className="row">
          <script src="https://cdn.plot.ly/plotly-1.51.3.min.js"></script>
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
              <div data-test="racial">
                <dt>Race</dt>
                <dd>{context.racial}</dd>
              </div>

            </dl>
          </PanelBody>
        </Panel>
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

