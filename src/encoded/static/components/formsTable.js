import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class FormsTable extends React.Component {
    constructor(props) {
        super(props);
        this.forms = this.transformData(this.props.data);
    }

    transformData(data) {
        let forms = []
        console.log(data.ivp_a1[0]['@id'])
        let visitObj = {
            visit_name: "Initial Visit",
            a1_id: "/ivp_a1s/824cd6fd-ec55-4336-94ff-5529e5b01ae7/"
            //a1_id: data.ivp_a1[0]['@id']           
        }
        //if (data[ivp_a2].length > 0) {
        //    visitObj.a2_id = data[ivp_a2][0]['@id'] 
        //}
        forms[0] = visitObj


        return forms
    }

    renderData() {
       
        const tableColumns = {
            visit_name: {
                title: 'Visit',
                
            },
            a1_id: {
                title: 'Form A1',
                display: form => <a href={form.a1_id}>Form A1</a>,
            },

      
        };
        return (
            <SortTablePanel title={this.props.tableTitle}>
                <SortTable list={this.forms} columns={tableColumns} />
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

export default FormsTable;

