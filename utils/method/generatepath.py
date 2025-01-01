import random

def generate_paths(ants, jobs, matches, alpha, beta):
    for ant in ants:
        ant.path = []
        for job in jobs:
            matching_elements = [match for match in matches if match.value[0] == job]
            p = calculate_probabilities(matching_elements, alpha, beta)  # calculate probabilities (worker, probability)
            r = random.random()
            w = pick_worker(r, p)
            ant.path.append((job, w))  # append job-worker pair to the ant's path
    return ants

def calculate_probabilities(matches, alpha, beta):
    """
    Calculate the probability of selecting each worker for the given job.
    
    :param matches: List of Match objects where value[0] is the job and value[1] is the worker.
    :param alpha: Weight for pheromone importance.
    :param beta: Weight for processing duration (distance) importance.
    :return: List of tuples (worker, probability).
    """
    desirabilities = []
    total_desirability = 0

    # Calculate desirability for each match and sum them for normalization
    for match in matches:
        worker = match.value[1]  # worker is the second item in the tuple (job, worker)
        pheromone = match.pheromone
        processing_duration = match.processing_duration
        proximity = 1 / processing_duration  # Inverse of the distance is the proximity

        # Desirability formula: τ_ik^α * η_ik^β
        desirability = (pheromone ** alpha) * (proximity ** beta)
        desirabilities.append((worker, desirability))
        total_desirability += desirability

    # Normalize desirabilities to get probabilities
    probabilities = [(worker, desirability / total_desirability) for worker, desirability in desirabilities]

    return probabilities

def pick_worker(random_value, worker_probabilities):
    """
    Select a worker based on the calculated probabilities and a random value.
    
    :param random_value: Random number between 0 and 1.
    :param worker_probabilities: List of tuples (worker, probability).
    :return: The selected worker.
    """
    cumulative_prob = 0

    for worker, probability in worker_probabilities:
        cumulative_prob += probability
        if random_value <= cumulative_prob:
            return worker  # Return the exact worker when the random value falls within the cumulative probability

    return worker_probabilities[-1][0]  # Fallback to return the last worker in case of rounding issues
