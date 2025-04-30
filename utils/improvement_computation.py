import re

def hms_to_seconds(time_str):
  """Converts HH:MM:SS string to total seconds."""
  # Use regex to handle potential variations or ensure format
  match = re.match(r'(\d{1,2}):(\d{2}):(\d{2})', time_str)
  if not match:
      raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM:SS")
  h, m, s = map(int, match.groups())
  if m >= 60 or s >= 60:
       raise ValueError(f"Invalid time values: {time_str}. Minutes/seconds cannot be >= 60")
  return h * 3600 + m * 60 + s

def seconds_to_hms(seconds):
  """Converts total seconds to HH:MM:SS string."""
  if seconds < 0:
      sign = "-"
      seconds = abs(seconds)
  else:
      sign = ""

  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  secs = seconds % 60
  # Use f-string formatting for zero-padding
  return f"{sign}{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"

def calculate_improvement(time_str_initial, time_str_improved):
  """
  Calculates the improvement between two makespan times.

  Args:
    time_str_initial: The initial makespan time (e.g., Local Search) in HH:MM:SS format.
    time_str_improved: The improved makespan time (e.g., Proposal ACO) in HH:MM:SS format.

  Returns:
    A tuple containing:
      - improvement_time_str: The time difference (initial - improved) in HH:MM:SS format.
      - improvement_percentage: The percentage improvement relative to the initial time.
                                Returns None if the initial time is zero.
    Returns None if there's an error during conversion.
  """
  try:
    seconds_initial = hms_to_seconds(time_str_initial)
    seconds_improved = hms_to_seconds(time_str_improved)

    improvement_seconds = seconds_initial - seconds_improved
    improvement_time_str = seconds_to_hms(improvement_seconds)

    if seconds_initial == 0:
      # Avoid division by zero. Percentage is undefined or could be considered infinite
      # if improved is also 0, or 0% if improved > 0. Let's return None.
      improvement_percentage = None
    else:
      improvement_percentage = (improvement_seconds / seconds_initial) * 100

    return improvement_time_str, improvement_percentage

  except ValueError as e:
    print(f"Error: {e}")
    return None, None # Indicate error

# --- Example Usage with data from the table ---

ls_times = ["00:54:21", "01:13:36", "01:41:41", "02:00:07", "02:27:37", "02:50:48", "03:14:58", "03:34:57", "04:00:00"]
aco_times = ["00:36:09", "00:44:09", "00:53:47", "01:04:41", "01:17:54", "01:25:53", "01:44:24", "02:00:12", "02:09:07"]
num_jobs = [18, 27, 36, 45, 54, 63, 72, 81, 90]

print("Calculating Improvements:")
print("-" * 30)

for i in range(len(num_jobs)):
  ls_time = ls_times[i]
  aco_time = aco_times[i]
  jobs = num_jobs[i]

  print(f"Case: {jobs} Jobs")
  print(f"  Local Search: {ls_time}")
  print(f"  Proposal (ACO): {aco_time}")

  improvement_time, improvement_perc = calculate_improvement(ls_time, aco_time)

  if improvement_time is not None:
    print(f"  Improvement: {improvement_time} ({improvement_perc:.2f}%)")
  else:
    print("  Could not calculate improvement.")
  print("-" * 30)

# --- Example with no improvement (or worsening) ---
print("Case: Worsening Example")
time1 = "00:10:00"
time2 = "00:12:30"
print(f"  Initial Time: {time1}")
print(f"  'Improved' Time: {time2}")
imp_time, imp_perc = calculate_improvement(time1, time2)
if imp_time is not None:
    print(f"  Improvement: {imp_time} ({imp_perc:.2f}%)") # Note the negative values
print("-" * 30)