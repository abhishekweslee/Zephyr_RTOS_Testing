========================================
Mutex Handling with Priority Inheritance
========================================

**Test Case ID:** TZR008  
**Category:** Inter-task Communication  

Overview
--------
This test demonstrates mutex handling in Zephyr RTOS and verifies the priority inheritance mechanism.
It ensures that a high-priority thread is not indefinitely blocked when a low-priority thread holds a mutex.

Key aspects tested:
- Mutex acquisition and release
- Priority inversion scenarios
- Effectiveness of priority inheritance

Prerequisites
-------------
- Mutex support enabled (`CONFIG_PRINTK=y`, `CONFIG_SERIAL=y`)
- Logging enabled (`CONFIG_LOG=y`, `CONFIG_LOG_DEFAULT_LEVEL=3`)

Expected Output
---------------
- "Mutex Test: Started" log message at initialization.
- Low-priority thread acquires the mutex first.
- High-priority thread attempts to acquire the mutex and is temporarily blocked.
- Priority inheritance boosts the low-priority thread’s execution priority to prevent delays.
- Medium-priority thread does not cause undue blocking of the high-priority thread.

Sample Log
----------
.. code-block:: console

   Mutex Test: Started
   [Low] Attempting to acquire mutex
   [Low] Acquired mutex
   [High] Attempting to acquire mutex
   [Medium] Running
   [Medium] Running
   [Low] Releasing mutex
   [High] Acquired mutex
   [High] Releasing mutex

Additional Notes
----------------
- Test with `CONFIG_MUTEX_PRIORITY_INHERITANCE=n` to observe priority inversion effects.
- Modify task sleep durations to stress different inversion scenarios.
- Monitor system response to ensure no deadlocks occur.
