# QueueBot
Simple queue managing bot. Made for creating and managing user queues on Discord.

## Run inside Docker

- 1 - Start by building the project with `docker build -t nachiten/queue-bot:local .`
- 2 - Update `bot.env` with your own `DISCORD_TOKEN` (and other fields, if relevant).
- 3 - Run `docker run --rm --env-file ./bot.env nachiten/queue-bot:local`

Please avoid commiting your changes to `bot.env`.

## Example bot.env:

```
DISCORD_TOKEN=STRING
canalSpamComandosID=NUMBER
canalOutputBotID=NUMBER
rangosMOD=RANK1NUMBER_RANK2NUMBER
PYTHONUNBUFFERED=1
```

Important: All the env listed above are required and none of them should be between "".
