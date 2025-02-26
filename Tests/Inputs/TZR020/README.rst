=====================================
Resource Contention Simulation
=====================================

**Test Case ID:** TZR020  
**Category:** Synchronization  

Overview
--------
This test simulates resource contention between two threads accessing a shared resource protected by a mutex.
It ensures proper synchronization and verifies that mutual exclusion is maintained.

Key aspects tested:
- Mutex-based resource protection
- Prevention of simultaneous resource access
- Proper logging of thread access sequences

Prerequisites
-------------
- Threading support enabled (`CONFIG_THREAD_MONITOR=y`)
- Serial output enabled (`CONFIG_PRINTK=y`)

Expected Output
---------------
- Threads wait to acquire the resource without overlapping usage.
- Access and release logs follow a consistent sequence.
- No simultaneous resource access or deadlocks occur.

Sample Log
----------
.. code-block:: console

   Starting Resource Contention Simulation...
   Thread A: Waiting to acquire resource...
   Thread A: Acquired resource, working...
   Thread B: Waiting to acquire resource...
   Thread A: Releasing resource.
   Thread B: Acquired resource, working...
   Thread A: Waiting to acquire resource...
   Thread B: Releasing resource.

Additional Notes
----------------
- Adjust the thread delays to increase or reduce contention frequency.
- Add additional threads to observe behavior under high contention.
- Use priority settings to analyze priority inversion scenarios.
