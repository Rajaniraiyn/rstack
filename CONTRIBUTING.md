# Contributing

Use [uv](https://docs.astral.sh/uv/) for everything.

```sh
uv sync                                          # install dependencies
uv run scripts/rstack.py check                   # validate the package
uv run python -m unittest discover -s tests      # run tests
uv run scripts/rstack.py package                 # build dist/ archives
```

After changing `plugins/rstack/plugin.json`, run `uv run scripts/rstack.py sync` to regenerate client metadata.

See [docs/authoring.md](docs/authoring.md) to add a skill.