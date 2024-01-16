"""
Author:     Michael Ababio
Main file for garage services
Wrapper Garage services for Triggering garage door to open and close and getting garage state
This service is used by Tesla-Automation-Platform-Control-Panel
This service needs to have Raspberry Pi listening to
redis pubsub for garage requests. and updating redis with garage state
"""
from enum import Enum
from fastapi import FastAPI
import redis

app = FastAPI()

r = redis.Redis(
    host='redis-pub-sub',
    port=6379,
    decode_responses=True
)


class GarageRequest(Enum):
    """
    Narrow down the possible states for garage and failure due to invalid state
    """

    OPEN = 'open'
    CLOSED = 'close'


def publish_garage_request(request: GarageRequest):
    """
    :param request:
    :return:
    Publish garage request to redis pubsub
    """
    try:
        r.publish('garage-request', request.value)
        return {"message": f"publishing {request.value} to redis"}
    except redis.exceptions.RedisError as e:
        return {"message": f"publishing the following error: {e}"}


@app.put("/request_garage_change/{state}")
def request_garage_change(state: str):
    """
    :rtype: object
    API endpoint to set garage state
    """
    if state.lower() not in GarageRequest.__members__:
        return {"message": f"state {state} is not a valid state. "
                           f"Valid states are {GarageRequest.__members__}"}
    publish_garage_request(GarageRequest(state.lower()))
    return {"message": f"setting state to {state}"}


@app.get("/get_state")
def get_state():
    """
    :rtype: object
    API endpoint to get garage state. Which is stored in redis by raspberry pi
    """
    try:
        state = r.get('garage-state')
        return state
    except redis.exceptions.RedisError as e:
        return {"message": f"getting the following error: {e}"}
