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
          <div>
            <div className="flex-container" >
    
              <div className="chart-main" >
                <div id={this.props.chartId}  >
    
                </div>
              </div>
            </div>
          </div>)
    
    }

    drawChart() {
        var data = [{
            values: [19, 26, 55],
            labels: ['Residential', 'Non-Residential', 'Utility'],
            type: 'pie'
          }];
          
          var layout = {
            height: 400,
            width: 500
        };
        
        this.plotly.newPlot(this.props.chartId, data, layout, this.plotlyConfig);
        

    }

    componentDidMount() {
        this.plotly = window.Plotly;

        this.drawChart();
    }
}

export default SummaryChart;

