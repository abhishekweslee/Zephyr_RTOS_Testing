#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

#define STACK_SIZE 1024
#define MSGQ_SIZE 10

#define PRIORITY_HIGH   -1
#define PRIORITY_MEDIUM  0
#define PRIORITY_LOW     1

struct message {
    int id;
    int sender_priority;
};

K_MSGQ_DEFINE(my_msgq, sizeof(struct message), MSGQ_SIZE, 4);

K_THREAD_STACK_DEFINE(sender_stack_high, STACK_SIZE);
K_THREAD_STACK_DEFINE(sender_stack_medium, STACK_SIZE);
K_THREAD_STACK_DEFINE(sender_stack_low, STACK_SIZE);
K_THREAD_STACK_DEFINE(receiver_stack, STACK_SIZE);

void sender_task(void *priority, void *arg1, void *arg2) {
    struct message msg;
    msg.sender_priority = (intptr_t)priority;
    
    for (int i = 0; i < 5; i++) {
        msg.id = i;
        printk("Sender Task (Priority %d): Sent Message ID %d\n", msg.sender_priority, msg.id);
        k_msgq_put(&my_msgq, &msg, K_NO_WAIT);
        k_sleep(K_MSEC(500));
    }
}

void receiver_task(void *arg1, void *arg2, void *arg3) {
    struct message msg;
    while (1) {
        if (k_msgq_get(&my_msgq, &msg, K_FOREVER) == 0) {
            printk("Receiver: Received Message ID %d from Priority %d\n", msg.id, msg.sender_priority);
        }
    }
}

void main(void) {
    printk("Starting Message Queue Priority Test\n");
    
    struct k_thread sender_thread_high, sender_thread_medium, sender_thread_low, receiver_thread;

    k_thread_create(&sender_thread_high, sender_stack_high, STACK_SIZE,
                    sender_task, (void *)(intptr_t)PRIORITY_HIGH, NULL, NULL,
                    PRIORITY_HIGH, 0, K_NO_WAIT);

    k_thread_create(&sender_thread_medium, sender_stack_medium, STACK_SIZE,
                    sender_task, (void *)(intptr_t)PRIORITY_MEDIUM, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);

    k_thread_create(&sender_thread_low, sender_stack_low, STACK_SIZE,
                    sender_task, (void *)(intptr_t)PRIORITY_LOW, NULL, NULL,
                    PRIORITY_LOW, 0, K_NO_WAIT);

    k_thread_create(&receiver_thread, receiver_stack, STACK_SIZE,
                    receiver_task, NULL, NULL, NULL,
                    PRIORITY_MEDIUM, 0, K_NO_WAIT);
}
