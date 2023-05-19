from flask import Flask, request, jsonify
import osmnx as ox
import json
import OSM_utils 
import algorithm

app = Flask(__name__)

@app.route('/get_path', methods=['GET','POST'])
def get_path():
    data = request.get_json()
    start = data['start']
    end = data['end']
    maximize_minimize = data['maximize_minimize']
    percent = float(data['percent'])
    city = data['city']
    state = data['state']
    maximize = False
    if maximize_minimize == "maximize":
        maximize = True
        
    path_coord, path_length, shortest_path_length, total_elevation = OSM_utils.get_path(city, state, start, end, True, percent, maximize)
    
    response = jsonify({"coordinates": path_coord, 
                        "path_length": path_length, 
                        "shortest_path_length": shortest_path_length,
                        "elevation": total_elevation})
        
    return response

if __name__ == '__main__':
    app.run(debug=True)
    
    # Test Run: 
    # G = OSM_utils.get_graph("Amherst", "MA", True)
    # start = [42.401800, -72.531840]
    # end = [42.375381, -72.520500]
    # start_nearest = algorithm.nearest_node(G, start[1], start[0])
    # end_nearest = algorithm.nearest_node(G, end[1], end[0])
    # print(len(G.nodes))
    # path, shortest_length, total_elevation = (algorithm.dijkstra_path(G, start_nearest, end_nearest, 200, False))
    # print(f"Elevation gained: {total_elevation}")
    # print(f"Path length: {algorithm.path_length(G, path)}")
    # print(f"Shortest path length: {shortest_length}")
    # path_coord = algorithm.path_nodes_to_coordinates(G, path)
    # x = path_coord 
    # temp_coor = list()
    # for items in path_coord:
    #   temp_coor.append([items[1],items[0]])
    # print(temp_coor)
