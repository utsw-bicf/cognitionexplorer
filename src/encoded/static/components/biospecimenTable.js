/* eslint-disable linebreak-style */
// eslint-disable-next-line linebreak-style
import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class BiospecimenTable extends React.Component {
    constructor(props) {
        super(props);

    }

    renderData() {

            const tableColumns = {
                accession: {
                    title: 'Accession',
                    display: biospecimen => <a href={biospecimen['@id']}>{biospecimen.accession}</a>,
                },
                openspecimen_id: {
                    title: 'OpenSpecimen ID',
                },
                specimen_label: {
                    title: "Specimen label"
                },
                surgery: {
                    title: "Surgery",
                    display: biospecimen => {
                        if (typeof biospecimen['surgery'] != 'undefined') {
                            return  <a href={biospecimen['surgery']}>{biospecimen['surgery'].split('/')[2]}</a>
                        }
                    
                    },
                },
                sample_type: {
                    title: 'Specimen type',
                },
                tissue_derivatives: {
                    title: 'Tissue derivatives',
                },
                tissue_type: {
                    title: 'Specimen pathological type',
                },
                anatomic_site_display: {
                    title: 'Anatomic site',
                },
                species: {
                    title: "Species",
                },
                specimen_lineage: {
                    title: "Specimen lineage"
                },
                activity_status: {
                    title: "Activity status"
                }
            };
            return (
                <SortTablePanel title={this.props.tableTitle}>
                    <SortTable list={this.props.data} columns={tableColumns} />
                </SortTablePanel>
            );


    }

    render() {
        return (
            <div> {this.renderData()}</div>
        );
    }

    componentDidMount() {

        this.renderData();
    }

}

export default BiospecimenTable;

