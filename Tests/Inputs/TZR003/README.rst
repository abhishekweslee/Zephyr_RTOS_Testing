=====================
Context Switching Time
=====================

**Test Case ID:** TZR003  
**Category:** Task Management  

Overview
--------
This test validates the context switching time in Zephyr RTOS by measuring the cycles taken to switch between tasks of varying priorities (HIGH, MEDIUM, LOW).

Key aspects tested:
- Accurate measurement of context switch durations
- Impact of task priority on switching time
- Consistency under repeated measurements

Prerequisites
-------------
- Multithreading enabled (`CONFIG_MULTITHREADING=y`)
- Thread naming support (`CONFIG_THREAD_NAME=y`)
- Logging enabled with default level 3 (`CONFIG_LOG=y`, `CONFIG_LOG_DEFAULT_LEVEL=3`)

Expected Output
---------------
- "Starting Context Switching Test..." appears at the start.
- High, medium, and low priority tasks run, logging their activity.
- Context switch times are recorded and logged consistently.
- All measured times remain within acceptable limits.

Sample Log
----------
.. code-block:: console

   [00:00:00.001,000] <inf> context_switch: Starting Context Switching Test...
   [00:00:00.002,000] <inf> context_switch: High Priority Task Running
   [00:00:00.503,000] <inf> context_switch: Context switch time: 320 cycles
   [00:00:01.003,000] <inf> context_switch: High Priority Task Running
   [00:00:01.504,000] <inf> context_switch: Context switch time: 315 cycles
   [00:00:02.005,000] <inf> context_switch: Medium Priority Task Running
   [00:00:02.506,000] <inf> context_switch: Low Priority Task Running

Additional Notes
----------------
- Test under varying CPU loads to assess the effect on context switch time.
- Use cycle-to-time conversion based on the system clock to interpret results in microseconds.
- Consider capturing multiple data points for statistical analysis.
