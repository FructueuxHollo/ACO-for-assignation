from threading import Thread
from copy import deepcopy
import time

class Job(Thread):  # Inherit from threading.Thread to make the class runnable
    def __init__(self, ID=0, standard_processing_durations=None, required_memory_size_for_execution=0.0, 
                 required_disk_size_for_execution=0.0, assigned_worker=None, job_current_cpu_time=0.0, 
                 docker_file_size=0.0, assignment_time=0, estimated_result_file_size=0.0, 
                 docker_file_generation_duration_on_master_pc=0.0, currently_being_processed_on_assigned_worker=False, 
                 thread_process_count=1, currently_assigned_to_worker=False, 
                 finished_being_processed_on_assigned_worker=False, name="", induced_cpu_usage_increase_percentage=0.0):
        super().__init__()
        self.ID = ID
        self.standard_processing_durations = standard_processing_durations or {}
        self.required_memory_size_for_execution = required_memory_size_for_execution
        self.required_disk_size_for_execution = required_disk_size_for_execution
        self.assigned_worker = assigned_worker
        self.job_current_cpu_time = job_current_cpu_time
        self.docker_file_size = docker_file_size
        self.assignment_time = assignment_time
        self.estimated_result_file_size = estimated_result_file_size
        self.docker_file_generation_duration_on_master_pc = docker_file_generation_duration_on_master_pc
        self.currently_being_processed_on_assigned_worker = currently_being_processed_on_assigned_worker
        self.thread_process_count = thread_process_count
        self.currently_assigned_to_worker = currently_assigned_to_worker
        self.finished_being_processed_on_assigned_worker = finished_being_processed_on_assigned_worker
        self.name = name
        self.induced_cpu_usage_increase_percentage = induced_cpu_usage_increase_percentage

    def duplicate(self, job):
        return deepcopy(self)

    def run(self):
        try:
            self.currently_being_processed_on_assigned_worker = True
            if self.assigned_worker:
                print(f"{self.assigned_worker.name}---<< {self.name} <<---")

                # Simulating processing time based on the assigned worker's CPU info
                family_name = self.assigned_worker.cpu_info['family_name']
                denomination = self.assigned_worker.cpu_info['denomination']
                cores = self.assigned_worker.cpu_info['number_of_cores']
                key = f"{family_name}-{denomination}-{cores}"

                # Sleep for the standard processing duration
                if key in self.standard_processing_durations:
                    processing_time = self.standard_processing_durations[key]
                    time.sleep(processing_time)

                # Processing complete
                self.finished_being_processed_on_assigned_worker = True
                self.currently_being_processed_on_assigned_worker = False
                print(f"{self.assigned_worker.name}--->> {self.name} >>---")

                # Update worker's resources after processing
                self.assigned_worker.assigned_jobs.remove(self)
                self.assigned_worker.available_disk_size += self.required_disk_size_for_execution
                self.assigned_worker.available_memory_size += self.required_memory_size_for_execution
                self.assigned_worker.cpu_usage_in_percentage -= self.induced_cpu_usage_increase_percentage

                # Reset job's worker assignment
                self.currently_assigned_to_worker = False
                self.assigned_worker = None

        except Exception as e:
            print(f"Job execution failed: {e}")

    def print(self):
        print("++++++++++ Job Details ++++++++++")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        for cpu, duration in self.standard_processing_durations.items():
            print(f"Standard Processing Duration On {cpu}: {duration}")
        print(f"Required Memory Size For Execution: {self.required_memory_size_for_execution}")
        print(f"Required Disk Size For Execution: {self.required_disk_size_for_execution}")
        print(f"Docker File Size: {self.docker_file_size}")
        print(f"Arrival Time: {self.assignment_time}")
        print(f"Thread Process Count: {self.thread_process_count}")
        print(f"Estimated Result File Size: {self.estimated_result_file_size}")
        print(f"Docker File Generation Duration On Master PC: {self.docker_file_generation_duration_on_master_pc}")
        print(f"Current CPU Time: {self.job_current_cpu_time}")
        print(f"Currently Assigned To Worker: {self.currently_assigned_to_worker}")
        print(f"Currently Being Processed On Assigned Worker: {self.currently_being_processed_on_assigned_worker}")
        print(f"Finished Being Processed On Assigned Worker: {self.finished_being_processed_on_assigned_worker}")
        if self.assigned_worker:
            print(f"Assigned Worker: {self.assigned_worker.name}")
        print("++++++++++ End ++++++++++\n\n")
