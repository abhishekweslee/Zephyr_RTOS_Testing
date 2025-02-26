=====================
Out-of-Memory Handling
=====================

**Test Case ID:** TZR012  
**Category:** Memory Management  

Overview
--------
This test evaluates how Zephyr RTOS handles out-of-memory conditions.
It continuously allocates memory until no more heap space is available, ensuring graceful failure handling.

Key aspects tested:
- Detection of heap exhaustion
- Proper logging when allocations fail
- System stability after memory exhaustion

Prerequisites
-------------
- Heap memory pool enabled (`CONFIG_HEAP_MEM_POOL_SIZE=4096`)
- Newlib C library enabled (`CONFIG_NEWLIB_LIBC=y`)

Expected Output
---------------
- Blocks are allocated successfully until heap is exhausted.
- Allocation failure logs the total successful allocations.
- No system crashes or unexpected behavior occur.

Sample Log
----------
.. code-block:: console

   Starting out-of-memory test...
   Allocated block 1 at address: 0x20000100
   Allocated block 2 at address: 0x20000200
   Allocated block 3 at address: 0x20000300
   Allocated block 4 at address: 0x20000400
   Allocated block 5 at address: 0x20000500
   Out of memory! Allocation failed after 5 blocks.
   Out-of-memory test completed.

Additional Notes
----------------
- Modify `BLOCK_SIZE` and `CONFIG_HEAP_MEM_POOL_SIZE` to test various scenarios.
- Verify system recovery and responsiveness after hitting out-of-memory conditions.
- Use heap monitoring tools to visualize memory consumption.
