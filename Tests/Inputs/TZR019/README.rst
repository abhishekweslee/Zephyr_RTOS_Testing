===========================
Sleep & Delay Accuracy Test
===========================

**Test Case ID:** TZR019  
**Category:** Timing and Delays  

Overview
--------
This test validates the timing accuracy of Zephyr RTOS’s `k_sleep()` and `k_busy_wait()` functions.
It measures the actual elapsed time during both operations and compares it with the expected durations.

Key aspects tested:
- Accuracy of sleep-based delays (`k_sleep()`)
- Precision of busy-wait delays (`k_busy_wait()`)
- Impact of system load on delay accuracy

Prerequisites
-------------
- Serial output and printing enabled (`CONFIG_PRINTK=y`, `CONFIG_SERIAL=y`)

Expected Output
---------------
- `k_sleep()` delay closely matches the requested 1000 ms duration.
- `k_busy_wait()` delay is accurate within acceptable tolerance of 500000 µs.
- Logs display expected versus actual timings.

Sample Log
----------
.. code-block:: console

   Starting Sleep & Delay Accuracy Test...
   k_sleep() expected: 1000 ms, actual: 1002 ms
   k_busy_wait() expected: 500000 us, actual: 500300 us
   Test Completed.

Additional Notes
----------------
- Adjust `SLEEP_DURATION_MS` and `BUSY_WAIT_DURATION_US` to test different delay lengths.
- Run the test under various system loads to assess timing consistency.
- Use hardware-based timing tools for precise validation if available.
