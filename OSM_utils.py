import osmnx as ox

def populate_elevation(graph):
		
	# Get elevation data from Open Topo Data
	url = "https://api.opentopodata.org/v1/aster30m?locations={}&key={}"
	
	G = ox.add_node_elevations_google(
		graph,
		api_key="",
		max_locations_per_batch=100,
		pause_duration=0.02,
		precision=3,
		url_template=url,
	)
	return G

def get_graph(city, state, is_walk):
	# Query to generate graph using OSMNX
	query = {
		'city': city,
		'state': state,
		'country': 'USA',
	}

	nw_type = "bike"
	if is_walk:
		nw_type = "walk"
	
		
	graph = ox.graph_from_place(query, network_type=nw_type)
	
 	# Add Elevation data to graph
	
	graph = populate_elevation(graph)
 
	return graph
 
