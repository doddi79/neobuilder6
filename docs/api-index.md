# Neobuilder6 Public API Index

Task-oriented reference for using `neobuilder6` (distribution `neobuilder6`,
import `neobuilder6`, CLI `neobuild` / `neobuild6`). Covers the working tree
for version **6.2.0** (see [`neobuilder6/__init__.py`](../neobuilder6/__init__.py)).

Neobuilder6 is the build-time half of a pair: it compiles `.proto` files and
generates Python code that runs on [`protoplasm6`](https://github.com/doddi79/protoplasm6).
For *using* the generated code (dataclasses, services, clients, errors,
metadata, converters) see the
[Protoplasm6 Public API index](https://github.com/doddi79/protoplasm6/blob/main/docs/api-index.md).

## Find it by task

| I want to...                                             | Use |
|----------------------------------------------------------|-----|
| Build a Python package from a directory of `.proto` files | [`neobuild <package>`](#command-line) |
| Build from Python code / a build script                  | [`NeoBuilder(...).build()`](#python-api) |
| Version the generated package                            | [`VERSION` file or `-m`/`-p`](#versioning) |
| Include protos from other directories (imports)          | [`-I/--include`](#command-line) |
| Get IDE/type checker support for `*_pb2.py`              | [`.pyi` stubs (on by default)](#command-line) |
| `from my.proto.package import *` like the proto package  | [Alias imports (on by default)](#package-alias-imports) |
| Know what files/classes get generated and their names    | [Generated layout](#generated-layout) |
| Make `Any` unpacking find every message                  | [`load_symbols()`](#generated-layout) |

## Command line

[Source](../neobuilder6/cli/neobuilder.py)

```
neobuild [-m | -p] [-b BUILDROOT] [-v] [--pyi | --no-pyi] [--alias-imports | --no-alias-imports]
         [-I INCLUDE ...] package [protopath]
```

| Argument                       | Default     | Meaning |
|--------------------------------|-------------|---------|
| `package`                      | (required)  | Root proto/Python package, i.e. `<protopath>/<package>/**.proto` |
| `protopath`                    | `./proto`   | Root of the proto files (the `-I` root for `protoc`) |
| `-b, --buildroot`              | `./build`   | Output root; the package ends up in `<buildroot>/<package>` |
| `-m, --major` / `-p, --patch`  | minor bump  | How to bump the previous build's version when there's no `VERSION` file |
| `-v, --verbose`                | off         | DEBUG logging |
| `-i, --pyi` / `--no-pyi`       | on          | Generate `*_pb2.pyi` type stubs |
| `--alias-imports` / `--no-alias-imports` | on | [Package alias imports](#package-alias-imports) |
| `-I, --include PATH`           | none        | Extra proto include paths (repeatable); the well-known Google protos are always included |

Exit codes: `0` success, `10` `protoc` failed, `20` code generation failed,
`99` anything else. On failure the previous build is restored and the failed
one kept in `<buildroot>/<package>__fail`.

## Python API

```python
from neobuilder6.neobuilder import NeoBuilder

NeoBuilder(package: str,
           protopath: str = './proto',
           build_root: str = './build',
           major: bool = False,
           patch: bool = False,
           verbose: bool = False,
           include_pyi: bool = True,
           extra_includes: list[str] | None = None,
           alias_imports: bool = True).build()
```

Same options as the CLI ([source](../neobuilder6/neobuilder/__init__.py)).
Notes:

- `build()` replaces `<build_root>/<package>` entirely (the old one is moved to
  `<package>__backup` during the build and deleted on success).
- Failures call `sys.exit()` with the codes above (also from Python).
- It imports the freshly compiled `*_pb2` modules (and appends the build root
  to `sys.path`), so a given package can only be built **once per Python
  process**; use subprocesses to build it again or into another build root
  (see [tests/test_alias_imports.py](../tests/test_alias_imports.py)).
- It calls `logging.basicConfig(...)` on construction.

## Versioning

[Source](../neobuilder6/neobuilder/__init__.py) (`read_next_version`)

1. If `<protopath>/<package>/VERSION` exists, its first line is the version
   (`x.y.z`, a 4th part like `x.y.z.a` is ignored, pre-release semver tags
   are allowed) and any following lines are a "commit message".
2. Otherwise the `__version__` of the previous build in the build root is
   bumped (minor by default, `-m` major, `-p` patch).
3. Otherwise `0.1.0`.

The built package gets `__version__`, `__protoplasm_version__` and
`__neobuilder_version__` in its root `__init__.py`, and a `VERSION` file
containing `Version <x.y.z> - <commit message>`.

## Generated layout

For every `<name>.proto` in `<protopath>/<package>/...` (paths, not proto
package names, decide where files go):

| File                        | When                      | Contents |
|-----------------------------|---------------------------|----------|
| `<name>_pb2.py` (+ `.pyi`)  | always                    | Plain `protoc` output |
| `<name>_dc.py`              | always                    | One `plasm.DataclassBase` dataclass per message and `enum.IntEnum` per enum (nested ones as nested classes); proto3 `optional` scalars/enums are `typing.Optional[...] = None` (needs protoplasm6 6.2+); see the protoplasm6 index for field conventions |
| `<name>_pb2_grpc.py`        | file has a `service` *    | Plain `grpcio-tools` output |
| `<name>_api.py`             | file has a `service`      | `<Service>Interface` with one `snake_case` method per RPC (request fields as keyword arguments, response fields as the return value) and `__servicer_cls__` |
| `<name>_grpc_receiver.py`   | file has a `service` *    | `<Service>GrpcServicer` (wraps your interface implementation for a gRPC server) |
| `<name>_grpc_sender.py`     | file has a `service` *    | `<Service>` client implementing `<Service>Interface` over gRPC: `<Service>(grpc_host='localhost:50051', credentials=None, options=None, metadata=None)` |

\* Unless the file sets `option py_generic_services = true;` (detected by a
line starting with that option or with `service `).

Package level files:

- `<package>/__init__.py`: version info and `load_symbols()`, which imports
  `__everything__` so every message is registered in protobuf's symbol
  database (needed for `Any` unpacking and type URL lookups).
- `<package>/__everything__.py`: imports every generated module.
- `__init__.py` in every directory (with [alias imports](#package-alias-imports)
  where a directory matches a proto package).
- `<package>/VERSION`: see [Versioning](#versioning).

Generated files start with an `# md5:` checksum header and must not be
edited by hand. Generated code imports `protoplasm6` and needs a
`protobuf` runtime with the same major version and at least the minor version
of the `grpcio-tools` that built it.

## Package alias imports

[Source](../neobuilder6/neobuilder/render/__init__.py) (`package_aliases`) ·
[tests](../tests/test_alias_imports.py)

Python modules follow proto *file* paths while protobuf namespaces follow
`package` statements, so by default the `__init__.py` of each directory that
matches a proto package star-imports every `*_dc.py` module of that package
(with a static `__all__`):

```python
# myshop/orders/{orders,customers}.proto with `package myshop.orders;`
from myshop.orders import *          # Order, Customer, ... from both files
from myshop.orders.orders_dc import Order   # Still works
```

Only dataclass modules are aliased (not `_api`/`_grpc_*`). Proto packages that
don't match a generated directory get no alias imports. Duplicate names
(shouldn't happen within one proto package) are logged and left out of
`__all__`. Use `--no-alias-imports` / `alias_imports=False` for empty
`__init__.py` files (the 6.0 behaviour).

## Coverage gaps

- Internal modules (`neobuilder6.generators`, `neobuilder6.descwrap`,
  `neobuilder6.structs`, `neobuilder6.neobuilder.render`) and the Jinja2
  templates in `neobuilder6/data/templates` aren't a supported extension
  point.
- `NeoBuilder`'s step methods (`collect_proto_files`, `proto_build`,
  `plasm_build`, `add_inits`, ...) are public by name but only meant to be
  called via `build()`.
