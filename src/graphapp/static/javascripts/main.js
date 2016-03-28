/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Main javascript code for handling user interaction.
*/

//Priorities: Plan to have something to show in 2 weeks.
//Label
//Zoom
//Undo-Redo
//Save-Load


// Create the graph and all the GUI elements and interaction handlers
$(document).ready(function(){
    var svg = d3.select("#viz");
    graph = init_graph(svg);
    tool = $("#select-tool").attr("data-value");

    //Create the graph and setup interaction
    graph.new().done(setup_interaction);

    //Keep track of which tool is selected
    $(".tools .btn").click(function() {
        tool = $(this).attr("data-value");
        graph.clear_selection();
        setup_interaction();
    });
    

    /* Sets up all the interactions for the user.
    ** There is a pattern of use here where any time we post to the server
    ** we clear interactions before sending the request
    ** and then only reenable interactions when the server responds.
    **
    */
    var setup_interaction = function() {
        //remove old interaction
        clear_interaction();

        //select tool interactions
        if (tool == $("#select-tool").attr("data-value")) {
            graph.bind_handler("click", "vertex", select);
            graph.bind_handler("click", "edge", select);
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
                })
                graph.bind_handler("mouseup", "vertex", function() {
                    console.log("drag over");
                    setup_interaction();
                });
            })
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
                        graph.add_edge(i, j).done(clear_line);
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
        };

        //label tool interactions
        if (tool == $("#label-tool").attr("data-value")) {

        };

        //Delete selected
        $("#delete-selected").click(function() {
            clear_interaction();
            console.log("deleting selected");
            graph.delete_selected().done(setup_interaction);
        });
    };

    /* Removes up all the interactions for the user. Used when server is busy to enforce server truth.
    **
    */
    var clear_interaction = function() {
        graph.clear_handlers("click", "vertex");
        graph.clear_handlers("click", "edge");
        graph.clear_handlers("mouseup", "vertex");
        graph.clear_handlers("mouseup","edge");
        graph.clear_handlers("mousedown","vertex");
        graph.clear_handlers("mousedown","edge");
        graph.clear_handlers("mouseover","vertex");
        graph.clear_handlers("mouseover","edge");

        $("#delete-selected").unbind();

        svg.on("click", null);
        svg.on("mousemove", null);
        svg.on("mouseup", null);
    }

    /* select a graph element. Used as a click handler, not for external use.
    **
    ** d - datum of the graph element selected
    ** i - index of the graph element selected
    */
    var select = function(d, i) {
        if (!d3.event.shiftKey) {
            graph.clear_selection();
        }
        d.selected = true;
        graph.draw();
    };

});