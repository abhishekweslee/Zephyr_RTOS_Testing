#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/timeutil.h>

#define SLEEP_DURATION_MS 1000  // Sleep for 1000 ms (1 second)
#define BUSY_WAIT_DURATION_US 500000  // Busy-wait for 500000 us (0.5 seconds)

void main(void)
{
    printk("Starting Sleep & Delay Accuracy Test...\n");

    /* Measure k_sleep() Accuracy */
    int64_t start_time = k_uptime_get();
    k_sleep(K_MSEC(SLEEP_DURATION_MS));
    int64_t elapsed_time = k_uptime_get() - start_time;

    printk("k_sleep() expected: %d ms, actual: %lld ms\n", SLEEP_DURATION_MS, elapsed_time);

    /* Measure k_busy_wait() Accuracy */
    start_time = k_uptime_get();
    k_busy_wait(BUSY_WAIT_DURATION_US);
    elapsed_time = k_uptime_get() - start_time;

    printk("k_busy_wait() expected: %d us, actual: %lld us\n", BUSY_WAIT_DURATION_US, elapsed_time * 1000);

    printk("Test Completed.\n");
}
