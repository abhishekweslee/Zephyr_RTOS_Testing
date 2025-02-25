#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/timing/timing.h>

#define TIMER_DURATION_MS 1000  // 1 second
#define TIMER_PERIOD_MS   500   // 500ms periodic

static struct k_timer my_timer;
static volatile bool timer_expired = false;

/* Timer expiry callback */
void timer_expiry_fn(struct k_timer *timer_id)
{
    ARG_UNUSED(timer_id);
    timer_expired = true;
    printk("Timer expired! Callback executed.\n");
}

/* Timer stop callback (optional) */
void timer_stop_fn(struct k_timer *timer_id)
{
    ARG_UNUSED(timer_id);
    printk("Timer stopped.\n");
}

void main(void)
{
    printk("Starting Timer Creation, Deletion & Expiry Test...\n");

    /* Initialize the timer */
    k_timer_init(&my_timer, timer_expiry_fn, timer_stop_fn);
    printk("Timer initialized successfully.\n");

    /* Start the timer (one-shot mode) */
    k_timer_start(&my_timer, K_MSEC(TIMER_DURATION_MS), K_MSEC(TIMER_PERIOD_MS));
    printk("Timer started: %d ms timeout, %d ms period.\n", TIMER_DURATION_MS, TIMER_PERIOD_MS);

    /* Wait for expiry */
    k_sleep(K_MSEC(TIMER_DURATION_MS + 200));

    /* Validate expiry */
    if (timer_expired) {
        printk("Test Passed: Timer expired as expected.\n");
    } else {
        printk("Test Failed: Timer did not expire.\n");
    }

    /* Stop and delete the timer */
    k_timer_stop(&my_timer);
    printk("Timer stopped and deleted.\n");
}
