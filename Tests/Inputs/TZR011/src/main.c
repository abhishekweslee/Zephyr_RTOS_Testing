#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <stdlib.h>

#define ALLOC_SIZE 256  // Allocate 256 bytes per block
#define NUM_BLOCKS 10   // Total number of allocations

void test_memory_fragmentation() {
    void *ptrs[NUM_BLOCKS];

    printk("Starting memory fragmentation test...\n");

    // Allocate memory blocks
    for (int i = 0; i < NUM_BLOCKS; i++) {
        ptrs[i] = malloc(ALLOC_SIZE);
        if (ptrs[i] == NULL) {
            printk("Allocation failed at block %d\n", i);
            return;
        }
        printk("Allocated block %d at address: %p\n", i, ptrs[i]);
    }

    // Free every other block to simulate fragmentation
    for (int i = 0; i < NUM_BLOCKS; i += 2) {
        free(ptrs[i]);
        ptrs[i] = NULL;  // Prevent use-after-free
        printk("Freed block %d\n", i);
    }

    // Try allocating a larger block to check fragmentation impact
    void *large_block = malloc(ALLOC_SIZE * 2);
    if (large_block) {
        printk("Successfully allocated large block at: %p\n", large_block);
        free(large_block);
    } else {
        printk("Large block allocation failed! Possible fragmentation.\n");
    }

    // Free remaining memory
    for (int i = 1; i < NUM_BLOCKS; i += 2) {
        free(ptrs[i]);
        ptrs[i] = NULL;  // Prevent use-after-free
        printk("Freed block %d\n", i);
    }

    printk("Memory fragmentation test completed.\n");
}

void main() {  // `void` is correct for Zephyr
    test_memory_fragmentation();
}
