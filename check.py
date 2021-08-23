from proto.asynq_pb2 import TaskMessage
import json

task_message = TaskMessage()
task_message.type = "my_type"
task_message.id = "sddsdsd"
task_message.payload = bytes(json.dumps({"uid": 100}), "utf8")
