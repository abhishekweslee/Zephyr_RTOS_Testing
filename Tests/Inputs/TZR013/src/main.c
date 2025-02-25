#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/__assert.h>

#define STACK_SIZE 256  // Small stack size to induce overflow
K_THREAD_STACK_DEFINE(test_stack, STACK_SIZE);
struct k_thread test_thread;

void stack_overflow_entry(void *p1, void *p2, void *p3)
{
    volatile uint8_t buffer[STACK_SIZE];  // Overwrite stack
    for (int i = 0; i < STACK_SIZE; i++) {
        buffer[i] = 0xAA;
    }

    printk("This should never print! Stack overflow missed.\n");
}

void test_stack_overflow()
{
    printk("Starting Stack Overflow Test...\n");

    k_thread_create(&test_thread, test_stack, STACK_SIZE,
                    stack_overflow_entry, NULL, NULL, NULL,
                    K_PRIO_PREEMPT(1), 0, K_NO_WAIT);
}

void test_stack_underflow()
{
    printk("Starting Stack Underflow Test...\n");

    volatile uint32_t *fake_stack_pointer = (uint32_t *)0x10000000;
    __ASSERT_NO_MSG(fake_stack_pointer != NULL);

    __asm__ volatile (
        "mov sp, %0\n"  // Set stack pointer to an invalid location
        "bx lr\n"       // Attempt to return (should fail)
        :
        : "r"(fake_stack_pointer)
    );

    printk("This should never print! Stack underflow missed.\n");
}

void main(void)
{
    printk("Booting Zephyr Stack Overflow & Underflow Test...\n");

    test_stack_overflow();
    k_sleep(K_MSEC(500));  // Allow time for crash detection

    test_stack_underflow();
    k_sleep(K_MSEC(500));  // Allow time for crash detection

    printk("Test completed.\n");
}
