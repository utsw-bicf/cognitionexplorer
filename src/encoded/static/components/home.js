'use strict';
var React = require('react');
var globals = require('./globals');
var {FetchedData, Param} = require('./fetched');
var cloneWithProps = require('react/lib/cloneWithProps');


// Main page component to render the home page
var Home = module.exports.Home = React.createClass({
    getInitialState: function(){
        return {
            current: "?type=Experiment&status=released"
        };
    },

    callback: function(newUrl){
        this.setState({
            current: newUrl

        });
        console.log("this.state.current: " + this.state.current);
    },

    render: function() {
        return (
            <div>
                <div className="homepage-banner">
                    <div className="home-page-banner-title">
                        ENCYCLOPEDIA of DNA ELEMENTS
                    </div>
                </div>
                <AssayClicking current={this.state.current} callback={this.callback}/>
                <div className="row">
                    <TabPanel tabs={{panel1: 'Human', panel2: 'Mouse', panel3: 'Worm', panel4: 'Fly'}}>
                        <TabPanelPane key="panel1">
                            <div>
                                <div className="col-sm-6">
                                    <div className="title">
                                        Project: Human
                                    </div>
                                    <center> <hr width="80%" position="static"></hr> </center>
                                    <HomepageChartLoader searchBase={this.state.current + '&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens'} 
                                         callback={this.callback}/>
                                </div>
                            </div>
                        </TabPanelPane>
                        <TabPanelPane key="panel2">
                            <div>
                                <div className="col-sm-6">
                                    <div className="title">
                                        Project: Mouse
                                    </div>
                                    <center> <hr width="80%" position="static"></hr> </center>
                                    <HomepageChartLoader searchBase={this.state.current + '&replicates.library.biosample.donor.organism.scientific_name=Mus+musculus'} 
                                         callback={this.callback}/>
                                </div>
                            </div>
                        </TabPanelPane>
                        <TabPanelPane key="panel3">
                            <div>
                                <div className="col-sm-6">
                                    <div className="title">
                                        Project: Worm
                                    </div>
                                    <center> <hr width="80%" position="static"></hr> </center>
                                    <HomepageChartLoader searchBase={this.state.current + '&replicates.library.biosample.donor.organism.scientific_name=Caenorhabditis+elegans'} 
                                         callback={this.callback}/>
                                </div>
                            </div>
                        </TabPanelPane>
                        <TabPanelPane key="panel4">
                            <div>
                                <div className="col-sm-6">
                                    <div className="title">
                                        Project: Fly
                                    </div>
                                    <center> <hr width="80%" position="static"></hr> </center>
                                    <HomepageChartLoader searchBase={this.state.current + '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+melanogaster' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+pseudoobscura' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+simulans' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+mojavensis' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+ananassae' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+virilis' +
                                                                                        '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+yakuba'} 
                                                        callback={this.callback}/>
                                </div>
                            </div>
                        </TabPanelPane>
                    </TabPanel>
                    

                    <div className="col-sm-6">
                        <div className="title">
                            Biosample Type
                        </div>
                        <center> <hr width="80%"></hr> </center>
                        <HomepageChartLoader2 searchBase={this.state.current} callback={this.callback}/>
                    </div>
                
                </div>
                
            </div>
        );
    }

});




// Component to display the D3-based chart
var AssayClicking = React.createClass({
    propTypes: {
        current: React.PropTypes.string,
        callback: React.PropTypes.func
    },

    getInitialState: function(){
        return {
            updatedLink: this.props.current
        };
    },

    sortByAssay: function(category) {
        // var temp = category;
        // var oldSearchBase = this.props.searchBase;
        //var updatedLink = this.props.current + '&assay_slims=' + category;
        var oldLink = this.props.current; // getting original search
        var startingIndex = oldLink.search("&assay_slims="); // getting index of "&assay_slims=" in original search link if it's there
        if (startingIndex != -1) { // if &assay_slims already is in original search link, then remove it so we can add the correct "&assay_slims="
            var endingIndex = startingIndex + 13; // adding the length of "&assay_slims" to make endingIndex the index of the category
            while (endingIndex < oldLink.length-1 && oldLink.substring(endingIndex, endingIndex + 1) != "&") { // either get to end of string or find next parameter starting with "&"
                endingIndex++; // increase endingIndex until the end of the "&assay_slims=" parameter
                console.log("endingIndex: " + endingIndex);
            }
            if(endingIndex != oldLink.length-1){ // if did not reach end of string, "&assay_slims=" is in middle of search
                console.log("from starting to ending: " + oldLink.substr(startingIndex, endingIndex));
                oldLink = oldLink.substr(0, startingIndex) + oldLink.substr(endingIndex +1); // assay_slims part is from (startingIndex, endingIndex), so cut that out of oldLink
            }
            else{ // "&assay_slims=" is at end of search
                oldLink = oldLink.substr(0, startingIndex); // assay_slims is from (startingIndex, oldLink.length, so cut that out
            }
        }
        
        this.props.callback(oldLink + '&assay_slims=' + category);
        //return {this.props.callback.bind(null, this.props.current + '&assay_slims=' + category)};
        //return {updatedLink: this.props.current + '&assay_slims=' + category};
        this.setState({updatedLink: oldLink + '&assay_slims=' + category});

    },

    bindClickHandlers: function(d3, el) {
        // Add click event listeners txo each node rendering. Node's ID is its ENCODE object ID
        var svg = el[0];
        //var nodes = svg.selectAll("rect.id");
        //var breakPoint2 = 0;
        //var subnodes = svg.selectAll("g.subnode circle");

        el.on('click', rect => {
            console.log(rect);
            //this.props.
            this.sortByAssay(rect);
        });
        // subnodes.on('click', subnode => {
        //     d3.event.stopPropagation();
        //     this.props.nodeClickHandler(subnode.id);
        // });
    },


    componentDidMount: function() {
        // Draw the chart of search results given in this.props.data.facets. Since D3 doesn't work
        // with the React virtual DOM, we have to load it separately using the webpack .ensure
        // mechanism. Once the callback is called, it's loaded and can be referenced through
        // require.


        require.ensure(['d3'], function(require) {
                 if (this.refs.graphdisplay) {
                    this.d3 = require('d3');
                //     this.dagreD3 = require('dagre-d3');
                var allRects = this.d3.selectAll("rect.box");
                var dataset = [];
                for(var x = 0; x < allRects[0].length; x++){
                    dataset.push(allRects[0][x].id);
                }

                    var el = this.d3.selectAll("rect.box")
                        .data(dataset);
                        //.enter();
                    var breakPoint = 0;
                //     // Add SVG element to the graph component, and assign it classes, sizes, and a group
                //     var svg = this.d3.selectAll("rect");
                //         .attr('id', 'pipeline-graph')
                //         .attr('preserveAspectRatio', 'none')
                //         .attr('version', '1.1');
                //     var svgGroup = svg.append("g");
                //     this.cv.savedSvg = svg;

                //     // Draw the graph into the panel; get the graph's view box and save it for
                //     // comparisons later
                //     var {viewBoxWidth, viewBoxHeight} = this.drawGraph(el);
                //     this.cv.viewBoxWidth = viewBoxWidth;
                //     this.cv.viewBoxHeight = viewBoxHeight;

                //     // Based on the size of the graph and view box, 
                //     var initialZoomLevel = this.setInitialZoomLevel(el, svg);
                //     this.setState({zoomLevel: initialZoomLevel});

                //     // Bind node/subnode click handlers to parent component handlers
                     this.bindClickHandlers(this.d3, el);
                 }

                
            }.bind(this));


        var temp = document.getElementById("graphdisplay");

        // var chromatin = document.getElementById("3D+chromatin+structure");
        // chromatin.addEventListener("click", AssayChartLoader);
        // var breaker = 0;



    },

    render: function() {
        return (
            <div ref="graphdisplay"> 
             <div className="overall-classic">

                    <img src="static/img/classic-image.jpg" className="classicImage"/>
                    
                    <svg id="classic-image-svg-full" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 1440" className="classic-svg" 
                        >
                    
                    <rect id = "3D+chromatin+structure" x="1025" y="774.1" class="st0" width="240.4" height="213.2" className="box"/>
                    <rect id = "DNA+accessibility" x="1289.3" y="774.1" class="st0" width="255.6" height="213.2" className="box"/>
                    <rect id = "DNA+binding" x="1566.7" y="774.1" class="st0" width="219.2" height="213.2" className="box"/>
                    <rect id = "DNA+methylation" x="1807.8" y="774.1" class="st0" width="272.2" height="213.2" className="box"/>
                    <rect id = "tbd" x="2104.5" y="774.1" class="st0" width="345" height="213.2" className="box"/>
                    <rect id = "Transcription" x="2472" y="774.1" class="st0" width="219.2" height="213.2" className="box"/>
                    <rect id = "RNA+binding" x="2713.8" y="774.1" class="st0" width="209.3" height="214.6" className="box"/>
                    
                    </svg>

                    

                </div>
            </div>
        );
    }

});





// Component to display the D3-based chart
var HomepageChart = React.createClass({

    contextTypes: {
        location_href: React.PropTypes.string,
        navigate: React.PropTypes.func
    },

    drawChart: function() {
          // Draw the chart of search results given in this.props.data.facets. Since D3 doesn't work
        // with the React virtual DOM, we have to load it separately using the webpack .ensure
        // mechanism. Once the callback is called, it's loaded and can be referenced through
        // require.
        require.ensure(['chart.js'], function(require) {
            var Chart = require('chart.js');
            var colorList = [
                '#9C008A',
                '#FDC325',
                '#33298C',
                '#179A53',
                '#E5E4E2'
            ];
            var colorList2 = [
                '#bf2e25',
                '#bf2e25',
                '#bf2e25',
                '#bf2e25',
                '#bf2e25'
            ];
            var data = [];
            var labels = [];
            var colors = [];
            var tempColors = ['0000FF'];

            // Get the assay_title counts from the facets
            var facets = this.props.data.facets;
            var assayFacet = facets.find(facet => facet.field === 'award.project');

            // Collect up the experiment assay_title counts to our local arrays to prepare for
            // the charts.
            var totalDocCount = 0;
            assayFacet.terms.forEach(function(term, i) {
                data[i] = term.doc_count;
                totalDocCount += term.doc_count;
                labels[i] = term.key;
                colors[i] = colorList[i % colorList.length];
            });


            // Pass the assay_title counts to the charting library to render it.

            var canvas = document.getElementById("myChart");
            var ctx = canvas.getContext("2d")


            // var width = 400,
            //     height = 400;

            // var text = "Total: " + totalDocCount,
            //     textX = Math.round((width - ctx.measureText(text).width) / 2),
            //     textY = height / 2;

            // ctx.fillText(text, textX, textY);
            // ctx.save();


            this.myPieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors
                    }]
                },

                // tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>%",
                // animateRotate: true
                // multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>",
                options: {

                    // tooltips: {
                    //         enabled: true;
                    // },

                    tooltips: {
                        enabled: true,
                        mode: 'single',
                        callbacks: {
                            legend: function(tooltipItems, data) {
                                return data.labels[tooltipItems.index];
                                //return tooltipItems.yLabel + ' €';
                            }
                        }
                    },

                    legend:{ // to create onClick events for legend, similar to onClick on doughnut sections
                        //legendItemClick: function(){}
                        onClick: (e, legendItem) => {
                            var activeLabel = legendItem;
                            var labelTerm = activeLabel.text;
                            this.context.navigate(this.props.data['@id'] + '&award.project=' + labelTerm);
                            var blocker = 0;
                            
                        }
                        
                        // showTooltip([activeSegment]);
                        // activeSegment.restore();
                    },
                    
                    onClick: (e) => {
                        // React to clicks on pie sections
                        var activePoints = this.myPieChart.getElementAtEvent(e);
                        //colors[0] = "#0000FF"; //changes initial color values
                        if (activePoints[0] == null) {
                            var hi = 0;
                        }
                        else{
                            var term = assayFacet.terms[activePoints[0]._index].key;
                            // var idk = new Array();
                            // assayFacet.terms.forEach(function(term, i) {
                            //     idk.push(term.key);
                            // });
                            this.context.navigate(this.props.data['@id'] + '&award.project=' + term);
                        }
                        
                        this.myPieChart.update();
                        //this.myPieChart.clear();
                        this.myPieChart.render();
                        this.forceUpdate();
                    }
                }
            });
        }.bind(this));
    },

    componentDidMount: function() {
        this.drawChart();
    },

    componentDidUpdate: function(){
        this.drawChart();
    },

    // var legendHolder = document.createElement('div');
    // legendHolder.innerHTML = this.myPieChart.generateLegend();

    // helpers.each(legendHolder.firstChild.childNodes, function (legendNode, index) {
    //     helpers.addEvent(legendNode, 'mouseover', function () {
    //         var activeSegment = this.myPieChart.segments[index];
    //         activeSegment.save();
    //         this.myPieChart.showTooltip([activeSegment]);
    //         activeSegment.restore();
    //     });
    // });

    // helpers.addEvent(legendHolder.firstChild, 'mouseout', function () {
    //     this.myPieChart.draw();
    // });

    // this.myPieChart.chart.canvas.parentNode.parentNode.appendChild(legendHolder.firstChild);

    render: function() {
        return (
            <canvas id="myChart" width="0" height="0"></canvas>
        );
    }

});

/*

// Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// component to draw the resulting chart.
var HumanSecondLoader = React.createClass({

    getDefaultProps: function () {
        // Default searchBase if none passed in
        return {searchBase: '?type=Experiment&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens';
    },

    getInitialState: function() {
        return {search: this.props.searchBase};
    },

    render: function() {
        return (
            <FetchedData>
                <Param name="data" url={'/search/' + this.state.search} />
                <HomepageChart searchBase={this.state.search + '&'} />
            </FetchedData>
        );
    }

});
*/











// // Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// // component to draw the resulting chart.
// var TestLoaderHuman = React.createClass({

//     getDefaultProps: function () {
//         // Default searchBase if none passed in
//         //var oldSearch = this.props.searchBase;
//         return {searchBase: '?type=Experiment&status=released&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens'};
//         //return {searchBase: '?type=Experiment&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens&organ_slims=bronchus'};
//     },

//     getInitialState: function() {
//         return {search: this.props.searchBase};
//     },

//     render: function() {
//         return (
//             <FetchedData>
//                 <Param name="data" url={'/matrix/' + this.state.search} />
//                 <HomepageChart searchBase={this.state.search + '&'} />
//             </FetchedData>
//         );
//     }

// });

// // Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// // component to draw the resulting chart.
// var TestLoaderMouse = React.createClass({

//     getDefaultProps: function () {
//         // Default searchBase if none passed in
//         return {searchBase: '?type=Experiment&status=released&replicates.library.biosample.donor.organism.scientific_name=Mus+musculus'};
//     },

//     getInitialState: function() {
//         return {search: this.props.searchBase};
//     },

//     render: function() {
//         return (
//             <FetchedData>
//                 <Param name="data" url={'/matrix/' + this.state.search} />
//                 <HomepageChart searchBase={this.state.search + '&'} />
//             </FetchedData>
//         );
//     }

// });

// // Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// // component to draw the resulting chart.
// var TestLoaderWorm = React.createClass({

//     getDefaultProps: function () {
//         // Default searchBase if none passed in
//         return {searchBase: '?type=Experiment&status=released&replicates.library.biosample.donor.organism.scientific_name=Caenorhabditis+elegans'};
//     },

//     getInitialState: function() {
//         return {search: this.props.searchBase};
//     },

//     render: function() {
//         return (
//             <FetchedData>
//                 <Param name="data" url={'/matrix/' + this.state.search} />
//                 <HomepageChart searchBase={this.state.search + '&'} />
//             </FetchedData>
//         );
//     }

// });

// // Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// // component to draw the resulting chart.
// var TestLoaderFly = React.createClass({

//     getDefaultProps: function () {
//         // Default searchBase if none passed in
//         return {searchBase: '?type=Experiment&status=released&replicates.library.biosample.donor.organism.scientific_name=Drosophila+melanogaster' + 
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+pseudoobscura' +
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+simulans' +
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+mojavensis' +
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+ananassae' +
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+virilis' +
//                             '&replicates.library.biosample.donor.organism.scientific_name=Drosophila+yakuba'};
//     },

//     getInitialState: function() {
//         return {search: this.props.searchBase};
//     },

//     render: function() {
//         return (
//             <FetchedData>
//                 <Param name="data" url={'/matrix/' + this.state.search} />
//                 <HomepageChart searchBase={this.state.search + '&'} />
//             </FetchedData>
//         );
//     }

// });


// Initiates the GET request to search for experiments, and then pass the data to the HomepageChart
// component to draw the resulting chart.
var HomepageChartLoader = React.createClass({
    propTypes: {
        
        callback: React.PropTypes.func
    },

    updateSearch: function(newSearch) {

        this.props.callback(newSearch);
    },

    componentDidMount: function(){
        this.updateSearch(this.props.searchBase);
    },

    // getDefaultProps: function () {
    //     // Default searchBase if none passed in
    //     return {searchBase: this.props.current};
    // },

    // getInitialState: function() {
    //     console.log("getInitialState searchBase: " + this.props.searchBase);
    //     return {search: this.props.searchBase};
    // },

    render: function() {
        console.log("searchBase: " + this.props.searchBase);
        return (
            <FetchedData>
                <Param name="data" url={'/matrix/' + this.props.searchBase} />
                <HomepageChart searchBase={this.props.searchBase + '&'} />
                
            </FetchedData>
        );
    }

});

// Component to display the D3-based chart
var HomepageChart2 = React.createClass({

    contextTypes: {
        navigate: React.PropTypes.func
    },

    drawChart: function() {

        // Draw the chart of search results given in this.props.data.facets. Since D3 doesn't work
        // with the React virtual DOM, we have to load it separately using the webpack .ensure
        // mechanism. Once the callback is called, it's loaded and can be referenced through
        // require.
        require.ensure(['chart.js'], function(require) {
            var Chart = require('chart.js');
            var colorList = [
                '#871F78',
                '#FFB90F',
                '#003F87',
                '#3D9140',
                '#E5E4E2'
            ];
            var data = [];
            var labels = [];
            var colors = [];

            // Get the assay_title counts from the facets
            var facets = this.props.data.facets;
            var assayFacet = facets.find(facet => facet.field === 'replicates.library.biosample.biosample_type');

            // Collect up the experiment assay_title counts to our local arrays to prepare for
            // the charts.
            assayFacet.terms.forEach(function(term, i) {
                data[i] = term.doc_count;
                labels[i] = term.key;
                colors[i] = colorList[i % colorList.length];
            });

            // Pass the assay_title counts to the charting library to render it.
            var canvas = document.getElementById("myChart2");
            var ctx = canvas.getContext("2d");
            this.myPieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors
                    }]
                },
                options: {
                    onClick: (e) => {
                        // React to clicks on pie sections
                        var activePoints = this.myPieChart.getElementAtEvent(e);
                        var term = assayFacet.terms[activePoints[0]._index].key;
                        this.context.navigate(this.props.data['@id'] + '&replicates.library.biosample.biosample_type=' + term);
                    }
                }
            });

        }.bind(this));

    },

    componentDidMount: function() {
        this.drawChart();
    },

    componentDidUpdate: function() {
        this.drawChart();
    },

    render: function() {
        return (
            <canvas id="myChart2" width="0" height="0"></canvas>
        );
    }

});

var HomepageChartLoader2 = React.createClass({
    propTypes: {
        
        callback: React.PropTypes.func
    },


    // getDefaultProps: function () {
    //     // Default searchBase if none passed in
    //     //return {searchBase: '?type=Experiment&files.file_type=fastq&assay_title=ChIP-seq'};
    //     return {searchBase: '?type=Experiment&status=released'};
    // },

    // getInitialState: function() {
    //     return {search: this.props.searchBase};
    // },

    render: function() {
        return (
            <FetchedData>
                <Param name="data" url={'/matrix/' + this.props.searchBase} />
                <HomepageChart2 searchBase={this.props.searchBase + '&'} />
            </FetchedData>
        );
    }

});


var Panel = module.exports.Panel = React.createClass({
    propTypes: {
        addClasses: React.PropTypes.string, // Classes to add to outer panel div
        noDefaultClasses: React.PropTypes.bool // T to not include default panel classes
    },

    render: function() {
        var {addClasses, noDefaultClasses} = this.props;

        return (
            <div className={(noDefaultClasses ? '' : 'panel panel-default') + (addClasses ? ' ' + addClasses : '')}>
                {this.props.children}
            </div>
        );
    }
});


var PanelBody = module.exports.PanelBody = React.createClass({
    propTypes: {
        addClasses: React.PropTypes.string // Classes to add to outer panel div
    },

    render: function() {
        return (
            <div className={'panel-body' + (this.props.addClasses ? ' ' + this.props.addClasses : '')}>
                {this.props.children}
            </div>
        );
    }
});


var PanelHeading = module.exports.PanelHeading = React.createClass({
    propTypes: {
        addClasses: React.PropTypes.string // Classes to add to outer panel div
    },

    render: function() {
        return (
            <div className={'panel-heading' + (this.props.addClasses ? ' ' + this.props.addClasses : '')}>
                {this.props.children}
            </div>
        );
    }
});


var PanelFooter = module.exports.PanelFooter = React.createClass({
    propTypes: {
        addClasses: React.PropTypes.string // Classes to add to outer panel div
    },

    render: function() {
        return (
            <div className={'panel-footer' + (this.props.addClasses ? ' ' + this.props.addClasses : '')}>
                {this.props.children}
            </div>
        );
    }
});


// <TabPanel> components have tabs that select between panes, and so the main child components of
// <TabPanel> must be <TabPanelPane> components. The children of <TabPanelPane> components are the
// content you want to have rendered within a tab's pane. <TabPanel> takes a required `tabs`
// parameter -- an object that maps an identifier to a tab title. The identifier has to map to a
// child <TabPanelPane> `key` property. Here's an example tabbed panel.
//
// <TabPanel tabs={{panel1: 'Panel 1', panel2: 'Panel 2', panel3: 'Panel 3'}}>
//     <TabPanelPane key="panel1">
//         <div>Content for panel 1</div>
//     </TabPanelPane>
//     <TabPanelPane key="panel2">
//         <div>Content for panel 2</div>
//     </TabPanelPane>
//     <TabPanelPane key="panel3">
//         <div>Content for panel 3</div>
//     </TabPanelPane>
// </TabPanel>
//
// Note that <TabPanelPane> takes an `id` property, not a `key` property because components can't
// receive those. <TabPanel> copies the `key` property to an `id` property in any child <TabPanel>
// components so that <TabPanel> can see it.

var TabPanel = module.exports.TabPanel = React.createClass({
    propTypes: {
        tabs: React.PropTypes.object.isRequired, // Object with tab=>pane specifications
        addClasses: React.PropTypes.string, // Classes to add to navigation <ul>
        moreComponents: React.PropTypes.object, // Other components to render in the tab bar
        moreComponentsClasses: React.PropTypes.string // Classes to add to moreComponents wrapper <div>
    },

    getInitialState: function() {
        return {currentTab: ''};
    },

    // Handle a click on a tab
    handleClick: function(tab) {
        if (tab !== this.state.currentTab) {
            this.setState({currentTab: tab});
        }
    },

    render: function() {
        var children = [];
        var {tabs, addClasses, moreComponents, moreComponentsClasses} = this.props;
        var firstPaneIndex = -1; // React.Children.map index of first <TabPanelPane> component

        // We expect to find <TabPanelPane> child elements inside <TabPanel>. For any we find, get
        // the React `key` value and copy it to an `id` value that we add to each child component.
        // That lets each child get an HTML ID matching `key` without having to pass both a key and
        // id with the same value. We also set the `active` property in the TabPanelPane component
        // here too so that each pane knows whether it's the active one or not. ### React14
        if (this.props.children) {
            children = React.Children.map(this.props.children, (child, i) => {
                if (child.type === TabPanelPane.type) {
                    firstPaneIndex = firstPaneIndex === -1 ? i : firstPaneIndex;

                    // Replace the existing child <TabPanelPane> component
                    return cloneWithProps(child, {id: child.key, active: this.state.currentTab ? this.state.currentTab === child.key : firstPaneIndex === i});
                }
                return child;
            });
        }

        return (
            <div>
                <ul className={'nav nav-tabs' + (addClasses ? (' ' + addClasses) : '')} role="tablist">
                    {Object.keys(tabs).map((tab, i) => {
                        var currentTab = (i === 0 && this.state.currentTab === '') ? tab : this.state.currentTab;

                        return (
                            <li key={tab} role="presentation" aria-controls={tab} className={currentTab === tab ? 'active' : ''}>
                                <a href={'#' + tab} ref={tab} onClick={this.handleClick.bind(this, tab)} data-trigger="tab" aria-controls={tab} role="tab" data-toggle="tab">
                                    {tabs[tab]}
                                </a>
                            </li>
                        );
                    })}
                    {moreComponents ? <div className={moreComponentsClasses}>{moreComponents}</div> : null}
                </ul>
                <div className="tab-content">
                    {children}
                </div>
            </div>
        );
    }
});


var TabPanelPane = module.exports.TabPanelPane = React.createClass({
    propTypes: {
        id: React.PropTypes.string.isRequired, // ID of the pane; not passed explicitly -- comes from `key` of <TabPanelPane>
        active: React.PropTypes.bool // True if this panel is the active one
    },

    render: function() {
        return (
            <div role="tabpanel" className={'tab-pane' + (this.props.active ? ' active' : '')} id={this.props.id}>
                {this.props.active ? <div>{this.props.children}</div> : null}
            </div>
        );
    }
});