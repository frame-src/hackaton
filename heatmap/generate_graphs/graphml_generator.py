import osmnx as ox

# Download the network for different types of transportation
point = (49.141720, 9.218849)
dist = 5600
walk_network = ox.graph_from_point(point, dist=dist, network_type='walk') 
cycle_network = ox.graph_from_point(point, dist=dist, network_type='bike') 
vehicle_network = ox.graph_from_point(point, dist=dist, network_type='drive') 

# Save them as GraphML files
ox.save_graphml(walk_network, "walk1.graphml")
ox.save_graphml(cycle_network, "bicycle1.graphml")
ox.save_graphml(vehicle_network, "car1.graphml")
