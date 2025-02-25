#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/util.h>

#define JITTER_TASK_PRIORITY 1
#define LOAD_TASK_PRIORITY 5
#define JITTER_TASK_PERIOD_MS 1000
#define LOAD_TASK_PERIOD_MS 10
#define LOAD_ITERATIONS 100000

void jitter_task(void *arg1, void *arg2, void *arg3) {
    int64_t next_wakeup = k_uptime_get() + JITTER_TASK_PERIOD_MS;

    printk("\n*** Zephyr Jitter Test with High System Load (Improved) ***\n");
    printk("Starting jitter measurement...\n\n");

    while (1) {
        int64_t now = k_uptime_get();
        int32_t jitter = (int32_t)(now - next_wakeup);

        printk("Scheduled at: %lld ms, Actual: %lld ms, Jitter: %d ms\n", next_wakeup, now, jitter);

        next_wakeup += JITTER_TASK_PERIOD_MS;
        k_sleep(K_MSEC(MAX(0, next_wakeup - k_uptime_get())));
    }
}

void load_task(void *arg1, void *arg2, void *arg3) {
    while (1) {
        volatile uint32_t dummy = 0;
        for (int i = 0; i < LOAD_ITERATIONS; i++) {
            dummy += i;  // Simulated CPU load
        }
        k_sleep(K_MSEC(LOAD_TASK_PERIOD_MS));  // Yield CPU time
    }
}

K_THREAD_DEFINE(jitter_tid, 1024, jitter_task, NULL, NULL, NULL,
                JITTER_TASK_PRIORITY, 0, 0);

K_THREAD_DEFINE(load_tid, 1024, load_task, NULL, NULL, NULL,
                LOAD_TASK_PRIORITY, 0, 0);