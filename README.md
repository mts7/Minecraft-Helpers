# Minecraft-Helpers

Minecraft helper utilities written in Python 3.7+

## give.py

This script handles giving items to players. It is incomplete, but has a basic menu system that can track which item to
give. It will soon have the ability to add enchantments to the item, then give the item to a player.

### Usage

```shell
python give.py
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

## mts_logger.py

This is the logger class that logs messages to the standard output, standard error, or a file.

### Usage

```python
import mts_logger

# available log levels are error, warning, info, and debug
# warning is the default log level
logger = mts_logger.Logger('info')

# log to stdout
logger.info('This goes to stdout since there were no options.')

# log to stderr
logger.error('This goes to stderr with the default settings.')

# send errors to stdout instead
logger.use_error = False
logger.error('This goes to stdout instead.')

# configure to send all logs to stderr
logger.output = 'error'
logger.warning('This goes to stderr')

# log to a file
logger.output = 'file'
logger.log_file = 'log.txt'
logger.error('This goes to the log.txt file.')
```

When logging to stdout or stderr, colors are provided in the output. Colors do not go to files. Files are written in
append mode rather than write mode so that the previous contents are preserved.

Future ideas include

* Logging to third-party services
* Handling a second parameter that serializes to JSON
* Logging to an external script/program

#### Variables

##### log_file

The full path of the file used for writing. This must be combined with the `output = 'file'` option.

##### message_colors

This contains the 4 log modes and their corresponding colors.

##### modes

The list of error modes in order of revelation. See `write` for details.

##### outputs

This contains the allowed outputs.

##### output

This defaults to `out` and corresponds with one of the available keys in `outputs`.

##### use_error

This defaults to `True` and is used only when `output` is `out` and `error` is called. If this is `False`, `error` will
write to `stdout`.

#### Methods

##### log(message)

Log output using the current mode. Set the mode when instantiating the object. This is an alias for one of the other
methods.

##### debug(message)

Log output with a light yellow background and black foreground.

##### info(message)

Log output with a light cyan foreground.

##### warning(message)

Log output with a light yellow foreground.

##### error(message)

Log output with a red foreground.

##### write(level, message)

Write the actual message, based on the level and output selected. This is the actual method used for writing the log
messages and is called by the other four methods.

The logger uses the log level to determine if the log message will be written. If the current mode is `warning` and the
current log level is `debug`, the log message will not be written.

---

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