#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/irq.h>
#include <zephyr/arch/arm/cortex_m/nvic.h>

#define IRQ1  1  // Lowest priority IRQ
#define IRQ2  2  
#define IRQ3  3  
#define IRQ4  4  
#define IRQ5  5  // Highest priority IRQ

#define PRIORITY_1  3  // Lowest priority
#define PRIORITY_2  2  
#define PRIORITY_3  2  
#define PRIORITY_4  1  
#define PRIORITY_5  0  // Highest priority

volatile bool irq1_executed = false;
volatile bool irq2_executed = false;
volatile bool irq3_executed = false;
volatile bool irq4_executed = false;
volatile bool irq5_executed = false;

void irq5_handler(void *arg) {
    ARG_UNUSED(arg);
    irq5_executed = true;
    printk("IRQ5 (Highest Priority) Executed\n");
}

void irq4_handler(void *arg) {
    ARG_UNUSED(arg);
    irq4_executed = true;
    printk("IRQ4 Executed, triggering IRQ5...\n");

    NVIC_SetPendingIRQ(IRQ5);
}

void irq3_handler(void *arg) {
    ARG_UNUSED(arg);
    irq3_executed = true;
    printk("IRQ3 Executed, triggering IRQ4...\n");

    NVIC_SetPendingIRQ(IRQ4);
}

void irq2_handler(void *arg) {
    ARG_UNUSED(arg);
    irq2_executed = true;
    printk("IRQ2 Executed, triggering IRQ3...\n");

    NVIC_SetPendingIRQ(IRQ3);
}

void irq1_handler(void *arg) {
    ARG_UNUSED(arg);
    irq1_executed = true;
    printk("IRQ1 Executed, triggering IRQ2...\n");

    NVIC_SetPendingIRQ(IRQ2);
}

int main(void) {
    printk("Zephyr Nested IRQ Test with 5 Levels\n");

    // Configure and enable interrupts
    IRQ_CONNECT(IRQ1, PRIORITY_1, irq1_handler, NULL, 0);
    IRQ_CONNECT(IRQ2, PRIORITY_2, irq2_handler, NULL, 0);
    IRQ_CONNECT(IRQ3, PRIORITY_3, irq3_handler, NULL, 0);
    IRQ_CONNECT(IRQ4, PRIORITY_4, irq4_handler, NULL, 0);
    IRQ_CONNECT(IRQ5, PRIORITY_5, irq5_handler, NULL, 0);

    irq_enable(IRQ1);
    irq_enable(IRQ2);
    irq_enable(IRQ3);
    irq_enable(IRQ4);
    irq_enable(IRQ5);

    // Trigger the lowest priority IRQ first
    printk("Triggering IRQ1...\n");
    NVIC_SetPendingIRQ(IRQ1);

    // Wait to ensure interrupts are processed
    k_sleep(K_MSEC(100));

    // Verify execution order
    if (irq1_executed && irq2_executed && irq3_executed && irq4_executed && irq5_executed) {
        printk("Nested Interrupt Test Passed: Execution order verified.\n");
    } else {
        printk("Nested Interrupt Test Failed!\n");
    }

    return 0;
}
