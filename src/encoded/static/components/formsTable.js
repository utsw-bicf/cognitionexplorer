import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class FormsTable extends React.Component {
    constructor(props) {
        super(props);
        this.forms = this.transformData(this.props.data);
    }

    transformData(data) {
        let forms = []

        let visitObj = {
            visit_number: 1,
            visit_name: "Initial Visit",
            a1_name: "ivp_a1",
            a1_id: data.ivp_a1[0]['@id'],
            a2_name: "",  
            a2_id: ""
                     
        }
        if (data.ivp_a2.length > 0) {
            visitObj.a2_id = data.ivp_a2[0]['@id']
            visitObj.a2_name = "ivp_a2" 
        } 
        forms[0] = visitObj
        let followUpVisistTimes = this.getFollowUpVisitTimes(data)

        console.log(followUpVisistTimes)
        for (let i = 0; i < followUpVisistTimes.length; i++) {
            let visitObj = {
                visit_number: i + 2,
                visit_name: "Fllow Up Visit " + (i + 1),
                a1_name: "",
                a1_id: "",
                a2_name: "",  
                a2_id: ""          
            }
            forms.push(visitObj)
        }
        console.log(forms)
        for (let i = 0; i < data.fvp_a1.length; i++) {
            let index = followUpVisistTimes.indexOf(data.fvp_a1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a1_id = data.fvp_a1[i]['@id']
            forms[index].a1_name = "fvp_a1"

        }
        for (let i = 0; i < data.fvp_a2.length; i++) {
            let index = followUpVisistTimes.indexOf(data.fvp_a2[i]["visdate"]) + 1;
            console.log(index)
            forms[index].a2_id = data.fvp_a2[i]['@id']
            forms[index].a2_name = "fvp_a2"

        }


        return forms
    }

    getFollowUpVisitTimes(data) {
        let followUpVisistTimes = []
        data.fvp_a1.forEach(element => followUpVisistTimes.push(element["visdate"]))
        data.fvp_a2.forEach(element => followUpVisistTimes.push(element["visdate"]))
        followUpVisistTimes = [...new Set(followUpVisistTimes)];
        followUpVisistTimes = Array.from(followUpVisistTimes);
        followUpVisistTimes.sort(function(a,b) {
            a = a.split('-').join('');
            b = b.split('-').join('');
            return a > b ? 1 : a < b ? -1 : 0;
        });
        return followUpVisistTimes
        

    }

    renderData() {
       
        const tableColumns = {
            visit_number: {
                title: "No."
            },
            visit_name: {
                title: 'Visit',
                
            },
            a1_id: {
                title: 'Form A1',
                display: form => <a href={form.a1_id}>{form.a1_name}</a>,
            },
            a2_id: {
                title: 'Form A2',
                display: form => <a href={form.a2_id}>{form.a2_name}</a>,
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


