#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <stdlib.h>

#define BLOCK_SIZE 256  // Allocate 256 bytes per block

void test_out_of_memory() {
    void *ptr;
    int count = 0;

    printk("Starting out-of-memory test...\n");

    while (1) {
        ptr = malloc(BLOCK_SIZE);
        if (ptr == NULL) {
            printk("Out of memory! Allocation failed after %d blocks.\n", count);
            break;
        }
        count++;
        printk("Allocated block %d at address: %p\n", count, ptr);
    }

    printk("Out-of-memory test completed.\n");
}

void main() {
    test_out_of_memory();
}
