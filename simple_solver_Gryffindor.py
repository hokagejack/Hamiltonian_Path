#!/usr/bin/env python3
import csv
import itertools
import time

# Function to find vertices and edges from a CSV file, yielding one graph at a time
def read_graphs_from_csv(test_file):
    current_graph = {'v': [], 'e': []}

    with open(test_file, mode='r') as file:
        csv_reader = csv.reader(file)
        
        for line in csv_reader:
            if not line or len(line) == 0:
                continue
            
            # Detect the start of a new graph with the 'c' line
            if line[0] == 'c':
                if current_graph['v'] or current_graph['e']:
                    yield current_graph
                    current_graph = {'v': [], 'e': []}
            elif line[0] == 'v':
                numbers = list(map(int, line[1:]))  # Convert to integers
                current_graph['v'] = numbers
            elif line[0] == 'e':
                source_id = int(line[1])
                dest_id = int(line[2])
                current_graph['e'].append((source_id, dest_id)) 
        
        # Yield the last graph at the end of the file
        if current_graph['v'] or current_graph['e']:
            yield current_graph

# Function to check if a Hamiltonian path exists in a given graph
def hamiltonian_path_exists(graph):
    vertices = graph['v']
    edges = set(tuple(e) for e in graph['e'])

    # Early exit for cases where Hamiltonian path is impossible
    if len(vertices) < 2:
        return len(vertices) == 1

    if not edges:
        return False

    # Generate all permutations of vertices
    for perm in itertools.permutations(vertices):
        # Check if every consecutive pair of vertices is connected
        path_exists = True
        for i in range(len(perm) - 1):
            if (perm[i], perm[i+1]) not in edges and (perm[i+1], perm[i]) not in edges:
                path_exists = False
                break
        
        if path_exists:
            return True  # A Hamiltonian path is found

    return False  # No Hamiltonian path exists

# List to hold results for CSV output
results = []

# Processing the graphs from the CSV file one at a time
for index, graph in enumerate(read_graphs_from_csv('test_graphs.csv')):
    print(f"Processing graph {index + 1}:")
    print(f"Vertices: {graph['v']}, Edges: {graph['e']}")

    start_time = time.time()  # start time
    result = hamiltonian_path_exists(graph)
    end_time = time.time()  # end time
    
    total_time = end_time - start_time
    result_code = 1 if result else 0
    
    # Change here: use the number of vertices instead of graph number
    num_vertices = len(graph['v'])
    results.append([num_vertices, total_time, result_code])  # Store number of vertices, result, and time

    if result:
        print("A Hamiltonian Path exists!")
    else:
        print("No Hamiltonian Path exists.")
    
    print(f"Total time taken: {total_time:.7f} seconds\n")

# Writing the results to a CSV file
with open('hamiltonian_path_results.csv', mode='w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['Number of Vertices', 'Time Taken (seconds)', 'Hamiltonian Path Found (0/1)'])  # Header
    csv_writer.writerows(results)  # Write all results

print("Results have been written to 'hamiltonian_path_results.csv'")

