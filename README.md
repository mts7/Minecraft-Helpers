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

## start.py

This script handles the basics for getting a Minecraft server up and running. Pass command line arguments for better
handling of the actions.

### Usage

All usages print whatever is returned by the call.

```shell
python start.py check
```

Check to see if the server is running.

This checks `ps` to see if the specified (in the code) Java executable is running with `minecraft` somewhere in the
command. Example: `/usr/bin/java -jar minecraft_server.jar nogui`
It returns a Boolean value.

---

```shell
python start.py get
```

Get the command string for starting the server.

This compiles the command string (based on the variables and configuration) and returns it to the caller.

---

```shell
python start.py start
```

Start the server according to the compiled command string.

This script first checks to see if the server is running. If it is running, the script will return void. If the server
is not yet running, send the start command string to the operating system. There is no return for a successful start.
