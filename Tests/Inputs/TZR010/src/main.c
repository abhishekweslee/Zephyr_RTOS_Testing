#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define ALLOC_SIZE 64  // Size of memory to allocate

void test_dynamic_memory(void)
{
    printk("Testing dynamic memory allocation...\n");

    // Allocate memory using k_malloc
    uint8_t *mem_block = k_malloc(ALLOC_SIZE);

    if (mem_block == NULL) {
        printk("Memory allocation failed!\n");
        return;
    }

    printk("Memory allocated at address: %p\n", mem_block);

    // Write data to allocated memory
    for (int i = 0; i < ALLOC_SIZE; i++) {
        mem_block[i] = i;
    }

    // Read and verify data
    for (int i = 0; i < ALLOC_SIZE; i++) {
        if (mem_block[i] != i) {
            printk("Memory corruption detected at index %d!\n", i);
            return;
        }
    }

    printk("Memory allocation and verification successful!\n");

    // Free allocated memory
    k_free(mem_block);
    printk("Memory freed successfully.\n");
}

void main(void)
{
    test_dynamic_memory();
}
