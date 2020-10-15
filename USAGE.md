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
* `repl`: In an infinite prompt, give an epoch, get a datetime.

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

* `--help`: Show this message and exit.

## `ee repl`

In an infinite prompt, give an epoch, get a datetime. And vice versa.

Can be controlled with various redundant hotwords:

To exit the repl use: `{'quit', 'q', 'end', 'done', 'exit'}`.
[ctrl + d] and [ctrl + c] also work.

To remove the last item from the list use: `{'drop', 'remove', 'd', 'rm'}`.
To remove arbitrary items, include the 0-based index of the item.
i.e. `drop 3` will drop the 4th item shown on screen.

To clear the list use: `{'restart', 'clear', 'c'}`.

To inspect your configuration (env vars) use: `{'settings', 'variables', 'env', 'config', 'vars'}`.

To see this help in the repl use: `{'help', 'h', '?'}`.

**Usage**:

```console
$ ee repl [OPTIONS]
```

**Options**:

* `--tz TEXT`: [default: America/Chicago]
* `--help`: Show this message and exit.
