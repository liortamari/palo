import flask
import redis
import datetime


app = flask.Flask(__name__)
redis_db = redis.StrictRedis(host='redis', port=6379, socket_timeout=30, decode_responses=True)


def stat_function(f):
    def wrap(*args, **kwargs):
        begin = datetime.datetime.now()
        ret = f(*args, **kwargs)
        end = datetime.datetime.now()
        processing_timer = end - begin
        redis_db.incr("requests_counter")
        redis_db.incr("processing_timer", int(processing_timer.total_seconds()*1000*1000))
        return ret
    return wrap


@app.route('/api/v1/stats')
def stats():
    words_counter = redis_db.get("words_counter")
    requests_counter = redis_db.get("requests_counter")
    processing_timer = redis_db.get("processing_timer")
    response = {
        "totalWords": int(words_counter),
        "totalRequests": int(requests_counter),
        "avgProcessingTimeNs": int(processing_timer) // int(requests_counter) if int(requests_counter) != 0 else 0,
    }
    return flask.jsonify(response)


@app.route('/api/v1/similar')
@stat_function
def similar():
    word = flask.request.args.get('word')
    key = ''.join(sorted(word))
    similar_words = redis_db.smembers(key)
    similar_words.remove(word)
    response = {
        "similar": list(similar_words)
    }
    return flask.jsonify(response)