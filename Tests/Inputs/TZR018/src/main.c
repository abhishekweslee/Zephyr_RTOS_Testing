#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys_clock.h>

#define ONESHOT_TIMEOUT_MS 1000    // 1 second
#define PERIODIC_TIMEOUT_MS 500    // 500 ms
#define TEST_DURATION_MS 3000      // Run test for 3 seconds

static struct k_timer oneshot_timer;
static struct k_timer periodic_timer;
static int periodic_count = 0;
static int64_t oneshot_start_time, oneshot_end_time;
static int64_t periodic_start_time, periodic_end_time;

/* One-shot timer callback */
void oneshot_timer_expiry(struct k_timer *timer_id)
{
    ARG_UNUSED(timer_id);
    oneshot_end_time = k_uptime_get();
    int64_t elapsed_time = oneshot_end_time - oneshot_start_time;
    printk("One-shot timer expired! Expected: %d ms, Actual: %lld ms\n",
           ONESHOT_TIMEOUT_MS, elapsed_time);
}

/* Periodic timer callback */
void periodic_timer_expiry(struct k_timer *timer_id)
{
    ARG_UNUSED(timer_id);
    periodic_end_time = k_uptime_get();
    int64_t elapsed_time = periodic_end_time - periodic_start_time;
    periodic_start_time = periodic_end_time;  // Update for next interval

    printk("Periodic timer expired! Expected: %d ms, Actual: %lld ms\n",
           PERIODIC_TIMEOUT_MS, elapsed_time);

    periodic_count++;
}

/* Main function */
void main(void)
{
    printk("Starting Timer Precision Test...\n");

    /* Initialize and start one-shot timer */
    k_timer_init(&oneshot_timer, oneshot_timer_expiry, NULL);
    oneshot_start_time = k_uptime_get();
    k_timer_start(&oneshot_timer, K_MSEC(ONESHOT_TIMEOUT_MS), K_NO_WAIT);
    printk("One-shot timer started: %d ms timeout\n", ONESHOT_TIMEOUT_MS);

    /* Initialize and start periodic timer */
    k_timer_init(&periodic_timer, periodic_timer_expiry, NULL);
    periodic_start_time = k_uptime_get();
    k_timer_start(&periodic_timer, K_MSEC(PERIODIC_TIMEOUT_MS), K_MSEC(PERIODIC_TIMEOUT_MS));
    printk("Periodic timer started: %d ms period\n", PERIODIC_TIMEOUT_MS);

    /* Wait for test duration */
    k_sleep(K_MSEC(TEST_DURATION_MS));

    /* Stop timers */
    k_timer_stop(&periodic_timer);
    printk("Test completed. Periodic timer triggered %d times.\n", periodic_count);
}
