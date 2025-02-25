#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define PERIOD_MS 1000  // Task period in milliseconds

void periodic_task(void)
{
    int64_t next_wakeup = k_uptime_get();  // Initial wake-up time

    while (1) {
        int64_t start_time = k_uptime_get();
        int64_t jitter = start_time - next_wakeup;

        printk("Task started at %lld ms (Jitter: %lld ms)\n", start_time, jitter);

        // Simulate task workload (e.g., 200 ms)
        k_sleep(K_MSEC(200));

        int64_t end_time = k_uptime_get();
        printk("Task completed at %lld ms, execution time: %lld ms\n", end_time, end_time - start_time);

        // Update next expected wake-up time
        next_wakeup += PERIOD_MS;

        int64_t delay = next_wakeup - k_uptime_get();
        if (delay > 0) {
            k_sleep(K_MSEC(delay));  // Sleep until the next period
        } else {
            printk("Missed deadline by %lld ms!\n", -delay);  // Deadline miss
            next_wakeup = k_uptime_get();  // Resynchronize
        }
    }
}

void main(void)
{
    printk("Starting periodic task for deadline adherence check...\n");
    periodic_task();
}
