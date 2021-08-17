AllServers    = "asynq:servers"    # ZSET
AllWorkers    = "asynq:workers"    # ZSET
AllSchedulers = "asynq:schedulers" # ZSET
AllQueues     = "asynq:queues"     # SET
CancelChannel = "asynq:cancel"     # PubSub channel


DefaultQueueName = "default"

TaskState = {
    "active":1,
    "pending":2,
    "scheduled":3,
    "retry":4,
    "archived":5
}
