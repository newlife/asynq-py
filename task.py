import uuid
import time
import json
from datetime import datetime, timedelta

TaskState = {"active": 1, "pending": 2, "scheduled": 3, "retry": 4, "archived": 5}

DefaultMaxRetry = 25
DefaultTimeout = 30 * 60


class Task:
    def __init__(self, type_name, payload):
        self.type = type_name
        self.payload = payload

    @property
    def bytes_payload(self):
        return json.dumps(self.payload).encode()


class Option:
    def __init__(self):
        self.retry = DefaultMaxRetry
        self.queue = "default"
        self.timeout = DefaultTimeout
        self.deadline = None
        self.unique_ttl = 0
        self.process_at = time.time


class TaskInfo:
    def __init__(self, args):
        self.id = uuid.uuid4()  # ID is a unique identifier for each task.
        self.type = ""
        # Type indicates the kind of the task to be performed , user defined

        self.queue = "default"
        # Queue is a name this message should be enqueued to.

        self.payload = b""  # Payload holds data needed to process the task
        self.max_retry = 0  # Retry is the max number of retry for this task.
        self.retried = 0
        # Retried is the number of times we've retried this task so far.

        self.error_msg = ""
        # ErrorMsg holds the error message from the last failure.
        self.last_failed_at = time.time()
        # Time of last failure in Unix time,
        # the number of seconds elapsed since January 1, 1970 UTC.
        # Use zero to indicate no last failure
        self.timeout = 0
        # Timeout specifies timeout in seconds.
        # If task processing doesn't complete within the timeout,
        # the task will be retried
        # if retry count is remaining.
        # Otherwise it will be moved to the archive.

        # Use zero to indicate no timeout.
        self.deadline = 0
        # Deadline specifies the deadline for the task in Unix time,
        # the number of seconds elapsed since January 1, 1970 UTC.
        # If task processing doesn't complete before the deadline,
        # the task will be retried
        # if retry count is remaining.
        # Otherwise it will be moved to the archive.

        # Use zero to indicate no deadline.
        self.unique_key = ""
        # UniqueKey holds the redis key used for uniqueness lock for this task.
        # Empty string indicates that no uniqueness lock was used.

    @property
    def task_key(self):
        return f"asynq:{self.queue_name}:{self.id}"

    @property
    def pending_key(self):
        return f"asynq:{self.queue_name}:pending"
