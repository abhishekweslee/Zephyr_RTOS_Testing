===========================================
Task Starvation and Priority Inversion Test
===========================================

**Test Case ID:** TZR005  
**Category:** Task Management  

Overview
--------
This test validates the handling of task starvation and priority inversion scenarios in Zephyr RTOS. 
It involves three tasks with different priorities:
- High-priority task running periodically
- Medium-priority task interrupting execution
- Low-priority task holding a mutex

Key aspects tested:
- Priority inheritance during mutex acquisition
- Prevention of task starvation under resource contention
- Correct task execution order under varying priorities

Prerequisites
-------------
- Mutex support enabled (`CONFIG_SERIAL=y`, `CONFIG_PRINTK=y`)
- Logging enabled with default level (`CONFIG_LOG=y`, `CONFIG_LOG_DEFAULT_LEVEL=3`)

Expected Output
---------------
- "Starting Task Starvation & Priority Inversion Test" logs at initialization.
- Low-priority task acquires and releases the mutex as expected.
- High-priority task continues to execute with minimal blocking.
- Medium-priority task runs periodically without causing starvation.

Sample Log
----------
.. code-block:: console

   [00:00:00.001,000] <inf> task_starvation: Starting Task Starvation & Priority Inversion Test
   [00:00:00.002,000] <inf> task_starvation: Low-Priority Task: Trying to acquire Mutex
   [00:00:00.003,000] <inf> task_starvation: Low-Priority Task: Holding Mutex
   [00:00:00.105,000] <inf> task_starvation: High-Priority Task Running
   [00:00:00.605,000] <inf> task_starvation: Medium-Priority Task Running
   [00:00:03.004,000] <inf> task_starvation: Low-Priority Task: Releasing Mutex
   [00:00:03.105,000] <inf> task_starvation: High-Priority Task Running

Additional Notes
----------------
- Enable priority inheritance (`CONFIG_MUTEX_PRIORITY_INHERITANCE=y`) to mitigate inversion.
- Compare execution order with inheritance disabled to observe starvation effects.
- Adjust sleep durations to stress-test different priority levels.
