# asynq-py

related https://github.com/hibiken/asynq/

```
from task import Task, Option
from client import Client

task = Task("test_aa", {"aa": 1})

c = Client()
c.enqueue(task)
```