#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/sys/mutex.h>

#define THREAD_STACK_SIZE 1024
#define THREAD_PRIORITY 5
#define ITERATIONS 5

K_MUTEX_DEFINE(shared_mutex);

volatile int shared_resource = 0;

/* Function to simulate shared resource access without a mutex */
void unsafe_access(void *arg1, void *arg2, void *arg3)
{
    for (int i = 0; i < ITERATIONS; i++) {
        int temp = shared_resource;
        k_sleep(K_MSEC(50));  // Simulate processing delay
        shared_resource = temp + 1;
        printk("Unsafe: Thread %s updated shared_resource to %d\n",
               (char *)arg1, shared_resource);
    }
}

/* Function to simulate shared resource access with a mutex */
void safe_access(void *arg1, void *arg2, void *arg3)
{
    for (int i = 0; i < ITERATIONS; i++) {
        k_mutex_lock(&shared_mutex, K_FOREVER);  // Lock mutex
        int temp = shared_resource;
        k_sleep(K_MSEC(50));  // Simulate processing delay
        shared_resource = temp + 1;
        printk("Safe: Thread %s updated shared_resource to %d\n",
               (char *)arg1, shared_resource);
        k_mutex_unlock(&shared_mutex);  // Unlock mutex
    }
}

/* Thread Definitions */
K_THREAD_DEFINE(thread1, THREAD_STACK_SIZE, unsafe_access, "A", NULL, NULL, THREAD_PRIORITY, 0, 0);
K_THREAD_DEFINE(thread2, THREAD_STACK_SIZE, unsafe_access, "B", NULL, NULL, THREAD_PRIORITY, 0, 0);

K_THREAD_DEFINE(thread3, THREAD_STACK_SIZE, safe_access, "C", NULL, NULL, THREAD_PRIORITY, 0, 1000);
K_THREAD_DEFINE(thread4, THREAD_STACK_SIZE, safe_access, "D", NULL, NULL, THREAD_PRIORITY, 0, 1000);

/* Main function */
void main(void)
{
    printk("Starting Concurrent Access Test...\n");

    k_sleep(K_SECONDS(2));  // Wait for threads to complete
    printk("Final shared_resource value: %d\n", shared_resource);
    printk("Test Completed.\n");
}
