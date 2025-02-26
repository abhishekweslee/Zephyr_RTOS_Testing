===============================
Code Execution Time Measurement
===============================

**Test Case ID:** TZR026  
**Category:** Timing and Profiling  

Overview
--------
This test measures the execution time of a code block in Zephyr RTOS using CPU cycle counters.
It calculates the number of cycles consumed by a simulated workload and converts the result to nanoseconds.

Key aspects tested:
- CPU cycle counting for precise timing measurements
- Conversion of cycles to real-time units (nanoseconds)
- Consistency of execution time under various conditions

Prerequisites
-------------
- Timing and cycle counting enabled (`CONFIG_TIMING_FUNCTIONS=y`)
- Thread monitoring and runtime statistics enabled
- Timeslicing enabled for accurate measurement under multi-threaded environments

Expected Output
---------------
- Startup logs indicate measurement initiation.
- Elapsed cycles and nanoseconds are displayed.
- Results are consistent across multiple runs unless influenced by system load.

Sample Log
----------
.. code-block:: console

   Starting execution time measurement...
   Elapsed cycles: 150000
   Elapsed time: 3750000 ns

Additional Notes
----------------
- Adjust the workload size to observe scaling in execution time.
- Test under different CPU frequencies to assess clock source impacts.
- Use Zephyr’s timing API for hardware-specific calibration.
