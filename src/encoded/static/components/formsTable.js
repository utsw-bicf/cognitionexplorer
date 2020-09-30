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
            a2_id: "",
            a3_name: "",  
            a3_id: "",
            a4_name: "",  
            a4_id: "",
            a5_name: "",  
            a5_id: "",
            b1_name: "",  
            b1_id: "",
            b4_name: "",  
            b4_id: "",
            b5_name: "",  
            b5_id: "",
            b6_name: "",  
            b6_id: "",
            b7_name: "",  
            b7_id: "",
            b8_name: "",  
            b8_id: "",
            b9_name: "",  
            b9_id: "",
            c2_name: "",  
            c2_id: "",
            d1_name: "",  
            d1_id: "",
            d2_name: "",  
            d2_id: "",
            z1x_name: "",  
            z1x_id: ""
                     
        }
        if (data.ivp_a2.length > 0) {
            visitObj.a2_id = data.ivp_a2[0]['@id']
            visitObj.a2_name = "ivp_a2" 
        }
        if (data.ivp_a5.length > 0) {
            visitObj.a5_id = data.ivp_a5[0]['@id']
            visitObj.a5_name = "ivp_a5" 
        } 
        if (data.ivp_b5.length > 0) {
            visitObj.b5_id = data.ivp_b5[0]['@id']
            visitObj.b5_name = "ivp_b5" 
        } 
        if (data.ivp_b6.length > 0) {
            visitObj.b6_id = data.ivp_b6[0]['@id']
            visitObj.b6_name = "ivp_b6" 
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
                a2_id: "",
                a3_name: "",  
                a3_id: "",
                a4_name: "",  
                a4_id: "",
                a5_name: "",  
                a5_id: "",
                b1_name: "",  
                b1_id: "",
                b4_name: "",  
                b4_id: "",
                b5_name: "",  
                b5_id: "",
                b6_name: "",  
                b6_id: "",
                b7_name: "",  
                b7_id: "",
                b8_name: "",  
                b8_id: "",
                b9_name: "",  
                b9_id: "",
                c2_name: "",  
                c2_id: "",
                d1_name: "",  
                d1_id: "",
                d2_name: "",  
                d2_id: "",
                z1x_name: "",  
                z1x_id: ""          
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
                title: 'Form A',
                display: form => <div>{form.a1_id &&<span><a href={form.a1_id}>{form.a1_name}</a> </span>}
                {form.a2_id &&<span><a href={form.a2_id}>{form.a2_name}</a> </span>}
                {form.a3_id &&<span><a href={form.a3_id}>{form.a3_name}</a> </span>}
                {form.a4_id &&<span><a href={form.a4_id}>{form.a4_name}</a> </span>}
                {form.a5_id &&<span><a href={form.a5_id}>{form.a5_name}</a> </span>}
                </div>,
                
            },


            b1_id: {
                title: 'Form B',
                display: form => <div>{form.b1_id &&<span><a href={form.b1_id}>{form.b1_name}</a> </span>}
                {form.b4_id &&<span><a href={form.b4_id}>{form.a4_name}</a> </span>}
                {form.b5_id &&<span><a href={form.b5_id}>{form.b5_name}</a> </span>}
                {form.b6_id &&<span><a href={form.b6_id}>{form.b6_name}</a> </span>}
                {form.b7_id &&<span><a href={form.b7_id}>{form.b7_name}</a> </span>}
                {form.b8_id &&<span><a href={form.b8_id}>{form.b8_name}</a> </span>}
                {form.b9_id &&<span><a href={form.b9_id}>{form.b9_name}</a> </span>}
                </div>,
            },

            c2_id: {
                title: 'Form C',
                display: form => <a href={form.c2_id}>{form.c2_name}</a>,
            },
            d1_id: {
                title: 'Form D',
                display: form => <div>{form.d1_id &&<span><a href={form.d1_id}>{form.d1_name}</a> </span>}
                {form.d2_id &&<span><a href={form.d2_id}>{form.d2_name}</a> </span>}
                </div>,
            },
            z1x_id: {
                title: 'Form Z1x',
                display: form => <a href={form.z1x_id}>{form.z1x_name}</a>,
            },
            

      
        };
        return (
            <SortTablePanel >
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




