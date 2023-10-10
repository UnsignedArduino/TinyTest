# Database architecture

Rough outline of the database architecture tables and columns. 

## Users
* Id
* Username
* Hashed password
* Verified (bool)
* Admin (bool)
* Jwt session
* API key

## Games
* Id
* Sprt (sprt id)
* Result (queued, running, canceled, error, white mate, black mate, draw)
* Queue, start, end times
* Executor (user id)
* FEN (text)
* PGN (text)

## Sprts
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
* Id
* Name (ex. TinyChess debug, Stockfish release, Lc0 debug)
* Build commands
