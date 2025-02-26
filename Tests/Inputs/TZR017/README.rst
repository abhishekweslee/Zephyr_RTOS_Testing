======================================
Timer Creation, Deletion & Expiry Test
======================================

**Test Case ID:** TZR017  
**Category:** Timer Management  

Overview
--------
This test verifies the functionality of timers in Zephyr RTOS, focusing on their creation, expiration, and deletion.
It ensures that timers trigger callbacks at expected intervals and stop without issues.

Key aspects tested:
- Timer initialization and callback registration
- Accurate timer expiry handling
- Proper stopping and cleanup of timers

Prerequisites
-------------
- Serial and console output enabled (`CONFIG_SERIAL=y`, `CONFIG_PRINTK=y`)
- Timer support enabled (`CONFIG_TIMER=y`)

Expected Output
---------------
- Timer initializes and starts with correct timeout and period values.
- Expiry callback executes at the expected time.
- Logs confirm successful execution and stopping of the timer.

Sample Log
----------
.. code-block:: console

   Starting Timer Creation, Deletion & Expiry Test...
   Timer initialized successfully.
   Timer started: 1000 ms timeout, 500 ms period.
   Timer expired! Callback executed.
   Test Passed: Timer expired as expected.
   Timer stopped and deleted.

Additional Notes
----------------
- Test different configurations by changing `TIMER_DURATION_MS` and `TIMER_PERIOD_MS`.
- Use periodic mode for repeated expiry validation.
- Monitor for any missed expiries or timing inconsistencies under system load.
