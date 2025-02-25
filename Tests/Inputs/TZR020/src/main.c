#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/mutex.h>

#define STACK_SIZE 1024
#define PRIORITY  5

K_MUTEX_DEFINE(resource_mutex);

void shared_resource_access(const char *thread_name)
{
    printk("%s: Waiting to acquire resource...\n", thread_name);

    /* Attempt to lock the resource */
    k_mutex_lock(&resource_mutex, K_FOREVER);
    printk("%s: Acquired resource, working...\n", thread_name);

    /* Simulate resource usage */
    k_sleep(K_MSEC(1000));

    printk("%s: Releasing resource.\n", thread_name);
    k_mutex_unlock(&resource_mutex);
}

void threadA(void *arg1, void *arg2, void *arg3)
{
    while (1) {
        shared_resource_access("Thread A");
        k_sleep(K_MSEC(500));  // Delay before retrying
    }
}

void threadB(void *arg1, void *arg2, void *arg3)
{
    while (1) {
        shared_resource_access("Thread B");
        k_sleep(K_MSEC(700));  // Delay before retrying
    }
}

/* Define and start the threads */
K_THREAD_DEFINE(thread_a_id, STACK_SIZE, threadA, NULL, NULL, NULL, PRIORITY, 0, 0);
K_THREAD_DEFINE(thread_b_id, STACK_SIZE, threadB, NULL, NULL, NULL, PRIORITY, 0, 0);

void main(void)
{
    printk("Starting Resource Contention Simulation...\n");
}
