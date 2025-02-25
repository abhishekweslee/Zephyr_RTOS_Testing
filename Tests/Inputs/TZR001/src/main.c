/*
 * Task Management Test in Zephyr
 * Verifies thread creation, deletion, and priority assignment.
 */

 #include <zephyr/kernel.h>
 #include <zephyr/logging/log.h>
 
 LOG_MODULE_REGISTER(task_mgmt, LOG_LEVEL_INF);
 
 // Stack size for threads
 #define STACK_SIZE 1024
 
 // Thread priorities
 #define HIGH_PRIORITY  1
 #define MEDIUM_PRIORITY 2
 #define LOW_PRIORITY   3
 
 // Thread objects
 K_THREAD_STACK_DEFINE(thread1_stack, STACK_SIZE);
 K_THREAD_STACK_DEFINE(thread2_stack, STACK_SIZE);
 K_THREAD_STACK_DEFINE(thread3_stack, STACK_SIZE);
 
 struct k_thread thread1;
 struct k_thread thread2;
 struct k_thread thread3;
 
 // Dummy delay for task simulation
 #define TASK_DELAY K_SECONDS(2)
 
 // Thread 1 function
 void thread1_func(void *arg1, void *arg2, void *arg3)
 {
     LOG_INF("Thread 1 started with HIGH priority");
     k_sleep(TASK_DELAY);
     LOG_INF("Thread 1 exiting...");
 }
 
 // Thread 2 function
 void thread2_func(void *arg1, void *arg2, void *arg3)
 {
     LOG_INF("Thread 2 started with MEDIUM priority");
     k_sleep(TASK_DELAY);
     LOG_INF("Thread 2 exiting...");
 }
 
 // Thread 3 function
 void thread3_func(void *arg1, void *arg2, void *arg3)
 {
     LOG_INF("Thread 3 started with LOW priority");
     k_sleep(TASK_DELAY);
     LOG_INF("Thread 3 exiting...");
 }
 
 // Main function
 void main(void)
 {
     LOG_INF("Task Management Test Started");
 
     // Creating threads
     k_tid_t t1 = k_thread_create(&thread1, thread1_stack, STACK_SIZE,
                                  thread1_func, NULL, NULL, NULL,
                                  HIGH_PRIORITY, 0, K_NO_WAIT);
 
     k_tid_t t2 = k_thread_create(&thread2, thread2_stack, STACK_SIZE,
                                  thread2_func, NULL, NULL, NULL,
                                  MEDIUM_PRIORITY, 0, K_NO_WAIT);
 
     k_tid_t t3 = k_thread_create(&thread3, thread3_stack, STACK_SIZE,
                                  thread3_func, NULL, NULL, NULL,
                                  LOW_PRIORITY, 0, K_NO_WAIT);
 
     k_sleep(K_SECONDS(3));
 
     // Deleting threads
     LOG_INF("Deleting Thread 1...");
     k_thread_abort(t1);
 
     LOG_INF("Deleting Thread 2...");
     k_thread_abort(t2);
 
     LOG_INF("Deleting Thread 3...");
     k_thread_abort(t3);
 
     LOG_INF("Task Management Test Completed");
 }
 