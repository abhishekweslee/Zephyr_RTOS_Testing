=========================================
Periodic Task Deadline Adherence Check
=========================================

**Test Case ID:** TZR024  
**Category:** Task Scheduling and Timing  

Overview
--------
This test assesses how well a periodic task in Zephyr RTOS meets its deadlines.
It measures jitter (the deviation from the expected start time) and identifies any missed deadlines.

Key aspects tested:
- Periodic scheduling accuracy
- Jitter measurement between expected and actual start times
- Deadline adherence under various system conditions

Prerequisites
-------------
- Timing functions enabled (`CONFIG_TIMING_FUNCTIONS=y`)
- Console and UART output enabled for logging
- Thread monitoring and logging configurations set

Expected Output
---------------
- Task starts approximately at the expected periodic intervals.
- Jitter remains minimal under light system loads.
- "Missed deadline" logs indicate cases where the task couldn't start on time.

Sample Log
----------
.. code-block:: console

   Starting periodic task for deadline adherence check...
   Task started at 1000 ms (Jitter: 2 ms)
   Task completed at 1200 ms, execution time: 200 ms
   Task started at 2000 ms (Jitter: 1 ms)
   Task completed at 2200 ms, execution time: 200 ms
   Missed deadline by 15 ms!

Additional Notes
----------------
- Modify the `PERIOD_MS` and workload duration to explore deadline margins.
- Introduce competing tasks to analyze scheduling robustness.
- Monitor jitter trends over extended periods for stability assessments.
