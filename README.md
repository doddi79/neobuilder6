# NeoBuilder6

Builds Neobuf Packages from Protobuf files using Protoplasm6! :D

## Note

This is a fork of the [`neobuilder`](https://github.com/ccpgames/neobuilder)
package (v5.3.1) by CCP Games, made in order to continue its development and
maintenance. The package _and_ module are now called `neobuilder6` (starting
at version 6.0.0) and the code it generates uses
[`protoplasm6`](https://github.com/doddi79/protoplasm6) (the fork of
`protoplasm`).

## What it does

Given a directory of `*.proto` files, Neobuilder6 builds a Python package
("Neobuf package") containing, for each `foo.proto`:

| File                    | What                                                                               |
|-------------------------|------------------------------------------------------------------------------------|
| `foo_pb2.py`            | The plain `protoc` generated protobuf code                                         |
| `foo_pb2.pyi`           | Type stubs for `foo_pb2.py` so IDEs and type checkers understand it (skip with `--no-pyi`) |
| `foo_pb2_grpc.py`       | The plain `protoc` generated gRPC code (if `foo.proto` has a `service`)            |
| `foo_dc.py`             | Python dataclasses for every message and enum, extending Protoplasm6's `DataclassBase` |
| `foo_api.py`            | Interface classes for every `service` with plain Python methods per RPC            |
| `foo_grpc_receiver.py`  | gRPC servicers that forward calls to your implementation of the interface          |
| `foo_grpc_sender.py`    | gRPC clients that implement the interface by calling a remote service              |

...along with `__init__.py` files everywhere, a root `__init__.py` with a
`__version__` (and the Protoplasm6 and Neobuilder6 versions used), a
`VERSION` file and an `__everything__.py` module that imports every module
(call `your_package.load_symbols()` to make sure the protobuf symbol database
knows every message, e.g. for `Any` unpacking).

See the [Protoplasm6 README](https://github.com/doddi79/protoplasm6) for how
to use the generated code.

## Installation

```
pip install neobuilder6
```

This installs Protoplasm6, `grpcio-tools` (which provides `protoc`) and creates
the `neobuild` command (and its alias `neobuild6`) in Python's `Scripts`/`bin`
folder. Neobuilder6 requires Python 3.10+.

## Usage

Assuming you've got a package called `sandbox` and you're storing your
protobuf files in a directory called `proto` (i.e. `./proto/sandbox/**.proto`)
and you want to spit out the build into the directory `build` just go:

```
neobuild sandbox
```

The resulting `./build/sandbox` package depends on `protoplasm6` (with the
same major version and the same or later minor version as the Neobuilder6
used to build it) and on a `protobuf` runtime matching the `grpcio-tools` that
built it (the `*_pb2.py` files check this when imported).

You can also run it from Python:

```python
from neobuilder6.neobuilder import NeoBuilder

NeoBuilder(package='sandbox', protopath='./proto', build_root='./build').build()
```

### Versioning your package

If you place a plain text file called `VERSION` in the root of your proto
package (e.g. `./proto/sandbox/VERSION` from the example above) and skip any
versioning parameters (`--major`/`-m` or `--patch`/`-p`) Neobuilder6 will use
that file for versioning.

The first line in the file should be the semantic version number (`x.y.z`,
and if there's a 4th part like in `x.y.z.a` it's ignored) and any following
lines are treated as a "commit message" that's written to the built package's
`VERSION` file.

Without a `VERSION` file, the version of the previous build (if found in the
build root) is bumped (minor by default) or `0.1.0` is used for a first build.

### Full CLI usage

```
usage: neobuild [-h] [-m | -p] [-b [BUILDROOT]] [-v] [-i | --pyi | --no-pyi] [-I INCLUDE]
                package [protopath]

Builds neobuf packages with protoplasm6.

positional arguments:
  package               Package name
  protopath             Path to the root of the protobuf files (default="./proto")

options:
  -h, --help            show this help message and exit
  -m, --major           Bump the major version number instead of the minor
  -p, --patch           Bump the patch version number instead of the minor
  -b, --buildroot [BUILDROOT]
                        Path to the root of the output build files (default="./build")
  -v, --verbose         Spits out DEBUG level logs
  -i, --pyi, --no-pyi   Builds *.pyi type stubs for the pb2 files as well (default=True, use --no-
                        pyi to skip)
  -I, --include INCLUDE
                        Optional additional proto paths to include (can be used multiple times)

Neobuilder6 v6.0.0 - Protoplasm6 v6.0.0
```

## Neobuilder6 & Protoplasm6 (the chicken and the egg)

The two packages depend on each other in a slightly odd way:

- **Neobuilder6 depends on Protoplasm6** at build time (it uses some of its
  utilities, e.g. for type casting and method I/O types) and the code it
  generates imports Protoplasm6 at runtime.
- **Protoplasm6 depends on Neobuilder6 only for its unit tests**, which use
  Neobuilder6 to build the protos they test against. It's installed with
  `--no-deps` there to avoid a circular install.

### Versioning

The versioning of Neobuilder6 and Protoplasm6 (major and minor versions) go
hand in hand; i.e. when Protoplasm6's major or minor versions bump, a new
Neobuilder6 should also be released with the same major and minor version,
even if there's no actual code change needed in Neobuilder6 to support
whatever changed in Protoplasm6.

Neobuilder6 releases are NOT guaranteed to be backwards compatible with older
versions of Protoplasm6 and trying to run Neobuilder6 built code with a
Protoplasm6 release whose major and/or minor versions lag behind will more
often than not just break. A difference in the patch version should most
often be fine, as should using a Protoplasm6 release that's one or more minor
versions ahead of the Neobuilder6 used to build code.

In order to keep this synchronous development and release simple, Neobuilder6
should generally NOT depend on new features added to the Protoplasm6 release
with the same version, so that it can build code for its corresponding
Protoplasm6 version without having that latest version actually installed.

### Releasing

1. Release Protoplasm6 first (its unit tests need Neobuilder6, installed with
   `--no-deps`, e.g. straight from its `main` branch or a sibling checkout)
2. Then release Neobuilder6 (which can then pull the new Protoplasm6 from
   PyPI)

## Development

With both repos checked out side by side:

```
python -m venv .venv
.venv/Scripts/activate   # or: source .venv/bin/activate
pip install -e ../protoplasm6
pip install -e .
python -m unittest discover -v -f ./tests
```
