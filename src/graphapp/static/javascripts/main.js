/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Main javascript code for handling user interaction.
*/

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
            graph.bind_click_handler("vertex", select);
            graph.bind_click_handler("edge", select);
        };

        //vertex tool interactions
        if (tool == $("#vertex-tool").attr("data-value")) {
            //Vertex add handler
            svg.on("click", function() {
                var coords = d3.mouse(this);
                var x = coords[0];
                var y = coords[1];
                clear_interaction();
                graph.add_vertex(x, y).done(setup_interaction);
            });    
        };

        //edge tool interactions
        if (tool == $("#edge-tool").attr("data-value")) {
            //Edge add handler
            graph.bind_click_handler("vertex", function(v, i) {
                //Don't trigger any click handlers on the svg itself.
                d3.event.stopPropagation();

                //make a line
                svg.append("line")
                    .attr("stroke", "black")
                    .attr("stroke-width", 3)
                    .attr("opacity", .5)
                    .attr("x1", v.x)
                    .attr("y1", v.y)
                    .attr("x2", v.x)
                    .attr("y2", v.y);

                //have the line follow the mouse
                svg.on("mousemove", function() {
                    var coords = d3.mouse(this);
                    var x = coords[0];
                    var y = coords[1];
                    svg.select("line").attr("x2", x).attr("y2", y);
                });

                var clear_line = function() {
                    svg.select("line").remove();
                    setup_interaction();
                };

                //if you click on nothing, clear the line and reset interactions
                svg.on("click", clear_line);

                //change vertex click handlers to add an edge to next clicked vertex
                graph.clear_click_handlers("vertex");
                graph.bind_click_handler("vertex", function(v2, j) {
                    //Don't trigger any click handlers on the svg itself.
                    d3.event.stopPropagation();

                    //if we clicked a different vertex, add the edge
                    if(i != j) {
                        clear_interaction();
                        graph.add_edge(i, j).done(setup_interaction);
                    }

                    //we are done, clear the line
                    clear_line();
                });
            });
        };

        //label tool interactions
        if (tool == $("#label-tool").attr("data-value")) {

        };
    };

    /* Removes up all the interactions for the user. Used when server is busy to enforce server truth.
    **
    */
    var clear_interaction = function() {
        graph.clear_click_handlers("vertex");
        graph.clear_click_handlers("edge");

        svg.on("click", null);
        svg.on("mousemove", null);
    }

    /* select a graph element. Used as a click handler, not for external use.
    **
    ** d - datum of the graph element selected
    ** i - index of the graph element selected
    */
    var select = function(d, i) {
        //Don't trigger any click handlers on the svg itself.
        d3.event.stopPropagation();

        if (!d3.event.shiftKey) {
            graph.clear_selection();
        }
        d.selected = true;
        graph.draw();
    };

});