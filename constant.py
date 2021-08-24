from datetime import datetime, timedelta

AllServers = "asynq:servers"  # ZSET
AllWorkers = "asynq:workers"  # ZSET
AllSchedulers = "asynq:schedulers"  # ZSET
AllQueues = "asynq:queues"  # SET
CancelChannel = "asynq:cancel"  # PubSub channel


DefaultQueueName = "default"



