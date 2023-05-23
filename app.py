from flask import Flask, request, jsonify
import osmnx as ox
import OSM_utils 
from flask_cors import CORS, cross_origin  

app = Flask(__name__)
cors = CORS(app)


@app.route('/get_path', methods=['POST'])
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
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    ox.config(use_cache=True, log_console=True)
    
    

