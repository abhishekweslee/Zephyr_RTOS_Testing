#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(task_state_demo, LOG_LEVEL_INF);

#define STACK_SIZE 1024
#define PRIORITY_HIGH -1
#define PRIORITY_MEDIUM 0
#define PRIORITY_LOW 1

K_THREAD_STACK_DEFINE(thread_high_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_medium_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(thread_low_stack, STACK_SIZE);

struct k_thread thread_high;
struct k_thread thread_medium;
struct k_thread thread_low;

struct k_sem sync_sem;  // Semaphore for blocking task

void high_priority_task(void *p1, void *p2, void *p3) {
    LOG_INF("High Priority Task: READY state");
    while (1) {
        LOG_INF("High Priority Task: RUNNING state");
        k_sleep(K_MSEC(500));
    }
}

void medium_priority_task(void *p1, void *p2, void *p3) {
    LOG_INF("Medium Priority Task: READY state");
    
    while (1) {
        LOG_INF("Medium Priority Task: BLOCKED state (waiting for semaphore)");
        k_sem_take(&sync_sem, K_FOREVER);  // Blocked state
        
        LOG_INF("Medium Priority Task: RUNNING state after unblocking");
        k_sleep(K_MSEC(500));
    }
}

void low_priority_task(void *p1, void *p2, void *p3) {
    LOG_INF("Low Priority Task: READY state");
    k_sleep(K_MSEC(2000));  // Allow others to execute

    LOG_INF("Low Priority Task: SUSPENDING Medium Priority Task");
    k_thread_suspend(&thread_medium);  // Suspend thread

    k_sleep(K_MSEC(2000));

    LOG_INF("Low Priority Task: RESUMING Medium Priority Task");
    k_thread_resume(&thread_medium);  // Resume thread

    while (1) {
        LOG_INF("Low Priority Task: RUNNING state");
        k_sleep(K_MSEC(1000));
    }
}

void main(void) {
    LOG_INF("Starting Task State Transition Test...");

    k_sem_init(&sync_sem, 0, 1);  // Initialize semaphore

    k_thread_create(&thread_high, thread_high_stack, STACK_SIZE,
                    high_priority_task, NULL, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);
    k_thread_name_set(&thread_high, "High_Priority");

    k_thread_create(&thread_medium, thread_medium_stack, STACK_SIZE,
                    medium_priority_task, NULL, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);
    k_thread_name_set(&thread_medium, "Medium_Priority");

    k_thread_create(&thread_low, thread_low_stack, STACK_SIZE,
                    low_priority_task, NULL, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);
    k_thread_name_set(&thread_low, "Low_Priority");

    LOG_INF("Threads created, scheduling will now begin...");

    k_sleep(K_MSEC(5000));  // Let the system run before releasing semaphore

    LOG_INF("Releasing Semaphore - Medium Priority Task will wake up");
    k_sem_give(&sync_sem);  // Unblock medium-priority thread
}
