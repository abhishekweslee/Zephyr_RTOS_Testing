=========================================
Task Switching and Scheduling Policies
=========================================

**Test Case ID:** TZR002  
**Category:** Task Management  

Overview
--------
This test validates task switching and scheduling policies in Zephyr RTOS. 
It focuses on Round-Robin and Priority-based scheduling using three concurrent tasks with different priorities.

Key aspects tested:
- Priority preemption
- Round-Robin scheduling for equal-priority tasks
- Timeslicing behavior

Prerequisites
-------------
- Logging and printing enabled (`CONFIG_LOG=y`, `CONFIG_PRINTK=y`)
- Multiqueue scheduler and timeslicing enabled (`CONFIG_SCHED_MULTIQ=y`, `CONFIG_TIMESLICING=y`)
- Timeslice size set appropriately (e.g., `CONFIG_TIMESLICE_SIZE=10`)

Expected Output
---------------
- "Starting Task Scheduling Test..." appears at the beginning.
- High priority task runs more frequently.
- Tasks with the same priority rotate execution in a round-robin manner.
- Logs indicate consistent and fair scheduling.

Sample Log
----------
.. code-block:: console

   Starting Task Scheduling Test...
   Threads created, scheduling will now begin...
   High Priority Task Running
   Medium Priority Task Running
   High Priority Task Running
   Low Priority Task Running
   Medium Priority Task Running
   High Priority Task Running

Additional Notes
----------------
- Adjust timeslice sizes to observe different scheduling behaviors.
- Monitor for any unintended task starvation or missed executions.
- Validate system responsiveness under varying task loads.
