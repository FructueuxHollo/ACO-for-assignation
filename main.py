import pandas as pd
from models.ant import Ant
from algorithm.aco import ACO
from utils.method.evaluate import format_duration
from utils.constants import find_optimal, all_jobs, fine_tune, jobs, verbose
from utils.method.visualization import display_duration_per_worker 
from utils.method.optimization import find_optimal_path, fine_tune_ACO, define_parameter_sets
from utils.method.data_treatment import create_jobs_from_df, create_workers_from_df, create_matches

jobData = pd.read_csv(f"data/jobs{jobs}.csv")
workersData = pd.read_csv("data/workers.csv")

jobs = create_jobs_from_df(jobData)
workers = create_workers_from_df(workersData)

matches = create_matches(jobs,workers,0.1)    
ants = []
for i in range(1, 4):
    ants.append(Ant(id=i))

optimal_path, total_duration = ACO(jobs, workers, matches, ants, alpha=3.875, beta=1, evap_coeff=0.5, Q=len(jobs), animate=1)

display_duration_per_worker(optimal_path)

print("Optimal Path:")
for job, worker in optimal_path:
    print(f"Job: {job.name}, Worker: {worker.name}")
print(f"Total Processing Duration: {format_duration(total_duration)}")

if find_optimal:
    best_path, lowest_duration = find_optimal_path(jobs, workers, alpha=3.875, beta=1, evap_coeff=0.7, Q=len(jobs), iterations=100, verbose=verbose)
    
    print("Optimal Path:", [(job.name, worker.name) for job, worker in best_path])
    print("Lowest Total Duration:", format_duration(lowest_duration))

if all_jobs:
    # Define dataset paths
    job_datasets = [f"data/jobs{i}.csv" for i in range(9, 91, 9)]
    
    results = []
    
    for job_path in job_datasets:
        # Load jobs data for each dataset
        job_data = pd.read_csv(job_path)
        jobs = create_jobs_from_df(job_data)
    
        # Run ACO
        optimal_path, total_duration = find_optimal_path(jobs, workers, alpha=3.875, beta=1, evap_coeff=0.7, Q=len(jobs), iterations=100)
    
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
        print(f"Total Duration: {format_duration(result['total_duration'])} hours, minutes, and seconds")  # format as needed
        print("\n")

# Usage to retrieve parameter sets
initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values = define_parameter_sets(jobs, workers)
print("Initial Pheromones:", initial_pheromones)
print("Number of Ants:", num_ants_list)
print("Alpha Values:", alpha_values)
print("Beta Values:", beta_values)
print("Evaporation Coefficients:", evap_coeffs)
print("Q Values:", Q_values)

if fine_tune:
    # Run the fine-tuning function
    fine_tune_ACO(jobs, workers, initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values)