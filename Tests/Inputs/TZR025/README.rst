=========================================
Jitter Measurement Under High System Load
=========================================

**Test Case ID:** TZR025  
**Category:** Task Scheduling and Timing  

Overview
--------
This test evaluates how high system load affects the timing precision of periodic tasks in Zephyr RTOS.
It measures jitter—the difference between scheduled and actual task start times—while the system is under load.

Key aspects tested:
- Jitter measurement in high-load conditions
- Scheduler responsiveness under competing tasks
- Impact of task priorities and timeslicing

Prerequisites
-------------
- Timeslicing enabled (`CONFIG_TIMESLICING=y`)
- High-resolution clock configured (`CONFIG_SYS_CLOCK_TICKS_PER_SEC=1000`)
- Adequate stack sizes set for all tasks (`CONFIG_MAIN_STACK_SIZE=2048`)
- Printing enabled (`CONFIG_PRINTK=y`)

Expected Output
---------------
- The jitter task logs scheduled and actual start times with jitter values.
- Minimal jitter under light load and moderate jitter under high load.
- No missed deadlines or excessive jitter spikes occur.

Sample Log
----------
.. code-block:: console

   *** Zephyr Jitter Test with High System Load (Improved) ***
   Starting jitter measurement...

   Scheduled at: 1000 ms, Actual: 1002 ms, Jitter: 2 ms
   Scheduled at: 2000 ms, Actual: 2001 ms, Jitter: 1 ms
   Scheduled at: 3000 ms, Actual: 3007 ms, Jitter: 7 ms
   Scheduled at: 4000 ms, Actual: 4004 ms, Jitter: 4 ms

Additional Notes
----------------
- Increase `LOAD_ITERATIONS` to intensify system load.
- Modify `JITTER_TASK_PRIORITY` and `LOAD_TASK_PRIORITY` to study priority effects.
- Long-term tests can reveal how jitter evolves over extended periods.
