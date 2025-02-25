/* src/main.c */
#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define EVENT_FLAG_1 0x01
#define EVENT_FLAG_2 0x02

struct k_event my_event;

void event_producer(void *arg1, void *arg2, void *arg3) {
    k_sleep(K_SECONDS(2));  // Simulate work
    printk("Setting EVENT_FLAG_1\n");
    k_event_set(&my_event, EVENT_FLAG_1);

    k_sleep(K_SECONDS(2));  // Simulate work
    printk("Setting EVENT_FLAG_2\n");
    k_event_set(&my_event, EVENT_FLAG_2);
}

void event_consumer(void *arg1, void *arg2, void *arg3) {
    printk("Waiting for EVENT_FLAG_1...\n");
    uint32_t events = k_event_wait(&my_event, EVENT_FLAG_1, false, K_FOREVER);
    printk("Received EVENT_FLAG_1: 0x%X\n", events);

    printk("Waiting for EVENT_FLAG_2...\n");
    events = k_event_wait(&my_event, EVENT_FLAG_2, false, K_FOREVER);
    printk("Received EVENT_FLAG_2: 0x%X\n", events);
}

K_THREAD_STACK_DEFINE(producer_stack, 1024);
K_THREAD_STACK_DEFINE(consumer_stack, 1024);
struct k_thread producer_thread, consumer_thread;

void main(void) {
    k_event_init(&my_event);

    k_thread_create(&producer_thread, producer_stack, 
                    K_THREAD_STACK_SIZEOF(producer_stack),
                    event_producer, NULL, NULL, NULL,
                    K_PRIO_PREEMPT(1), 0, K_NO_WAIT);

    k_thread_create(&consumer_thread, consumer_stack, 
                    K_THREAD_STACK_SIZEOF(consumer_stack),
                    event_consumer, NULL, NULL, NULL,
                    K_PRIO_PREEMPT(1), 0, K_NO_WAIT);
}
