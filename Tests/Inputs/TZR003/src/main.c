#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(context_switch, LOG_LEVEL_INF);

#define STACK_SIZE 1024
#define PRIORITY_HIGH -1
#define PRIORITY_MEDIUM 0
#define PRIORITY_LOW 1

K_THREAD_STACK_DEFINE(thread_high_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_medium_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_low_stack, STACK_SIZE);

struct k_thread thread_high;
struct k_thread thread_medium;
struct k_thread thread_low;

volatile uint32_t start_time, end_time;

void high_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        start_time = k_cycle_get_32();  // Capture start time
        LOG_INF("High Priority Task Running");
        k_sleep(K_MSEC(500));  // Simulate workload
        end_time = k_cycle_get_32();    // Capture end time

        uint32_t switch_time = end_time - start_time;
        LOG_INF("Context switch time: %u cycles", switch_time);
    }
}

void medium_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        LOG_INF("Medium Priority Task Running");
        k_sleep(K_MSEC(500));
    }
}

void low_priority_task(void *p1, void *p2, void *p3) {
    while (1) {
        LOG_INF("Low Priority Task Running");
        k_sleep(K_MSEC(500));
    }
}

void main(void) {
    LOG_INF("Starting Context Switching Test...");

    /* Creating threads with different priorities */
    k_thread_create(&thread_high, thread_high_stack, STACK_SIZE,
                    high_priority_task, NULL, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);
    k_thread_name_set(&thread_high, "High_Priority");

    k_thread_create(&thread_medium, thread_medium_stack, STACK_SIZE,
                    medium_priority_task, NULL, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);
    k_thread_name_set(&thread_medium, "Medium_Priority");

    k_thread_create(&thread_low, thread_low_stack, STACK_SIZE,
                    low_priority_task, NULL, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);
    k_thread_name_set(&thread_low, "Low_Priority");

    LOG_INF("Threads created, scheduling will now begin...");
}
