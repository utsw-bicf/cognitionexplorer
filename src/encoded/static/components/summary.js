import React from 'react';
import PropTypes from 'prop-types';
import { Panel, PanelBody } from '../libs/ui/panel';
import * as globals from './globals';
import { FacetList } from './search';
import { ViewControls } from './view_controls';


/**
 * Generate an array of data from one facet bucket for displaying in a chart, with one array entry
 * per experiment status. The order of the entries in the resulting array correspond to the order
 * of the statuses in `labels`.
 *
 * @param {array} buckets - Buckets for one facet returned in summary search results.
 * @param {array} labels - Experiment status labels.
 * @return {array} - Data extracted from buckets with an order of values corresponding to `labels`.
 */
function generateStatusData(buckets, labels) {
    // Fill the array to the proper length with zeroes to start with. Actual non-zero data will
    // overwrite the appropriate entries.
    const statusData = Array.from({ length: labels.length }, (() => 0));

    // Convert statusData to a form createBarChart understands.
    if (buckets && buckets.length > 0) {
        buckets.forEach((bucketItem) => {
            const statusIndex = labels.indexOf(bucketItem.key);
            if (statusIndex !== -1) {
                statusData[statusIndex] = bucketItem.doc_count;
            }
        });
    }
    return statusData;
}





class SummaryBody extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        const { context } = this.props;
        let numOfKidneySamples = 0;
        let numOfTumorgraftSample = 0

        let facets = context.facets;
        let filters = context.filters;
        let isKidneySampleIncluded = this.getIsIncluded(filters, "biospecimen.anatomic_site", "Kidney, NOS");

        let isMouseSampleIncluded = this.getIsIncluded(filters, "biospecimen.species", "Mouse");

        let anatomic_site = facets.filter(obj => {
            return obj.field === "biospecimen.anatomic_site"
          })
        if (anatomic_site && anatomic_site.length > 0){
            let terms = anatomic_site[0].terms;
            let result = terms.filter(obj => {
                return obj.key === "Kidney, NOS"
            })
            if (result && result.length > 0) {
                if (isKidneySampleIncluded) {
                    numOfKidneySamples = result[0].doc_count;
                } else {
                    numOfKidneySamples = 0;
                }
                
            }
        }
        let species = facets.filter(obj => {
            return obj.field === "biospecimen.species"
          })
        if (species && species.length > 0){
            let terms = species[0].terms;
            let result = terms.filter(obj => {
                return obj.key === "Mouse"
            })
            if (result && result.length > 0) {
                if (isMouseSampleIncluded) {
                    numOfTumorgraftSample = result[0].doc_count;
                } else {
                    numOfTumorgraftSample = 0;
                }
                
            }
        }
        
        let totalContainerStyle = {
            display: "flex",
            justifyContent: "space-between"
        };
        let totalLabelStyle ={
            minWidth: "25%"
        };
        let numberStyle = {
            fontSize: "80px",
            minWidth: "50%"
        }
        let noteStyle = {
            fontSize: "20px"
        }
        const selectedStageTerms = this.getSelectedTerms(facets, filters, "dominant_tumor.stage")
        const stageData = this.getPieChartData(facets, "dominant_tumor.stage", selectedStageTerms)
        const selectedsubtypeTerms = this.getSelectedTerms(facets, filters, "dominant_tumor.histology_filter")
        const subtypeData = this.getPieChartData(facets, "dominant_tumor.histology_filter", selectedsubtypeTerms)
        const selectedSpecimenTerms = this.getSelectedTerms(facets, filters, "biospecimen.tissue_derivatives")
        const specimenData = this.getBarChartData(facets, "biospecimen.tissue_derivatives",selectedSpecimenTerms )
        const selectedMetsTerms = this.getSelectedTerms(facets, filters, "metastasis.site")
        const metsData = this.getBarChartData(facets, "metastasis.site", selectedMetsTerms)

        return (
            <div className="summary-header">
                <header>
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                </header>
                <div className="summary-header__title_control">
                    <div className="summary-header__title">
                        <h1>{this.props.context.title}</h1>
                    </div>
                </div>
                <div className="summary-controls">
                    <div style={totalContainerStyle}>
                        
                        <label style={totalLabelStyle}>
                            <ul style={{ listStyleType: "none" }}>
                            <li><span style={numberStyle}>{context.total}</span><span>&nbsp;</span><span>&nbsp;</span><FontAwesomeIcon icon={faHospitalUser} size="4x" /></li>
                            <li><span style={noteStyle}>Patients</span></li>
                            </ul>
                        </label>

                        <label style={totalLabelStyle}>
                            <ul style={{ listStyleType: "none" }}>
                            <li><span style={numberStyle}>{numOfKidneySamples}</span><span>&nbsp;</span><span>&nbsp;</span><FontAwesomeIcon icon={faVial} size="4x" /></li>
                            <li><span style={noteStyle}>Patients with Primary Kidney Samples</span></li>
                            </ul>
                        </label>

                        <label style={totalLabelStyle}>
                            <ul style={{ listStyleType: "none" }}>
                            <li><span style={numberStyle}>{numOfTumorgraftSample}</span><span>&nbsp;</span><span>&nbsp;</span><FontAwesomeIcon icon={faDisease} size="4x" /></li>
                            <li><span style={noteStyle}>Patients with Tumorgraft Samples</span></li>
                            </ul>
                        </label>

                        <label style={totalLabelStyle}>
                            <ul style={{ listStyleType: "none" }}>
                            <li><span style={numberStyle}>0</span><span>&nbsp;</span><span>&nbsp;</span><FontAwesomeIcon icon={faDna} size="4x" /></li>
                            <li><span style={noteStyle}>Patients with Genomics Data</span></li>
                            </ul>
                        </label>                        
                    </div>
                    <hr/>
                    <Panel>
                        <PanelBody addClasses="panel__split">
                            <div className="panel__split-element">
                                <SummaryChart  title="Dominant Tumor Histologic Subtypes" chartId="summaryChart1" data={subtypeData} ></SummaryChart>
                            </div>
                            <div className="panel__split-element">
                                <SummaryChart  title="Dominant Tumor Stage" chartId="summaryChart2" data={stageData} ></SummaryChart>
                            </div>
                        
                        </PanelBody>
                        <hr/>
                        <PanelBody addClasses="panel__split">
                            <div className="panel__split-element">
                                <SummaryChart  title="Metastatic Site" chartId="summaryChart3" data={metsData} ></SummaryChart>
                            </div>
                            <div className="panel__split-element">
                                <SummaryChart  title="Biospecimen Inventory" chartId="summaryChart4" data={specimenData} ></SummaryChart>
                            </div>

                        </PanelBody>
                    </Panel>                  
                    <hr/>
                </div>
            </div>
        );
    }


    getPieChartData(facets, field, selectedTerms){
        let data = [];
        let values = [];
        let labels = [];
        let results =  facets.filter(obj => {
            return obj.field === field
          })
        if (results && results.length > 0){
            let terms = results[0].terms;
            let i;
            for (i = 0; i < terms.length; i++) {
                let result = terms[i];
                if (selectedTerms.includes(result.key)) {
                    values.push(result.doc_count);
                    labels.push(result.key);
                }
                


            }

        }
        data = [{
            values: values,
            labels: labels,
            type: 'pie'
          }

        ]
        return data;

    }

    getBarChartData(facets, field, selectedTerms){
        let data = [];
        let x = [];
        let y = [];
        let results =  facets.filter(obj => {
            return obj.field === field
          })
        if (results && results.length > 0){
            let terms = results[0].terms;
            let i;
            for (i = 0; i < terms.length; i++) {
                let result = terms[i];
                if (selectedTerms.includes(result.key)) {
                    y.push(result.doc_count);
                    x.push(result.key)
                }
            }

        }
        data = [{
            x: x,
            y: y,
            type: 'bar'
          }

        ]
        return data;

    }


    getIsIncluded(filters, field, term) {
        let isIncluded = true;
        let excludeField = field + "!";
        let results = filters.filter(obj => {
            return obj.field === excludeField;
        })
        if (results && results.length > 0){
            for (let i = 0; i < results.length; i++) {
                if (results[i].term === term) {
                    return false;
                }
            }

        }
        results = filters.filter(obj => {
                    return obj.field === field;
                })
                
        if (results && results.length > 0){
            let hasTerm = false;
            for (let i = 0; i < results.length; i++) {
                if (results[i].term === term) {
                    hasTerm = true;
                    break;
                }
            }
            if (!hasTerm){
                return false
            }
            
        }

        return isIncluded;
    }

    getSelectedTerms(facets, filters, field){
        let allterms = [];
        let selectedTerms = [];
        let excludeField = field + "!";
        
        let results = filters.filter(obj => {
            return obj.field === field;
        })
        if (results && results.length > 0){
            for (let i = 0; i < results.length; i++) {    
                selectedTerms.push(results[i].term);    
            }

        }


        results =  facets.filter(obj => {
            return obj.field === field
          })
        if (results && results.length > 0){
            let terms = results[0].terms;
            let i;
            for (i = 0; i < terms.length; i++) {
                let result = terms[i];
               
                allterms.push(result.key);
            }

        }

        results = filters.filter(obj => {
            return obj.field === excludeField;
        })
        if (results && results.length > 0){
            for (let i = 0; i < results.length; i++) {  
                allterms = allterms.filter(x=>x!=results[i].term); 
                   
            }

        }

        if (selectedTerms.length > 0) {
            
            return selectedTerms;
 
        } else {
            return allterms;
        }
    }

    chooseOrganism(e) {
        this.setState({
            selectedOrganism: e.currentTarget.id,
        });
        const parsedUrl = url.parse(this.props.context['@id']);
        const query = new QueryString(parsedUrl.query);
        
  
        query.replaceKeyValue(organismField, e.currentTarget.id, '');
        const href = `?${query.format()}`;
        this.context.navigate(href);
    }
    render() {
        const searchQuery = url.parse(this.props.context['@id']).search;
        const query = new QueryString(searchQuery);
        const nonPersistentQuery = query.clone();
        nonPersistentQuery.deleteKeyValue('?type');
        const clearButton = nonPersistentQuery.queryCount() > 0 && query.queryCount('?type') > 0;
        return (
            <div className="summary-header">
                <div className="summary-header__title_control">
                    <div className="summary-header__title">
                        <h1>{this.props.context.title}</h1>
                    </div>
                    <ClearFilters searchUri={this.props.context.clear_filters} enableDisplay={!!clearButton} />
                </div>
                <div className="summary-controls">
                    <div className="organism-button-instructions">Choose an organism:</div>
                    <div className="organism-button-container">
                        {organismTerms.map(term =>
                            <button
                                id={term}
                                onClick={e => this.chooseOrganism(e)}
                                className={`organism-button ${term.replace(' ', '-')} ${this.state.selectedOrganism === term ? 'active' : ''}`}
                                key={term}
                            >
                                
                                <span>{term}</span>
                            </button>
                        )}
                    </div>
                    <div className={`results-controls ${this.state.selectedOrganism.length > 0 ? `${this.state.selectedOrganism.replace(' ', '-')}` : ''}`}>
                        <div className="results-count">There {this.props.context.total > 1 ? 'are' : 'is'} <b className="bold-total">{this.props.context.total}</b> result{this.props.context.total > 1 ? 's' : ''}.</div>
                        <div className="view-controls-container">
                            <ViewControls results={this.props.context} alternativeNames={['Search list', 'Tabular report', 'Summary matrix']} />
                        </div>
                    </div>
                    {(this.state.selectedOrganism === 'Homo sapiens') ?
                        <React.Fragment>
                            <div className="flex-container">
                               
                                <SummaryData context={this.props.context} displayCharts={'donuts'} />
                            </div>
                            <div className="summary-content">
                                <SummaryData context={this.props.context} displayCharts={'area'} />
                            </div>
                        </React.Fragment>
                    :
                        <React.Fragment>
                            <SummaryHorizontalFacets context={this.props.context} facetList={'all'} />
                            <div className="summary-content">
                                <SummaryData context={this.props.context} displayCharts={'all'} />
                            </div>
                        </React.Fragment>
                    }
                </div>
            </div>
        );
    }
}

SummaryBody.propTypes = {
    context: PropTypes.object.isRequired, // Summary search result object
};

SummaryBody.contextTypes = {
    navigate: PropTypes.func,
    location_href: PropTypes.string,
};

// Render the entire summary page based on summary search results.
const Summary = (props) => {
    const { context } = props;
    const itemClass = globals.itemClass(context, 'view-item');


    if (context.total) {
        return (
            <div>
            <header className="row">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </header>
            <Panel addClasses={itemClass}>
                <PanelBody>
                    <div className="search-results">
                        <div className="search-results__facets">
                            <FacetList context={context} facets={context.facets} filters={context.filters} searchBase={context.searchBase} docTypeTitleSuffix="summary" />
                        </div>
                        <div className="search-results__report-list">
                            <h4>Showing results</h4>
                            <div className="results-table-control">
                                <div className="results-table-control__main">
                                    <ViewControls results={context} />
                                </div>  
                            </div>
                            <SummaryBody context={context} />

                        </div>
                    </div>
                </PanelBody>
            </Panel>
            </div>
        );
    }
    return <h4>No results found</h4>;
};

Summary.propTypes = {
    context: PropTypes.object.isRequired, // Summary search result object
};

globals.contentViews.register(Summary, 'Summary');





