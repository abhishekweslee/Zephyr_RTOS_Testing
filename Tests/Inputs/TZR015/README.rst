============================
Nested Interrupts Handling
============================

**Test Case ID:** TZR015  
**Category:** Interrupt Handling  

Overview
--------
This test validates the handling of nested interrupts in Zephyr RTOS.
Five interrupts (IRQ1 to IRQ5) are triggered sequentially, with each ISR initiating the next higher-priority interrupt.
The test ensures that higher-priority interrupts preempt lower-priority ones correctly.

Key aspects tested:
- Nested interrupt handling and priority-based preemption
- Correct execution order of ISR sequences
- System stability during deeply nested ISR execution

Prerequisites
-------------
- Serial and console output enabled (`CONFIG_SERIAL=y`, `CONFIG_PRINTK=y`)
- Interrupt offload support enabled (`CONFIG_IRQ_OFFLOAD=y`)
- Assertions enabled for error detection (`CONFIG_ASSERT=y`)
- Valid IRQ lines configured in hardware and code

Expected Output
---------------
- IRQs execute in the following order: IRQ1 → IRQ2 → IRQ3 → IRQ4 → IRQ5.
- Execution logs indicate proper nesting and priority handling.
- Final log confirms successful verification.

Sample Log
----------
.. code-block:: console

   Zephyr Nested IRQ Test with 5 Levels
   Triggering IRQ1...
   IRQ1 Executed, triggering IRQ2...
   IRQ2 Executed, triggering IRQ3...
   IRQ3 Executed, triggering IRQ4...
   IRQ4 Executed, triggering IRQ5...
   IRQ5 (Highest Priority) Executed
   Nested Interrupt Test Passed: Execution order verified.

Additional Notes
----------------
- Adjust priorities and observe changes in ISR execution order.
- Test under system load to analyze preemption delays.
- Monitor stack usage to prevent overflow with deep nesting.
