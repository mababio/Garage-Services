from fastapi import FastAPI
import redis

app = FastAPI()


r = redis.Redis(
    host='redis-pub-sub',
    port=6379,
    decode_responses=True
)


def publish(message):
    r.publish('garage-request', message)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/set_state/{state}")
def set_state(state: str):
    # TODO: Add logic to set state
    # TODO: sending message to redis pubsub to open or close garage
    publish(state)
    return {"message": f"setting state to {state}"}


@app.get("/get_state")
def get_state():
    # TODO: Add logic to get state TODO:  getting garage state from redis pubsub where raspberry pi has a contact
    #  sensor that sends message to redis pubsub
    try:
        state = r.get('garage-state')
        return state
    except Exception as e:
        return {"message": f"getting the following error: {e}"}
