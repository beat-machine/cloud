# cloud

A new collection of services for running The Beat Machine on Google Cloud.

## Subprojects

### `api/` - HTTP API

This is the point of communication with the client. It enqueues new tasks,
reports their statuses, delivers the final results when they finish.

### `worker/` - Audio Processing Worker

This is the code that uses `beatmachine` to apply effects and render the
remixed song.
