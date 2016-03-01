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

    graph.new = function(adj) {
        $.post("/graph/new", {adj:adj}, function(){
            console.log("new graph created on backend")
        });
    }

    /* Add a vertex to the graph at the specified location
    **
    ** x - x coordinate
    ** y - y coordinate
    */
    graph.add_vertex = function(x, y) {
        // Make sure we successfully add a vertex on the backend before we do anything on the frontend.
        $.post("/graph/vertex/add", function(success){
            graph.vertices.push({x:x, y:y});
            graph.labeling.push(null);
            graph.draw();
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
                .x(function(d) { return d.x; })
                .y(function(d) { return d.y; });
            graph.draw();
        });
    };

    /* Try to complete a labeling of the graph.
    **
    */
    graph.complete_labeling = function(min, max) {
        $.post("/labeler/complete", {min:min, max:max}, function(resp){
            if (resp.problems) {
                alert(resp.err + resp.problems);
            } else if (resp.err) {
                alert(resp.err);
            } else {
                graph.labeling = resp.labels;
                graph.draw();
            }
        });
    }

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
            .attr("cx", function(v) { return v.x; })
            .attr("cy", function(v) { return v.y; })
            .attr("r", 5)
            .attr("fill", "black");

        // Labels
        svg.select("#vertices").selectAll("g")
            .append("text")
            .attr("x", function(v) { return v.x + 10; })
            .attr("y", function(v) { return v.y + 10; })
            .text(function(v, i) { return graph.labeling[i]; })


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
                    .x(function(v) { return v.x; })
                    .y(function(v) { return v.y; });
                return line_function(line_data);
            })
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("stroke-width", 2);
    }
    graph.new();
    return graph;
}