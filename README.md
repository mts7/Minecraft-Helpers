# Minecraft-Helpers

Minecraft helper utilities written in Python 3.7+

## give.py

This module handles giving items to players. It is incomplete, but has a basic menu system that can track which item to
give. It will soon have the ability to add enchantments to the item, then give the item to a player.

### Usage

```shell
python3 -m src.main give
```

Follow the prompts to see what is available.

Future ideas include

* Creating a command with the current selections
* Adding an all item for enchantments
* Adding a done option/key when finished selecting enchantments
* Adding the selected enchantments (at maximum level) to the item
* Naming the item
* Providing the name of the player (or use `@p` as default)
* Directly sending the `/give` command to the screen session (instead of displaying it)
* Adding mutual exclusions to specific item enchantments
* Providing an option for adding lore to the item
* Add the option for specifying quantity (rather than defaulting to `1`)
* Adding a blocks category

---

## server_actions.py

This module handles the basics for getting a Minecraft server up and running. Pass command line arguments for better
handling of the actions. To facilitate better handling, this sends all commands to the specified screen.

### Usage

All usages print whatever is returned by the call.

---

```shell
python3 -m src.main check
```

Check the screen name for existence.

This will only do the screen check. Start the screen session with `screen`.

---

```shell
python3 -m src.main date
```

Send the current date and time to the players.

This is useful for alerting players of the time in case of playing for hours with no real sense of the current time.
This can be used in a cron job as indicated below.

`*/30 * * * * python3 server-actions.py date > /dev/null`

---

```shell
python3 -m src.main get
```

Get the command string for starting the server.

This compiles the command string (based on the variables and configuration) and returns it to the caller.

---

```shell
python3 -m src.main restart
```

Restart the server.

This script calls the stop action (which waits for the provided number of seconds)
and then it calls the start action. This is merely a shortcut
for `python3 server-actions.py stop && python3 server-actions.py start`.

---

```shell
python3 -m src.main screen
```

Start the screen with the provided name if it is not already started.

NOTE: This appears to be broken and will need further investigation.

---

```shell
python3 -m src.main status
```

Check to see if the server is running.

This checks `ps` to see if the specified (in the code) Java executable is running with `minecraft` somewhere in the
command. Example: `/usr/bin/java -jar minecraft_server.jar nogui`
It returns a Boolean value.

---

```shell
python3 -m src.main start
```

Start the server according to the compiled command string.

This script first checks to see if the server is running. If it is running, the script will return void. If the server
is not yet running, send the start command string to the specified screen. There is no return for a successful start.
Once the command is sent, the script waits for 50 seconds before returning.

---

```shell
python3 -m src.main stop
```

Stop the server.

This sends the stop command to the screen, which should stop the server.

---

```shell
python3 -m src.main verify
```

Check to see if the server is running. If the server is not running, start the server.

This script is useful for cron jobs to ensure the server is up and running at the desired interval. The line below will
run the check every fifteen minutes.

`*/15 * * * * python3 -m src.main verify > /dev/null`

## Flask API with wsgi

The API works pretty much like the CLI, even with the same commands (endpoints).

### Usage

```shell
python3 m src.wsgi
```

Get the status of the server.

```
http://127.0.0.1:5000/api/status
```

#### Routes

* /api/check
* /api/date
* /api/command
* /api/restart
* /api/create
* /api/start
* /api/status
* /api/stop

Each of the above routes executes the provided command and does not take any arguments.

## Testing

The below command will execute the tests and display a code coverage report.

```shell
coverage run -m pytest && coverage report
```

## TODO

1. add tests
1. add authentication to the API endpoints
1. build an executable package for pip
