# RuneScape Archaeology Assistant

A small tool written in Python to help calculate useful quantities for materials and artefacts gathered from the archaeology skill in RuneScape.

## Planned Features

* List materials needed to restore an artefact.
* Aggregate needed materials over multiple types of artefacts and multiple numbers of the same artefact.
* Track how many materials a user has, calculate how many more are needed, and provide what the remaining porter charges will be after getting materials.

## Contributing

Install the project in editable mode in a virtualenv.

```sh
pip install -e ".[dev]"
```

Install pre-commit hooks.

```sh
pre-commit install
```

Run tests with `pytest`. Linting and formatting will be run on commit with pre-commit. Coverage report can be generated with `coverage`.

```sh
coverage run -m pytest
coverage report
coverage html
```
