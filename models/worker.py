from threading import Thread
from copy import deepcopy

class Worker:
    def __init__(self, ID=0, cpu_info=None, current_global_cpu_time=0.0, available_memory_size=0.0, 
                 available_disk_size=0.0, assigned_jobs=None, connection_bandwidth_with_master_pc=0.0, 
                 connection_delay_with_master_pc=0.0, cpu_usage_in_percentage=0.0, name="", 
                 original_available_memory_size=0.0, original_available_disk_size=0.0, 
                 original_connection_bandwidth_with_master_pc=0.0, original_connection_delay_with_master_pc=0.0):
        self.ID = ID
        self.cpu_info = cpu_info
        self.available_memory_size = available_memory_size
        self.available_disk_size = available_disk_size
        self.connection_bandwidth_with_master_pc = connection_bandwidth_with_master_pc
        self.connection_delay_with_master_pc = connection_delay_with_master_pc
        self.original_available_memory_size = original_available_memory_size
        self.original_available_disk_size = original_available_disk_size
        self.original_connection_bandwidth_with_master_pc = original_connection_bandwidth_with_master_pc
        self.original_connection_delay_with_master_pc = original_connection_delay_with_master_pc
        self.assigned_jobs = assigned_jobs if assigned_jobs is not None else []
        self.cpu_usage_in_percentage = cpu_usage_in_percentage
        self.name = name
        self.current_global_cpu_time = current_global_cpu_time
        self.base10_name = 0
    def duplicate(self):
        return deepcopy(self)

    def print(self):
        print("********** Worker PC Details **********")
        print(f"ID: {self.ID}")
        print(f"Name: {self.name}")
        print(f"Current Global CPU Time: {self.current_global_cpu_time}")
        print(f"CPU Number Of Cores: {self.cpu_info.number_of_cores}")
        print(f"CPU Clock Rate In GHz: {self.cpu_info.clock_rate_in_hz / 1_000_000_000}")
        print(f"CPU Name: {self.cpu_info.family_name} {self.cpu_info.denomination}")
        print(f"Available Memory Size: {self.available_memory_size}")
        print(f"Available Disk Size: {self.available_disk_size}")
        print(f"Connection Bandwidth With Master PC: {self.connection_bandwidth_with_master_pc}")
        print(f"Connection Delay With Master PC: {self.connection_delay_with_master_pc}")
        print(f"CPU Usage In Percentage: {self.cpu_usage_in_percentage}")
        print("----- Assigned Jobs -----")
        for job in self.assigned_jobs:
            print(f"Job Name: {job.name}")
        print("********** End **********\n\n")

    def can_handle_job(self, job):
        if self.available_memory_size < job.required_memory_size_for_execution:
            return False
        if self.available_disk_size < job.required_disk_size_for_execution:
            return False
        if self.cpu_info.number_of_cores < job.thread_process_count:
            return False
        return True

    def reset_resource_usage(self, job):
        self.cpu_usage_in_percentage = 0.0
        self.available_disk_size += job.required_disk_size_for_execution
        self.available_memory_size += job.required_memory_size_for_execution

    def execute_job(self, job):
        job_execution_thread = Thread(target=job.run)
        job_execution_thread.start()
