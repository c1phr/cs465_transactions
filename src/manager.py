import multiprocessing
from multiprocessing import Manager as man
from random import randint
from src.barchart import barchart
import time
import threading


class Manager(object):
    """
    The Manager does exactly what would be expected. Only one exists per
    system, and it maintains an array of cubbyholes, an array of agents, and
    other information about system state.
    """
    def __init__(self, num_cubbies, initial_cubby_value, plot_val, locking_enabled=True, terminate_on="transactions", termination_point=10):
        # terminate_on specifies 'transactions' or 'time', and
        # termination_point specifies (depending on the value of
        # terminate_on) the number of transactions or seconds after which to
        # terminate. 

        self.locking_enabled = locking_enabled
        self.terminate_on = terminate_on
        self.num_procs = multiprocessing.cpu_count()
        self.num_cubbies = num_cubbies
        self.manager = man()
        self.termination_point = int(termination_point)
        self.lock = multiprocessing.Lock()
        self.plot = plot_val

        self.cubbyholes = self.manager.list()
        for cubby in range(num_cubbies):
            self.cubbyholes.append(int(initial_cubby_value))
        self.chart = barchart(self.cubbyholes)

    def run(self):
        agent_processes = []
        if self.terminate_on == "time":
            start_time = time.clock() # Get current time
            end_time = float(start_time) + float(self.termination_point)
            while time.clock() < end_time:
                for proc in range(self.num_procs):
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole)
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()
                    if self.plot:
                        self.chart.change_value(self.cubbyholes)
                        self.chart.make_barchart()

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()

        else:
            self.run_counter = 0
            while self.run_counter < self.termination_point:
                for proc in range(self.num_procs):
                    this_agent_process = multiprocessing.Process(target=self.modify_cubbyhole)
                    agent_processes.append(this_agent_process)
                    this_agent_process.start()
                    self.run_counter += 1
                    if self.plot:
                        self.chart.change_value(self.cubbyholes)
                        self.chart.make_barchart()

                # Make sure we wait for processes to finish before running again
                for elem in agent_processes:
                    proc = agent_processes.pop()
                    proc.join()


    def modify_cubbyhole(self, delta_upper_bound=10):
        # The calling process should indicate which cubbyholes to modify,
        # but the Agent will automatically select a value by which to change
        # the cubbyholes' values.
        if self.terminate_on != "time" and self.termination_point <= self.run_counter:
            # Since systems with more CPUs than the user selected executions will keep spawning processes,
            # double check to make sure that we don't do too many runs, break out if so
            return None
        cubby_a = randint(0, len(self.cubbyholes)-1) #cubby_array[randint(0, self.num_self.cubbyholes-1)]
        cubby_b = randint(0, len(self.cubbyholes)-1) #cubby_array[randint(0, self.num_self.cubbyholes-1)]
        delta_value_a = randint(0, delta_upper_bound)
        delta_value_b = delta_value_a * (-1)

        if self.locking_enabled:
            # Critical section
            self.lock.acquire()
            self.cubbyholes[cubby_a] += delta_value_a
            self.cubbyholes[cubby_b] += delta_value_b
            self.lock.release()

        else:
            # Change values without locking
            self.cubbyholes[cubby_a] += delta_value_a
            self.cubbyholes[cubby_b] += delta_value_b

        # Lock prints so the output doesn't get jumbled between processes
        self.lock.acquire()
        output = "["
        for cubby in self.cubbyholes:
            output += str(cubby) + ","
        output = output[:-1]
        output += "] -- Cubby sum: " + str(sum(self.cubbyholes))
        print(output)
        self.lock.release()