from client import Client
from task import Task, Option
import time

task = Task("email:welcome", {"UserID": 222})
c = Client()
c.enqueue(task)

option = Option()
at = time.time() + 10
option.process_at = at
task = Task("email:welcome", {"UserID": 232})
c.enqueue(task, option=option)

option.process_at += 10
task = Task("email:welcome", {"UserID": 242})
c.enqueue(task, option=option)
