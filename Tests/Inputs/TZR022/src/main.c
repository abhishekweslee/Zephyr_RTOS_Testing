#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>
#include <zephyr/timing/timing.h>

#define MONITOR_INTERVAL_MS 1000  // CPU usage print interval in milliseconds
#define LOAD_TASK_STACK_SIZE 512
#define MONITOR_TASK_STACK_SIZE 512
#define LOAD_TASK_PRIORITY 5
#define MONITOR_TASK_PRIORITY 4
#define NUM_LOAD_TASKS 2

K_THREAD_STACK_DEFINE(load_task_stack[NUM_LOAD_TASKS], LOAD_TASK_STACK_SIZE);
K_THREAD_STACK_DEFINE(monitor_task_stack, MONITOR_TASK_STACK_SIZE);
struct k_thread load_task_data[NUM_LOAD_TASKS];
struct k_thread monitor_task_data;

/* Load Task: Creates a CPU load */
void load_task(void *arg1, void *arg2, void *arg3) {
    while (1) {
        for (volatile int i = 0; i < 500000; i++) {
            __asm__ volatile("nop");
        }
        k_msleep(100);
    }
}

/* Monitor Task: Monitors and prints CPU usage */
void monitor_task(void *arg1, void *arg2, void *arg3) {
    struct k_thread_runtime_stats stats;

    while (1) {
        if (k_thread_runtime_stats_get(k_current_get(), &stats) == 0) {
            printk("CPU Usage: %llu cycles\n", stats.execution_cycles);
        } else {
            printk("Failed to get runtime stats.\n");
        }
        k_msleep(MONITOR_INTERVAL_MS);
    }
}

void main(void) {
    printk("*** Booting Zephyr OS ***\n");

    /* Start load tasks */
    for (int i = 0; i < NUM_LOAD_TASKS; i++) {
        k_thread_create(&load_task_data[i], load_task_stack[i], LOAD_TASK_STACK_SIZE,
                        load_task, NULL, NULL, NULL, LOAD_TASK_PRIORITY, 0, K_NO_WAIT);
    }

    /* Start CPU usage monitor task */
    k_thread_create(&monitor_task_data, monitor_task_stack, MONITOR_TASK_STACK_SIZE,
                    monitor_task, NULL, NULL, NULL, MONITOR_TASK_PRIORITY, 0, K_NO_WAIT);
}