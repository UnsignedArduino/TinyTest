# Database architecture

Rough outline of the database architecture tables and columns. 

## Users

Will be handled by web UI. Using GitHub sign-in to authenticate user, we then get an API key. 

* Id
* Username
* Profile picture URL
* Verified (bool)
* Admin (bool)
* API key

## Games

Will be used by web for read only. 

* Id
* Sprt (sprt id)
* Result (queued, running, canceled, error, white mate, black mate, draw)
* Queue, start, end times
* Executor (user id)
* FEN (text)
* PGN (text)

## Sprts

Will be used by both client and web. Uses API token to authenticate. Admin privileges needed to start and approve SPRTs.
Need to be verified to claim games to run. 

* Id
* Engine 1 (git url, commit, build configuration id)
* Engine 2 (git url, commit, build configuration id)
* Sprt Params (elo 1, elo 2, alpha, beta, game count, time control, book)
* Queued games (int)
* Running games (int)
* Finished games (white mates, black mates, draws, canceled, errors)
* Result (queued, running, canceled, error, elo diff)
* Scheduled by (user id)
* Queue, start, end times
* Priority
* Approved by (user id | null)
* Paused (bool)

## Build configurations

Will be used by both client and web. Reading does not need authentication, writing needs admin privileges.  

* Id
* Name (ex. TinyChess debug, Stockfish release, Lc0 debug)
* Build commands
