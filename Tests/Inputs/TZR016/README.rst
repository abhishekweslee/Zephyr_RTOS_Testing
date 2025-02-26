======================
ISR Deadlock Detection
======================

**Test Case ID:** TZR016  
**Category:** Interrupt Handling  

Overview
--------
This test checks for potential deadlocks when executing an ISR in Zephyr RTOS.
By simulating a software interrupt, it ensures that ISR execution occurs without blocking the system.

Key aspects tested:
- ISR execution under software-triggered interrupts
- System stability during ISR execution
- Detection of potential deadlocks caused by interrupts

Prerequisites
-------------
- Software interrupt offloading enabled (`CONFIG_IRQ_OFFLOAD=y`)
- Assertions and timing configurations enabled
- Timeslicing active for fair thread scheduling

Expected Output
---------------
- ISR executes within the specified test duration.
- System logs confirm successful ISR execution without hanging.
- "Test passed" or "Test failed" indicates the outcome.

Sample Log
----------
.. code-block:: console

   Starting ISR deadlock test...
   Triggering software interrupt...
   ISR executed!
   Test passed: ISR executed without deadlock.

Additional Notes
----------------
- Modify `TEST_DURATION` to test different ISR response times.
- Introduce CPU stress to validate system stability under load.
- Ensure no critical sections within the ISR cause unintended blocking.
