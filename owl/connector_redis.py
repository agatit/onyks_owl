import connector_base

class Connector(connector_base.Connector):
    
    def __init__(self, config: dict):
        self.stream_queue_limit = config.get('stream_queue_limit', 100)
        self.task_expire_time = config.get('task_expire_time', 10)
        self.stream_expire_time = config.get('stream_expire_time', 10)
        self.task_timeout = config.get('task_timeout', 10)
        self.stream_timeout = config.get('stream_timeout', 10)

    def task_get(self, queue):
        return self.redis.blpop(f"owl:task_queue:{self.task_queue}", self.task_timeout)

    def task_put(self, queue, task):
        p = self.redis.pipeline()  
        p.rpush(queue, task)
        p.expire(queue, self.task_expire_time)
        p.execute()          


    def task_size(self):
        pass

    def stream_put(self, queue):
        pass

    def stream_get(self, queue):
        pass

    def stream_size(self, queue):
        pass    