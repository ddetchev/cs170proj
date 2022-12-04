from starter import *
import networkx as nx
import random
import nxmetis as mt
	
def solve(G: nx.Graph):
	curr_score = float('inf')

	
	# make graph with no 0 degree nodes
	
	
	# Remove fully connected nodes 




	# run metis partitioning on this graph with 0 nodes
	def edgeWeightKey(edge):
		edgeWeight = G.get_edge_data(edge[0], edge[1], default = 0)
		return edgeWeight['weight']

	G_best = None
	for i in range(1, G.number_of_nodes()):
		G_copy = G.copy()
		inter_weight, parts = mt.partition(G,nparts = i, edge_weight = 'weight')
	
		counter = 0
		
		for team in parts:
			counter += 1
			for v in team:
				G_copy.nodes[v]['team'] = counter

		
		#for i in range(len(parts)):
			#G_copy.nodes[i]['team'] = parts[i]
			
		# print("score : ", score(G_copy), "weight ", inter_weight)
		
		

		if (score(G_copy) < curr_score):
			curr_score = score(G_copy)
			G_best = G_copy

	
		else:
			break

	remove_list = []
	connected_list = []
	degree_list = list(nx.degree(G))
	degree_dict = dict(enumerate(degree_list))

	ogLength = G.number_of_nodes()

	removedNodes = set()
	for elem in degree_list.copy():
		if elem[1] == 0:
			removedNodes.add(elem[0])
			G.remove_node(elem[0])
			remove_list.append(elem[0])


	for v in range(0, ogLength): 
		if v not in removedNodes:
			G.nodes[v]['team'] = G_best.nodes[v]['team'] 
	
	# finding smallest cluster by size
	minLength = float('inf')
	for part in parts:
		if len(part) < minLength: 
			minLength = len(part)

	# team_dict = {}
	# for node in nx.nodes(G):
	# 	if G.nodes[node]['team'] in team_dict:
	# 		team_dict[G.nodes[node]['team']] += 1
	# 	else:
	# 		team_dict[G.nodes[node]['team']] = 1

	# minLength = min(team_dict.values())

	 
	# for i in range(len(parts)):
	# 	print("original cluster ", i, " ", len(parts[i]))
	
	newTeams = []
	i = 0


	#change Metis parts output to resemble nxmetis parts output (list of lists of nodes instead of list of team numbers)
	# parts2D = [[] * len(team_dict.values())]
	# for i in range(len(parts)):
	# 	parts2D[parts[i]].append(i)   


	# keep track of i after the while loop so we dont have to remove nodes from old teams just iterate through remaining ones 
	# ---------------------------------------------------------------------------
	while i < minLength:
		team = []
		for part in parts: 
			if part[i] not in removedNodes:
				team.append(part[i]) 
		i += 1
		

	# ------------------- new Teams ------------------------
	# counter = 0
	# for group in newTeams:
	# 	counter += 1
	# 	for v in group:
	# 		if v not in removedNodes:
	# 			G.nodes[v]['team'] = counter 

	
	# after_inter_weight = 0
	# for e in G.edges:
	# 	edgeWeight = G.get_edge_data(e[0], e[1], default = 0)
	# 	if G.nodes[e[0]]['team'] != G.nodes[e[1]]['team']:
	# 		after_inter_weight += edgeWeight['weight']
	#print(after_inter_weight)

	
	# for i in range(0, len(G.edges)):
		
		
		#if G.nodes[edges_and_weights][0]['team'] != G.nodes[edges_and_weights][1]['team']:
			#after_inter_weight += edges_and_weights[2]
	#print("Weight after new teams:", after_inter_weight)

	# newTeams = [ [1, 2, 3], [5, 6, 7]]
#i is now saved at xth index so you ca nkeep iterating through the remaining parts without deleting vertices

#now to redistribute the vertices remaining in all other clusters (smallest is iterated through)

	


	# balance team sizes out if uneven, first create team_dict of team numbers and their team sizes
	# team_dict = {}
	# for node in nx.nodes(G):
	# 	if G.nodes[node]['team'] in team_dict:
	# 		team_dict[G.nodes[node]['team']] += 1
	# 	else:
	# 		team_dict[G.nodes[node]['team']] = 1
	
	# we have a team_dict that maps each team number to the number of penguins in that team
	
	# for node in remove_list:
	#     G.add_node(node)
		
	#     move_on = False
		
	#     for key1 in team_dict.keys():
	#         for key2 in team_dict.keys():
	#             if key1 != key2 and not move_on:
	#                 if team_dict[key1] == team_dict[key2]:
	#                     continue
	#                 elif team_dict[key1] > team_dict[key2]:
	#                     G.nodes[node]['team'] = team_dict[key2]
	#                     count += 1
	#                     move_on = True
	#                 else:
	#                     G.nodes[node]['team'] = team_dict[key1]
	#                     count += 1
	#                     move_on = True
						
	#     if G.nodes[node]['team'] is None:
	#         G.nodes[node]['team'] = random.choice(team_dict.keys())
						
	index = 0
	# print("remove list: ", remove_list)
	while index < len(remove_list):  # iteratively add degree 0 nodes to each of minLength teams one at a time 
		if minLength != 0: 
			i = (index % minLength) 
		else:
			i  = 0
		# print("node team: ", G.nodes[remove_list[index]]['team'])
		G.add_node(remove_list[index])
		G.nodes[remove_list[index]]['team'] = i + 1
		index += 1
		
	# for node in remove_list:
	#     G.add_node(node)
	
	
	# re-add edge weights of 0 to the degree 0 nodes
	#for e in nx.non_edges(G):
		#G.add_edge(*e, weight=0)
	
	return G
	#print(G.number_of_nodes())


#G = read_input('inputs/small1.in')


def solve3(G: nx.Graph):
	curr_score = float('inf')


	G_best = None
	for i in range(1, G.number_of_nodes()):
		G_copy = G.copy()
		cut_value, parts = nx.approximation.one_exchange(G, weight = 'weight')
	
		counter = 0
		
		for team in parts:
			counter += 1
			for v in team:
				G_copy.nodes[v]['team'] = counter
		

		if (score(G_copy) < curr_score):
			curr_score = score(G_copy)
			G_best = G_copy

		else:
			break

	for v in range(0, G.number_of_nodes()): 
		G.nodes[v]['team'] = G_best.nodes[v]['team'] 

	return G



count = 0
totalScore = 0
for i in range(1, 260):
	G = read_input('inputs/small' + str(i) + ".in")
	# G = solve(G)
	count += 1
	totalScore += score(solve3(G))
	print("input ", i)

print(totalScore / count )
# score(G)

# G = nx.Graph()

# G.add_edge(1, 7, weight = 500)
# G.add_edge(6, 8, weight = 250)
# G.add_edge(2, 7, weight = 700)
# G.add_edge(2, 4, weight = 600)
# G.add_edge(3, 8, weight = 1000)
# G.add_edge(4, 8, weight = 900)
# G.add_edge(4, 5, weight = 100)
# G.add_edge(1, 5, weight = 300)


# cut_value, partition = nx.one_exchange(G, initial_cut = set([1, 2, 3, 4]), weight = 'weight')
# print("cut val: ", cut_value, "; partition: ", partition)