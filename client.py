from uuid import uuid4
from constant import DefaultQueueName, AllQueues
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


class Client:
    def __init__(self):
        self.redis = r
        self.opts = {}

    def enqueue(self, task, option=Option()):
        task_message = TaskMessage()
        task_message.id = str(uuid4())
        task_message.type = task.type
        task_message.payload = task.bytes_payload
        task_message.queue = option.queue
        task_message.retry = option.retry

        self.redis.sadd(AllQueues, task_message.queue)
        task_key = f"asynq:{option.queue}:{task_message.id}"
        pending_key = f"asynq:{option.queue}:pending"
        key_list = [task_key, pending_key]
        arg_list = [
            task_message.SerializeToString(),
            task_message.id,
            task_message.timeout,
            task_message.deadline,
        ]
        print(key_list)
        print(arg_list)
        enqueue_cmd = self.redis.register_script(enqueue_script)
        enqueue_cmd(keys=key_list, args=arg_list)
