=============================
Memory Fragmentation Behavior
=============================

**Test Case ID:** TZR011  
**Category:** Memory Management  

Overview
--------
This test validates how Zephyr RTOS handles memory fragmentation. 
It simulates fragmentation by allocating and freeing memory blocks in a pattern, then attempts a larger allocation to assess impact.

Key aspects tested:
- Fragmentation impact on subsequent allocations
- System’s ability to handle non-contiguous free memory
- Memory cleanup and prevention of leaks

Prerequisites
-------------
- Heap memory pool enabled (`CONFIG_HEAP_MEM_POOL_SIZE=4096`)
- Newlib C library enabled (`CONFIG_NEWLIB_LIBC=y`, `CONFIG_MINIMAL_LIBC=n`)
- Standard output enabled (`CONFIG_PRINTK=y`, `CONFIG_STDOUT_CONSOLE=y`)

Expected Output
---------------
- Initial 256-byte blocks are allocated successfully.
- Every other block is freed to simulate fragmentation.
- Large 512-byte block allocation success or failure is logged.
- Remaining blocks are freed, ensuring no leaks.

Sample Log
----------
.. code-block:: console

   Starting memory fragmentation test...
   Allocated block 0 at address: 0x20000100
   Allocated block 1 at address: 0x20000200
   Allocated block 2 at address: 0x20000300
   Allocated block 3 at address: 0x20000400
   Allocated block 4 at address: 0x20000500
   Freed block 0
   Freed block 2
   Freed block 4
   Successfully allocated large block at: 0x20000600
   Freed block 1
   Freed block 3
   Memory fragmentation test completed.

Additional Notes
----------------
- Change `NUM_BLOCKS` or `ALLOC_SIZE` to explore fragmentation thresholds.
- Use external tools to monitor real-time heap usage.
- Test under long-term allocation/free cycles to assess fragmentation buildup.
