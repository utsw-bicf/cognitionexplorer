import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class FormsTable extends React.Component {
    constructor(props) {
        super(props);
        this.forms = this.transformData(this.props.data);
    }

    transformData(data) {

        let forms = []
        console.log("data", data);
        let visitObj = {
            visit_number: 1,
            visit_name: "Initial Visit",
            visit_date: data.ivp_a1[0]['visdate'],
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
            t1_name: "",
            t1_id: "",
            d2_name: "",
            d2_id: "",
            z1x_name: "",
            z1x_id: "",
            m1_name: "",
            m1_id: ""

        }
        if (data.ivp_a2.length > 0) {
            visitObj.a2_id = data.ivp_a2[0]['@id']
            visitObj.a2_name = "ivp_a2"
        }
        if (data.ivp_a3.length > 0) {
            visitObj.a3_id = data.ivp_a3[0]['@id']
            visitObj.a3_name = "ivp_a3"
        }
        if (data.ivp_a5.length > 0) {
            visitObj.a5_id = data.ivp_a5[0]['@id']
            visitObj.a5_name = "ivp_a5"
        }
        if (data.ivp_b4.length > 0) {
            visitObj.b4_id = data.ivp_b4[0]['@id']
            visitObj.b4_name = "ivp_b4"
        }
        if (data.ivp_b5.length > 0) {
            visitObj.b5_id = data.ivp_b5[0]['@id']
            visitObj.b5_name = "ivp_b5"
        }
        if (data.ivp_b6.length > 0) {
            visitObj.b6_id = data.ivp_b6[0]['@id']
            visitObj.b6_name = "ivp_b6"
        }
        if (data.ivp_b7.length > 0) {
            visitObj.b7_id = data.ivp_b7[0]['@id']
            visitObj.b7_name = "ivp_b7"
        }
        if (data.ivp_b8.length > 0) {
            visitObj.b8_id = data.ivp_b8[0]['@id']
            visitObj.b8_name = "ivp_b8"
        }
        if (data.ivp_b9.length > 0) {
            visitObj.b9_id = data.ivp_b9[0]['@id']
            visitObj.b9_name = "ivp_b9"
        }
        if (data.ivp_c2.length > 0) {
            visitObj.c2_id = data.ivp_c2[0]['@id']
            visitObj.c2_name = "ivp_c2"

        }

        if (data.ivp_d1.length > 0) {
            visitObj.d1_id = data.ivp_d1[0]['@id']
            visitObj.d1_name = "ivp_d1"
        }
        if (data.ivp_d2.length > 0) {
            visitObj.d2_id = data.ivp_d2[0]['@id']
            visitObj.d2_name = "ivp_d2"
        }
        if (data.m1.length > 0) {
            visitObj.m1_id = data.m1[0]['@id']
            visitObj.m1_name = "m1"
        }
        if (data.ivp_a4.length > 0) {
            visitObj.a4_id = data.ivp_a4[0]['@id']
            visitObj.a4_name = "ivp_a4"
        }
        if (data.ivp_z1x.length > 0) {
            visitObj.z1x_id = data.ivp_z1x[0]['@id']
            visitObj.z1x_name = "ivp_z1x"
        }
        forms[0] = visitObj
        let followUpVisitTimes = this.getFollowUpVisitTimes(data)

        console.log(followUpVisitTimes)
        for (let i = 0; i < followUpVisitTimes.length; i++) {
            let visitObj = {
                visit_number: i + 2,
                visit_name: "Follow Up Visit " + (i + 1),
                visit_date: followUpVisitTimes[i],
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
                c1_name: "",
                c1_id: "",
                c2_name: "",
                c2_id: "",
                d1_name: "",
                d1_id: "",
                d2_name: "",
                d2_id: "",
                t1_name: "",
                t1_id: "",
                z1x_name: "",
                z1x_id: "",
                m1_name: "",
                m1_id: ""
            }
            forms.push(visitObj)
        }
        console.log(forms)
        for (let i = 0; i < data.fvp_a1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a1_id = data.fvp_a1[i]['@id']
            forms[index].a1_name = "fvp_a1"

        }
        for (let i = 0; i < data.fvp_a2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a2[i]["visdate"]) + 1;
            console.log(index)
            forms[index].a2_id = data.fvp_a2[i]['@id']
            forms[index].a2_name = "fvp_a2"

        }
        for (let i = 0; i < data.fvp_c2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c2[i]["visdate"]) + 1;
            console.log(index)
            forms[index].c2_id = data.fvp_c2[i]['@id']
            forms[index].c2_name = "fvp_c2"
        }

        for (let i = 0; i < data.fvp_b6.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b6[i]["visdate"]) + 1;
            forms[index].b6_id = data.fvp_b6[i]['@id']
            forms[index].b6_name = "fvp_b6"
        }

        for (let i = 0; i < data.fvp_b4.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b4[i]["visdate"]) + 1;
            forms[index].b4_id = data.fvp_b4[i]['@id']
            forms[index].b4_name = "fvp_b4"
        }
        for (let i = 0; i < data.fvp_c1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c1[i]["visdate"]) + 1;
            console.log(index)
            forms[index].c1_id = data.fvp_c1[i]['@id']
            forms[index].c1_name = "fvp_c1"
        }
        for (let i = 0; i < data.fvp_b9.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b9[i]["visdate"]) + 1;
            console.log(index)
            forms[index].b9_id = data.fvp_b9[i]['@id']
            forms[index].b9_name = "fvp_b9"
        }
        for (let i = 0; i < data.fvp_b7.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b7[i]["visdate"]) + 1;
            forms[index].b7_id = data.fvp_b7[i]['@id']
            forms[index].b7_name = "fvp_b7"
        }
        for (let i = 0; i < data.fvp_b5.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b5[i]["visdate"]) + 1;
            forms[index].b5_id = data.fvp_b5[i]['@id']
            forms[index].b5_name = "fvp_b5"
        }
        for (let i = 0; i < data.fvp_b1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b1[i]["visdate"]) + 1;
            // console.log(index)
            // console.log("data",data);
            forms[index].b1_id = data.fvp_b1[i]['@id']
            forms[index].b1_name = "fvp_b1"
        }
        for (let i = 0; i < data.fvp_d2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d2[i]["visdate"]) + 1;
            forms[index].d2_id = data.fvp_d2[i]['@id']
            forms[index].d2_name = "fvp_d2"
        }
        for (let i = 0; i < data.fvp_b8.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b8[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].b8_id = data.fvp_b8[i]['@id']
            forms[index].b8_name = "fvp_b8"
        }
        for (let i = 0; i < data.fvp_d1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d1[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].d1_id = data.fvp_d1[i]['@id']
            forms[index].d1_name = "fvp_d1"
        }
        for (let i = 0; i < data.fvp_a3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a3[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a3_id = data.fvp_a3[i]['@id']
            forms[index].a3_name = "fvp_a3"
        }
        for (let i = 0; i < data.tvp_a1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_a1[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a1_id = data.tvp_a1[i]['@id']
            forms[index].a1_name = "tvp_a1"
        }
        for (let i = 0; i < data.tvp_a3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_a3[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a3_id = data.tvp_a3[i]['@id']
            forms[index].a3_name = "tvp_a3"
        }
        for (let i = 0; i < data.tvp_z1x.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_z1x[i]["visdate"]) + 1;
            forms[index].z1x_id = data.tvp_z1x[i]['@id']
            forms[index].z1x_name = "tvp_z1x"
        }
        for (let i = 0; i < data.fvp_z1x.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_z1x[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].z1x_id = data.fvp_z1x[i]['@id']
            forms[index].z1x_name = "fvp_z1x"
        }
        for (let i = 0; i < data.tvp_d2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_d2[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].d2_id = data.tvp_d2[i]['@id']
            forms[index].d2_name = "tvp_d2"
        }

        for (let i = 0; i < data.tvp_t1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_t1[i]["visdate"]) + 1;
            console.log(index)
            forms[index].t1_id = data.tvp_t1[i]['@id']
            forms[index].t1_name = "tvp_t1"
        }
        for (let i = 0; i < data.tvp_b4.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_b4[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].b4_id = data.tvp_b4[i]['@id']
            forms[index].b4_name = "tvp_b4"
        }
        for (let i = 0; i < data.tvp_b7.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_b7[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].b7_id = data.tvp_b7[i]['@id']
            forms[index].b7_name = "tvp_b7"
        }
        for (let i = 0; i < data.tvp_b5.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_b5[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].b5_id = data.tvp_b5[i]['@id']
            forms[index].b5_name = "tvp_b5"
        }
        for (let i = 0; i < data.tvp_a2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_a2[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a2_id = data.tvp_a2[i]['@id']
            forms[index].a2_name = "tvp_a2"
        }
        for (let i = 0; i < data.fvp_a4.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a4[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a4_id = data.fvp_a4[i]['@id']
            forms[index].a4_name = "fvp_a4"
        }
        for (let i = 0; i < data.tvp_a4.length; i++) {
            let index = followUpVisitTimes.indexOf(data.tvp_a4[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].a4_id = data.tvp_a4[i]['@id']
            forms[index].a4_name = "tvp_a4"
        }
        return forms
    }

    getFollowUpVisitTimes(data) {
        let followUpVisitTimes = [];
        data.fvp_a1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b5.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b4.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_b5.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b6.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b7.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b8.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_z1x.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_z1x.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_d2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_t1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_b4.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_b7.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b9.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a4.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a4.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        followUpVisitTimes = [...new Set(followUpVisitTimes)];
        followUpVisitTimes = Array.from(followUpVisitTimes);
        followUpVisitTimes.sort(function (a, b) {
            a = a.split('-').join('');
            b = b.split('-').join('');
            return a > b ? 1 : a < b ? -1 : 0;
        });
        return followUpVisitTimes


    }

    renderData() {

        const tableColumns = {
            visit_number: {
                title: "No."
            },
            visit_name: {
                title: 'Visit',

            },
            visit_date: {
                title: 'Visit Date',

            },
            a1_id: {
                title: 'Form A',
                display: form => <div>{form.a1_id && <span><a href={form.a1_id}>{form.a1_name}</a> </span>}
                    {form.a2_id && <span><a href={form.a2_id}>{form.a2_name}</a> </span>}
                    {form.a3_id && <span><a href={form.a3_id}>{form.a3_name}</a> </span>}
                    {form.a4_id && <span><a href={form.a4_id}>{form.a4_name}</a> </span>}
                    {form.a5_id && <span><a href={form.a5_id}>{form.a5_name}</a> </span>}
                </div>,

            },


            b1_id: {
                title: 'Form B',
                display: form => <div>{form.b1_id && <span><a href={form.b1_id}>{form.b1_name}</a> </span>}
                    {form.b4_id && <span><a href={form.b4_id}>{form.b4_name}</a> </span>}
                    {form.b5_id && <span><a href={form.b5_id}>{form.b5_name}</a> </span>}
                    {form.b6_id && <span><a href={form.b6_id}>{form.b6_name}</a> </span>}
                    {form.b7_id && <span><a href={form.b7_id}>{form.b7_name}</a> </span>}
                    {form.b8_id && <span><a href={form.b8_id}>{form.b8_name}</a> </span>}
                    {form.b9_id && <span><a href={form.b9_id}>{form.b9_name}</a> </span>}
                </div>,
            },

            c2_id: {
                title: 'Form C',
                display: form => <div>{form.c1_id && <span><a href={form.c1_id}>{form.c1_name}</a> </span>}
                    {form.c2_id && <span><a href={form.c2_id}>{form.c2_name}</a> </span>}</div>

            },
            d1_id: {
                title: 'Form D',
                display: form => <div>{form.d1_id && <span><a href={form.d1_id}>{form.d1_name}</a> </span>}
                    {form.d2_id && <span><a href={form.d2_id}>{form.d2_name}</a> </span>}
                </div>,
            },
            z1x_id: {
                title: 'Form Z1x',
                display: form => <a href={form.z1x_id}>{form.z1x_name}</a>,
            },
            m1_id: {
                title: 'Form M1',
                display: form => <a href={form.m1_id}>{form.m1_name}</a>,
            },
            t1_id: {
                title: 'Form T1',
                display: form => <a href={form.t1_id}>{form.t1_name}</a>,
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
