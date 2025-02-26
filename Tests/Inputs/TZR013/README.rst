==================================
Stack Overflow and Underflow Tests
==================================

**Test Case ID:** TZR013  
**Category:** Memory Management  

Overview
--------
This test validates the Zephyr RTOS mechanisms for detecting stack overflow and underflow conditions.
It intentionally causes both scenarios to ensure the system’s protection features respond correctly.

Key aspects tested:
- Hardware and software-based stack overflow detection
- Assertion-based detection of stack underflow
- Proper system response to illegal stack operations

Prerequisites
-------------
- Stack protection features enabled:
  - `CONFIG_TEST=y`
  - `CONFIG_THREAD_MONITOR=y`
  - `CONFIG_ASSERT=y`
  - `CONFIG_HW_STACK_PROTECTION=y`
  - `CONFIG_STACK_CANARIES=y`
  - `CONFIG_STACK_SENTINEL=y`
  - `CONFIG_NO_OPTIMIZATIONS=y`

Expected Output
---------------
- System detects overflow when the test thread exceeds its stack limit.
- Underflow triggers an assertion failure or system fault.
- Messages indicating overflow/underflow detection are logged.
- "This should never print!" lines are not displayed, confirming fault handling.

Sample Log
----------
.. code-block:: console

   Booting Zephyr Stack Overflow & Underflow Test...
   Starting Stack Overflow Test...
   *** Stack smashing detected ***
   *** Fault detected: Stack overflow on thread test_thread ***
   Starting Stack Underflow Test...
   *** Kernel panic: assertion failed at main.c: Stack underflow detected ***

Additional Notes
----------------
- Modify `STACK_SIZE` to test detection thresholds.
- Use Zephyr’s fault handlers to capture and log exceptions.
- Be aware that some hardware platforms may reboot on fault detection.
