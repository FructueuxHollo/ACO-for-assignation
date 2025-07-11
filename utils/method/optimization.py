import numpy as np
from tqdm import tqdm
from models.ant import Ant
from itertools import product
# from algorithm.aco import ACO
from algorithm.aco_elitist_minmax import ACO_elitist_minmax as ACO
from utils.options import jobs 
from random import uniform, choice
from utils.method.data_treatment import create_matches
from utils.method.evaluate import format_duration  # Add this import

def find_optimal_path(jobs, workers, num_ants=5, initial_pheromone=0.554, alpha=1.182, beta=0.497, evap_coeff=0.892, Q=75.021, iterations=10, verbose=0):
    """
    Executes the ACO function multiple times to find the best path with the lowest total duration.
    
    :param jobs: List of jobs.
    :param matches: List of Match objects.
    :param ants: List of Ant objects.
    :param alpha: Pheromone importance.
    :param beta: Heuristic importance.
    :param evap_coeff: Pheromone evaporation coefficient.
    :param Q: Constant for pheromone deposition.
    :param iterations: Number of times to run the ACO function.
    :return: A tuple containing the optimal path, the lowest total duration found, and mean duration.
    """
    best_path = None
    lowest_duration = float('inf')
    all_durations = []

    for i in range(iterations):
        matches = create_matches(jobs,workers,initial_pheromone)    
        ants = []
        for j in range(1, num_ants + 1):
            ants.append(Ant(id=j))
        # Run the ACO algorithm
        optimal_path, total_duration = ACO(jobs, workers, matches, ants, alpha, beta, evap_coeff, Q)
        
        all_durations.append(total_duration)

        # Check if the current run's duration is the lowest
        if total_duration < lowest_duration:
            lowest_duration = total_duration
            best_path = optimal_path
        if verbose:
            print(f"Iteration {i+1}: Duration={total_duration}, Best Duration={lowest_duration}")
    
    mean_duration = sum(all_durations) / len(all_durations)
    return best_path, lowest_duration, mean_duration


def fine_tune_ACO(jobs, workers, initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values, max_iterations=1000, tolerance=1e-5):
    """
    Fine-tunes the ACO algorithm by testing all combinations of the given parameter values.
    
    :param jobs: List of job objects.
    :param workers: List of worker objects.
    :param initial_pheromones: List of initial pheromone levels to test.
    :param num_ants_list: List of numbers of ants to test.
    :param alpha_values: List of alpha values to test.
    :param beta_values: List of beta values to test.
    :param evap_coeffs: List of evaporation coefficients to test.
    :param Q_values: List of Q values to test.
    :param max_iterations: Maximum number of iterations for each ACO run.
    :param tolerance: Convergence tolerance for each ACO run.
    :return: Sorted list of results with total duration and corresponding parameters.
    """
    # Initialize a list to store results
    results = []
   
    # Calculate the total number of combinations for tqdm
    total_combinations = len(initial_pheromones) * len(num_ants_list) * len(alpha_values) * len(beta_values) * len(evap_coeffs) * len(Q_values)

    # Generate all combinations of the parameter values
    for initial_pheromone, num_ants, alpha, beta, evap_coeff, Q in tqdm(product(initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values), total=total_combinations, desc="Fine-tuning parameters"):
        
        # Create matches for the current initial pheromone level
        matches = create_matches(jobs, workers, initial_pheromone)
       
        # Create ants for the current number of ants
        ants = [Ant(id=i) for i in range(1, num_ants + 1)]
        
        # Run the ACO algorithm with the current combination of parameters
        optimal_path, total_duration = ACO(jobs, matches, ants, alpha, beta, evap_coeff, Q, max_iterations, tolerance, max_iterations/2)
       
        # Store the result with parameters for sorting later
        results.append({
            'total_duration': total_duration,
            'parameters': {
                'initial_pheromone': initial_pheromone,
                'num_ants': num_ants,
                'alpha': alpha,
                'beta': beta,
                'evap_coeff': evap_coeff,
                'Q': Q
            }
        })

    # Sort results by total duration in ascending order
    results.sort(key=lambda x: x['total_duration'])

    # Print sorted results
    for result in results:
        params = result['parameters']
        print(f"Total Duration: {result['total_duration']} | Parameters: Initial Pheromone: {params['initial_pheromone']}, "
              f"Num Ants: {params['num_ants']}, Alpha: {params['alpha']}, Beta: {params['beta']}, "
              f"Evap Coeff: {params['evap_coeff']}, Q: {params['Q']}")

    return results

# Define the parameters based on provided ranges and scaling method
def define_parameter_sets(jobs):
    # Number of jobs (nodes) used to scale Q
    N = len(jobs)
    
    # Define parameter sets
    initial_pheromones = np.linspace(0.1, 1.0, 5).tolist()  # Initial pheromone level τ₀ from 0.1 to 1.0
    num_ants_list = [int(x) for x in np.linspace(N, 2 * N, 10).tolist()]  # Number of ants from N to 2N
    alpha_values = np.linspace(0.5, 5, 5).tolist()  # Alpha (α) values from 0.5 to 5
    beta_values = np.linspace(1, 10, 5).tolist()  # Beta (β) values from 1 to 10
    evap_coeffs = np.linspace(0.1, 0.9, 5).tolist()  # Evaporation coefficient (ρ) from 0.1 to 0.9

    # Q value for pheromone deposition
    Q_values = N

    # Combine parameter sets for fine-tuning
    return initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values


def random_search_ACO(jobs, workers, param_ranges, num_trials=100,inner_iterations=100):
    """
    Fine-tunes the ACO algorithm using Random Search.

    :param jobs: List of job objects.
    :param workers: List of worker objects.
    :param param_ranges: Dictionary containing ranges for parameters.
    :param num_trials: Number of random parameter sets to test.
    :param max_iterations: Maximum number of iterations for each ACO run.
    :param inner_iterations: Number of iterations for find_optimal_path.
    :param tolerance: Convergence tolerance for each ACO run.
    :return: Sorted list of results with total duration and corresponding parameters.
    """
    # Initialize a list to store results
    results = []

    # Run Random Search for the given number of trials
    for _ in tqdm(range(num_trials), desc="Random Search Trials"):
        # Randomly sample parameter values from the given ranges
        initial_pheromone = uniform(*param_ranges['initial_pheromones'])
        num_ants = int(choice(range(param_ranges['num_ants_list'][0], param_ranges['num_ants_list'][1]+1)))
        alpha = uniform(*param_ranges['alpha_values'])
        beta = uniform(*param_ranges['beta_values'])
        evap_coeff = uniform(*param_ranges['evap_coeffs'])
        Q = uniform(*param_ranges['Q_values'])

        # # run ACO with the sampled parameters
        # # Create matches for the current initial pheromone level
        # matches = create_matches(jobs, workers, initial_pheromone)
       
        # # Create ants for the current number of ants
        # ants = [Ant(id=i) for i in range(1, num_ants + 1)]
        
        # # Run the ACO algorithm with the current combination of parameters
        # optimal_path, total_duration = ACO(jobs, workers,  matches, ants, alpha, beta, evap_coeff, Q, inner_iterations, patience= 10)

        # Use find_optimal_path instead of single ACO run
        optimal_path, total_duration, mean_duration = find_optimal_path(
            jobs=jobs,
            workers=workers,
            num_ants=num_ants,
            initial_pheromone=initial_pheromone,
            alpha=alpha,
            beta=beta,
            evap_coeff=evap_coeff,
            Q=Q,
        )

        # Store the result with parameters
        results.append({
            'total_duration': total_duration,
            'parameters': {
                'initial_pheromone': initial_pheromone,
                'num_ants': num_ants,
                'alpha': alpha,
                'beta': beta,
                'evap_coeff': evap_coeff,
                'Q': Q
            }
        })

    # Sort results by both total duration and mean duration
    results.sort(key=lambda x: (x['total_duration']))

    # Print sorted results
    for result in results[:10]:  # Show only the top 10 configurations
        params = result['parameters']
        formatted_duration = format_duration(result['total_duration'])
        print(f"Best Duration: {formatted_duration} | "
              f"Parameters: Initial Pheromone: {params['initial_pheromone']:.3f}, "
              f"Num Ants: {params['num_ants']}, Alpha: {params['alpha']:.3f}, Beta: {params['beta']:.3f}, "
              f"Evap Coeff: {params['evap_coeff']:.3f}, Q: {params['Q']:.3f}")

    return results

# Define parameter ranges for Random Search
def define_random_search_ranges(jobs):
    N = len(jobs)

    # Define parameter ranges
    param_ranges = {
        'initial_pheromones': (0.01, 10.0),  # τ₀ from 0.1 to 1.0
        'num_ants_list': (3, 2*N),  # Number of ants from 3 to N
        'alpha_values': (0.1, 5),  # Alpha (α) from 0.2 to 2
        'beta_values': (0.1, 5),  # Beta (β) from 0.2 to 1
        'evap_coeffs': (0.1, 0.9),  # Evaporation coefficient (ρ) from 0.1 to 0.9
        'Q_values': (0.1*N, 10*N)  # Q value scaled to the number of jobs
    }
    return param_ranges

def deep_random_search_ACO(jobs, workers, param_ranges, num_trials=100, max_iterations=100, inner_iterations=10, tolerance=1e-5, min_interval_width=1e-2, max_depth=10, log_file="deep_random_search_log.txt"):
    """
    Performs a Deep Random Search to fine-tune ACO parameters by recursively narrowing the search space.

    :param jobs: List of job objects.
    :param workers: List of worker objects.
    :param param_ranges: Dictionary containing initial ranges for parameters.
    :param num_trials: Number of random parameter sets to test in each iteration.
    :param max_iterations: Maximum number of iterations for each ACO run.
    :param inner_iterations: Number of iterations for find_optimal_path.
    :param tolerance: Convergence tolerance for each ACO run.
    :param min_interval_width: Minimum width of the parameter interval to stop recursion.
    :param max_depth: Maximum recursion depth to prevent infinite loops.
    :param log_file: Path to file where the results will be logged.
    :return: Best parameters and their corresponding total duration.
    """
    def recursive_random_search(param_ranges, depth=0):
        # Parameter name mapping
        param_mapping = {
            'initial_pheromones': 'initial_pheromone',
            'num_ants_list': 'num_ants',
            'alpha_values': 'alpha',
            'beta_values': 'beta', 
            'evap_coeffs': 'evap_coeff',
            'Q_values': 'Q'
        }
        
        # Perform Random Search in the current parameter ranges
        results = random_search_ACO(
            jobs=jobs,
            workers=workers,
            param_ranges=param_ranges,
            num_trials=num_trials,
            max_iterations=max_iterations,
            inner_iterations=inner_iterations,
            tolerance=tolerance
        )
        
        # Calculate the mean total duration across all trials
        total_durations = [r['total_duration'] for r in results]
        mean_duration = sum(total_durations) / len(total_durations)
        
        # Get the best result from the current Random Search
        best_result = results[0]
        best_duration = best_result['total_duration']
        best_params = best_result['parameters']

        # Format and log the best result and the mean duration for the current depth
        log_line = (f"Depth {depth}: Best Duration = {format_duration(best_duration)} | "
                    f"Mean Duration = {format_duration(mean_duration)}\nBest Parameters: {best_params}\n")
        with open(log_file, "a") as f:
            f.write(log_line)
        print(log_line)

        # Check if the interval width for all parameters is too small to continue
        interval_widths = {
            key: abs(param_ranges[key][1] - param_ranges[key][0])
            for key in param_ranges
        }
        
        if all(width < min_interval_width for width in interval_widths.values()):
            log_line = "Stopping recursion: Interval width for all parameters is too small.\n"
            with open(log_file, "a") as f:
                f.write(log_line)
            print(log_line)
            return best_params, best_duration

        # Also stop if maximum depth is reached
        if depth >= max_depth:
            log_line = f"Stopping recursion: Maximum depth of {max_depth} reached.\n"
            with open(log_file, "a") as f:
                f.write(log_line)
            print(log_line)
            return best_params, best_duration

        # Narrow the parameter ranges around the best candidate
        new_param_ranges = {}
        for key, (lower, upper) in param_ranges.items():
            mapped_key = param_mapping[key]
            best_value = best_params[mapped_key]
            if key == 'num_ants_list':  # Handle num_ants (integer) separately
                new_lower = max(int(best_value - (upper - lower) / 4), lower)
                new_upper = min(int(best_value + (upper - lower) / 4), upper)
                if new_lower == new_upper:  # Ensure the interval is at least 1
                    new_lower = max(new_lower - 1, lower)
                    new_upper = min(new_upper + 1, upper)
            else:
                new_lower = max(best_value - (upper - lower) / 4, lower)
                new_upper = min(best_value + (upper - lower) / 4, upper)
            new_param_ranges[key] = (new_lower, new_upper)
        
        log_line = f"New parameter ranges: {new_param_ranges}\n"
        with open(log_file, "a") as f:
            f.write(log_line)
        print(log_line)

        # Recursively call the function with the new parameter ranges
        return recursive_random_search(new_param_ranges, depth + 1)

    # Start the recursive search with the initial parameter ranges
    return recursive_random_search(param_ranges)

