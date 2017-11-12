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
function init_graph(svg, width, height) {
    // Vertices contain coordinate information, edges contain a pair of vertex numbers
    var graph = {width: width, height: height};

    /* Function to initialize a graph
    **
    ** adj           - optional adjacency list of graph to initialize, otherwise empty
    ** location_data - list of {x, y} objects to indicate where to put vertices, same length as adj
    ** labeling      - optional list of existing labels in the graph (nulls for empty), same length as adj
    **
    */
    graph.new = function(adj, location_data, labeling) {
        //If we didn't pass in adjacency matrix
        if (typeof(adj) != typeof([])) {
            adj = [];
        };

        if (typeof(labeling) != typeof([])) {
            labeling = [];
            for (var i = 0; i < adj.length; i++) {
                labeling.push(null);
            };
        };

        return $.ajax({
            method: "POST",
            url: "/graph/new/from_adjacency_matrix", 
            data: JSON.stringify({ adj:adj, labeling:labeling }),
            contentType: "application/json"
        }).then(function() {
            console.log("doin it");
            graph.vertices = [];
            graph.edges = [];
            graph.labeling = labeling;
            graph.handlers = {
                click: { vertex:[], edge:[] },
                mouseup: { vertex:[], edge:[] },
                mousedown: { vertex:[], edge:[] },
                mousemove: { vertex:[], edge:[] },
                mouseover: { vertex:[], edge:[] }
            };

            //If the graph isn't empty, we need to do some work to sync the server and client
            for (var i = 0; i < adj.length; i++) {
                graph.vertices.push({x:0, y:0, selected:false});
                //Randomize x and y unless we know it
                if (typeof(location_data) == typeof([])) {
                    graph.vertices[i].x = location_data[i].x;
                    graph.vertices[i].y = location_data[i].y;
                } else {
                    graph.vertices[i].x = $(svg.node).width() * Math.random();
                    graph.vertices[i].y = $(svg.node).height() * Math.random();
                };
                for (var j = i; j < adj.length; j++) {
                    if (adj[i][j] > 0) {
                        graph.edges.push({ v1:i, v2:j, selected:false });
                    }
                };
            };
            graph.draw();
        });
    };

    /* New grid
    **
    ** rows    - number of rows
    ** columns - number of columns
    */
    graph.new_grid = function(rows, columns) {
        // var adj = new Array(rows * columns).fill(new Array(rows * columns).fill(0));
        var adj = []
        for (var i = 0; i < rows * columns; i++) {
            adj.push(new Array(rows * columns).fill(0));
        }
        location_data = [];
        var step = Math.max(30, Math.min((graph.width) / rows, (graph.height) / columns));
        var x = step/2;
        var y = step/2;
        for (var r = 0; r < rows; r++) {
            for (var c = 0; c < columns; c++) {
                var i = r * columns + c;
                if (c > 0) {
                    adj[i-1][i] = 1;
                    adj[i][i-1] = 1;
                }
                if (r > 0) {
                    adj[i-columns][i] = 1;
                    adj[i][i-columns] = 1;
                }
                location_data.push({x:x, y:y});
                y += step;
            }
            x += step;
            y = step/2;
        }
        console.log(step);
        return graph.new(adj, location_data);
    }

    /* Get the adjacency matrix representation of the graph
    **
    */
    graph.get_adjacency_matrix = function() {
        var adj = [];
        for (var i = 0; i < graph.vertices.length; i++) {
            adj.push([]);
            for (var j = 0; j < graph.vertices.length; j++) {
                adj[i].push(0);
            };
        };
        for (var i = 0; i < graph.edges.length; i++) {
            adj[graph.edges[i].v1][graph.edges[i].v2] = 1;
            adj[graph.edges[i].v2][graph.edges[i].v1] = 1;
        };
        return adj;
    };

    /* Get the x and y coordinates of the vertices
    **
    */
    graph.get_location_data = function() {
        var location_data = [];
        for (var i = 0; i < graph.vertices.length; i++) {
            location_data.push({ x:graph.vertices[i].x, y:graph.vertices[i].y });
        };
        return location_data;
    };

    /* Get labeling
    **
    */
    graph.get_labeling = function() {
        return graph.labeling;
    };

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
    graph.delete_selected = function() {
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
            contentType: "application/json"
        });
    };

    /* Add many graph elements with one call to the server
    **
    ** vertices - list of vertices to add in {x: float, y: float} form
    ** edges    - list of edges to add in {v1: int, v2: int} form
    ** labels   - list of labels for new vertices, one label per vertex to add
    **
    */
    graph.add_many = function(vertices, edges, labels) {
        return $.ajax({
            method: "POST",
            url: "/graph/add", 
            data: JSON.stringify({es:edges, ls:labels}), 
            complete: function(success) {
                console.log("added on server");
                for (var e = 0; e < edges.length; e++) {
                    graph.edges.push({v1:edges[e].v1, v2:edges[e].v2, selected:false});
                };
                for (var v = 0; v < vertices.length; v++) {
                    graph.vertices.push({x:vertices[v].x, y:vertices[v].y, selected:false});
                };
                for (var l = 0; l < labels.length; l++) {
                    graph.labeling.push(labels[l]);
                };
                graph.draw();
            },
            contentType: "application/json"
        });
    }

    /* Try to complete a labeling of the graph.
    **
    */
    graph.complete_labeling = function(min, max, constraints) {
        return $.post("/labeler/complete", {min:min, max:max, constraints:constraints}, function(resp){
            if (resp.problems) {
                alert(resp.err + resp.problems);
            } else if (resp.err) {
                alert(resp.err);
            } else {
                graph.labeling = resp.labels;
                graph.draw();
            }
        });
    };

    /* Label a single vertex.
    **
    ** label - value of the label
    ** index - which vertext to label
    */
    graph.label = function(label, index) {
        return $.post("/labeling/label", {v:index, label:label}, function(resp){
            graph.labeling[index] = label;
        });
    };

    /* Label all vertices.
    **
    ** labeling - labeling to use
    */
    graph.set_labeling = function(labeling) {
        return $.ajax({
            method: "POST",
            url: "/labeling/set", 
            data: JSON.stringify({labeling:labeling}), 
            complete: function(resp){
                graph.labeling = labeling;
                graph.draw();
            },
            contentType: "application/json"
        });
    };

    /* bind a handler to a graph element type
    **
    ** event_type    - the event on which to fire the handler
    ** element_type  - type of element to bind to: "edge", "vertex"
    ** f             - function to handle click events
    */
    graph.bind_handler = function(event_type, element_type, f) {
        graph.handlers[event_type][element_type].push(f);
    };

    /* unbind all click handler for a graph element type
    **
    ** event_type    - the event on which to fire the handler
    ** element_type  - type of element to bind to: "edge", "vertex"
    ** f             - function to handle click events
    */
    graph.clear_handlers = function(event_type, element_type) {
        graph.handlers[event_type][element_type] = [];
    };

    /* get the current selection
    **
    */
    graph.get_selection = function() {
        var selected_vertices = [];
        var selected_edges = [];
        for (var i = 0; i < graph.edges.length; i++) {
            if(graph.edges[i].selected) {
                selected_edges.push(i);
            };
        };
        for (var i = 0; i < graph.vertices.length; i++) {
            if(graph.vertices[i].selected) {
                selected_vertices.push(i);
            };
        };
        return { edges: selected_edges, vertices: selected_vertices };
    };

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
    };


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
                            // console.log("vertex handler for", event_type);
                            //Don't let the event bubble to the svg itself.
                            d3.event.preventDefault();
                            //Call all the handlers
                            for (var j = 0; j < graph.handlers[event_type][element_type].length; j++) {
                                graph.handlers[event_type][element_type][j](v, i, this);
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
    };

    return graph;
}
