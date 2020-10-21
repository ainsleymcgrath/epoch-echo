# `ee`

A salve for timesmiths 🧴🕰️

**Usage**:

```console
$ ee [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `flip`: `repl` without the prompt.
* `repl`: In an infinite prompt, give an epoch, get a...

## `ee flip`

`repl` without the prompt.
Takes a list of dates/timestamps (mixing them works fine)

**Usage**:

```console
$ ee flip [OPTIONS] DATES...
```

**Arguments**:

* `DATES...`: [required]

**Options**:

* `--copy / --no-copy`: [default: False]
* `--plain / --no-plain`: [default: False]
* `--help`: Show this message and exit.

## `ee repl`

In an infinite prompt, give an epoch, get a datetime, and vice versa.

Can be controlled with various redundant hotwords:


To exit the repl use: [31m{'end', 'q', 'quit', 'done', 'exit'}[0m.
[ctrl + d] and [ctrl + c] also work.

To remove the last item from the list use: [31m{'drop', 'rm', 'd', 'remove'}[0m.
To remove arbitrary items, include the 0-based index of the item.
i.e. `drop 3` will drop the 4th item shown on screen.

To send all your conversions to the clipboard, use [31m{'yy', 'cp', 'copy'}[0m.
This will exit the repl.

To clear the list use: [31m{'c', 'restart', 'clear'}[0m.

To inspect your configuration (env vars) use: [31m{'settings', 'vars', 'variables', 'env', 'config'}[0m.

To see this help in the repl use: [31m{'h', 'help', '?'}[0m.


**Usage**:

```console
$ ee repl [OPTIONS]
```

**Options**:

* `--tz TEXT`: [default: America/Chicago]
* `--help`: Show this message and exit.
