/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Main javascript code for handling user interaction.
*/

//Priorities: Plan to have something to show in 1 week.
//deployment or install instructions
//Snap to grid
//Undo-Redo
//copy paste
//basic graphs


// Create the graph and all the GUI elements and interaction handlers
$(document).ready(function(){
    var height = "600px";
    var width = "600px";
    var svg = d3.select("#viz").append("svg")
        .attr("id", "image")
        .attr("width", width)
        .attr("height", height)
        .append("g")
            .attr("id", "container")
            .append("g");
    var container = d3.select("#container");
    svg.append("rect")
        .attr("fill", "white")
        .attr("pointer-events", "all")
        .attr("width", width)
        .attr("height", height);
    graph = init_graph(svg);
    var tool = $("#select-tool").attr("data-value");

    var undo_redo = new UndoRedo();

    //data to keep zoom persistent
    var zoom_data = {
        dirty: false,
        base_translate: [0, 0],
        delta_translate: [0, 0],
        base_scale: 1,
        delta_scale: 1
    };

    var array_add = function(a, b) {
        res = [];
        for (var i = 0; i < a.length; i++) {
            res.push(a[i] + b[i]);
        };
        return res
    }

    /* Sets up all the interactions for the user.
    ** There is a pattern of use here where any time we post to the server
    ** we clear interactions before sending the request
    ** and then only reenable interactions when the server responds.
    **
    */
    var setup_interaction = function() {
        console.log("setup");
        //remove old interaction
        clear_interaction();

        //Keep track of which tool is selected
        $(".tools .btn").click(function() {
            tool = $(this).attr("data-value");
            graph.clear_selection();
            setup_interaction();
        });


        //select tool interactions
        if (tool == $("#select-tool").attr("data-value")) {
            graph.bind_handler("click", "vertex", select);
            graph.bind_handler("click", "edge", select);

            if (!zoom_data.dirty) {
                zoom_data.base_scale *= zoom_data.delta_scale;
                zoom_data.base_translate = array_add(zoom_data.base_translate, zoom_data.delta_translate);
                zoom_data.dirty = true;
            };
            console.log(zoom_data);

            //zoom
            container.call(d3.behavior.zoom().on("zoom", function() {
                if (!d3.event.defaultPrevented) {
                    console.log("zooming");
                    zoom_data.delta_translate = d3.event.translate;
                    zoom_data.delta_scale = d3.event.scale;
                    svg.attr("transform", "translate(" + array_add(zoom_data.base_translate, zoom_data.delta_translate) + ")scale(" + zoom_data.base_scale * zoom_data.delta_scale + ")");
                    zoom_data.dirty = false;
                    console.log(svg.attr("transform"));
                }
            }));
        };

        //vertex tool interactions
        if (tool == $("#vertex-tool").attr("data-value")) {
            //Vertex add handler
            svg.on("click", function() {
                if (!d3.event.defaultPrevented) {
                    var coords = d3.mouse(this);
                    var x = coords[0];
                    var y = coords[1];
                    clear_interaction();
                    graph.add_vertex(x, y).done(setup_interaction);
                };
            });

            //Vertex drag handler
            graph.bind_handler("mousedown", "vertex", function(v, i, ele) {
                svg.on("mousemove", function() {
                    var coords = d3.mouse(this);
                    var x = coords[0];
                    var y = coords[1];
                    v.x = x;
                    v.y = y;
                    graph.draw();
                    // console.log("we in mousemove");
                });
                graph.bind_handler("mouseup", "vertex", function() {
                    console.log("drag over");
                    setup_interaction();
                });
            });
        };

        //edge tool interactions
        if (tool == $("#edge-tool").attr("data-value")) {
            //Edge add handler
            graph.bind_handler("click", "vertex", function(v, i) {

                //make a line
                svg.append("line")
                    .attr("stroke", "black")
                    .attr("stroke-width", 3)
                    .attr("opacity", .5)
                    .attr("x1", v.x)
                    .attr("y1", v.y)
                    .attr("x2", v.x)
                    .attr("y2", v.y)
                    .attr("pointer-events", "none");

                //have the line follow the mouse
                svg.on("mousemove", function() {
                    var coords = d3.mouse(this);
                    var x = coords[0];
                    var y = coords[1];
                    svg.select("line").attr("x2", x).attr("y2", y);
                });

                var clear_line = function() {
                    console.log("clearing");
                    svg.select("line").remove();
                    setup_interaction();
                };

                //change vertex click handlers to add an edge to next clicked vertex
                graph.clear_handlers("click", "vertex");
                graph.bind_handler("click", "vertex", function(v2, j) {
                    console.log("adding edge");
                    //if we clicked a different vertex, add the edge
                    if(i != j) {
                        clear_interaction();
                        graph.add_edge(i, j).done(clear_line).fail(function(){console.log("UGH");});
                    } else {
                        //we are done, clear the line
                        console.log("same vertex");
                        clear_line();
                    }
                });

                //if you click on nothing, clear the line and reset interactions
                svg.on("click", function() {
                    if (!d3.event.defaultPrevented) {
                        clear_line();
                    };
                });
                console.log("bound");
                console.log(graph.handlers);
                console.log(graph.handlers.vertex);
            });

            //Edge drag handler
            graph.bind_handler("mousedown", "edge", function(e, i, ele) {
                svg.on("mousemove", function() {
                    // console.log(v1, v2);
                    var v1 = d3.event.shiftKey ? graph.vertices[e.v1] : graph.vertices[e.v2];
                    var v2 = d3.event.shiftKey ? graph.vertices[e.v2] : graph.vertices[e.v1];
                    var mag = cartesian_to_polar([v2.x - v1.x, v2.y -v1.y])[0];
                    var coords = d3.mouse(this);
                    var x = coords[0] - v1.x;
                    var y = coords[1] - v1.y;
                    var angle = snap_to_angle(cartesian_to_polar([x,y])[1], 8);
                    console.log(mag);
                    var diff = polar_to_cartesian([mag, angle]);
                    v2.x = v1.x + diff[0];
                    v2.y = v1.y + diff[1];
                    graph.draw();
                    // console.log("we in mousemove");
                    // console.log(angle);
                    // console.log(diff);
                })
                svg.on("mouseup", function() {
                    console.log("drag over");
                    setup_interaction();
                });
            })
        };

        //label tool interactions
        if (tool == $("#label-tool").attr("data-value")) {
            graph.bind_handler("click", "vertex", function(v, i, ele) {
                d3.select(ele).append("foreignObject")
                    .attr("x", -8)
                    .attr("y", -13)
                    .append("xhtml:div")
                        .html("<input id=label type=text>")
                        .on("click", function() { d3.event.stopPropagation(); })
                        .on("mouseup", function() { d3.event.stopPropagation(); })
                        .on("mousedown", function() { d3.event.stopPropagation(); });
                $("#label").focus()
                .keyup(function(e) {
                    //13 is the enter key
                    if (e.keyCode == 13) {
                        var label = $(this).val();
                        if (label.match(/^\d+$/) !== null) {
                            clear_interaction();
                            graph.label(parseInt(label), i).done(function() {
                                graph.draw();
                                setup_interaction();
                            });
                        } else {
                            alert("Label things using number only please!");
                        };
                    };
                    //27 is the escape key, on escape unlabel the vertex
                    if (e.keyCode == 27) {
                        graph.label(null, i).done(function() {
                            graph.draw();
                            setup_interaction();
                        });
                    };
                })
            });

        };

        //Delete selected
        $("#delete-selected").click(function() {
            clear_interaction();
            console.log("deleting selected");
            graph.delete_selected().done(setup_interaction).fail(function(){console.log("DARN")});
        });

        //Complete labeling
        $("#complete-labeling").click(function() {
            clear_interaction();
            console.log("completing labeling");
            graph.complete_labeling(0, 30).done(setup_interaction);
        });

        //Save graph data locally
        $("#save-data").click(function() {
            var adjacency_matrix = graph.get_adjacency_matrix();
            var location_data = graph.get_location_data();
            var labeling = graph.get_labeling();
            console.log(adjacency_matrix);
            download(JSON.stringify({
                adjacency_matrix: adjacency_matrix,
                location_data: location_data,
                labeling: labeling
            }), "graph.json", "application/json");
        });

        //Save graph image locally
        $("#save-image").click(function() {
            var data = (new XMLSerializer()).serializeToString(d3.select("#image").node());
            download([data], "graph.svg", "'image/svg+xml;charset=utf-8'");
        });

        //Upload graph data
        $("#load-data").on("change", function() {
            console.log("on change");
            var file = this.files[0];
            console.log(file);
            fr = new FileReader();
            fr.onload = function() {
                console.log(fr.result);
                var data = JSON.parse(fr.result);
                var adjacency_matrix = data.adjacency_matrix;
                var location_data = data.location_data;
                var labeling = data.labeling;
                console.log(data);
                clear_interaction();
                graph.new(adjacency_matrix, location_data, labeling).done(function() {
                    console.log(labeling)
                    console.log("Here");
                    console.log(graph.labeling);
                    graph.draw();
                    setup_interaction();
                });
            };
            fr.readAsText(file);
            // console.log(adjacency_matrix);
            // download(JSON.stringify({
            //     adjacency_matrix: adjacency_matrix,
            //     location_data: location_data,
            //     labeling: labeling
            // }), "graph.json", "application/json");
        });
    };

    /* Removes up all the interactions for the user. Used when server is busy to enforce server truth.
    **
    */
    var clear_interaction = function() {
        console.log(graph);
        graph.clear_handlers("click", "vertex");
        graph.clear_handlers("click", "edge");
        graph.clear_handlers("mouseup", "vertex");
        graph.clear_handlers("mouseup","edge");
        graph.clear_handlers("mousedown","vertex");
        graph.clear_handlers("mousedown","edge");
        graph.clear_handlers("mouseover","vertex");
        graph.clear_handlers("mouseover","edge");

        $(".tools .btn").unbind();
        $("#delete-selected").unbind();
        $("#complete-labeling").unbind();
        $("#save-image").unbind();
        $("#save-data").unbind();
        $("#load-data").unbind();

        svg.on("click", null);
        svg.on("mousemove", null);
        svg.on("mouseup", null);

        container.on(".zoom", null);
    }

    /* select a graph element. Used as a click handler, not for external use.
    **
    ** d - datum of the graph element selected
    ** i - index of the graph element selected
    */
    var select = function(d, i) {
        var selected = d.selected;
        if (!d3.event.shiftKey) {
            graph.clear_selection();
        }
        d.selected = !selected;
        graph.draw();
    };

    /* download a file 
    **
    ** text - content of the file
    ** name - name of the file
    ** type - type of the file
    */
    var download = function(text, name, type) {
        var a = document.createElement("a");
        var file = new Blob([text], {type: type});
        a.href = URL.createObjectURL(file);
        a.download = name;
        a.click();
    }

    /* Convert to polar 
    **
    ** v - vector in cartesian coordinates
    */
    var cartesian_to_polar = function(v) {
        var x = v[0];
        var y = v[1];
        var mag = Math.sqrt(Math.pow(x,2) + Math.pow(y,2));
        var phase = Math.atan2(y, x);
        return [mag, phase];
    }

    /* Convert to cartesian 
    **
    ** v - vector in polar coordinates
    */
    var polar_to_cartesian = function(v) {
        var mag = v[0];
        var phase = v[1];
        var x = mag * Math.cos(phase);
        var y = mag * Math.sin(phase);
        // console.log(mag, phase);
        // console.log(x, y);
        return [x, y];
    }

    /* Snap to the nearest angle  
    **
    ** angle  - angle to round
    ** angles - number of evenly-spaced, snappable angles
    */
    var snap_to_angle = function(angle, angles) {
        var round = Math.round(angle * angles / 2 / Math.PI);
        // console.log(angle, angles);
        console.log(round);
        return round / angles * 2 * Math.PI;
    }

    //Create the graph and setup interaction
    graph.new().done(setup_interaction).fail(function(){console.log("DARN")});
});