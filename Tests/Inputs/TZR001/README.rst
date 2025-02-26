===============================
Task Creation, Deletion, and Priority Assignment
===============================

**Test Case ID:** TZR001  
**Category:** Task Management  

Overview
--------
This test verifies task management in Zephyr RTOS, specifically focusing on:

- Task creation
- Task deletion
- Priority assignment

Three threads with different priorities (HIGH, MEDIUM, LOW) are created, executed, and deleted.  
The test ensures that the threads execute in the correct order based on priority and are properly cleaned up.

Prerequisites
-------------
- Zephyr RTOS environment set up
- Logging enabled (`CONFIG_LOG=y`)
- Thread monitoring and naming enabled (`CONFIG_THREAD_MONITOR=y`, `CONFIG_THREAD_NAME=y`)

Building and Running
--------------------
1. Build the project:
   .. code-block:: bash

      west build -b <your_board> -s . -d build

2. Flash the firmware:
   .. code-block:: bash

      west flash -d build

3. Monitor the logs:
   .. code-block:: bash

      west log -d build

Expected Output
---------------
- "Task Management Test Started" log message.
- Threads start with the following priorities:
  - Thread 1: HIGH priority
  - Thread 2: MEDIUM priority
  - Thread 3: LOW priority
- Each thread runs for 2 seconds and logs exit messages.
- Threads are deleted with corresponding log confirmations.
- "Task Management Test Completed" appears at the end.

Sample Log
----------
.. code-block:: console

   [00:00:00.001,000] <inf> task_mgmt: Task Management Test Started
   [00:00:00.002,000] <inf> task_mgmt: Thread 1 started with HIGH priority
   [00:00:00.003,000] <inf> task_mgmt: Thread 2 started with MEDIUM priority
   [00:00:00.004,000] <inf> task_mgmt: Thread 3 started with LOW priority
   [00:00:02.002,000] <inf> task_mgmt: Thread 1 exiting...
   [00:00:02.003,000] <inf> task_mgmt: Thread 2 exiting...
   [00:00:02.004,000] <inf> task_mgmt: Thread 3 exiting...
   [00:00:03.000,000] <inf> task_mgmt: Deleting Thread 1...
   [00:00:03.001,000] <inf> task_mgmt: Deleting Thread 2...
   [00:00:03.002,000] <inf> task_mgmt: Deleting Thread 3...
   [00:00:03.003,000] <inf> task_mgmt: Task Management Test Completed

Additional Notes
----------------
- Test different priority combinations to ensure correct scheduling.
- Use Zephyr's thread analyzer to verify no stack overflows occur.
- Ensure proper cleanup to avoid memory/resource leaks.
