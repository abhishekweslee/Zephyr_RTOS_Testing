=========================
CPU Load Measurement Test
=========================

**Test Case ID:** TZR022  
**Category:** System Monitoring  

Overview
--------
This test measures CPU usage and task execution time using Zephyr’s runtime statistics.
Two load tasks continuously consume CPU cycles, while a monitor task prints CPU usage at regular intervals.

Key aspects tested:
- CPU load generation using busy loops
- Task execution time measurement with runtime statistics
- System responsiveness under varying load conditions

Prerequisites
-------------
- Thread runtime statistics enabled (`CONFIG_THREAD_RUNTIME_STATS=y`)
- Timing functions enabled (`CONFIG_TIMING_FUNCTIONS=y`)
- Printing enabled (`CONFIG_PRINTK=y`)

Expected Output
---------------
- Load tasks consume CPU resources as expected.
- Monitor task prints execution cycles every second.
- Higher cycle counts indicate increased CPU load.

Sample Log
----------
.. code-block:: console

   *** Booting Zephyr OS ***
   CPU Usage: 1500000 cycles
   CPU Usage: 1525000 cycles
   CPU Usage: 1498000 cycles

Additional Notes
----------------
- Increase `NUM_LOAD_TASKS` to observe higher CPU usage.
- Modify `MONITOR_INTERVAL_MS` for faster or slower monitoring rates.
- Ensure load tasks have lower priority than the monitor to prevent starvation.
