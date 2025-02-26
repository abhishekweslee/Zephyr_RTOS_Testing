=========================================
Concurrent Access with and without Mutex
=========================================

**Test Case ID:** TZR021  
**Category:** Synchronization and Concurrency  

Overview
--------
This test compares concurrent access to a shared resource using two methods:
1. Without synchronization (unsafe access), leading to potential data races.
2. With mutex protection (safe access), ensuring data integrity.

Key aspects tested:
- Data consistency with concurrent resource access
- Effectiveness of mutex protection against race conditions
- Comparison of unsafe vs. safe access methods

Prerequisites
-------------
- Threading support enabled (`CONFIG_THREAD_NAME=y`)
- Assertions enabled for error detection (`CONFIG_ASSERT=y`)
- Printing enabled for runtime logs (`CONFIG_PRINTK=y`)

Expected Output
---------------
- Unsafe access shows overlapping updates and inconsistent `shared_resource` values.
- Safe access ensures correct, sequential increments.
- Final `shared_resource` matches the expected total increments.

Sample Log
----------
.. code-block:: console

   Starting Concurrent Access Test...
   Unsafe: Thread A updated shared_resource to 1
   Unsafe: Thread B updated shared_resource to 2
   Unsafe: Thread A updated shared_resource to 2  # Overlap detected
   Safe: Thread C updated shared_resource to 11
   Safe: Thread D updated shared_resource to 12
   Final shared_resource value: 20
   Test Completed.

Additional Notes
----------------
- Modify `ITERATIONS` and thread delays to test various concurrency scenarios.
- Observe logs to identify data races in unsafe access.
- Use priority inheritance features to mitigate potential priority inversion.
