function drawGraph(data_url, user_points) {
    var area = d3.select("#graph");
    var margin = {top: 10, right: 30, bottom: 20, left: 30},
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
        var n = d3.max(data)
        var scX = d3.scaleLinear().domain([0, n]).range([0, width])

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

        svg.append("g").call(d3.axisLeft(scY));

        // Bars
        svg.selectAll("rect")
            .data(bins)
            .enter()
            .append("rect")
            .attr("x", 1)
            .attr("transform", d => "translate(" + scX(d.x0) + "," + scY(d.length) + ")")
            .attr("width", d => scX(d.x1) - scX(d.x0))
            .attr("height", d => height - scY(d.length))
            .style("fill", "grey")

        // Vertical Line
        svg
            .append("line")
            .attr("x1", scX(user_points))
            .attr("x2", scX(user_points))
            .attr("y1", 0)
            .attr("y2", height)
            .attr("stroke", "blue")
            .attr("stroke-dasharray", "4")
    })
}
