import fastapi
import pydantic
import starlette
import cacheout

import enum
import uuid
import time
import logging

from typing import *

app = fastapi.FastAPI()

# Used to track job status. TODO: Should eventually be Redis.
cache = cacheout.Cache(default=False, ttl=256)


class JobStatus(enum.Enum):
    """
    JobStatus is the possible status a queued processing job has.
    """

    waiting = "waiting"  # Waiting for available worker
    processing = "processing"  # Currently being processed
    rendering = "rendering"  # Waiting for ffmpeg to render MP3
    finished = "finished"  # Finished and available

    timed_out = "timed_out"  # Took too long and was canceled
    expired = "expired"  # Finished and removed to free up space

    def __str__(self):
        return self.value


class ProcessingArgs(pydantic.BaseModel):
    """
    ProcessingArgs are common parameters required for all processing jobs.
    """

    min_bpm: Optional[int] = None
    max_bpm: Optional[int] = None
    effects: List[Dict[str, Any]]


class UrlRequest(pydantic.BaseModel):
    """
    A UrlRequest describes a processing job using a song from a remote URL.
    """

    url: str
    args: ProcessingArgs


def new_job_id() -> str:
    """
    Generates a new, unique job ID.
    """

    return str(uuid.uuid4().hex)


@app.post("/submit/file")
async def submit_song_file(
    file: fastapi.UploadFile = fastapi.File(None, media_type="audio/mpeg"),
    args: ProcessingArgs = fastapi.Form(None),
):
    job_id = new_job_id()
    logging.info(f"Started job {job_id}")
    logging.info("TODO: Construct and submit task")
    cache.add(job_id, True)

    return starlette.responses.Response(
        status_code=starlette.status.HTTP_202_ACCEPTED,
        headers={"Location": "/queue/{job_id}"},
    )


@app.post("/submit/url")
async def submit_song_url(args: UrlRequest):
    job_id = new_job_id()
    logging.info(f"Started job {job_id}")
    logging.info("TODO: Construct and submit task")
    cache.add(job_id, True)

    return starlette.responses.Response(
        status_code=starlette.status.HTTP_202_ACCEPTED,
        headers={"Location": f"/queue/{job_id}"},
    )


@app.get("/queue/{job_id}")
async def get_queue_info(job_id: str):
    if cache.get(job_id):
        logging.info("TODO: Query job status")
        return starlette.responses.Response(
            status_code=starlette.status.HTTP_200_OK, content="lalala..."
        )
    else:
        logging.warning(f"Lookup nonexistent job {job_id}")
        return starlette.responses.Response(
            status_code=starlette.status.HTTP_404_NOT_FOUND
        )
