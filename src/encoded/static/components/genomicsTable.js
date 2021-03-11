/* eslint-disable linebreak-style */
// eslint-disable-next-line linebreak-style
import React from 'react';
import { SortTablePanel, SortTable } from './sorttable';

class GenomicsTable extends React.Component {
    constructor(props) {
        super(props);
        this.library = this.transformData(this.props.data);
    }

    transformData(data) {
        let files = [];
        for (let i = 0; i < data.length; i++) {     
            files[i] = {
                award: data[i].award,
                biodataset: data[i].biodataset,
                assay_term_name: data[i].assay_term_name,
                library_type: data[i].library_type,
                file_accession: data[i].accession,
                file_id: data[i]['@id'],
                file_format: data[i].file_format,
                file_run_type: data[i].run_type,
                submitted_file_name: data[i].submitted_file_name,
                
            }    
        }
        return files;
    }

    renderData() {
       
            const tableColumns = {
                award: {
                    title: 'Project',
                    
                },
                biodataset: {
                    title: 'Dataset',
                },
                assay_term_name: {
                    title: 'Assay',
                },
                library_type: {
                    title: 'Library type',
                },
                file_accession: {
                    title: 'File',
                    display: files => <a href={files.file_id}>{files.file_accession}</a>,
                },
                file_format: {
                    title: 'File format',
                },
                file_run_type: {
                    title: 'File run type',
                },
                submitted_file_name: {
                    title: 'File name',
                },
          
            };
            return (
                <SortTablePanel title={this.props.tableTitle}>
                    <SortTable list={this.library} columns={tableColumns} />
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

export default GenomicsTable;

