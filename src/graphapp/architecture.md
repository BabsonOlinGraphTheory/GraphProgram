Here's the plan so far:

In terms of structure, we have the base /__init__.py, which defines the graphapp package, creates the app, registers all the routes. /app.py imports and starts the app.

The routes live in the /routes directory, implemented as a set of blueprints that /__init__.py registers.
/routes/graph.py has all the routes for manipulating a graphlib graph object that it stores 
/routes/labeler.py has all the routes for manipulating a graphlib labeler object that it stores
/routes/labeling.py has all the routes for manipulating a graphlib labeling object that it stores

Templates live in the /templates directory - I only plan on just the one page so probably one template

/static has /static/stylesheets with any .css files, and /static/javascripts with any .js files for the front end.
The idea is to have the frontend written in d3, using ajax to keep in sync with the python backend. Visualization gets handled in d3 and all the graph logic is shipped to the python.