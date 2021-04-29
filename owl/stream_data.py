import json
		

class Producer:
    def __init__(self, redis, stream_queue, expire_time=10, timeout=5):
        self.id = id
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time     
        self.refresh = 1
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.end()

    def emit(self, data):
        data_bytes = json.dumps(data)
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", data_bytes)
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)

    def end(self):
        self.redis.rpush(f"owl:stream_queue:{self.stream_queue}", b"")
        self.redis.expire(f"owl:stream_queue:{self.stream_queue}", self.expire_time)


class Consumer:
    def __init__(self, redis, stream_queue, expire_time=10, timeout=5):
        self.redis = redis
        self.stream_queue = stream_queue
        self.expire_time = expire_time     
        self.refresh = 1
        self.timeout = timeout

    def __iter__(self):
        return self

    def __next__(self):        
        resp = self.redis.blpop(f"owl:stream_queue:{self.stream_queue}", self.timeout)
        if resp is None:
            raise StopIteration

        data_bytes = resp[1]        

        if data_bytes != b"":
            return json.loads(data_bytes)
        else:
            raise StopIteration            


