=====================
Semaphore Operations
=====================

**Test Case ID:** TZR007  
**Category:** Inter-task Communication  

Overview
--------
This test verifies the correct use of semaphores in Zephyr RTOS. Three threads compete for a single semaphore
ensuring only one thread accesses a critical section at a time.

Key aspects tested:
- Proper semaphore acquisition and release
- Prevention of simultaneous critical section access
- Fairness and avoidance of deadlocks or starvation

Prerequisites
-------------
- Semaphore support enabled (`CONFIG_PRINTK=y`, `CONFIG_SERIAL=y`)
- Logging enabled (`CONFIG_LOG=y`, `CONFIG_LOG_DEFAULT_LEVEL=3`)

Expected Output
---------------
- "Semaphore Test: Started" log message at initialization.
- Threads log attempts to acquire the semaphore.
- Only one thread logs "Acquired semaphore" at any time.
- Semaphore is always released before another thread acquires it.
- System remains deadlock-free and fair.

Sample Log
----------
.. code-block:: console

   [00:00:00.001,000] <inf> semaphore_test: Semaphore Test: Started
   [00:00:00.502,000] <inf> semaphore_test: Thread A: Attempting to acquire semaphore
   [00:00:00.503,000] <inf> semaphore_test: Thread A: Acquired semaphore
   [00:00:01.503,000] <inf> semaphore_test: Thread A: Released semaphore
   [00:00:01.504,000] <inf> semaphore_test: Thread B: Attempting to acquire semaphore
   [00:00:01.505,000] <inf> semaphore_test: Thread B: Acquired semaphore
   [00:00:02.505,000] <inf> semaphore_test: Thread B: Released semaphore
   [00:00:02.506,000] <inf> semaphore_test: Thread C: Attempting to acquire semaphore
   [00:00:02.507,000] <inf> semaphore_test: Thread C: Acquired semaphore
   [00:00:03.507,000] <inf> semaphore_test: Thread C: Released semaphore

Additional Notes
----------------
- Test with varied sleep durations to simulate different workloads.
- Increase semaphore token count to observe multi-thread access.
- Monitor for fair semaphore allocation across all threads.
