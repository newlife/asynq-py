from constant import DefaultMaxRetry, DefaultQueueName, AllQueues

r = redis.Redis()


class Option:
    def __init__(self):
        self.retry = DefaultMaxRetry
        self.queue = DefaultQueueName
        self.timeout = 0
        self.deadline = None
        self.processAt = None


lua = """
local ok = redis.call("SET", KEYS[1], ARGV[1], "NX", "EX", ARGV[2])
if not ok then
  return 0
end
redis.call("HSET", KEYS[2],
           "msg", ARGV[3],
           "state", "pending",
           "timeout", ARGV[4],
           "deadline", ARGV[5],
           "unique_key", KEYS[1])
redis.call("LPUSH", KEYS[3], ARGV[1])
return 1
"""


class Client:
    def __init__(self):
        self.redis = None
        self.opts = {}

    def enqueue(self, task):
        self.redis.sadd(AllQueues, task.queue)
        key_list = [task.key_name, task.pending_key]
        arg_list = []