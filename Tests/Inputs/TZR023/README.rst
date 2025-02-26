========================================================
Task Execution Time Profiling Under Varying Conditions
========================================================

**Test Case ID:** TZR023  
**Category:** Task Scheduling and Profiling  

Overview
--------
This test measures the execution times of multiple tasks with varying workloads in Zephyr RTOS.
Tasks with low, medium, and high computational loads are executed concurrently, and their execution cycles are logged.
A monitor task provides periodic system status updates.

Key aspects tested:
- Task execution time measurement under different load conditions
- Scheduler behavior with tasks of varying priorities and loads
- Impact of task workload intensity on execution time

Prerequisites
-------------
- Thread runtime statistics enabled (`CONFIG_THREAD_RUNTIME_STATS=y`)
- Timing functions enabled (`CONFIG_TIMING_FUNCTIONS=y`)
- Printing enabled (`CONFIG_PRINTK=y`)

Expected Output
---------------
- Tasks log their execution times every 500 ms.
- High-load tasks have longer execution cycles compared to low-load tasks.
- Monitor task logs system status every 2 seconds.

Sample Log
----------
.. code-block:: console

   *** Booting Zephyr OS: Task Execution Profiling ***
   Low Load Task executed in 50000 cycles
   Medium Load Task executed in 120000 cycles
   High Load Task executed in 300000 cycles
   [Monitor] System running...
   Low Load Task executed in 48000 cycles
   Medium Load Task executed in 118000 cycles
   High Load Task executed in 305000 cycles

Additional Notes
----------------
- Increase `LOAD_ITERATIONS` to stress the system further.
- Observe the effect of task priorities on scheduling and execution times.
- Use hardware performance monitors for cross-validation of timing data.
