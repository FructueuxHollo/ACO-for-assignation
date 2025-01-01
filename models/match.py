class Match:
    def __init__(self, value, pheromone):
        self.value = value  # value is expected to be a tuple (job, worker)
        self.pheromone = pheromone
        self.processing_duration = self.calculate_processing_duration()

    def calculate_processing_duration(self):
        job, worker = self.value
        # Use the worker's name (e.g., 'PC1') to get the correct duration from the job's dictionary
        return job.standard_processing_durations[worker.name]  # Assume worker has an 'name' or identifier like 'PC1'
