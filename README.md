# QueueBot
Simple queue managing bot. Used for creating and managing user queues on Discord.

## Run inside Docker
1) Duplicate the file `bot.env.example` and name it `bot.env`
2) Update `bot.env` with the enviroment keys needed.
3) Build the project with `docker build -t nachiten/queue-bot:local .`
4) Run `docker run --rm --env-file ./bot.env nachiten/queue-bot:local`

**Note:** bot.env is gitignored

## Example bot.env:
```
DISCORD_TOKEN=STRING
CANAL_OUTPUT_COMANDOS_ID=NUMBER
RANGOS_MOD=RANK1NUMBER_RANK2NUMBER
PYTHONUNBUFFERED=1
```

**Important:** All the env listed above are required and none of them should be between "".
