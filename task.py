import uuid
import time


class TaskInfo:
    def __init__(self, args):
        self.type = ""
        # Type indicates the kind of the task to be performed , user defined

        self.payload = {}  # Payload holds data needed to process the task
        self.id = uuid.uuid4()  # ID is a unique identifier for each task.
        self.queue = "default"
        # Queue is a name this message should be enqueued to.
        self.retry = 0  # Retry is the max number of retry for this task.
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


class Task:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

    def enqueue(self, option):
        pass
