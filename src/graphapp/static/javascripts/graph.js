/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Javascript code for the graph view.
*/

/* Function to create the graph object
**
** svg - svg DOM element to contain the graph
**
** RETURNS: object representing the graph.
*/
function init_graph(svg) {
    // Vertices contain coordinate information, edges contain a pair of vertex numbers
    graph = {
        vertices: [],
        edges: [],
        labeling: []
    };

    /* Add a vertex to the graph at the specified location
    **
    ** x - x coordinate
    ** y - y coordinate
    */
    graph.add_vertex = function(x, y) {
        // Make sure we successfully add a vertex on the backend before we do anything on the frontend.
        $.post("/graph/vertex/add", function(success){
            graph.vertices.push({x:x, y:y});
            graph.draw()
        });
    };

    /* Add an edge to the graph between the specified vertices
    **
    ** v1 - first vertex index
    ** v2 - second vertex index
    */
    graph.add_edge = function (v1, v2) {
        // Make sure we successfully add an edge on the backend before we do anything on the frontend.
        $.post("/graph/edge/add", {v1:v1, v2:v2}, function(success){
            graph.edges.push({v1:v1, v2:v2});
            var line_data = [graph.vertices[v1], graph.vertices[v2]]
            var line_function = d3.svg.line()
                .x(function(d) { return d.x })
                .y(function(d) { return d.y });
            graph.draw()
        });
    };

    /* Draw the graph
    **
    */
    graph.draw = function () {
        svg.selectAll("g").remove();

        // Vertices
        svg.append("g")
        .attr("id", "vertices")
        .selectAll("g")
        .data(graph.vertices)
        .enter()
        .append("g")
            .append("circle")
            .attr("cx", function(v) { return v.x })
            .attr("cy", function(v) { return v.y })
            .attr("r", 5)
            .attr("fill", "black");

        // Edges
        svg.append("g")
        .attr("id", "edges")
        .selectAll("g")
        .data(graph.edges)
        .enter()
        .append("g")
            .append("path")
            .attr("d", function(d) {
                var line_data = [graph.vertices[d.v1], graph.vertices[d.v2]];
                var line_function = d3.svg.line()
                    .x(function(v) { return v.x })
                    .y(function(v) { return v.y });
                return line_function(line_data);
            })
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("stroke-width", 2)

    }

    return graph
}