#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/device.h>
#include <zephyr/drivers/timer/system_timer.h>
#include <zephyr/irq.h>

#define TEST_DURATION K_SECONDS(5)  // Test run time

volatile bool isr_executed = false;

/* Interrupt Service Routine */
void test_isr(void *arg)
{
    ARG_UNUSED(arg);
    printk("ISR executed!\n");
    isr_executed = true;
}

/* Main function */
void main(void)
{
    printk("Starting ISR deadlock test...\n");

    /* Simulate an interrupt */
    printk("Triggering software interrupt...\n");
    irq_offload(test_isr, NULL);  // Simulate an IRQ

    /* Wait and check if ISR executed */
    k_sleep(TEST_DURATION);

    if (isr_executed) {
        printk("Test passed: ISR executed without deadlock.\n");
    } else {
        printk("Test failed: ISR did not execute.\n");
    }
}
