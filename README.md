# QueueBot
Simple queue managing bot. Made for creating and managing user queues on Discord.

## Run inside Docker

Start by building the project with `docker build -t nachiten/queue-bot:local .`, then update `bot.env` with your own `DISCORD_TOKEN` (and other fields, if relevant). Then run `docker run --rm --env-file ./bot.env nachiten/queue-bot:local`.

Please avoid commiting your changes to `bot.env`.
