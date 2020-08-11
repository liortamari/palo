import redis

redis_db = redis.StrictRedis(host='redis', port=6379, socket_timeout=30)
print(redis_db.ping())

words_counter = 0
words_dict = {}
with open("/words_clean.txt") as f:
    for line in f:
        word = line.rstrip()
        key = ''.join(sorted(word))
        words_dict.setdefault(key, set()).add(word)
        words_counter += 1

for word_key, word_val in words_dict.items():
    redis_db.sadd(word_key, *word_val)
redis_db.set("words_counter", words_counter)
redis_db.set("requests_counter", 0)
redis_db.set("processing_timer", 0)
print("COMPLETED")

