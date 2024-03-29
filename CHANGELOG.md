## 1.1.3

### New

- The following input formats are now supported by default in addition to the original `YYYY-MM-DD`:
`"MM-DD-YY", "MMM DD YYYY", "MMM D YYYY", "MMM D YY", "MMM DD YY"`

## Fixes

- A link to Pendulum docs is more specific now.

## 1.1.2

### New

- A new option (on by default) shows a heads up of what timezone you're using. Toggle it with `EE_TZ_SHOW_HEADS_UP`.

### Breaks

- Environment variables are now prefixed with `EE_` to avoid collisions. Old-style env vars will not work anymore.

### Fixes

- The changelog entry below. It had the wrong version! :sweat_smile:

## 1.1.1

### Fixes
- A bug where pressing <enter> repeatedly at the REPL would break it
- Leaky state that was damaging tests. TY, closures!
- An evergreen test case that was passing erroneously.

### Changes
- The arrangement of some code. `content.py` was not a descriptive name and confused the sole maintainer. `repl_content_state` is what's actually happening there.

## 1.1.0

:tada: Mostly code cleanup, a good deal of refactoring.

### Changes

- Dependency upgrades
- Mypy is here--types are hinted.

## 1.0.2

### New

- The `--show-config` flag will do just that!

### Changes

- The gifs have been replaced with cleaner SVGs
- Removed excess 'config' hotwords.
- Usage docs updated

## 1.0.1

### Fixes

- `--version` was referred to as `--value` in docs--no longer.

### Changes

- calling `ee` with no arguments or options displays help

## 1.0.0

### Breaks

- The old API. There are no more subcommands. `ee` now has the behavior formerly known as `ee flip` and `ee -R` now gives you what was formerly `ee repl`

### Fixes

- `--repl` can't be called with other args/options

## 0.1.14

### New

-  `ee --version` is a thing now.

## 0.1.13

### Changes

- Use `__init__.py` and stop being weird
- Remove failed releases from changelog
- Update README so you can install for real.

## 0.1.12

### New

- `copy` is available as a hotword in `repl` to send conversions to your clipboard.
- `--copy` is available for `flip` to do the same thing.
- `--plain` added to flip for simplified output.

### Fixes

- Test coverage continues to improve.

### Breaks

- Ironically, tests fail on CI.

## 0.1.1 - (2020-10-14)

Damn near a refactor.

### New

- Significantly richer repl experience with interactive docs
- Environment variable configuration, which you can inspect in the repl
- Generally more coherent implementation

###  Fixes

- Leaky state in `repl`
- Lack of tests
- Unused settings
- Undocumented hotwords


## 0.0.7 - (2020-10-13)

### Fixes

* This doc was wrong (incorrectly labeled 0.0.6)
* Rebase mistake left gif paths broken

## 0.0.6 - (2020-10-13)

### Fixes

* Gifs were borked because I wasn't using relative paths.

## 0.0.5 - (2020-10-13)

### Changes

* Gifs in the docs!

## 0.0.4 - (2020-10-13)


### New

* Docs 📖 Ironically including this document 🤔 Trying out generated usage docs from typer-cli.


## 0.0.3 - (2020-10-13)

### New

* Everything! Welcome to the world, `ee-cli` 🎉
