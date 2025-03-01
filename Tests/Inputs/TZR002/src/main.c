#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define STACK_SIZE 1024
#define PRIORITY_HIGH 1
#define PRIORITY_MEDIUM 2
#define PRIORITY_LOW 3

K_THREAD_STACK_DEFINE(thread_high_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_medium_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_low_stack, STACK_SIZE);

struct k_thread thread_high;
struct k_thread thread_medium;
struct k_thread thread_low;

void high_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        printk("High Priority Task Running\n");
        k_sleep(K_MSEC(500));
    }
}

void medium_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        printk("Medium Priority Task Running\n");
        k_sleep(K_MSEC(500));
    }
}

void low_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        printk("Low Priority Task Running\n");
        k_sleep(K_MSEC(500));
    }
}

void main(void) {
    printk("Starting Task Scheduling Test...\n");

    /* Creating threads with different priorities */
    k_thread_create(&thread_high, thread_high_stack, STACK_SIZE,
                    high_priority_task, NULL, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);

    k_thread_create(&thread_medium, thread_medium_stack, STACK_SIZE,
                    medium_priority_task, NULL, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);

    k_thread_create(&thread_low, thread_low_stack, STACK_SIZE,
                    low_priority_task, NULL, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);

    printk("Threads created, scheduling will now begin...\n");

    return;
}
