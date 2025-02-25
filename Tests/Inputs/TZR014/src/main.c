#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/irq.h>
#include <zephyr/arch/arm/cortex_m/nvic.h>

#define IRQ_LINE 5  // Ensure this IRQ is valid for your board
#define IRQ_PRIORITY 1

volatile uint32_t start_time, end_time;
volatile bool isr_executed = false;

void test_isr(void *arg) {
    ARG_UNUSED(arg);
    end_time = k_cycle_get_32();  // Capture end time
    isr_executed = true;
    printk("ISR Executed: end_time = %u\n", end_time);
}

int main(void) {
    printk("Zephyr ISR Execution Time Test\n");

    uint32_t cpu_freq = sys_clock_hw_cycles_per_sec();
    if (cpu_freq == 0) {
        printk("Error: Invalid CPU frequency!\n");
        return -1;
    }
    printk("CPU Frequency: %u Hz\n", cpu_freq);

    // Connect the interrupt handler
    IRQ_CONNECT(IRQ_LINE, IRQ_PRIORITY, test_isr, NULL, 0);
    irq_enable(IRQ_LINE);

    start_time = k_cycle_get_32();  // Capture start time
    NVIC_SetPendingIRQ(IRQ_LINE);   // Trigger the ISR

    // Wait until ISR is executed
    while (!isr_executed) {
        k_yield();
    }

    uint64_t execution_time_ns = ((uint64_t)(end_time - start_time) * 1000000000) / cpu_freq;
    printk("ISR Execution Time: %llu ns\n", execution_time_ns);

    irq_disable(IRQ_LINE);  // Disable IRQ after measurement
    return 0;
}

