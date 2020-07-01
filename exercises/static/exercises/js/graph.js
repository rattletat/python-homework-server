function drawGraph(data_url, user_points) {
    var area = d3.select("#graph");
    var margin = {top: 10, right: 30, bottom: 55, left: 45},
        borders = area.node().getBoundingClientRect(),
        width = borders.width - margin.left - margin.right,
        height = borders.height - margin.top - margin.bottom;

    window.onresize = function () {
        width = borders.width - margin.left - margin.right;
        height = borders.height - margin.top - margin.bottom;
        area.selectAll("*").remove();
        this.drawGraph(data_url, user_points)
    };

    var svg = area
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data = d3.json(data_url).then(function (data) {
        var n = d3.max(data) * 1.05
        var scX = d3.scaleLinear().domain([1, n]).range([0, width])

        // Axis
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(scX));

        var histogram = d3.histogram()
            .domain(scX.domain())
            .thresholds(scX.ticks(50));

        var bins = histogram(data)
        var scY = d3.scaleLinear()
            .domain([0, d3.max(bins, d => d.length)])
            .range([height, 0]);

        const yAxisTicks = scY.ticks()
            .filter(tick => Number.isInteger(tick));
        const yAxis = d3.axisLeft(scY)
            .tickValues(yAxisTicks)
            .tickFormat(d3.format('d'));
        svg.append("g").call(yAxis);

        // Bars
        svg.selectAll("rect")
            .data(bins)
            .enter()
            .append("rect")
            .attr("x", 1)
            .attr("y", 0)
            .attr("transform", d => "translate(" + scX(d.x0) + "," + height + ")")
            .attr("width", d => scX(d.x1) - scX(d.x0))
            .style("fill", "grey")
            .transition()
            .duration(3000)
            .style("fill", "#0275d8")
            .attr("height", d => height - scY(d.length))
            .attr("transform", d => "translate(" + scX(d.x0) + "," + (scY(d.length)) + ")")

        // Vertical Line
        svg
            .append("line")
            .attr("x1", scX(user_points))
            .attr("x2", scX(user_points))
            .attr("y1", 0)
            .attr("y2", height)
            .attr("stroke", "red")
            .attr("stroke-dasharray", "4");

        // Labels
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height + (2 * margin.bottom / 3))
            .attr("font-family", "sans-serif")
            .attr("font-size", "12px")
            .attr("text-anchor", "middle")
            .attr("class", "x label")
            .text("Punkte");

        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .attr("font-family", "sans-serif")
            .attr("font-size", "12px")
            .attr("class", "y label")
            .text("Studenten");
    })
}
