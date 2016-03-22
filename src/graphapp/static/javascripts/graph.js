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
    var graph = {};

    graph.new = function(adj) {
        return $.post("/graph/new", {adj:adj}, function(){
            graph.vertices = [];
            graph.edges = [];
            graph.labeling = [];
            graph.click_handlers = { vertex:[], edge:[] };
            graph.mouseup_handlers = { vertex:[], edge:[] };
            graph.mousedown_handlers = { vertex:[], edge:[] };
        });
    }

    /* Add a vertex to the graph at the specified location
    **
    ** x - x coordinate
    ** y - y coordinate
    */
    graph.add_vertex = function(x, y) {
        // Make sure we successfully add a vertex on the backend before we do anything on the frontend.
        return $.post("/graph/vertex/add", function(success){
            graph.vertices.push({x:x, y:y, selected:false});
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
        return $.post("/graph/edge/add", {v1:v1, v2:v2}, function(success){
            graph.edges.push({v1:v1, v2:v2, selected:false});
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
        return $.post("/labeler/complete", {min:min, max:max}, function(resp){
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

    /* bind a click handler to a graph element type
    **
    ** type - type of element to bind to: "edge", "vertex", or "label"
    ** f    - function to handle click events
    */
    graph.bind_click_handler = function(type, f) {
        graph.click_handlers[type].push(f);
    }

    /* unbind all click handler for a graph element type
    **
    ** type - type of element to unbind: "edge", "vertex", or "label"
    */
    graph.clear_click_handlers = function(type) {
        graph.click_handlers[type] = [];
    }

    /* bind a mouseup handler to a graph element type
    **
    ** type - type of element to bind to: "edge", "vertex", or "label"
    ** f    - function to handle mouseup events
    */
    graph.bind_mouseup_handler = function(type, f) {
        graph.mouseup_handlers[type].push(f);
    }

    /* unbind all mouseup handler for a graph element type
    **
    ** type - type of element to unbind: "edge", "vertex", or "label"
    */
    graph.clear_mouseup_handlers = function(type) {
        graph.mouseup_handlers[type] = [];
    }

    /* bind a mousedown handler to a graph element type
    **
    ** type - type of element to bind to: "edge", "vertex", or "label"
    ** f    - function to handle mousedown events
    */
    graph.bind_mousedown_handler = function(type, f) {
        graph.mousedown_handlers[type].push(f);
    }

    /* unbind all mousedown handler for a graph element type
    **
    ** type - type of element to unbind: "edge", "vertex", or "label"
    */
    graph.clear_mousedown_handlers = function(type) {
        graph.mousedown_handlers[type] = [];
    }

    /* clear the current selection
    **
    */
    graph.clear_selection = function() {
        for (var i = 0; i < graph.edges.length; i++) {
            graph.edges[i].selected = false;
        };
        for (var i = 0; i < graph.vertices.length; i++) {
            graph.vertices[i].selected = false;
        };
    }


    /* Draw the graph
    **
    */
    graph.draw = function () {
        svg.selectAll("g").remove();

        // Edges
        svg.append("g")
        .attr("id", "edges")
        .selectAll("g")
        .data(graph.edges)
        .enter()
        .append("g")
            .append("path")
            .attr("d", function(e) {
                var line_data = [graph.vertices[e.v1], graph.vertices[e.v2]];
                var line_function = d3.svg.line()
                    .x(function(v) { return v.x; })
                    .y(function(v) { return v.y; });
                return line_function(line_data);
            })
            .attr("fill", "none")
            .attr("stroke", function(e) { return e.selected ? "blue" : "black" })
            .attr("stroke-width", 3)
            .on("click", function(e, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.click_handlers.edge.length; j++) {
                    graph.click_handlers.edge[j](e, i);
                };
            })
            .on("mouseup", function(e, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.mouseup_handlers.edge.length; j++) {
                    graph.mouseup_handlers.edge[j](e, i);
                };
            })
            .on("mousedown", function(e, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.mousedown_handlers.edge.length; j++) {
                    graph.mousedown_handlers.edge[j](e, i);
                };
            });

        // Vertices
        svg.append("g")
        .attr("id", "vertices")
        .selectAll("g")
        .data(graph.vertices)
        .enter()
        .append("g")
        .attr("transform", function(v) { return "translate(" + v.x + ", " + v.y + ")"; })
            .on("click", function(v, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.click_handlers.vertex.length; j++) {
                    graph.click_handlers.vertex[j](v, i);
                };
            })
            .on("mouseup", function(v, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.mouseup_handlers.vertex.length; j++) {
                    graph.mouseup_handlers.vertex[j](v, i);
                };
            })
            .on("mousedown", function(v, i) {
                d3.event.stopPropagation();
                for (var j = 0; j < graph.mousedown_handlers.vertex.length; j++) {
                    graph.mousedown_handlers.vertex[j](v, i);
                };
            })
            .append("circle")
            .attr("r", 12)
            .attr("stroke", function(v) { return v.selected ? "blue" : "black" })
            .attr("fill", "white");

        // Labels
        svg.select("#vertices").selectAll("g")
            .append("text")
            .attr("text-anchor", "middle")
            .attr("dy", ".3em")
            .attr("fill", function(v) { return v.selected ? "blue" : "black" })
            .text(function(v, i) { return graph.labeling[i]; });
    }
    return graph;
}
