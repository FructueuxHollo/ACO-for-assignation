import pandas as pd
from models.ant import Ant
from algorithm.aco import ACO
from utils.method.evaluate import format_duration
from utils.method.visualization import display_duration_per_worker 
from utils.options import find_optimal, all_jobs, fine_tune, jobs, verbose, animate
from utils.method.data_treatment import create_jobs_from_df, create_workers_from_df, create_matches
from utils.method.optimization import deep_random_search_ACO, define_random_search_ranges, find_optimal_path, fine_tune_ACO, define_parameter_sets, random_search_ACO

jobData = pd.read_csv(f"data/jobs{jobs}.csv")
workersData = pd.read_csv("data/workers.csv")

jobs = create_jobs_from_df(jobData)
workers = create_workers_from_df(workersData)

# matches = create_matches(jobs,workers,0.398)    
# ants = []
# for i in range(1, 6):
#     ants.append(Ant(id=i))

# optimal_path, total_duration = ACO(jobs, workers, matches, ants, alpha=1.913, beta=0.462, evap_coeff=0.133, Q=0.237, animate=animate)

# display_duration_per_worker(optimal_path)

# print("Optimal Path:")
# for job, worker in optimal_path:
#     print(f"Job: {job.name}, Worker: {worker.name}")

if find_optimal:
    best_path, lowest_duration, mean_duration = find_optimal_path(jobs, workers,iterations=100, verbose=verbose)
    
    print("Optimal Path:", [(job.name, worker.name) for job, worker in best_path])
    print("Lowest Total Duration:", format_duration(lowest_duration))

if all_jobs:
    # Define dataset paths
    job_datasets = [f"data/jobs{i}.csv" for i in range(18, 91, 9)]
    
    results = []
    
    for job_path in job_datasets:
        # Load jobs data for each dataset
        job_data = pd.read_csv(job_path)
        jobs = create_jobs_from_df(job_data)
    
        # Run ACO
        optimal_path, total_duration, mean_duration = find_optimal_path(jobs, workers, iterations=100 ,verbose=verbose)
    
        # Store the result with path and duration
        results.append({
        "job_dataset": job_path,
        "optimal_path": [(job.name, worker.name) for job, worker in optimal_path],
        "total_duration": total_duration
        })
    
    # Display results sorted by total duration
    for result in sorted(results, key=lambda x: x["total_duration"]):
        print(f"Dataset: {result['job_dataset']}")
        print(f"Optimal Path: {result['optimal_path']}")
        print(f"Total Duration: {format_duration(result['total_duration'])}")  # format as needed
        print("\n")

# Usage to retrieve parameter sets
# initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values = define_parameter_sets(jobs, workers)
param_ranges = define_random_search_ranges(jobs)

if fine_tune:
    if verbose: 
        print("Initial Pheromones:", param_ranges['initial_pheromones'])
        print("Number of Ants:", param_ranges["num_ants_list"])
        print("Alpha Values:", param_ranges["alpha_values"])
        print("Beta Values:", param_ranges["beta_values"])
        print("Evaporation Coefficients:", param_ranges["evap_coeffs"])
        print("Q Values:", param_ranges["Q_values"])
    # Run the fine-tuning function
    # fine_tune_ACO(jobs, workers, initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values)
    best_results = random_search_ACO(jobs, workers, param_ranges)
    # Run Deep Random Search
    # best_params, best_duration = deep_random_search_ACO(
    #     jobs=jobs,
    #     workers=workers,
    #     param_ranges=param_ranges,
    #     num_trials=100,
    #     max_iterations=200,
    #     inner_iterations=10,
    #     tolerance=1e-5,
    #     min_interval_width=1e-3,
    #     max_depth=10
    # )

    # print("\nFinal Best Parameters:")
    # print(best_params)
    # print(f"Best Duration: {best_duration}")