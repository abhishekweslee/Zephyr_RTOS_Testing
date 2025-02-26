======================
ISR Execution Time Test
======================

**Test Case ID:** TZR014  
**Category:** Interrupt Handling  

Overview
--------
This test measures the execution time of an Interrupt Service Routine (ISR) in Zephyr RTOS.
It calculates the duration between triggering an interrupt and the ISR execution.

Key aspects tested:
- Accurate timing of ISR execution latency
- Proper interrupt configuration and handling
- Impact of CPU frequency on ISR timing

Prerequisites
-------------
- Serial and console outputs enabled (`CONFIG_SERIAL=y`, `CONFIG_STDOUT_CONSOLE=y`)
- Logging enabled with immediate mode (`CONFIG_LOG=y`, `CONFIG_LOG_MODE_IMMEDIATE=y`)
- Timer support enabled (`CONFIG_TIMER=y`)
- Valid IRQ line configured (`IRQ_LINE` in `main.c`)

Expected Output
---------------
- Startup logs display CPU frequency.
- ISR is triggered and executes as expected.
- ISR execution time is logged in nanoseconds.
- No unexpected failures or missed interrupts occur.

Sample Log
----------
.. code-block:: console

   Zephyr ISR Execution Time Test
   CPU Frequency: 64000000 Hz
   ISR Executed: end_time = 12345678
   ISR Execution Time: 3125 ns

Additional Notes
----------------
- Use different `IRQ_LINE` values to test various interrupts.
- Measure under different system loads to analyze jitter.
- Ensure hardware interrupt support for accurate testing.
