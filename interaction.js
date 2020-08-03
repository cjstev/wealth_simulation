// Sources:
// https://observablehq.com/@d3/d3-format
// https://bl.ocks.org/d3noob/a22c42db65eb00d4e369

// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 800 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// Parse the date / time
//var parseDate = d3.time.format("%d-%b-%y").parse;
//var formatTime = d3.time.format("%e %B");
var formatCash = d3.format("$.3s");
var formatPercent = d3.format(".0%");

// Set the ranges
//var x = d3.time.scale().range([0, width]);
var x = d3.scale.linear().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var valueline = d3.svg.line()
    .x(function(d) { return x(d.wealth); })
    .y(function(d) { return y(d.probability); });

// Define the div for the tooltip
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// Adds the svg canvas
var svg = d3.select("body")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.csv("data.csv", function(error, data) {
    data.forEach(function(d) {
//        d.wealth = parseDate(d.wealth);

        d.wealth = +d.wealth;
        d.probability = +d.probability;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.wealth; }));
    y.domain([0, d3.max(data, function(d) { return d.probability; })]);

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(data));

    // Add the scatterplot
    svg.selectAll("dot")
        .data(data)
    .enter().append("circle")
        .attr("r", 5)
        .attr("cx", function(d) { return x(d.wealth); })
        .attr("cy", function(d) { return y(d.probability); })
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div	.html(formatCash(d.wealth) + "<br/>"  + formatPercent(d.probability))
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
            })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis.tickFormat(formatCash));

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis.tickFormat(formatPercent));

});
