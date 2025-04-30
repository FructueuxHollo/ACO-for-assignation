import re
from datetime import datetime
from models.job import Job
from models.worker import Worker
from models.cpu import CPU
from models.match import Match

def create_jobs_from_df(df):
    jobs = []
    
    for index, row in df.iterrows():
        # Parse the processing durations for each PC
        standard_processing_durations = {
            'PC1': parse_time_to_seconds(row['Standard Processing Duration PC1']),
            'PC2': parse_time_to_seconds(row['Standard Processing Duration PC2']),
            'PC3': parse_time_to_seconds(row['Standard Processing Duration PC3']),
            'PC4': parse_time_to_seconds(row['Standard Processing Duration PC4']),
            'PC5': parse_time_to_seconds(row['Standard Processing Duration PC5']),
            'PC6': parse_time_to_seconds(row['Standard Processing Duration PC6']),
        }

        # Convert memory, disk sizes, and other attributes
        required_memory_size = parse_size(row['Required Memory Size For Execution'])
        required_disk_size = parse_size(row['Required Disk Size For Execution'])
        docker_file_size = parse_size(row['Docker File Size'])
        estimated_result_file_size = parse_size(row['Estimated Result File Size'])
        docker_file_gen_duration = parse_time_to_seconds(row['Docker File Generation Duration On Master PC'])

        # Create a Job object with the parsed values
        job = Job(
            ID = index,
            name=row['Job Name'],
            standard_processing_durations=standard_processing_durations,
            required_memory_size_for_execution=required_memory_size,
            required_disk_size_for_execution=required_disk_size,
            docker_file_size=docker_file_size,
            estimated_result_file_size=estimated_result_file_size,
            docker_file_generation_duration_on_master_pc=docker_file_gen_duration,
            thread_process_count=int(row['Thread Process Count'])
        )
        
        jobs.append(job)
    
    return jobs

# Helper function to parse sizes (e.g., GB, MB, KB) to bytes
def parse_size(size_str):
    size_str = size_str.lower()
    if 'gb' in size_str:
        return float(size_str.split('gb')[0].strip()) * 1024 * 1024 * 1024
    elif 'mb' in size_str:
        return float(size_str.split('mb')[0].strip()) * 1024 * 1024
    elif 'kb' in size_str:
        return float(size_str.split('kb')[0].strip()) * 1024
    elif 'b' in size_str:
        return float(size_str.split('b')[0].strip())
    return 0.0

# Helper function to parse time strings to seconds (e.g., HH:mm:ss)
def parse_time_to_seconds(time_str):
    time_parts = list(map(int, time_str.split(':')))
    return time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]

def create_workers_from_df(df):
    # List to store Worker objects
    workers = []
    
    for index, row in df.iterrows():
        # Create a new CPU object
        cpu_info = CPU(
            number_of_cores=int(row['Available CPU Core Number']),
            clock_rate_in_hz=convert_to_hz(row['CPU Clock Rate']),
            family_name=row['CPU Family Name'].strip(),
            denomination=row['CPU Denomination'].strip()
        )
    
        # Create a new Worker object
        worker = Worker(
            ID=index,
            cpu_info=cpu_info,
            available_memory_size=convert_to_bytes(row['Available Memory Size']),
            available_disk_size=convert_to_bytes(row['Available Disk Size']),
            connection_bandwidth_with_master_pc=convert_to_bytes(row['Connection Bandwidth With Master PC']),
            connection_delay_with_master_pc=convert_to_seconds(row['Connection Delay With Master PC']),
            name=row['Worker PC Name'].strip(),
            cpu_usage_in_percentage=0.0,
            current_global_cpu_time=0.0
        )
    
        # Add the worker to the list
        workers.append(worker)
        
    return workers
    
# Function to convert CPU clock rate from various formats to Hz
def convert_to_hz(value):
    value = value.lower().strip()
    if 'ghz' in value:
        return float(re.split(r"ghz", value)[0].strip()) * 1_000_000_000
    elif 'mhz' in value:
        return float(re.split(r"mhz", value)[0].strip()) * 1_000_000
    elif 'khz' in value:
        return float(re.split(r"khz", value)[0].strip()) * 1_000
    elif 'hz' in value:
        return float(re.split(r"hz", value)[0].strip())
    return float(value)

# Function to convert memory and disk size to bytes
def convert_to_bytes(value):
    value = value.lower().strip()
    if 'gb' in value:
        return float(re.split(r"gb", value)[0].strip()) * 1_073_741_824
    elif 'mb' in value:
        return float(re.split(r"mb", value)[0].strip()) * 1_048_576
    elif 'kb' in value:
        return float(re.split(r"kb", value)[0].strip()) * 1_024
    elif 'b' in value:
        return float(re.split(r"b", value)[0].strip())
    return float(value)

# Function to parse connection delay from time format to seconds
def convert_to_seconds(value):
    try:
        time_obj = datetime.strptime(value.strip(), '%H:%M:%S')
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    except ValueError:
        return float(value)

# def create_matches(jobs,workers,pheromone,VERBOSE = 0):
#     #list to create matches
#     matches = []
    
#     for job in jobs: 
#         for worker in workers:
#             # Check if the worker meets the conditions to handle the job
#             if worker.can_handle_job(job):
#                 match = Match(value=(job,worker),pheromone=pheromone)
#                 matches.append(match)
#                 # if VERBOSE:
#                 #     print(f"{job.name} {worker.name}")
#             else:
#                 if VERBOSE:
#                     print(f"{job.name} {worker.name} not possible")
#     return matches
def create_matches(jobs,workers,pheromone,VERBOSE = 0):
    #list to create matches
    matches = []
    for job in jobs: 
        for worker in workers:
            match = Match(value=(job,worker),pheromone=pheromone)
            matches.append(match)
    return matches
