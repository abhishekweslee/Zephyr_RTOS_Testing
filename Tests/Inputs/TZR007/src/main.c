#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(semaphore_test, LOG_LEVEL_INF);

#define STACK_SIZE 1024
#define THREAD_PRIORITY 5

K_SEM_DEFINE(my_semaphore, 1, 1); // Initialized with 1 token

void thread_A(void *arg1, void *arg2, void *arg3) {
    while (1) {
        LOG_INF("Thread A: Attempting to acquire semaphore");
        k_sem_take(&my_semaphore, K_FOREVER);
        LOG_INF("Thread A: Acquired semaphore");
        k_sleep(K_MSEC(1000));
        k_sem_give(&my_semaphore);
        LOG_INF("Thread A: Released semaphore");
        k_sleep(K_MSEC(500));
    }
}

void thread_B(void *arg1, void *arg2, void *arg3) {
    while (1) {
        LOG_INF("Thread B: Attempting to acquire semaphore");
        k_sem_take(&my_semaphore, K_FOREVER);
        LOG_INF("Thread B: Acquired semaphore");
        k_sleep(K_MSEC(1000));
        k_sem_give(&my_semaphore);
        LOG_INF("Thread B: Released semaphore");
        k_sleep(K_MSEC(500));
    }
}

void thread_C(void *arg1, void *arg2, void *arg3) {
    while (1) {
        LOG_INF("Thread C: Attempting to acquire semaphore");
        k_sem_take(&my_semaphore, K_FOREVER);
        LOG_INF("Thread C: Acquired semaphore");
        k_sleep(K_MSEC(1000));
        k_sem_give(&my_semaphore);
        LOG_INF("Thread C: Released semaphore");
        k_sleep(K_MSEC(500));
    }
}

K_THREAD_DEFINE(thread_A_id, STACK_SIZE, thread_A, NULL, NULL, NULL, THREAD_PRIORITY, 0, 0);
K_THREAD_DEFINE(thread_B_id, STACK_SIZE, thread_B, NULL, NULL, NULL, THREAD_PRIORITY, 0, 0);
K_THREAD_DEFINE(thread_C_id, STACK_SIZE, thread_C, NULL, NULL, NULL, THREAD_PRIORITY, 0, 0);

void main(void) {
    LOG_INF("Semaphore Test: Started");
    while (1) {
        k_sleep(K_FOREVER);
    }
}
