==========================
Dynamic Memory Allocation
==========================

**Test Case ID:** TZR010  
**Category:** Memory Management  

Overview
--------
This test verifies the dynamic memory allocation functionality in Zephyr RTOS.
It allocates memory, writes and verifies data, and ensures proper deallocation without leaks.

Key aspects tested:
- Successful memory allocation and deallocation
- Data integrity after writing and reading allocated memory
- Detection of allocation failures and handling

Prerequisites
-------------
- Heap memory pool enabled (`CONFIG_HEAP_MEM_POOL_SIZE=1024`)
- Standard library support (`CONFIG_NEWLIB_LIBC=y`)
- Aligned heap configuration (`CONFIG_NEWLIB_LIBC_ALIGNED_HEAP_SIZE=1024`)

Expected Output
---------------
- "Testing dynamic memory allocation..." log message.
- Successful allocation with memory address printed.
- Data written and verified without corruption.
- Memory freed with confirmation message.

Sample Log
----------
.. code-block:: console

   Testing dynamic memory allocation...
   Memory allocated at address: 0x20000abc
   Memory allocation and verification successful!
   Memory freed successfully.

Additional Notes
----------------
- Test edge cases by attempting to allocate more memory than available.
- Use tools to monitor heap usage and detect fragmentation.
- Vary `ALLOC_SIZE` to observe allocation limits and behavior.
