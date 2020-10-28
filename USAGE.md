# `ee`

A salve for timesmiths. 🧴🕰️

**Usage**:

```console
$ ee [OPTIONS] DATES...
```

**Arguments**:

* `DATES...`: Dates/datetimes separated by spaces.
Can be in the style of an epoch timestamp (milliseconds will be ignored) or
in any of the formats specified in EXTRA_DATETIME_INPUT_FORMATS  [required]

**Options**:

* `-c, --copy`: Send output to the clipboard.
* `-p, --plain`: Don't show pretty output, just transformations.
* `-r, --repl`: In an infinite prompt, give an epoch, get a datetime, and vice versa.
Can be controlled with various redundant hotwords:

To exit the repl use: `{'exit', 'done', 'quit', 'q', 'end'}`.
[ctrl + d] and [ctrl + c] also work.

To remove the last item from the list use: `{'d', 'remove', 'rm', 'drop'}`.
To remove arbitrary items, include the 0-based index of the item.
i.e. `drop 3` will drop the 4th item shown on screen.

To send all your conversions to the clipboard, use `{'yy', 'copy', 'cp'}`.
This will exit the repl.

To clear the list use: `{'restart', 'c', 'clear'}`.

To inspect your configuration (env vars) use: `{'config', 'settings', 'variables', 'vars', 'env'}`.

To see this help in the repl use: `{'help', 'h', '?'}`.

* `-v, --version`: Print the version and exit
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
