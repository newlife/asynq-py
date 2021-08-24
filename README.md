# asynq-py

related https://github.com/hibiken/asynq/

```
from client import Client
from task import Task

task = Task("email:welcome", {"UserID": 222})
c = Client()
c.enqueue(task)
```