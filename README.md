# asynq-py

related https://github.com/hibiken/asynq/


```python
from client import Client
from task import Task

task = Task("email:welcome", {"UserID": 222})
c = Client()
c.enqueue(task)
```
