import random

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

import prometheus_client
import uvicorn


app = FastAPI()

# allow all inputs
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ['*'],
    allow_headers = ['*']
)

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


@app.get("/flip-coins")

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
    uvicorn.run(app, host = '0.0.0.0', port = 15000)