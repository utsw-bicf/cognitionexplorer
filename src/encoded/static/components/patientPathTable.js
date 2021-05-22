/* eslint-disable linebreak-style */
// eslint-disable-next-line linebreak-style
import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class patientPathTable extends React.Component {
    constructor(props) {
        super(props);
        this.surgery = this.transformData(this.props.data);
    }

    transformData(data) {
        let surgeryData = [];
        let index = 0;

        for (let i = 0; i < data.length; i++) {
            let obj1 = {
                surgery_accession: data[i].accession,
                surgery_id: data[i]['@id'],
                surgery_date: data[i].date,
            }
            if (data[i].surgery_procedure.length > 0){

                for (let j = 0; j < data[i].surgery_procedure.length; j++) {

                    let obj2 = {
                        surgery_accession: obj1.surgery_accession,
                        surgery_id: obj1.surgery_id,
                        surgery_date: obj1.surgery_date,
                        procedure_type: data[i].surgery_procedure[j].surgery_treatment,

                    }
                    if (data[i].surgery_procedure[j].pathology_report.length > 0) {
                        for (let k = 0; k < data[i].surgery_procedure[j].pathology_report.length; k++) {
                            let obj3 = {
                                surgery_accession: obj1.surgery_accession,
                                surgery_id: obj1.surgery_id,
                                surgery_date: obj1.surgery_date,
                                procedure_type: data[i].surgery_procedure[j].surgery_treatment,
                                path_accession: data[i].surgery_procedure[j].pathology_report[k].accession,
                                path_id: data[i].surgery_procedure[j].pathology_report[k]['@id'],
                                path_histology: data[i].surgery_procedure[j].pathology_report[k].histology,
                                t_stage: data[i].surgery_procedure[j].pathology_report[k].t_stage,
                                n_stage: data[i].surgery_procedure[j].pathology_report[k].n_stage,
                                m_stage: data[i].surgery_procedure[j].pathology_report[k].m_stage,
                            }
                             surgeryData[index] = obj3;
                             index++;
                        }

                    }else {
                        surgeryData[index] = obj2;
                        index++;
                    }
                }


            } else {
                surgeryData[index] = obj1;
                index++;
            }

        }
        return surgeryData;
    }

    renderData() {

            const tableColumns = {
                surgery_date: {
                    title: 'Surgery Date',
                },
                surgery_accession: {
                    title: 'Surgery',
                    display: surgeryData => <a href={surgeryData.surgery_id}>{surgeryData.surgery_accession}</a>,
                },
                procedure_type: {
                    title: 'Surgery Procedure',
                },

                path_accession: {
                    title: 'Pathology Report',
                    display: surgeryData => <a href={surgeryData.path_id}>{surgeryData.path_accession}</a>,
                },
                path_histology: {
                    title: 'Histologic Subtype',
                },
                t_stage: {
                    title: 'pT Stage',
                },
                n_stage: {
                    title: 'pN Stage',
                },
                m_stage: {
                    title: 'pM Stage',
                },


            };
            return (
                <SortTablePanel title={this.props.tableTitle}>
                    <SortTable list={this.surgery} columns={tableColumns} />
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

export default patientPathTable;
