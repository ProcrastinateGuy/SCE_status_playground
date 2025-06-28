import random
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

import prometheus_client
import uvicorn

app = FastAPI()

# allow all inputs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)

# HTTP Status Code
# Informational responses (100 – 199)
# Successful responses (200 – 299)
# Redirection messages (300 – 399)
# Client error responses (400 – 499)
# Server error responses (500 – 599)

# device 1, sends 100
# device 2, sends 200
# device 3, sends 300
# device 4, sends 400
# device 5, sends 500

# device 6, sends "starting up"
# device 7, sends "up"
device7 = prometheus_client.Gauge("up_signal", "device7:up")
# device 8, sends "recoverable error"
# device 9, sends "shutting down"
# device 10, sends "down"
device10 = prometheus_client.Gauge("down_signal", "device10:down")
# device 11, sends "not reachable / no such device"
# device 12, sends "sometimes down (dynamic)"
device12 = prometheus_client.Gauge("mix_signal", "device12:sometimes down")

def rand_float():
    return random.random()


@app.on_event("startup")
async def on_startup():
    # Optionally seed with an initial value
    device7.set(1)
    device10.set(0)

    global value
    value = rand_float()
    device12.set(value)


@app.get("/")
# return to the client as JSON file
def default_access():
    global value
    value = rand_float()
    return {
        "device7": 1,
        "device10": 0,
        "device12": value
    }


@app.get('/metrics')
async def metrics():
    # Simulate a status change each scrape
    global value
    value = rand_float()
    device12.set(value)
    data = prometheus_client.generate_latest()
    return Response(content=data, media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9100)

"""
heads_count = prometheus_client.Counter(
    "heads_count",
    "Number of heads",
)

tails_count = prometheus_client.Counter(
    "tails_count",
    "Number of Tails",
)

flips_count = prometheus_client.Counter(
    "flips_count",
    "Number of Flips",
)


@app.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content = prometheus_client.generate_latest()

    )


@app.get("/generate-status")

async def flip_coins(times = None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code = 400,
            detail = "times must be set in request and must be an integer"
        )

    times_as_int = int(times)

    heads = 0

    for _ in range(times_as_int):
        if random.randint(0,1):
            heads += 1


    tails = times_as_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flips_count.inc(times_as_int)

    # return to the client as JSON file

    return {
        "head": heads,
        "Tail": tails
    }

if __name__ == "__main__":
    initialize()
    uvicorn.run(app, host = '0.0.0.0', port = 15000)"""
