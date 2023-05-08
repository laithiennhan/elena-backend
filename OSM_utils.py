import osmnx as ox
import algorithm

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
 
def get_path(city, state, start, destination, is_walk, percent, maximize):
    # Get graph of place
    G = get_graph(city, state, is_walk)
    # Nearest coordiantes to start and destination 
    start_nearest = algorithm.nearest_node(G, start[1], start[0])
    end_nearest = algorithm.nearest_node(G, destination[1], destination[0])
    
    path, shortest_path_length, total_elevation = algorithm.dijkstra_path(G, start_nearest, end_nearest, percent, maximize)
    
    path_coord = algorithm.path_nodes_to_coordinates(G, path)
    
    return path_coord, shortest_path_length, total_elevation
    
    
    