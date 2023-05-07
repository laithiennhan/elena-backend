from flask import Flask
import osmnx as ox

import OSM_utils 

app = Flask(__name__)

@app.route('/')
def index():
	return "Lajima"

if __name__ == '__main__':
    # app.run(debug=True)
    G = OSM_utils.get_graph("Amherst", "MA", True)
    ox.plot_graph(G)
    