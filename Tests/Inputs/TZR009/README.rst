======================
Event Flags Signalling
======================

**Test Case ID:** TZR009  
**Category:** Inter-task Communication  

Overview
--------
This test verifies the correct signaling and reception of event flags in Zephyr RTOS.
It demonstrates synchronization between a producer and consumer task using `k_event` APIs.

Key aspects tested:
- Proper setting and waiting for event flags
- Task synchronization using event flags
- Correct bitwise event flag reception

Prerequisites
-------------
- Event support enabled (`CONFIG_EVENTS=y`)
- Printing enabled (`CONFIG_PRINTK=y`)

Expected Output
---------------
- Producer sets `EVENT_FLAG_1` and `EVENT_FLAG_2` sequentially.
- Consumer waits and logs the reception of each flag.
- Received flags match the expected bit values.

Sample Log
----------
.. code-block:: console

   Waiting for EVENT_FLAG_1...
   Setting EVENT_FLAG_1
   Received EVENT_FLAG_1: 0x1
   Waiting for EVENT_FLAG_2...
   Setting EVENT_FLAG_2
   Received EVENT_FLAG_2: 0x2

Additional Notes
----------------
- Increase the number of consumer threads to test event broadcasting.
- Adjust delays between flag settings to test synchronization under varying conditions.
- Verify flags with combined bitmask operations for multiple events.
