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
* `repl`: Give an epoch, get a datetime.

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

Give an epoch, get a datetime. And vice versa.

**Usage**:

```console
$ ee repl [OPTIONS]
```

**Options**:

* `--tz TEXT`: [default: America/Chicago]
* `--help`: Show this message and exit.
