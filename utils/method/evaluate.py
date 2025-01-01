from utils.method.pheromone_update import calculate_worker_duration

def evaluate(jobs, matches):
    """
    Evaluates the matches to determine the optimal path with the minimum processing duration.
    
    :param jobs: List of jobs.
    :param matches: List of Match objects (job-worker pairs with pheromone and processing duration).
    :return: A tuple containing the optimal path and the total processing duration.
             The optimal path is a list of tuples (job, worker), and the total duration is an integer.
    """
    optimal_path = []
    worker_jobs = {}  # Dictionary to store jobs assigned to each worker

    # Build the optimal path by selecting the match with the highest pheromone level for each job
    for job in jobs:
        # Filter matches that correspond to the current job
        job_matches = [match for match in matches if match.value[0] == job]

        # Select the match with the highest pheromone level (most likely assignment)
        best_match = max(job_matches, key=lambda m: m.pheromone)

        # Add the job-worker pair to the optimal path
        worker = best_match.value[1]
        optimal_path.append((job, worker))

        # Store the job under the worker's list of jobs
        if worker not in worker_jobs:
            worker_jobs[worker] = []
        worker_jobs[worker].append(job)

    # Calculate the total processing duration based on the max worker processing duration
    total_processing_duration = 0
    for worker, assigned_jobs in worker_jobs.items():
        worker_duration = calculate_worker_duration(assigned_jobs, worker)
        total_processing_duration = max(total_processing_duration, worker_duration)

    return optimal_path, total_processing_duration
    
def format_duration(seconds):
    """
    Converts a duration from seconds to a string in the format of hours, minutes, and seconds.
    
    :param seconds: The total duration in seconds.
    :return: A string representing the duration in 'H hours M minutes S seconds' format.
    """
    hours, remainder = divmod(seconds, 3600)  # Get hours and the remainder seconds
    minutes, seconds = divmod(remainder, 60)  # Get minutes and remaining seconds

    # Build the formatted string
    duration_str = f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
    
    return duration_str
