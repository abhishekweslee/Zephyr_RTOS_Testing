#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#define STACK_SIZE 1024
#define PRIORITY_HIGH -1
#define PRIORITY_MED  0
#define PRIORITY_LOW  1

LOG_MODULE_REGISTER(task_starvation, LOG_LEVEL_DBG); // Enable logging

K_THREAD_STACK_DEFINE(high_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(med_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(low_stack, STACK_SIZE);

struct k_thread high_task_data;
struct k_thread med_task_data;
struct k_thread low_task_data;

struct k_mutex test_mutex;

/* High-Priority Task (Starvation Producer) */
void high_task(void *p1, void *p2, void *p3)
{
    while (1) {
        LOG_INF("High-Priority Task Running");
        k_sleep(K_MSEC(100));  // Let others run
    }
}

/* Medium-Priority Task (Interrupting Execution) */
void med_task(void *p1, void *p2, void *p3)
{
    while (1) {
        LOG_INF("Medium-Priority Task Running");
        k_sleep(K_MSEC(500));  // Allows high to dominate
    }
}

/* Low-Priority Task (Blocked by Mutex) */
void low_task(void *p1, void *p2, void *p3)
{
    LOG_INF("Low-Priority Task: Trying to acquire Mutex");
    k_mutex_lock(&test_mutex, K_FOREVER);
    
    LOG_INF("Low-Priority Task: Holding Mutex");
    k_sleep(K_SECONDS(3)); // Simulate long processing time

    LOG_INF("Low-Priority Task: Releasing Mutex");
    k_mutex_unlock(&test_mutex);
}

void main(void)
{
    LOG_INF("Starting Task Starvation & Priority Inversion Test");

    k_mutex_init(&test_mutex);

    k_thread_create(&high_task_data, high_stack, STACK_SIZE,
                    high_task, NULL, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);

    k_thread_create(&med_task_data, med_stack, STACK_SIZE,
                    med_task, NULL, NULL, NULL,
                    PRIORITY_MED, 0, K_NO_WAIT);

    k_thread_create(&low_task_data, low_stack, STACK_SIZE,
                    low_task, NULL, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);
}
