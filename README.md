# Minecraft-Helpers

Minecraft helper utilities written in Python

## give.py

This script handles giving items to players. It is incomplete, but has a basic menu system that can track which item to
give. It will soon have the ability to add enchantments to the item, then give the item to a player.

### Usage

```shell
python give.py
```

Follow the prompts to see what is available.

## server-actions.py

This script handles the basics for getting a Minecraft server up and running. Pass command line arguments for better
handling of the actions. To facilitate better handling, this sends all commands to the specified screen.

### Usage

All usages print whatever is returned by the call.

---

```shell
python server-actions.py check
```

Check to see if the server is running. If the server is not running, start the server.

This script is useful for cron jobs to ensure the server is up and running at the desired interval. The line below will
run the check every fifteen minutes.

`*/15 * * * * python server-actions.py check > /dev/null`

---

```shell
python server-actions.py date
```

Send the current date and time to the players.

This is useful for alerting players of the time in case of playing for hours with no real sense of the current time.
This can be used in a cron job as indicated below.

`*/30 * * * * python server-actions.py date > /dev/null`

---

```shell
python server-actions.py get
```

Get the command string for starting the server.

This compiles the command string (based on the variables and configuration) and returns it to the caller.

---

```shell
python server-actions.py restart
```

Restart the server.

This script calls the stop action (which waits for the provided number of seconds)
and then it calls the start action. This is merely a shortcut
for `python server-actions.py stop && python server-actions.py start`.

---

```shell
python server-actions.py screen
```

Check the screen name for existence and start if it does not exist.

This will do the screen check and start the screen when necessary.

NOTE: This appears to be broken and will need further investigation.

---

```shell
python server-actions.py status
```

Check to see if the server is running.

This checks `ps` to see if the specified (in the code) Java executable is running with `minecraft` somewhere in the
command. Example: `/usr/bin/java -jar minecraft_server.jar nogui`
It returns a Boolean value.

---

```shell
python server-actions.py start
```

Start the server according to the compiled command string.

This script first checks to see if the server is running. If it is running, the script will return void. If the server
is not yet running, send the start command string to the specified screen. There is no return for a successful start.
Once the command is sent, the script waits for 50 seconds before returning.

---

```shell
python server-actions.py stop
```

Stop the server.

This sends the stop command to the screen, which should stop the server.