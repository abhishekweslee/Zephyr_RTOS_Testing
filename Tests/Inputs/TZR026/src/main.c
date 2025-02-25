#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/arch/cpu.h>  // For cycle counting functions

void main(void) {
    printk("Starting execution time measurement...\n");

    // Read the start cycle count
    uint32_t start_cycles = k_cycle_get_32();

    // Code block to measure
    for (volatile int i = 0; i < 100000; i++) {
        // Simulated workload
    }

    // Read the end cycle count
    uint32_t end_cycles = k_cycle_get_32();

    // Calculate elapsed cycles
    uint32_t elapsed_cycles = end_cycles - start_cycles;

    // Convert cycles to nanoseconds
    uint64_t elapsed_ns = k_cyc_to_ns_floor64(elapsed_cycles);

    printk("Elapsed cycles: %u\n", elapsed_cycles);
    printk("Elapsed time: %llu ns\n", elapsed_ns);
}
