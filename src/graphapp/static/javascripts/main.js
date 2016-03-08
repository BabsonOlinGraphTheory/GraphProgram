/*Olin Graph Program Spring 2016
**Authors: Josh Langowitz
**
**Main javascript code for handling user interaction.
*/

// Create the graph and all the GUI elements and interaction handlers
$(document).ready(function(){
    var svg = d3.select("#viz");
    var graph = init_graph(svg);
    var tool = "Vertex";

    graph.add_vertex(100,100);

    $(".tools .btn").click(function() {
        tool = $(this).text();
    });

    svg.on("click", function() {
        var coords = d3.mouse(this);
        var x = coords[0];
        var y = coords[1];
        if (tool == "Vertex") {
            graph.add_vertex(x, y);
            graph.add_edge(0, graph.vertices.length);
            graph.complete_labeling(0, graph.vertices.length + 1);
        }
    });
});