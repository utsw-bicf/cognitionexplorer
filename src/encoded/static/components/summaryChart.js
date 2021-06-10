import React from 'react';

class SummaryChart extends React.Component {

    constructor(props) {
        super(props);
    
        this.data = this.props.data;
        this.plotlyConfig = {
          displayModeBar: true,
          displaylogo: false,
          modeBarButtonsToRemove: [
                  "sendDataToCloud",
                  "editInChartStudio",
                  "select2d",
                  "lasso2d",
                  "hoverClosestCartesian",
                  "hoverCompareCartesian",
                  "toggleSpikelines",
                  "autoScale2d"
          ],
          responsive: true
        };
    }

    render() {
        return (
            <div id={this.props.chartId}  ></div>

        )
    
    }

    drawChart() {
          
        let layout = {
            title: {
                text:this.props.title,
                font: {
                  size: 16
                },
                xref: 'paper',
                x: 0.05,
            },
            xaxis: {
              showticklabels: false
            },
            height: 500,
            width: 500,
            margin: {
                l: 80,
                r: 20,
                b: 60,
                t: 80
              }
        };
        
        this.plotly.newPlot(this.props.chartId, this.props.data, layout, this.plotlyConfig);
        

    }



    componentDidMount() {
      if(typeof window.Plotly !== "undefined"){
        this.plotly = window.Plotly;

        this.drawChart();
      }
      else{
        window.location.reload();
      }
    }


  
}

export default SummaryChart;



