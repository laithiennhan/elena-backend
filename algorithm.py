import osmnx as ox
import networkx as nx
import heapq

def elevation_gain(graph, start, end):
    """ Calculate the elevation gain between two nodes

    Args:
        graph (NetworkX graph): Graph that contains 2 nodes
        start (_type_): _description_
        end (_type_): _description_

    Returns:
        _type_: _description_
    """
    ele = graph.nodes[end]['elevation'] - graph.nodes[start]['elevation']
    return max(0, ele)

def distance(graph, node1, node2):
    """Distance between two nodes

    Args:
        graph (_type_): _description_
        node1 (_type_): _description_
        node2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    return graph.edges[node1, node2, 0]['length']

def path_length(graph, path):
    """Return the total distance of a path

    Args:
        graph (_type_): _description_
        path (_type_): _description_
    """    
    length = 0
    for i in range(len(path) - 1):
        length += distance(graph, path[i], path[i+1])
    return length

def path_elevation(graph, path):
    """Calculate total elevation gain in path

    Args:
        graph (_type_): _description_
        path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    total_elevation = 0
    for i in range(len(path) - 1):
        total_elevation += elevation_gain(graph, path[i], path[i+1])
    
    return total_elevation

def nearest_node(g, x, y):
    # Find the nearest node to the given coordinates
    return ox.nearest_nodes(g, x, y)

def node_to_coordinates(G, node):
    return (G.nodes[node]['x'], G.nodes[node]['y'])

def path_nodes_to_coordinates(G, path):
    coord_path = []
    for node in path:
        coord_path.append(node_to_coordinates(G, node))
    return coord_path

def path_coordinates(G, path):
    coord_list = []
    for node in path:
        coord_list.append(node_to_coordinates(G, node))
    return coord_list

def dijkstra_path(graph, start, end, percent, maximize):
    """Dijkstra algorithm 

    Args:
        graph (_type_): _description_
        start (_type_): _description_
        end (_type_): _description_
        percent (_type_): _description_
        maximize (_type_): _description_
    """
        
    shortest_path = ox.shortest_path(graph, start, end)
    
    shortest_path_length = path_length(graph, shortest_path)
 
    distance_constraint = shortest_path_length * percent / 100
 
    # Elevation cost function
    def elevation_cost(node1, node2):
        node1_elevation = graph.nodes[node1]['elevation']
        node2_elevation = graph.nodes[node2]['elevation']
        # if maximize:
        # 	return min(0, node1_elevation - node2_elevation)
        # else:
        return max(0, node2_elevation - node1_elevation)

    # Dijkstra algorithm for route with respect to elevation cost
    distances = {node: float('inf') for node in graph.nodes}
    predecessors = {node: None for node in graph.nodes}	
    elevations = {node: float('inf') for node in graph.nodes}
    
    # Priority queue:
    p_queue = []
    path = []
    elevations[start] = 0
    distances[start] = 0
    if maximize:
        heapq.heappush(p_queue, (-elevation_cost(start, end), start))
    else:
        heapq.heappush(p_queue, (elevation_cost(start, end), start))
    while p_queue:
        # Get the node with the lowest estimated cost to the goal
        current_cost, current_node = heapq.heappop(p_queue)

        # If we reached the goal, reconstruct the path and return it
        if current_node == end:
            print("here")
            path = []
            while current_node:
                path.append(current_node)
                current_node = predecessors[current_node]
            return (path[::-1], shortest_path_length, path_elevation(graph, path))

        # Check the neighboring nodes
        for curr, neighbor, data in graph.edges(current_node, data=True):
            # Calculate the elevation gain between the current node and the neighbor
            curr_elevation = elevation_cost(current_node, neighbor)
            curr_distance = distance(graph, current_node, neighbor)
            # Calculate the total distance of the path so far
            total_elevation = elevations[current_node] + curr_elevation
            total_distance = distances[current_node] + curr_distance

            # Check if the total distance exceeds x% of the shortest path
            if total_distance > distance_constraint:
                continue

            # Update the distance and predecessor if the new distance is shorter
            if total_elevation < elevations[neighbor]:
                elevations[neighbor] = total_elevation
                distances[neighbor] = total_distance
                predecessors[neighbor] = current_node

                # Add the neighbor to the priority queue with its estimated cost to the goal
                if maximize:
                    heapq.heappush(p_queue, (-total_elevation, neighbor))
                else:
                    heapq.heappush(p_queue, (total_elevation, neighbor))
                

    # If we didn't find a path, return the shortest path
    return shortest_path, shortest_path, path_elevation(graph, shortest_path)



    
    