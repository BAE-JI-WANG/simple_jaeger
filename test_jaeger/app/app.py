from flask import Flask, request
from jaeger_client import Config
import logging
import time

app = Flask(__name__)

def init_tracer(service_name='simple-service'):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service_name,
    )
    return config.initialize_tracer()

tracer = init_tracer()

@app.route('/')
def index():
    with tracer.start_span('index') as span:
        span.log_kv({'event': 'index', 'value': 'Hello, World!'})
        time.sleep(1)
        return 'Hello, World!'

@app.route('/trace')
def trace():
    with tracer.start_span('trace') as span:
        span.log_kv({'event': 'trace', 'value': 'This is a trace'})
        time.sleep(1)
        return 'This is a trace'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)