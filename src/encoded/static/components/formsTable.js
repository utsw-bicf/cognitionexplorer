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
            visit_date: data.ivp_a1v3[0]['visdate'],
            a1v3_name: "ivp_a1v3",
            a1v3_id: data.ivp_a1v3[0]['@id'],
            a1v1_name: "",
            a1v1_id: "",
            a1v2_name: "",
            a1v2_id: "",

            a2v1_name: "",
            a2v1_id: "",
            a2v2_name: "",
            a2v2_id: "",
            a2v3_name: "",
            a2v3_id: "",
            a3v1_name: "",
            a3v1_id: "",
            a3v2_name: "",
            a3v2_id: "",
            a3v3_name: "",
            a3v3_id: "",
            a4v1_name: "",
            a4v1_id: "",
            a4v2_name: "",
            a4v2_id: "",
            a4v3_name: "",
            a4v3_id: "",
            a5v1_name: "",
            a5v1_id: "",
            a5v2_name: "",
            a5v2_id: "",
            a5v3_name: "",
            a5v3_id: "",
            b1v1_name: "",
            b1v1_id: "",
            b1v2_name: "",
            b1v2_id: "",
            b1v3_name: "",
            b1v3_id: "",
            b2v1_name: "",
            b2v1_id: "",
            b2v2_name: "",
            b2v2_id: "",
            b3v1_name: "",
            b3v1_id: "",
            b3v2_name: "",
            b3v2_id: "",
            b4v1_name: "",
            b4v1_id: "",
            b4v2_name: "",
            b4v2_id: "",
            b4v3_name: "",
            b4v3_id: "",
            b5v1_name: "",
            b5v1_id: "",
            b5v2_name: "",
            b5v2_id: "",
            b5v3_name: "",
            b5v3_id: "",
            b6v1_name: "",
            b6v1_id: "",
            b6v2_name: "",
            b6v2_id: "",
            b6v3_name: "",
            b6v3_id: "",
            b7v1_name: "",
            b7v1_id: "",
            b7v2_name: "",
            b7v2_id: "",
            b7v3_name: "",
            b7v3_id: "",
            b8v1_name: "",
            b8v1_id: "",
            b8v2_name: "",
            b8v2_id: "",
            b8v3_name: "",
            b8v3_id: "",
            b9v1_name: "",
            b9v1_id: "",
            b9v2_name: "",
            b9v2_id: "",
            b9v3_name: "",
            b9v3_id: "",
            c1v1_name: "",
            c1v1_id: "",
            c1v2_name: "",
            c1v2_id: "",
            c2v2_name: "",
            c2v2_id: "",
            c2v3_name: "",
            c2v3_id: "",
            d1v1_name: "",
            d1v1_id: "",
            d1v2_name: "",
            d1v2_id: "",
            d1v3_name: "",
            d1v3_id: "",
            d2v2_name: "",
            d2v2_id: "",
            d2v3_name: "",
            d2v3_id: "",
            e1v1_name: "",
            e1v1_id: "",
            e1v2_name: "",
            e1v2_id: "",
            z1v1_name: "",
            z1v1_id: "",
            z1v2_name: "",
            z1v2_id: "",
            z1xv2_name: "",
            z1xv2_id: "",
            z1xv3_name: "",
            z1xv3_id: "",
            m1_name: "",
            m1_id: "",
            local_form_name: "",
            local_form_id: ""

        }
        if (data.ivp_a1v1.length > 0) {
            visitObj.a1v1_id = data.ivp_a1v1[0]['@id']
            visitObj.a1v1_name = "ivp_a1v1"
        }
        if (data.ivp_a1v2.length > 0) {
            visitObj.a1v2_id = data.ivp_a1v2[0]['@id']
            visitObj.a1v2_name = "ivp_a1v2"
        }
        if (data.ivp_a1v3.length > 0) {
            visitObj.a1v3_id = data.ivp_a1v3[0]['@id']
            visitObj.a1v3_name = "ivp_a1v3"
        }
        if (data.ivp_a2v1.length > 0) {
            visitObj.a2v1_id = data.ivp_a2v1[0]['@id']
            visitObj.a2v1_name = "ivp_a2v1"
        }
        if (data.ivp_a2v2.length > 0) {
            visitObj.a2v2_id = data.ivp_a2v2[0]['@id']
            visitObj.a2v2_name = "ivp_a2v2"
        }
        if (data.ivp_a2v3.length > 0) {
            visitObj.a2v3_id = data.ivp_a2v3[0]['@id']
            visitObj.a2v3_name = "ivp_a2v3"
        }
        if (data.ivp_a3v1.length > 0) {
            visitObj.a3v1_id = data.ivp_a3v1[0]['@id']
            visitObj.a3v1_name = "ivp_a3v1"
        }
        if (data.ivp_a3v2.length > 0) {
            visitObj.a3v2_id = data.ivp_a3v2[0]['@id']
            visitObj.a3v2_name = "ivp_a3v2"
        }
        if (data.ivp_a3v3.length > 0) {
            visitObj.a3v3_id = data.ivp_a3v3[0]['@id']
            visitObj.a3v3_name = "ivp_a3v3"
        }
        if (data.ivp_a4v1.length > 0) {
            visitObj.a4v1_id = data.ivp_a4v1[0]['@id']
            visitObj.a4v1_name = "ivp_a4v1"
        }
        if (data.ivp_a4v2.length > 0) {
            visitObj.a4v2_id = data.ivp_a4v2[0]['@id']
            visitObj.a4v2_name = "ivp_a4v2"
        }
        if (data.ivp_a4v3.length > 0) {
            visitObj.a4v3_id = data.ivp_a4v3[0]['@id']
            visitObj.a4v3_name = "ivp_a4v3"
        }
        if (data.ivp_a5v1.length > 0) {
            visitObj.a5v1_id = data.ivp_a5v1[0]['@id']
            visitObj.a5v1_name = "ivp_a5v1"
        }
        if (data.ivp_a5v2.length > 0) {
            visitObj.a5v2_id = data.ivp_a5v2[0]['@id']
            visitObj.a5v2_name = "ivp_a5v2"
        }
        if (data.ivp_a5v3.length > 0) {
            visitObj.a5v3_id = data.ivp_a5v3[0]['@id']
            visitObj.a5v3_name = "ivp_a5v3"
        }
        if (data.ivp_b1v1.length > 0) {
            visitObj.b1v1_id = data.ivp_b1v1[0]['@id']
            visitObj.b1v1_name = "ivp_b1v1"
        }
        if (data.ivp_b1v2.length > 0) {
            visitObj.b1v2_id = data.ivp_b1v2[0]['@id']
            visitObj.b1v2_name = "ivp_b1v2"
        }
        if (data.ivp_b1v3.length > 0) {
            visitObj.b1v3_id = data.ivp_b1v3[0]['@id']
            visitObj.b1v3_name = "ivp_b1v3"
        }
        if (data.ivp_b2v1.length > 0) {
            visitObj.b2v1_id = data.ivp_b2v1[0]['@id']
            visitObj.b2v1_name = "ivp_b2v1"
        }
        if (data.ivp_b2v2.length > 0) {
            visitObj.b2v2_id = data.ivp_b2v2[0]['@id']
            visitObj.b2v2_name = "ivp_b2v2"
        }
        if (data.ivp_b3v1.length > 0) {
            visitObj.b3v1_id = data.ivp_b3v1[0]['@id']
            visitObj.b3v1_name = "ivp_b3v1"
        }
        if (data.ivp_b3v2.length > 0) {
            visitObj.b3v2_id = data.ivp_b3v2[0]['@id']
            visitObj.b3v2_name = "ivp_b3v2"
        }
        if (data.ivp_b4v1.length > 0) {
            visitObj.b4v1_id = data.ivp_b4v1[0]['@id']
            visitObj.b4v1_name = "ivp_b4v1"
        }
        if (data.ivp_b4v2.length > 0) {
            visitObj.b4v2_id = data.ivp_b4v2[0]['@id']
            visitObj.b4v2_name = "ivp_b4v2"
        }
        if (data.ivp_b4v3.length > 0) {
            visitObj.b4v3_id = data.ivp_b4v3[0]['@id']
            visitObj.b4v3_name = "ivp_b4v3"
        }
        if (data.ivp_b5v1.length > 0) {
            visitObj.b5v1_id = data.ivp_b5v1[0]['@id']
            visitObj.b5v1_name = "ivp_b5v1"
        }
        if (data.ivp_b5v2.length > 0) {
            visitObj.b5v2_id = data.ivp_b5v2[0]['@id']
            visitObj.b5v2_name = "ivp_b5v2"
        }
        if (data.ivp_b5v3.length > 0) {
            visitObj.b5v3_id = data.ivp_b5v3[0]['@id']
            visitObj.b5v3_name = "ivp_b5v3"
        }
        if (data.ivp_b6v1.length > 0) {
            visitObj.b6v1_id = data.ivp_b6v1[0]['@id']
            visitObj.b6v1_name = "ivp_b6v1"
        }
        if (data.ivp_b6v2.length > 0) {
            visitObj.b6v2_id = data.ivp_b6v2[0]['@id']
            visitObj.b6v2_name = "ivp_b6v2"
        }
        if (data.ivp_b6v3.length > 0) {
            visitObj.b6v3_id = data.ivp_b6v3[0]['@id']
            visitObj.b6v3_name = "ivp_b6v3"
        }
        if (data.ivp_b7v1.length > 0) {
            visitObj.b7v1_id = data.ivp_b7v1[0]['@id']
            visitObj.b7v1_name = "ivp_b7v1"
        }
        if (data.ivp_b7v2.length > 0) {
            visitObj.b7v2_id = data.ivp_b7v2[0]['@id']
            visitObj.b7v2_name = "ivp_b7v2"
        }
        if (data.ivp_b7v3.length > 0) {
            visitObj.b7v3_id = data.ivp_b7v3[0]['@id']
            visitObj.b7v3_name = "ivp_b7v3"
        }
        if (data.ivp_b8v1.length > 0) {
            visitObj.b8v1_id = data.ivp_b8v1[0]['@id']
            visitObj.b8v1_name = "ivp_b8v1"
        }
        if (data.ivp_b8v2.length > 0) {
            visitObj.b8v2_id = data.ivp_b8v2[0]['@id']
            visitObj.b8v2_name = "ivp_b8v2"
        }
        if (data.ivp_b8v3.length > 0) {
            visitObj.b8v3_id = data.ivp_b8v3[0]['@id']
            visitObj.b8v3_name = "ivp_b8v3"
        }
        if (data.ivp_b9v1.length > 0) {
            visitObj.b9v1_id = data.ivp_b9v1[0]['@id']
            visitObj.b9v1_name = "ivp_b9v1"
        }
        if (data.ivp_b9v2.length > 0) {
            visitObj.b9v2_id = data.ivp_b9v2[0]['@id']
            visitObj.b9v2_name = "ivp_b9v2"
        }
        if (data.ivp_b9v3.length > 0) {
            visitObj.b9v3_id = data.ivp_b9v3[0]['@id']
            visitObj.b9v3_name = "ivp_b9v3"
        }
        if (data.ivp_c1v1.length > 0) {
            visitObj.c1v1_id = data.ivp_c1v1[0]['@id']
            visitObj.c1v1_name = "ivp_c1v1"
        }
        if (data.ivp_c1v2.length > 0) {
            visitObj.c1v2_id = data.ivp_c1v2[0]['@id']
            visitObj.c1v2_name = "ivp_c1v2"
        }
        if (data.ivp_c2v2.length > 0) {
            visitObj.c2v2_id = data.ivp_c2v2[0]['@id']
            visitObj.c2v2_name = "ivp_c2v2"
        }
        if (data.ivp_c2v3.length > 0) {
            visitObj.c2v3_id = data.ivp_c2v3[0]['@id']
            visitObj.c2v3_name = "ivp_c2v3"
        }
        if (data.ivp_d1v1.length > 0) {
            visitObj.d1v1_id = data.ivp_d1v1[0]['@id']
            visitObj.d1v1_name = "ivp_d1v1"
        }
        if (data.ivp_d1v2.length > 0) {
            visitObj.d1v2_id = data.ivp_d1v2[0]['@id']
            visitObj.d1v2_name = "ivp_d1v2"
        }
        if (data.ivp_d1v3.length > 0) {
            visitObj.d1v3_id = data.ivp_d1v3[0]['@id']
            visitObj.d1v3_name = "ivp_d1v3"
        }
        if (data.ivp_d2v2.length > 0) {
            visitObj.d2v2_id = data.ivp_d2v2[0]['@id']
            visitObj.d2v2_name = "ivp_d2v2"
        }
        if (data.ivp_d2v3.length > 0) {
            visitObj.d2v3_id = data.ivp_d2v3[0]['@id']
            visitObj.d2v3_name = "ivp_d2v3"
        }
        if (data.ivp_e1v1.length > 0) {
            visitObj.e1v1_id = data.ivp_e1v1[0]['@id']
            visitObj.e1v1_name = "ivp_e1v1"
        }
        if (data.ivp_e1v2.length > 0) {
            visitObj.e1v2_id = data.ivp_e1v2[0]['@id']
            visitObj.e1v2_name = "ivp_e1v2"
        }
        if (data.ivp_z1v1.length > 0) {
            visitObj.z1v1_id = data.ivp_z1v1[0]['@id']
            visitObj.z1v1_name = "ivp_z1v1"
        }
        if (data.ivp_z1v2.length > 0) {
            visitObj.z1v2_id = data.ivp_z1v2[0]['@id']
            visitObj.z1v2_name = "ivp_z1v2"
        }
        if (data.ivp_z1xv2.length > 0) {
            visitObj.z1xv2_id = data.ivp_z1xv2[0]['@id']
            visitObj.z1xv2_name = "ivp_z1xv2"
        }
        if (data.ivp_z1xv3.length > 0) {
            visitObj.z1xv3_id = data.ivp_z1xv3[0]['@id']
            visitObj.z1xv3_name = "ivp_z1xv3"
        }
        if (data.concussion_history.length > 0) {
            visitObj.local_form_id = data.concussion_history[0]['@id']
            visitObj.local_form_name = "concussion_history"
        }
        forms[0] = visitObj
        let followUpVisitTimes = this.getFollowUpVisitTimes(data)

        console.log(followUpVisitTimes)
        for (let i = 0; i < followUpVisitTimes.length; i++) {
            let visitObj = {
                visit_number: i + 2,
                visit_name: "Follow Up Visit " + (i + 1),
                visit_date: followUpVisitTimes[i],
                a1v1_name: "",
                a1v1_id: "",
                a1v2_name: "",
                a1v2_id: "",
                a1v3_name: "",
                a1v3_id: "",
                a2v1_name: "",
                a2v1_id: "",
                a2v2_name: "",
                a2v2_id: "",
                a2v3_name: "",
                a2v3_id: "",
                a3v1_name: "",
                a3v1_id: "",
                a3v2_name: "",
                a3v2_id: "",
                a3v3_name: "",
                a3v3_id: "",
                a4v1_name: "",
                a4v1_id: "",
                a4v2_name: "",
                a4v2_id: "",
                a4v3_name: "",
                a4v3_id: "",
                a5v1_name: "",
                a5v1_id: "",
                a5v2_name: "",
                a5v2_id: "",
                b1v1_name: "",
                b1v1_id: "",
                b1v2_name: "",
                b1v2_id: "",
                b1v3_name: "",
                b1v3_id: "",
                b2v1_name: "",
                b2v1_id: "",
                b2v2_name: "",
                b2v2_id: "",
                b3v1_name: "",
                b3v1_id: "",
                b3v2_name: "",
                b3v2_id: "",
                b4v1_name: "",
                b4v1_id: "",
                b4v2_name: "",
                b4v2_id: "",
                b4v3_name: "",
                b4v3_id: "",
                b5v1_name: "",
                b5v1_id: "",
                b5v2_name: "",
                b5v2_id: "",
                b5v3_name: "",
                b5v3_id: "",
                b6v1_name: "",
                b6v1_id: "",
                b6v2_name: "",
                b6v2_id: "",
                b6v3_name: "",
                b6v3_id: "",
                b7v1_name: "",
                b7v1_id: "",
                b7v2_name: "",
                b7v2_id: "",
                b7v3_name: "",
                b7v3_id: "",
                b8v1_name: "",
                b8v1_id: "",
                b8v2_name: "",
                b8v2_id: "",
                b8v3_name: "",
                b8v3_id: "",
                b9v1_name: "",
                b9v1_id: "",
                b9v2_name: "",
                b9v2_id: "",
                b9v3_name: "",
                b9v3_id: "",
                c1v1_name: "",
                c1v1_id: "",
                c1v2_name: "",
                c1v2_id: "",
                c1v3_name: "",
                c1v3_id: "",
                c2v3_name: "",
                c2v3_id: "",
                d1v1_name: "",
                d1v1_id: "",
                d1v2_name: "",
                d1v2_id: "",
                d1v3_name: "",
                d1v3_id: "",
                d2v3_name: "",
                d2v3_id: "",
                e1v1_name: "",
                e1v1_id: "",
                e1v2_name: "",
                e1v2_id: "",
                z1v1_name: "",
                z1v1_id: "",
                z1v2_name: "",
                z1v2_id: "",
                z1xv3_name: "",
                z1xv3_id: "",
                m1_name: "",
                m1_id: ""

            }
            forms.push(visitObj)
        }
        console.log(forms)
        for (let i = 0; i < data.fvp_a1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a1v1_id = data.fvp_a1v1[i]['@id']
            forms[index].a1v1_name = "fvp_a1v1"

        }
        for (let i = 0; i < data.fvp_a1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a1v2_id = data.fvp_a1v2[i]['@id']
            forms[index].a1v2_name = "fvp_a1v2"

        }
        for (let i = 0; i < data.fvp_a1v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a1v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a1v3_id = data.fvp_a1v3[i]['@id']
            forms[index].a1v3_name = "fvp_a1v3"

        }
        for (let i = 0; i < data.fvp_a2v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a2v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a2v1_id = data.fvp_a2v1[i]['@id']
            forms[index].a2v1_name = "fvp_a2v1"

        }
        for (let i = 0; i < data.fvp_a2v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a2v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a2v2_id = data.fvp_a2v2[i]['@id']
            forms[index].a2v2_name = "fvp_a2v2"

        }
        for (let i = 0; i < data.fvp_a2v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a2v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a2v3_id = data.fvp_a2v3[i]['@id']
            forms[index].a2v3_name = "fvp_a2v3"

        }
        for (let i = 0; i < data.fvp_a3v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a3v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a3v1_id = data.fvp_a3v1[i]['@id']
            forms[index].a3v1_name = "fvp_a3v1"

        }
        for (let i = 0; i < data.fvp_a3v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a3v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a3v2_id = data.fvp_a3v2[i]['@id']
            forms[index].a3v2_name = "fvp_a3v2"

        }
        for (let i = 0; i < data.fvp_a3v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a3v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a3v3_id = data.fvp_a3v3[i]['@id']
            forms[index].a3v3_name = "fvp_a3v3"

        }
        for (let i = 0; i < data.fvp_a4v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a4v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a4v1_id = data.fvp_a4v1[i]['@id']
            forms[index].a4v1_name = "fvp_a4v1"

        }
        for (let i = 0; i < data.fvp_a4v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a4v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a4v2_id = data.fvp_a4v2[i]['@id']
            forms[index].a4v2_name = "fvp_a4v2"

        }
        for (let i = 0; i < data.fvp_a4v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a4v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a4v3_id = data.fvp_a4v3[i]['@id']
            forms[index].a4v3_name = "fvp_a4v3"

        }
        for (let i = 0; i < data.fvp_a5v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a5v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a5v1_id = data.fvp_a5v1[i]['@id']
            forms[index].a5v1_name = "fvp_a5v1"

        }
        for (let i = 0; i < data.fvp_a5v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_a5v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].a5v2_id = data.fvp_a5v2[i]['@id']
            forms[index].a5v2_name = "fvp_a5v2"

        }
        for (let i = 0; i < data.fvp_b1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b1v1_id = data.fvp_b1v1[i]['@id']
            forms[index].b1v1_name = "fvp_b1v1"

        }
        for (let i = 0; i < data.fvp_b1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b1v2_id = data.fvp_b1v2[i]['@id']
            forms[index].b1v2_name = "fvp_b1v2"

        }
        for (let i = 0; i < data.fvp_b1v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b1v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b1v3_id = data.fvp_b1v3[i]['@id']
            forms[index].b1v3_name = "fvp_b1v3"

        }
        for (let i = 0; i < data.fvp_b2v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b2v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b2v1_id = data.fvp_b2v1[i]['@id']
            forms[index].b2v1_name = "fvp_b2v1"

        }
        for (let i = 0; i < data.fvp_b2v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b2v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b2v2_id = data.fvp_b2v2[i]['@id']
            forms[index].b2v2_name = "fvp_b2v2"

        }
        for (let i = 0; i < data.fvp_b3v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b3v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b3v1_id = data.fvp_b3v1[i]['@id']
            forms[index].b3v1_name = "fvp_b3v1"

        }
        for (let i = 0; i < data.fvp_b3v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b3v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b3v2_id = data.fvp_b3v2[i]['@id']
            forms[index].b3v2_name = "fvp_b3v2"

        }
        for (let i = 0; i < data.fvp_b4v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b4v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b4v1_id = data.fvp_b4v1[i]['@id']
            forms[index].b4v1_name = "fvp_b4v1"

        }
        for (let i = 0; i < data.fvp_b4v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b4v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b4v2_id = data.fvp_b4v2[i]['@id']
            forms[index].b4v2_name = "fvp_b4v2"

        }
        for (let i = 0; i < data.fvp_b4v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b4v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b4v3_id = data.fvp_b4v3[i]['@id']
            forms[index].b4v3_name = "fvp_b4v3"

        }
        for (let i = 0; i < data.fvp_b5v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b5v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b5v1_id = data.fvp_b5v1[i]['@id']
            forms[index].b5v1_name = "fvp_b5v1"

        }
        for (let i = 0; i < data.fvp_b5v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b5v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b5v2_id = data.fvp_b5v2[i]['@id']
            forms[index].b5v2_name = "fvp_b5v2"

        }
        for (let i = 0; i < data.fvp_b5v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b5v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b5v3_id = data.fvp_b5v3[i]['@id']
            forms[index].b5v3_name = "fvp_b5v3"

        }
        for (let i = 0; i < data.fvp_b6v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b6v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b6v1_id = data.fvp_b6v1[i]['@id']
            forms[index].b6v1_name = "fvp_b6v1"

        }
        for (let i = 0; i < data.fvp_b6v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b6v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b6v2_id = data.fvp_b6v2[i]['@id']
            forms[index].b6v2_name = "fvp_b6v2"

        }
        for (let i = 0; i < data.fvp_b6v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b6v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b6v3_id = data.fvp_b6v3[i]['@id']
            forms[index].b6v3_name = "fvp_b6v3"

        }
        for (let i = 0; i < data.fvp_b7v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b7v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b7v1_id = data.fvp_b7v1[i]['@id']
            forms[index].b7v1_name = "fvp_b7v1"

        }
        for (let i = 0; i < data.fvp_b7v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b7v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b7v2_id = data.fvp_b7v2[i]['@id']
            forms[index].b7v2_name = "fvp_b7v2"

        }
        for (let i = 0; i < data.fvp_b7v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b7v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b7v3_id = data.fvp_b7v3[i]['@id']
            forms[index].b7v3_name = "fvp_b7v3"

        }
        for (let i = 0; i < data.fvp_b8v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b8v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b8v1_id = data.fvp_b8v1[i]['@id']
            forms[index].b8v1_name = "fvp_b8v1"

        }
        for (let i = 0; i < data.fvp_b8v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b8v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b8v2_id = data.fvp_b8v2[i]['@id']
            forms[index].b8v2_name = "fvp_b8v2"

        }
        for (let i = 0; i < data.fvp_b8v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b8v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b8v3_id = data.fvp_b8v3[i]['@id']
            forms[index].b8v3_name = "fvp_b8v3"

        }
        for (let i = 0; i < data.fvp_b9v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b9v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b9v1_id = data.fvp_b9v1[i]['@id']
            forms[index].b9v1_name = "fvp_b9v1"

        }
        for (let i = 0; i < data.fvp_b9v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b9v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b9v2_id = data.fvp_b9v2[i]['@id']
            forms[index].b9v2_name = "fvp_b9v2"

        }
        for (let i = 0; i < data.fvp_b9v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_b9v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].b9v3_id = data.fvp_b9v3[i]['@id']
            forms[index].b9v3_name = "fvp_b9v3"

        }
        for (let i = 0; i < data.fvp_c1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].c1v1_id = data.fvp_c1v1[i]['@id']
            forms[index].c1v1_name = "fvp_c1v1"

        }
        for (let i = 0; i < data.fvp_c1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].c1v2_id = data.fvp_c1v2[i]['@id']
            forms[index].c1v2_name = "fvp_c1v2"

        }
        for (let i = 0; i < data.fvp_c1v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c1v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].c1v3_id = data.fvp_c1v3[i]['@id']
            forms[index].c1v3_name = "fvp_c1v3"

        }
        for (let i = 0; i < data.fvp_c2v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_c2v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].c2v3_id = data.fvp_c2v3[i]['@id']
            forms[index].c2v3_name = "fvp_c2v3"

        }
        for (let i = 0; i < data.fvp_d1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].d1v1_id = data.fvp_d1v1[i]['@id']
            forms[index].d1v1_name = "fvp_d1v1"

        }
        for (let i = 0; i < data.fvp_d1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].d1v2_id = data.fvp_d1v2[i]['@id']
            forms[index].d1v2_name = "fvp_d1v2"

        }
        for (let i = 0; i < data.fvp_d1v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d1v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].d1v3_id = data.fvp_d1v3[i]['@id']
            forms[index].d1v3_name = "fvp_d1v3"

        }
        for (let i = 0; i < data.fvp_d2v3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_d2v3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].d2v3_id = data.fvp_d2v3[i]['@id']
            forms[index].d2v3_name = "fvp_d2v3"

        }
        for (let i = 0; i < data.fvp_e1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_e1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].e1v1_id = data.fvp_e1v1[i]['@id']
            forms[index].e1v1_name = "fvp_e1v1"

        }
        for (let i = 0; i < data.fvp_e1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_e1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].e1v2_id = data.fvp_e1v2[i]['@id']
            forms[index].e1v2_name = "fvp_e1v2"

        }
        for (let i = 0; i < data.fvp_z1v1.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_z1v1[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].z1v1_id = data.fvp_z1v1[i]['@id']
            forms[index].z1v1_name = "fvp_z1v1"

        }
        for (let i = 0; i < data.fvp_z1v2.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_z1v2[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].z1v2_id = data.fvp_z1v2[i]['@id']
            forms[index].z1v2_name = "fvp_z1v2"

        }
        for (let i = 0; i < data.fvp_z1xv3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_z1xv3[i]["visdate"]) + 1;
            //console.log(index)
            forms[index].z1xv3_id = data.fvp_z1xv3[i]['@id']
            forms[index].z1xv3_name = "fvp_z1xv3"

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
        for (let i = 0; i < data.fvp_z1xv3.length; i++) {
            let index = followUpVisitTimes.indexOf(data.fvp_z1xv3[i]["visdate"]) + 1;
            // console.log(index)
            forms[index].z1x_id = data.fvp_z1xv3[i]['@id']
            forms[index].z1x_name = "fvp_z1xv3"
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
        // for (let i = 0; i < data.tvp_b7v3.length; i++) {
        //     let index = followUpVisitTimes.indexOf(data.tvp_b7v3[i]["visdate"]) + 1;
        //     // console.log(index)
        //     forms[index].b7v3_id = data.tvp_b7v3[i]['@id']
        //     forms[index].b7v3_name = "tvp_b7v3"
        // }
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

        data.fvp_a1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a1v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a2v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a2v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a2v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a3v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a3v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a3v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a4v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a4v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a4v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a5v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_a5v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b1v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b2v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b2v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b3v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b3v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b4v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b4v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b4v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b5v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b5v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b5v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b6v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b6v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b6v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b7v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b7v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b7v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b8v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b8v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b8v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b9v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b9v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_b9v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c1v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_c2v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d1v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_d2v3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_e1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_e1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_z1v1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_z1v2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.fvp_z1xv3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_a3.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_b5.forEach(element => followUpVisitTimes.push(element["visdate"]))

        data.tvp_a1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_z1x.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_d2.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_t1.forEach(element => followUpVisitTimes.push(element["visdate"]))
        data.tvp_b4.forEach(element => followUpVisitTimes.push(element["visdate"]))
        // data.tvp_b7v3.forEach(element => followUpVisitTimes.push(element["visdate"]))

        data.tvp_a4.forEach(element => followUpVisitTimes.push(element["visdate"]))
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
                display: form => <div>
                    {form.a1v1_id && <span><a href={form.a1v1_id}>{form.a1v1_name}</a> </span>}
                    {form.a1v2_id && <span><a href={form.a1v2_id}>{form.a1v2_name}</a> </span>}
                    {form.a1v3_id && <span><a href={form.a1v3_id}>{form.a1v3_name}</a> </span>}
                    {form.a2v1_id && <span><a href={form.a2v1_id}>{form.a2v1_name}</a> </span>}
                    {form.a2v2_id && <span><a href={form.a2v2_id}>{form.a2v2_name}</a> </span>}
                    {form.a2v3_id && <span><a href={form.a2v3_id}>{form.a2v3_name}</a> </span>}
                    {form.a3v1_id && <span><a href={form.a3v1_id}>{form.a3v1_name}</a> </span>}
                    {form.a3v2_id && <span><a href={form.a3v2_id}>{form.a3v2_name}</a> </span>}
                    {form.a3v3_id && <span><a href={form.a3v3_id}>{form.a3v3_name}</a> </span>}
                    {form.a4v1_id && <span><a href={form.a4v1_id}>{form.a4v1_name}</a> </span>}
                    {form.a4v2_id && <span><a href={form.a4v2_id}>{form.a4v2_name}</a> </span>}
                    {form.a4v3_id && <span><a href={form.a4v3_id}>{form.a4v3_name}</a> </span>}
                    {form.a5v1_id && <span><a href={form.a5v1_id}>{form.a5v1_name}</a> </span>}
                    {form.a5v2_id && <span><a href={form.a5v2_id}>{form.a5v2_name}</a> </span>}
                </div>,

            },


            b1_id: {
                title: 'Form B',
                display: form => <div>{form.b1v3_id && <span><a href={form.b1v3_id}>{form.b1v3_name}</a> </span>}
                    {form.b1v1_id && <span><a href={form.b1v1_id}>{form.b1v1_name}</a> </span>}
                    {form.b1v2_id && <span><a href={form.b1v2_id}>{form.b1v2_name}</a> </span>}
                    {form.b1v3_id && <span><a href={form.b1v3_id}>{form.b1v3_name}</a> </span>}
                    {form.b2v1_id && <span><a href={form.b2v1_id}>{form.b2v1_name}</a> </span>}
                    {form.b2v2_id && <span><a href={form.b2v2_id}>{form.b2v2_name}</a> </span>}
                    {form.b3v1_id && <span><a href={form.b3v1_id}>{form.b3v1_name}</a> </span>}
                    {form.b3v2_id && <span><a href={form.b3v2_id}>{form.b3v2_name}</a> </span>}
                    {form.b4v1_id && <span><a href={form.b4v1_id}>{form.b4v1_name}</a> </span>}
                    {form.b4v2_id && <span><a href={form.b4v2_id}>{form.b4v2_name}</a> </span>}
                    {form.b4v3_id && <span><a href={form.b4v3_id}>{form.b4v3_name}</a> </span>}
                    {form.b5v1_id && <span><a href={form.b5v1_id}>{form.b5v1_name}</a> </span>}
                    {form.b5v2_id && <span><a href={form.b5v2_id}>{form.b5v2_name}</a> </span>}
                    {form.b5v3_id && <span><a href={form.b5v3_id}>{form.b5v3_name}</a> </span>}
                    {form.b6v1_id && <span><a href={form.b6v1_id}>{form.b6v1_name}</a> </span>}
                    {form.b6v2_id && <span><a href={form.b6v2_id}>{form.b6v2_name}</a> </span>}
                    {form.b6v3_id && <span><a href={form.b6v3_id}>{form.b6v3_name}</a> </span>}
                    {form.b7v1_id && <span><a href={form.b7v1_id}>{form.b7v1_name}</a> </span>}
                    {form.b7v2_id && <span><a href={form.b7v2_id}>{form.b7v2_name}</a> </span>}
                    {form.b7v3_id && <span><a href={form.b7v3_id}>{form.b7v3_name}</a> </span>}
                    {form.b8v1_id && <span><a href={form.b8v1_id}>{form.b8v1_name}</a> </span>}
                    {form.b8v2_id && <span><a href={form.b8v2_id}>{form.b8v2_name}</a> </span>}
                    {form.b8v3_id && <span><a href={form.b8v3_id}>{form.b8v3_name}</a> </span>}
                    {form.b9v1_id && <span><a href={form.b9v1_id}>{form.b9v1_name}</a> </span>}
                    {form.b9v2_id && <span><a href={form.b9v2_id}>{form.b9v2_name}</a> </span>}
                    {form.b9v3_id && <span><a href={form.b9v3_id}>{form.b9v3_name}</a> </span>}
                </div>,
            },

            c2_id: {
                title: 'Form C',
                display: form => <div>
                    {form.c1v1_id && <span><a href={form.c1v1_id}>{form.c1v1_name}</a> </span>}
                    {form.c1v2_id && <span><a href={form.c1v2_id}>{form.c1v2_name}</a> </span>}
                    {form.c1v3_id && <span><a href={form.c1v3_id}>{form.c1v3_name}</a> </span>}
                    {form.c2v3_id && <span><a href={form.c2v3_id}>{form.c2v3_name}</a> </span>}
                </div>

            },
            d1_id: {
                title: 'Form D',
                display: form => <div>{form.d1v1_id && <span><a href={form.d1v1_id}>{form.d1v1_name}</a> </span>}
                    {form.d1v2_id && <span><a href={form.d1v2_id}>{form.d1v2_name}</a> </span>}
                    {form.d1v3_id && <span><a href={form.d1v3_id}>{form.d1v3_name}</a> </span>}
                    {form.d2v3_id && <span><a href={form.d2v3_id}>{form.d2v3_name}</a> </span>}
                </div>,
            },
            e1_id: {
                title: 'Form E',
                display: form => <div>
                    {form.e1v1_id && <span><a href={form.e1v1_id}>{form.e1v1_name}</a> </span>}
                    {form.e1v2_id && <span><a href={form.e1v2_id}>{form.e1v2_name}</a> </span>}
                </div>
            },

            z1x_id: {
                title: 'Form Z1x',
                display: form => <div>
                    {form.z1v1_id && <span><a href={form.z1v1_id}>{form.z1v1_name}</a> </span>}
                    {form.z1v2_id && <span><a href={form.z1v2_id}>{form.z1v2_name}</a> </span>}
                    {form.z1xv3_id && <span><a href={form.z1xv3_id}>{form.z1xv3_name}</a> </span>}
                </div>
            },
            t1_id: {
                title: 'Form T1',
                display: form => <a href={form.t1_id}>{form.t1_name}</a>,
            },
            m1_id: {
                title: 'Form M1',
                display: form => <a href={form.m1_id}>{form.m1_name}</a>,
            },

            local_form_id: {
                title: 'Local Forms',
                display: form => <a href={form.local_form_id}>{form.local_form_name}</a>,
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




