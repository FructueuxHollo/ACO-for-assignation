from copy import deepcopy

class CPU:
    def __init__(self, number_of_cores=0, clock_rate_in_hz=0.0, family_name='', denomination=''):
        """
        Initializes a new CPU with the given parameters.
        """
        self.number_of_cores = number_of_cores
        self.clock_rate_in_hz = clock_rate_in_hz
        self.family_name = family_name
        self.denomination = denomination

    def duplicate(self):
        """
        Creates and returns a deep copy of this CPU.
        """
        return deepcopy(self)

    def outperforms(self, cpu_to_compare_with, multithreaded_program_execution):
        """
        Returns True if this CPU outperforms the one passed in as a parameter for the specified type of program.
        """

        # Priority mapping for CPU families and denominations
        cpu_hierarchy = {
            'core i9': 4,
            'core i7': 3,
            'core i5': 2,
            'core i3': 1
        }

        # Determine the CPU type
        this_cpu_type = f"{self.family_name} {self.denomination}".lower()
        other_cpu_type = f"{cpu_to_compare_with.family_name} {cpu_to_compare_with.denomination}".lower()

        # Compare based on family/denomination hierarchy
        this_priority = cpu_hierarchy.get(this_cpu_type, 0)
        other_priority = cpu_hierarchy.get(other_cpu_type, 0)

        if this_priority != other_priority:
            return this_priority > other_priority

        # If the same family, compare based on multithread or single-thread performance
        if multithreaded_program_execution:
            return self.number_of_cores > cpu_to_compare_with.number_of_cores
        else:
            return self.clock_rate_in_hz > cpu_to_compare_with.clock_rate_in_hz

    def __eq__(self, other):
        """
        Compares if two CPU objects are equivalent in terms of performance.
        This allows using '==' for CPU objects.
        """
        if not isinstance(other, CPU):
            return NotImplemented
        return (self.family_name == other.family_name and
                self.denomination == other.denomination and
                self.number_of_cores == other.number_of_cores and
                self.clock_rate_in_hz == other.clock_rate_in_hz)
