=======================
Timer Precision Validation
=======================

**Test Case ID:** TZR018  
**Category:** Timer Management  

Overview
--------
This test verifies the precision of one-shot and periodic timers in Zephyr RTOS.
It measures and compares the actual expiry times against expected values to ensure accurate timing under real-world conditions.

Key aspects tested:
- Accuracy of one-shot timer expirations
- Consistency of periodic timer intervals
- Impact of system load on timer precision

Prerequisites
-------------
- Timer support enabled (`CONFIG_TIMER=y`)
- Printing and logging enabled (`CONFIG_PRINTK=y`, `CONFIG_LOG=y`)

Expected Output
---------------
- One-shot timer expires close to the expected 1000 ms.
- Periodic timer triggers every 500 ms with minimal deviation.
- Logs detail expected vs. actual times for each expiry.
- Final log shows the total number of periodic expiries.

Sample Log
----------
.. code-block:: console

   Starting Timer Precision Test...
   One-shot timer started: 1000 ms timeout
   Periodic timer started: 500 ms period
   One-shot timer expired! Expected: 1000 ms, Actual: 1003 ms
   Periodic timer expired! Expected: 500 ms, Actual: 498 ms
   Periodic timer expired! Expected: 500 ms, Actual: 502 ms
   Periodic timer expired! Expected: 500 ms, Actual: 499 ms
   Test completed. Periodic timer triggered 5 times.

Additional Notes
----------------
- Modify `ONESHOT_TIMEOUT_MS` and `PERIODIC_TIMEOUT_MS` to test different intervals.
- Use timing analysis tools to validate consistency over extended durations.
- Consider testing under varying CPU loads to assess potential jitter effects.
