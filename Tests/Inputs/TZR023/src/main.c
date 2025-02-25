/*
 * Zephyr Project: Task Execution Time Profiling Under Varying System Conditions
 *
 * This application creates multiple tasks with different priorities and loads.
 * It measures and logs the execution times of these tasks under varying conditions.
 */

 #include <zephyr/kernel.h>
 #include <zephyr/sys/printk.h>
 #include <zephyr/sys/util.h>
 #include <zephyr/timing/timing.h>
 
 #define STACK_SIZE 1024
 #define LOW_LOAD_PRIORITY 3
 #define MEDIUM_LOAD_PRIORITY 2
 #define HIGH_LOAD_PRIORITY 1
 #define MONITOR_PRIORITY 0
 #define LOAD_ITERATIONS 50000
 
 K_THREAD_STACK_DEFINE(low_load_stack, STACK_SIZE);
 K_THREAD_STACK_DEFINE(medium_load_stack, STACK_SIZE);
 K_THREAD_STACK_DEFINE(high_load_stack, STACK_SIZE);
 K_THREAD_STACK_DEFINE(monitor_stack, STACK_SIZE);
 
 struct k_thread low_load_thread;
 struct k_thread medium_load_thread;
 struct k_thread high_load_thread;
 struct k_thread monitor_thread;
 
 /* Utility function to simulate work */
 void busy_work(int iterations) {
     volatile int dummy = 0;
     for (int i = 0; i < iterations; i++) {
         dummy += i;
     }
 }
 
 /* Task function template */
 void load_task(void *arg1, void *arg2, void *arg3) {
     int load = *(int *)arg1;
     while (1) {
         uint64_t start = k_cycle_get_64();
         busy_work(load);
         uint64_t end = k_cycle_get_64();
         uint64_t exec_cycles = end - start;
 
         printk("%s executed in %llu cycles\n", (char *)arg2, exec_cycles);
         k_msleep(500);  // Period between executions
     }
 }
 
 /* Monitor task to observe system behavior */
 void monitor_task(void *arg1, void *arg2, void *arg3) {
     while (1) {
         printk("[Monitor] System running...\n");
         k_msleep(2000);  // Print status every 2 seconds
     }
 }
 
 void main(void) {
     printk("*** Booting Zephyr OS: Task Execution Profiling ***\n");
 
     static int low_load = LOAD_ITERATIONS / 10;
     static int medium_load = LOAD_ITERATIONS / 5;
     static int high_load = LOAD_ITERATIONS;
 
     k_thread_create(&low_load_thread, low_load_stack, STACK_SIZE,
                     load_task, &low_load, "Low Load Task", NULL,
                     LOW_LOAD_PRIORITY, 0, K_NO_WAIT);
 
     k_thread_create(&medium_load_thread, medium_load_stack, STACK_SIZE,
                     load_task, &medium_load, "Medium Load Task", NULL,
                     MEDIUM_LOAD_PRIORITY, 0, K_NO_WAIT);
 
     k_thread_create(&high_load_thread, high_load_stack, STACK_SIZE,
                     load_task, &high_load, "High Load Task", NULL,
                     HIGH_LOAD_PRIORITY, 0, K_NO_WAIT);
 
     k_thread_create(&monitor_thread, monitor_stack, STACK_SIZE,
                     monitor_task, NULL, NULL, NULL,
                     MONITOR_PRIORITY, 0, K_NO_WAIT);
 }
 