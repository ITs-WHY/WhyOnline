import redis
import time
r = redis.Redis(host='localhost', port=6379, db=0, charset='utf8', decode_responses=True)

r.set('mobile', '123')
r.expire('mobile', 1)
print(r.get('mobile'))

time.sleep(2)
print(r.get('mobile'))
