#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define STACK_SIZE 1024
#define PRIORITY_LOW 3
#define PRIORITY_MEDIUM 2
#define PRIORITY_HIGH 1

K_MUTEX_DEFINE(test_mutex);
K_THREAD_STACK_DEFINE(low_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(medium_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(high_stack, STACK_SIZE);

struct k_thread low_thread, medium_thread, high_thread;

void low_priority_thread(void *p1, void *p2, void *p3) {
    printk("[Low] Attempting to acquire mutex\n");
    k_mutex_lock(&test_mutex, K_FOREVER);
    printk("[Low] Acquired mutex\n");
    k_sleep(K_MSEC(1000));
    printk("[Low] Releasing mutex\n");
    k_mutex_unlock(&test_mutex);
}

void medium_priority_thread(void *p1, void *p2, void *p3) {
    while (1) {
        printk("[Medium] Running\n");
        k_sleep(K_MSEC(300));
    }
}

void high_priority_thread(void *p1, void *p2, void *p3) {
    k_sleep(K_MSEC(100)); // Ensure low thread gets the mutex first
    printk("[High] Attempting to acquire mutex\n");
    k_mutex_lock(&test_mutex, K_FOREVER);
    printk("[High] Acquired mutex\n");
    k_sleep(K_MSEC(500));
    printk("[High] Releasing mutex\n");
    k_mutex_unlock(&test_mutex);
}

void main(void) {
    printk("Mutex Test: Started\n");
    
    k_thread_create(&low_thread, low_stack, STACK_SIZE, low_priority_thread, NULL, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);
    
    k_thread_create(&medium_thread, medium_stack, STACK_SIZE, medium_priority_thread, NULL, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);
    
    k_thread_create(&high_thread, high_stack, STACK_SIZE, high_priority_thread, NULL, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);
}
