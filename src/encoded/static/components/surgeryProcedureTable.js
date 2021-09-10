import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class surgeryProcedureTable extends React.Component {
    constructor(props) {
        super(props);
        this.surgeryProcedures = this.transformData(this.props.data);
    }

    transformData(data) {
        let surgeryProceduresData = [];
        let index = 0;
        for (let i = 0; i < data.length; i++) {
            var procedure_type
            if (data[i].surgery_treatment) {
              procedure_type = data[i].surgery_treatment
            }
            else if (data[i].surgery_diagnosis) {
              procedure_type = data[i].surgery_diagnosis
            }
            else {
              procedure_type = data[i].procedure_type
            }
            let obj1 = {
                procedure_type: procedure_type,
            }
            if (data[i].procedure_type == "Nephrectomy") {
                let robotic = "";
                if (data[i].nephrectomy_details.robotic_assist === true) {
                    robotic = 'Yes';
                } else if (data[i].nephrectomy_details.robotic_assist === false) {
                    robotic = 'No';
                }
                let obj2 = {
                    procedure_type: data[i].surgery_diagnosis ,
                    type: data[i].nephrectomy_details.type,
                    approach: data[i].nephrectomy_details.approach,
                    robotic_assist: robotic,
                }
                surgeryProceduresData[index] = obj2;
            } else {
                surgeryProceduresData[index] = obj1;
            }
            index++;

        }
        return surgeryProceduresData;
    }

    renderData() {

            const tableColumns = {
                procedure_type: {
                    title: 'Surgery Procedure',
                },
                type: {
                    title: 'Nephrectomy Type',
                },
                approach: {
                    title: 'Nephrectomy approach',
                },
                robotic_assist: {
                    title: 'Robotic Assist Nephrectomy',
                },



            };
            return (
                <SortTablePanel title={this.props.tableTitle}>
                    <SortTable list={this.surgeryProcedures} columns={tableColumns} />
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

export default surgeryProcedureTable;