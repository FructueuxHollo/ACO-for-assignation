def pheromone_update(ants, matches, evap_coeff, Q):
    """
    Updates the pheromone levels on the matches based on the ants' paths.

    :param ants: List of ants, where each ant has a path attribute (a list of job-worker tuples).
    :param matches: List of Match objects with pheromone levels to be updated.
    :param evap_coeff: Coefficient for pheromone evaporation (ρ).
    :param Q: Constant value for pheromone deposition.
    :return: Updated matches with new pheromone levels.
    """
    # Evaporate pheromones on all matches
    for match in matches:
        match.pheromone *= (1-evap_coeff)  # Apply evaporation to all pheromone values

    # Update pheromones based on each ant's path
    for ant in ants:
        l = max_worker_processing_duration(ant.path)  # Max processing duration across workers

        # Count the number of unique workers involved in the path
        unique_workers = set(worker for _, worker in ant.path)
        num_workers = len(unique_workers)

        # Calculate pheromone to deposit (Δτ_ij)
        # pheromone = Q / l # Inversely proportional to path length
        pheromone = Q / l * num_workers # Proportional to the number of workers and inversely proportional to path length

        for match in matches:
            if match.value in ant.path:  # Check if the job-worker pair was part of the ant's path
                match.pheromone += pheromone  # Add pheromone based on the ant's contribution                

    return matches



def pheromone_update_minmax(ants,
                            matches,
                            evap_coeff,
                            Q,
                            best_global_path,
                            best_global_length,
                            tau_min,
                            tau_max):
    """
    Mise à jour Min–Max + élitiste des phéromones.
    - matches : liste d’objets Match
    - ants : listes de fourmis
    - evap_coeff : ρ
    - Q : constante de dépôt
    - best_global_path : liste de (job,worker) de la meilleure solution vue
    - best_global_length : makespan de cette solution
    - tau_min, tau_max : bornes de clamp
    """
    # 1) Évaporation + clamp
    for m in matches:
        m.pheromone = (1 - evap_coeff) * m.pheromone
        m.pheromone = min(max(m.pheromone, tau_min), tau_max)

    # 2) Dépôt standard par chaque fourmi
    for ant in ants:
        Lk = max_worker_processing_duration(ant.path)
        num_workers = len({w for _, w in ant.path})
        delta = Q / Lk * num_workers

        for m in matches:
            if m.value in ant.path:
                m.pheromone += delta
                m.pheromone = min(max(m.pheromone, tau_min), tau_max)

    # # 3) Dépôt élitiste sur best_global_path
    # delta_elite = Q / best_global_length
    # for (job, worker) in best_global_path:
    #     # on trouve l’objet Match correspondant
    #     for m in matches:
    #         if m.value == (job, worker):
    #             m.pheromone += delta_elite
    #             m.pheromone = min(max(m.pheromone, tau_min), tau_max)
    #             break

    return matches

def init_min_max_pheromones(rho, best_length, n_decisions, p_best=0.05):
    """
    Calcule tau_max et tau_min selon Stützle & Hoos.
    n_decisions = nombre de choix (p.ex. len(jobs))
    p_best = probabilité de choisir la meilleure solution
    """
    tau_max = 1.0 / (rho * best_length)
    tau_min = (tau_max * (1 - p_best**(1/n_decisions))) / ((n_decisions/2 - 1) * p_best**(1/n_decisions))
    return tau_min, tau_max

def max_worker_processing_duration(path):
    """
    Calculates the maximum processing duration for any worker in the ant's path, 
    considering the worker's ability to run jobs simultaneously based on resource availability.
    
    :param path: A list of tuples (job, worker) representing the path of an ant.
    :return: The maximum processing duration across all workers.
    """
    # Dictionary to store jobs per worker, using worker.name as the key
    worker_jobs = {}

    # Group jobs by worker
    for job, worker in path:
        if worker.name not in worker_jobs:
            worker_jobs[worker.name] = {'worker': worker, 'jobs': []}  # Store worker object alongside jobs
        worker_jobs[worker.name]['jobs'].append(job)

    max_duration = 0

    # Evaluate the total processing duration per worker
    for worker_info in worker_jobs.values():
        worker = worker_info['worker']  # Get the worker object
        jobs = worker_info['jobs']  # Get the list of jobs
        worker_duration = calculate_worker_duration(jobs, worker)
        max_duration = max(max_duration, worker_duration)

    return max_duration

# def calculate_worker_duration(jobs, worker):
#     """
#     Calculates the total duration for a worker considering simultaneous job execution
#     based on the worker's available resources (memory, disk, CPU cores).
    
#     :param jobs: List of jobs assigned to the worker.
#     :param worker: The worker object with available resources (memory, disk, cores).
#     :return: The total time required for the worker to complete all jobs.
#     """
#     # Sort jobs by their processing duration as a heuristic to allocate resources efficiently
#     jobs = sorted(jobs, key=lambda job: job.standard_processing_durations[worker.name])

#     total_time = 0
#     # Initialize available resources for the worker
#     available_memory = worker.available_memory_size
#     available_disk = worker.available_disk_size
#     available_cores = worker.cpu_info.number_of_cores

#     # List of jobs that are executing in parallel with their remaining durations
#     executing_jobs = []

#     # List to track remaining job processing times
#     remaining_durations = {job: job.standard_processing_durations[worker.name] for job in jobs}

#     while jobs or executing_jobs:
#         # Try to allocate more jobs to be executed in parallel
#         remaining_jobs = []
#         for job in jobs:
#             # Check if the worker can handle this job along with the currently executing jobs
#             if (available_memory >= job.required_memory_size_for_execution and
#                 available_disk >= job.required_disk_size_for_execution and
#                 available_cores >= job.thread_process_count):
                
#                 # If the worker can handle this job, add it to the executing jobs
#                 executing_jobs.append(job)
#                 available_memory -= job.required_memory_size_for_execution
#                 available_disk -= job.required_disk_size_for_execution
#                 available_cores -= job.thread_process_count
#             else:
#                 # If the worker can't handle it, put it back in the remaining jobs
#                 remaining_jobs.append(job)

#         # If no jobs are currently executing, we advance time by the duration of the job that finishes next
#         if executing_jobs:
#             # Find the job with the shortest remaining processing time in the current executing jobs
#             min_duration = min(remaining_durations[job] for job in executing_jobs)
#             total_time += min_duration

#             # Remove completed jobs and update available resources
#             completed_jobs = []
#             for job in executing_jobs:
#                 remaining_durations[job] -= min_duration  # Reduce the remaining duration for this job
#                 if remaining_durations[job] == 0:  # Job has finished
#                     available_memory += job.required_memory_size_for_execution
#                     available_disk += job.required_disk_size_for_execution
#                     available_cores += job.thread_process_count
#                     completed_jobs.append(job)

#             # Remove completed jobs from the executing list
#             executing_jobs = [job for job in executing_jobs if job not in completed_jobs]

#         # Update the jobs list with the remaining jobs for the next iteration
#         jobs = remaining_jobs

#     return total_time

def calculate_worker_duration(jobs, worker):
    """
    Calculates the total duration for a worker considering simultaneous job execution
    based on the worker's available resources (memory, disk, CPU cores).
    
    :param jobs: List of jobs assigned to the worker.
    :param worker: The worker object with available resources (memory, disk, cores).
    :return: The total time required for the worker to complete all jobs.
    """
    # Sort jobs by their processing duration as a heuristic to allocate resources efficiently
    jobs = sorted(jobs, key=lambda job: job.standard_processing_durations[worker.name])

    total_time = 0
    # Initialize available resources for the worker
    # available_memory = 8.0 * 1024 * 1024 * 1024  # Example: 8 GB in bytes
    # available_disk = 64.0 * 1024 * 1024 * 1024  # Example: 64 GB in bytes
    available_memory = worker.available_memory_size
    available_disk = worker.available_disk_size
    available_cores = 20

    # List of jobs that are executing in parallel with their remaining durations
    executing_jobs = []

    # List to track remaining job processing times
    remaining_durations = {job: job.standard_processing_durations[worker.name] for job in jobs}

    while jobs or executing_jobs:
        # Try to allocate more jobs to be executed in parallel
        remaining_jobs = []
        for job in jobs:
            # Check if the worker can handle this job along with the currently executing jobs
            if (available_memory >= job.required_memory_size_for_execution and
                available_disk >= job.required_disk_size_for_execution and
                available_cores >= job.thread_process_count):
                
                # If the worker can handle this job, add it to the executing jobs
                executing_jobs.append(job)
                available_memory -= job.required_memory_size_for_execution
                available_disk -= job.required_disk_size_for_execution
                available_cores -= job.thread_process_count
            else:
                # If the worker can't handle it, put it back in the remaining jobs
                remaining_jobs.append(job)

        # If no jobs are currently executing, we advance time by the duration of the job that finishes next
        if executing_jobs:
            # Find the job with the shortest remaining processing time in the current executing jobs
            min_duration = min(remaining_durations[job] for job in executing_jobs)
            total_time += min_duration

            # Remove completed jobs and update available resources
            completed_jobs = []
            for job in executing_jobs:
                remaining_durations[job] -= min_duration  # Reduce the remaining duration for this job
                if remaining_durations[job] == 0:  # Job has finished
                    available_memory += job.required_memory_size_for_execution
                    available_disk += job.required_disk_size_for_execution
                    available_cores += job.thread_process_count
                    completed_jobs.append(job)

            # Remove completed jobs from the executing list
            executing_jobs = [job for job in executing_jobs if job not in completed_jobs]

        # Update the jobs list with the remaining jobs for the next iteration
        jobs = remaining_jobs

    return total_time