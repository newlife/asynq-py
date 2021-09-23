from uuid import uuid4
import time
from datetime import datetime, timedelta

from constant import AllQueues
from task import Option
from proto.asynq_pb2 import TaskMessage
import redis

r = redis.Redis()
r = redis.Redis(host="localhost", port=6379, db=0)

enqueue_script = """
redis.call("HSET", KEYS[1],
           "msg", ARGV[1],
           "state", "pending",
           "timeout", ARGV[3],
           "deadline", ARGV[4])
redis.call("LPUSH", KEYS[2], ARGV[2])
return 1
"""

schedule_script = """
redis.call("HSET", KEYS[1],
           "msg", ARGV[1],
           "state", "scheduled",
           "timeout", ARGV[4],
           "deadline", ARGV[5])
redis.call("ZADD", KEYS[2], ARGV[2], ARGV[3])
return 1
"""

enqueue_unique_script = """
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
        self.redis = r
        self.opts = {}
        self.enqueue_cmd = self.redis.register_script(enqueue_script)
        self.schedule_cmd = self.redis.register_script(schedule_script)
        self.enqueue_unique_cmd = self.redis.register_script(
            enqueue_unique_script)

    def enqueue(self, task, option=Option()):
        task_message = TaskMessage()
        task_message.id = str(uuid4())
        task_message.type = task.type
        task_message.payload = task.bytes_payload
        task_message.queue = option.queue
        task_message.retry = option.retry
        task_message.timeout = option.timeout
        task_message.deadline = option.deadline
        if option.unique_ttl > 0:
            self.enqueue_unique(task_message, option)
        if option.process_at < time.time():
            self.enqueue_now(task_message, option)
        else:
            self.schedule(task_message, option)

    def enqueue_now(self, task_message, option):
        self.redis.sadd(AllQueues, task_message.queue)
        task_key = f"asynq:{{{option.queue}}}:t:{task_message.id}"
        pending_key = f"asynq:{{{option.queue}}}:pending"
        key_list = [task_key, pending_key]
        arg_list = [
            task_message.SerializeToString(),
            task_message.id,
            task_message.timeout,
            task_message.deadline,
        ]

        self.enqueue_cmd(keys=key_list, args=arg_list)

    def schedule(self, task_message, option):
        self.redis.sadd(AllQueues, task_message.queue)
        task_key = f"asynq:{{{option.queue}}}:t:{task_message.id}"
        scheduled_key = f"asynq:{{{option.queue}}}:scheduled"
        key_list = [task_key, scheduled_key]
        arg_list = [
            task_message.SerializeToString(),
            option.process_at,
            task_message.id,
            task_message.timeout,
            task_message.deadline,
        ]

        self.schedule_cmd(keys=key_list, args=arg_list)

    def enqueue_unique(self, task_message, option):
        self.redis.sadd(AllQueues, task_message.queue)
        task_key = f"asynq:{{{option.queue}}}:t:{task_message.id}"
        pending_key = f"asynq:{{{option.queue}}}:pending"
        key_list = [task_key, pending_key]
        arg_list = [
            task_message.SerializeToString(),
            option.process_at,
            task_message.id,
            task_message.timeout,
            task_message.deadline,
        ]
        self.enqueue_unique_cmd(keys=key_list, args=arg_list)
