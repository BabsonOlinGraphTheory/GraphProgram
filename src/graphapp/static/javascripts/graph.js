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
            graph.handlers = {
                click: { vertex:[], edge:[] },
                mouseup: { vertex:[], edge:[] },
                mousedown: { vertex:[], edge:[] },
                mouseover: { vertex:[], edge:[] }
            };
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
            //Check if the edge already exists first
            for (var i = 0; i < graph.edges.length; i++) {
                if (graph.edges[i].v1 == v1 && graph.edges[i].v2 == v2) {
                    return;
                }
            };
            graph.edges.push({v1:v1, v2:v2, selected:false});
            graph.draw();
        });
    };

    /* Remove a vertex from the graph
    **
    ** v - index of vertex to remove
    */
    graph.remove_vertex = function(v) {
        // Make sure we successfully remove a vertex on the backend before we do anything on the frontend.
        return $.post("/graph/vertex/remove", {v:v}, function(success){
            graph._remove_vertex(v);
            graph.draw();
        });
    };

    //Helper for removing vertex, just on the client side.
    graph._remove_vertex = function(v) {
        graph.vertices.splice(v, 1);
        graph.labeling.splice(v, 1);
        removes = [];
        for (var i = 0; i < graph.edges.length; i++) {
            if (graph.edges[i].v1 == v || graph.edges[i].v2 == v) {
                //Edge contains removed vertex, remove it too
                removes.push(i);
            } else {
                //Update vertex indices bigger than v to reflect that v is gone.
                if (graph.edges[i].v1 > v) {
                    graph.edges[i].v1--;
                }
                if (graph.edges[i].v2 > v) {
                    graph.edges[i].v2--;
                }
            }
        };
        for (var j = removes.length - 1; j >= 0; j--) {
            graph.edges.splice(removes[j], 1);
        };
    };

    /* Remove an edge from the graph
    **
    ** e - edge index
    */
    graph.remove_edge = function (e) {
        // Make sure we successfully remove an edge on the backend before we do anything on the frontend.
        return $.post("/graph/edge/remove", {v1:graph.edges[e].v1, v2:graph.edges[e].v2}, function(success){
            graph.edges.splice(e, 1);
            graph.draw();
        });
    };

    /* Delete all selected graph elements
    **
    */
    graph.delete_selected = function () {
        console.log("deleting things");
        edges = [];
        verts = [];
        for (var e = graph.edges.length - 1; e >= 0 ; e--) {
            if (graph.edges[e].selected) {
                edges.push(graph.edges[e]);
            }
        };

        for (var v = graph.vertices.length - 1; v >= 0; v--) {
            console.log(v);
            if (graph.vertices[v].selected) {
                verts.push(v);
            }
        };
        console.log({es:edges, vs:verts});
        return $.ajax({
            method: "POST",
            url: "/graph/delete", 
            data: JSON.stringify({es:edges, vs:verts}), 
            complete: function(success) {
                console.log("deleted on server");
                for (var e = graph.edges.length - 1; e >= 0 ; e--) {
                    if (graph.edges[e].selected) {
                        graph.edges.splice(e, 1);
                    }
                };

                for (var v = 0; v < verts.length; v++) {
                    graph._remove_vertex(verts[v]);
                };
                graph.clear_selection();
                graph.draw();
            },
            mimeType: "application/json",
            contentType: "application/json"
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

    /* bind a handler to a graph element type
    **
    ** event_type    - the event on which to fire the handler
    ** element_type  - type of element to bind to: "edge", "vertex"
    ** f             - function to handle click events
    */
    graph.bind_handler = function(event_type, element_type, f) {
        graph.handlers[event_type][element_type].push(f);
    }

    /* unbind all click handler for a graph element type
    **
    ** event_type    - the event on which to fire the handler
    ** element_type  - type of element to bind to: "edge", "vertex"
    ** f             - function to handle click events
    */
    graph.clear_handlers = function(event_type, element_type) {
        graph.handlers[event_type][element_type] = [];
    }

    /* clears the current selection
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
        var set_handlers = function(selection, element_type) {
            for (event_type in graph.handlers) {
                if (graph.handlers.hasOwnProperty(event_type)) {
                    //IIFE to avoid aliasing issues with event type.
                    (function(event_type){
                        selection.on(event_type, function(v, i) {
                            console.log("vertex handler for", event_type);
                            //Don't let the event bubble to the svg itself.
                            d3.event.stopPropagation();
                            //Call all the handlers
                            for (var j = 0; j < graph.handlers[event_type][element_type].length; j++) {
                                graph.handlers[event_type].vertex[j](v, i);
                            };
                        });
                    })(event_type);
                }
            }
        }

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
            .attr("stroke-width", 3);

        var edges = svg.select("#edges").selectAll("g");
        //Bind all types of handlers to edges
        set_handlers(edges, "edge");

        // Vertices
        svg.append("g")
        .attr("id", "vertices")
        .selectAll("g")
        .data(graph.vertices)
        .enter()
        .append("g")
        .attr("transform", function(v) { return "translate(" + v.x + ", " + v.y + ")"; })
            .append("circle")
            .attr("r", 12)
            .attr("stroke", function(v) { return v.selected ? "blue" : "black" })
            .attr("fill", "white");

        var vertices = svg.select("#vertices").selectAll("g");

        // Labels
        vertices.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", ".3em")
            .attr("pointer-events", "none")
            .attr("fill", function(v) { return v.selected ? "blue" : "black" })
            .text(function(v, i) { return graph.labeling[i]; });

        //Bind all types of handlers to vertices
        set_handlers(vertices, "vertex");
    }
    return graph;
}
