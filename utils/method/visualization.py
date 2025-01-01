import networkx as nx
from utils.method.pheromone_update import calculate_worker_duration
from utils.method.evaluate import format_duration

def visualize_network(jobs, workers, matches, ax):
    """
    Visualizes the job-worker bipartite graph with NetworkX, where edge thickness represents pheromone levels.
    
    :param jobs: List of job objects.
    :param workers: List of worker objects.
    :param matches: List of Match objects with pheromone levels.
    :param iteration: The current iteration number (optional, for labeling the plot).
    """
    G = nx.DiGraph()
    
    # Create nodes for jobs and workers
    job_nodes = [f"{job.name}_{i}" for i, job in enumerate(jobs)]
    worker_nodes = [worker.name for worker in workers]
    
    # Add job and worker nodes to the graph
    G.add_nodes_from(job_nodes, bipartite=0, color='blue')
    G.add_nodes_from(worker_nodes, bipartite=1, color='green')
    
    # Add edges with pheromone as weight
    # edge_labels = {}
    for match in matches:
        job, worker = match.value
        job_name = f"{job.name}_{jobs.index(job)}"
        pheromone = match.pheromone
        edge_weight = match.processing_duration
        edge_thickness = 150*pheromone  

        # Edge from job to worker
        G.add_edge(job_name, worker.name, weight=edge_weight, thickness=edge_thickness)
        # # Prepare labels for edges: (pheromone, processing duration)
        # edge_labels[(job_name, worker.name)] =f"{pheromone:.2f} ; {edge_weight}"
    
    # Define positions with spacing
    vertical_offset = 10
    max_y = (len(job_nodes)*vertical_offset)
    pos = {}
    pos.update((job, (0, i * vertical_offset)) for i, job in enumerate(job_nodes))  # Jobs on left
    pos.update((worker, (1, i + i * max_y/len(workers))) for i, worker in enumerate(worker_nodes))  # Workers on right

    # Adjust edge label positions (move toward the left)
    # edge_label_pos = {
    #     (u, v): (
    #         0.75 * pos[u][0] + 0.25 * pos[v][0],
    #         0.75 * pos[u][1] + 0.25 * pos[v][1],
    #     )
    #     for u, v in G.edges()
    #     if u in pos and v in pos  # Ensure both nodes exist in pos
    # }


    # Draw nodes
    job_colors = 'skyblue'
    worker_colors = 'lightgreen'
    nx.draw_networkx_nodes(G, pos, nodelist=job_nodes, node_color=job_colors, node_size=300, label="Jobs", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=worker_nodes, node_color=worker_colors, node_size=300, label="Workers", ax=ax)
    
    # Draw edges with width based on pheromone level
    edges = G.edges(data=True)
    edge_widths = [data['thickness'] for _, _, data in edges]
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=edge_widths, alpha=0.5, edge_color="gray")
    
    # Draw labels for nodes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", ax=ax)
    
    # Draw edge labels (pheromone level and processing duration)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red", ax=ax)

def display_duration_per_worker(optimal_path):
	worker_jobs = {}
	
	for job, worker in optimal_path: 
		if worker not in worker_jobs:
			worker_jobs[worker] = []
		worker_jobs[worker].append(job) 
	for worker, assigned_jobs in worker_jobs.items():
		worker_duration = calculate_worker_duration(assigned_jobs, worker)
		print(f"Worker: {worker.name}, Total Duration: {format_duration(worker_duration)}")