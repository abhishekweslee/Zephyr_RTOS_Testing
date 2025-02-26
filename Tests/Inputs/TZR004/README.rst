=====================
Task State Transitions
=====================

**Test Case ID:** TZR004  
**Category:** Task Management  

Overview
--------
This test ensures that tasks in Zephyr RTOS transition correctly through the states:
READY, RUNNING, BLOCKED, and SUSPENDED.

Key aspects tested:
- Semaphore-induced blocking and unblocking
- Thread suspension and resumption
- State consistency across varying priority tasks

Prerequisites
-------------
- Multithreading enabled (`CONFIG_MULTITHREADING=y`)
- Semaphore support enabled (`CONFIG_SEMAPHORE=y`)
- Thread naming and logging enabled (`CONFIG_THREAD_NAME=y`, `CONFIG_LOG=y`)

Expected Output
---------------
- "Starting Task State Transition Test..." appears at the beginning.
- Tasks log transitions through READY, RUNNING, BLOCKED, and SUSPENDED states.
- Medium priority task blocks while waiting for the semaphore.
- Low priority task suspends and resumes the medium priority task.
- Releasing the semaphore wakes up the medium priority task.

Sample Log
----------
.. code-block:: console

   [00:00:00.001,000] <inf> task_state_demo: Starting Task State Transition Test...
   [00:00:00.002,000] <inf> task_state_demo: High Priority Task: READY state
   [00:00:00.003,000] <inf> task_state_demo: Medium Priority Task: READY state
   [00:00:00.004,000] <inf> task_state_demo: Low Priority Task: READY state
   [00:00:00.505,000] <inf> task_state_demo: High Priority Task: RUNNING state
   [00:00:01.006,000] <inf> task_state_demo: Medium Priority Task: BLOCKED state (waiting for semaphore)
   [00:00:02.007,000] <inf> task_state_demo: Low Priority Task: SUSPENDING Medium Priority Task
   [00:00:04.009,000] <inf> task_state_demo: Low Priority Task: RESUMING Medium Priority Task
   [00:00:05.000,000] <inf> task_state_demo: Releasing Semaphore - Medium Priority Task will wake up
   [00:00:05.501,000] <inf> task_state_demo: Medium Priority Task: RUNNING state after unblocking

Additional Notes
----------------
- Vary semaphore release timings to observe prolonged BLOCKED states.
- Use thread analyzer tools to verify state changes beyond logs.
- Ensure no unintended deadlocks occur during suspension or blocking.
