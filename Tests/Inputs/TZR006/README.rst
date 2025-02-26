======================
Message Queue Handling
======================

**Test Case ID:** TZR006  
**Category:** Inter-task Communication  

Overview
--------
This test verifies message queue handling in Zephyr RTOS. It involves three sender tasks with different priorities
and a receiver task to validate correct message ordering and reception.

Key aspects tested:
- Priority-based message sending
- Correct message reception through queues
- Stability under concurrent sender tasks

Prerequisites
-------------
- Message queue support enabled (`CONFIG_PRINTK=y`, `CONFIG_SERIAL=y`)
- Logging enabled with default level (`CONFIG_LOG=y`, `CONFIG_LOG_DEFAULT_LEVEL=3`)

Expected Output
---------------
- "Starting Message Queue Priority Test" appears at startup.
- Sender tasks log each sent message ID along with their priority.
- Receiver logs the received messages, showing correct correspondence with sender priorities.

Sample Log
----------
.. code-block:: console

   Starting Message Queue Priority Test
   Sender Task (Priority -1): Sent Message ID 0
   Sender Task (Priority 0): Sent Message ID 0
   Sender Task (Priority 1): Sent Message ID 0
   Receiver: Received Message ID 0 from Priority -1
   Receiver: Received Message ID 0 from Priority 0
   Receiver: Received Message ID 0 from Priority 1
   Sender Task (Priority -1): Sent Message ID 1
   Receiver: Received Message ID 1 from Priority -1

Additional Notes
----------------
- Modify `MSGQ_SIZE` to test queue overflow conditions.
- Observe the effect of different sender sleep durations on message ordering.
- Ensure no messages are lost or received out of sequence.
