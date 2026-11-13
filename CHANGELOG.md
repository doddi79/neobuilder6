# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [6.1.0] - 2026-11-14

### Added

- GitHub workflows (like the original ones, minus the Docker image stuff):
  unit tests on Python 3.10-3.14 for pushes to `main` and all pull requests,
  and publishing to PyPI when a GitHub release is created (with a check that
  the release tag matches the package version). The tests install
  `protoplasm6` from the branch with the same name in its repo (or `main`)
- Proto package alias imports
  ([neobuilder#2](https://github.com/ccpgames/neobuilder/issues/2)): The
  `__init__.py` of every generated directory that matches a proto package now
  star imports all the dataclass modules (`*_dc.py`) of that package (with a
  static `__all__`) so e.g. `from myshop.orders import *` gets you every
  message and enum in the `myshop.orders` proto package, no matter which
  `.proto` file they're in. On by default; use `--no-alias-imports` (or
  `NeoBuilder(alias_imports=False)`) to skip it
- A `metadata` argument on generated gRPC clients (for Protoplasm6 6.1's call
  metadata, e.g. authorization headers)
- A task-oriented [Public API index](docs/api-index.md) (for humans and LLMs
  alike)


## [6.0.0] - 2026-11-14

Forked and renamed!!

### Added

- This project by forking [`neobuilder`](https://github.com/ccpgames/neobuilder)
  (v5.3.1) in order to continue its development and maintenance
- A `neobuild6` CLI command (an alias for `neobuild`)
- Official support (as in: unit tests) for Python 3.10, 3.11, 3.12, 3.13 and
  3.14
- A `--no-pyi` CLI flag to skip building `*.pyi` type stubs (see below)

### Changed

- Renamed the package (and the module) from `neobuilder` to `neobuilder6`
- Building `*.pyi` type stubs for the `*_pb2.py` files (so IDEs and type
  checkers understand them) is now on by default; use `--no-pyi` to skip it
  (the `include_pyi` argument of `NeoBuilder` now defaults to `True`)
- Generated code now imports `protoplasm6` instead of `protoplasm`
- Now depends on [`protoplasm6`](https://github.com/doddi79/protoplasm6)
  instead of `protoplasm`
- Replaced the dependency on `ccptools` with its continuation fork
  [`batutils`](https://github.com/doddi79/batutils)
- `grpcio-tools` is now a direct dependency (it's what runs `protoc`, it used
  to be pulled in via `protoplasm`), now `>=1.80, <2` which generates code for
  `protobuf` 7
- Use `FieldDescriptor.is_repeated` instead of the `FieldDescriptor.label`
  that was removed in `protobuf` 7
- The CLI help now says `neobuild` (instead of the script path) and lists the
  Neobuilder6 and Protoplasm6 versions
- Modernized packaging metadata (SPDX license, `requires-python`)

### Removed

- Official support for Python 3.8 and 3.9 (`requires-python` is now `>=3.10`,
  as required by `protobuf` 7 anyway)
- Python <3.9 compatibility code paths (`pkg_resources` fallbacks)
- All of the old CCP GitHub workflows (unit tests and PyPI publishing), for
  now at least

### Fixed

- `repeated google.protobuf.Value` (and `Struct` and `ListValue`) fields
  getting the type hint and default value of a single field (e.g.
  `typing.Any` with a `...` default instead of `typing.List[typing.Any]` with
  an empty list) and maps of them getting the wrong value type hint (e.g.
  `typing.Dict[str, typing.Any]` instead of
  `typing.Dict[str, typing.Dict[str, typing.Any]]` for
  `map<string, google.protobuf.Struct>`)
- `VERSION` files with a 4-part version number (e.g. `4.11.2.0`) failing to
  parse (and silently falling back to a calculated version) because the
  version string's first 3 _characters_ were used instead of its first 3
  _parts_
- Reading the last version of a package whose `__version__` is a tuple of
  ints


---

_Everything below is the history of the original
[`neobuilder`](https://github.com/ccpgames/neobuilder) package by CCP Games._

## [5.3.1] - 2024-10-15

### Added

- The `-i`/`--pyi` option to the CLI to include building `*.pyi` files for the generated `*_pb2.py` files
- The ability to include multiple additional proto paths with `-I <path>`/`--include <path>` flags in the CLI


## [5.3.0] - 2024-09-24

### Added

- Support for the `google.protobuf.Value` message


## [5.2.1] - 2024-09-24

### Changed

- The line `from typing import *` in most templates to `import typing` and now 
  references to classes an such from `typing` are explicit (i.e. `List` -> 
  `typing.List`) 

### Fixed

- Side-effects caused by `from typing import *` when messages/classes share a 
  name of classes in the `typing` package
- Bug where `datetime` was missing from imports in gRPC senders and receivers


## [5.2.0] - 2024-09-23

### Added

- Support for the `google.protobuf.Struct` message


## [5.1.2] - 2024-07-02

### Fixed

- An issue with the last fix where, if the build root is a relative path, we'll 
  end up getting an exception because we can't find how one path is relative to 7
  another if one of them is absolute and the other is relative.


## [5.1.1] - 2024-06-28

### Fixed

- An issue where the `__everything__.py` file was missing the first character of
  the package name if the build root ended with a slash (or backslash)


## [5.1.0] - 2024-04-30

### Added

- A class attribute called `__servicer_cls__` to any service interfaces (for 
  a gRPC build) with reference to that services `GrpcServicer` class
- Added a bunch of useful sub-tests to unittests

### Fixed

- A bunch of unittesting issues

## [5.0.0] - 2024-04-15

### Changed

- Moved this entire project over to Github 
- Bumped the version in order to not confuse older stuff that doesn't expect 
  protoplasm to exist in Pypi.org (if we end up migrating this there and 
  just open-sourcing the whole thing)
  - Also in case something changes in the API while migrating, cause I tend 
    to fiddle with the code and tidy up and refactor when moving stuff
