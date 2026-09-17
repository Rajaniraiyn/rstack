# Worktrees

Give each parallel agent its own git worktree: isolated working copy, shared git objects, no merge conflicts. Then make each worktree cheap by sharing install and build caches, not by sharing state.

## Create

```sh
git worktree add ../wt-task-42 -b task/42
```

One worktree per task or per agent. Name it after the task or the agent that owns it. Remove it when done:

```sh
git worktree remove ../wt-task-42
```

Keep a small pool of recycled worktrees (for example `wt-1` through `wt-4`) when tasks are short: reset and reuse instead of creating and destroying.

## The sharing rule

Share anything reproducible: package caches, build caches, registry downloads. Never share active state two agents write at once: build output directories inside a worktree, `.git` internals, or the worktree's own dependency tree when a task mutates it.

Isolation boundaries matter more than disk savings. Wrong sharing breaks builds silently; keep correctness on the side of isolation.

## node_modules

- Identical lockfile across worktrees: symlink into one shared `node_modules` or, better, use a package manager with a content-addressed store.
- Different lockfiles: do not symlink. Two branches with different dependencies are exactly what breaks symlinked `node_modules`.

## pnpm

The global virtual store is the cheapest setup: packages live once in a content-addressable store, and each worktree's `node_modules` is symlinks into it. Configure it once:

```ini
# .npmrc
virtual-store-dir-max-length=120
```

Supported by default on recent pnpm. Second and later worktrees then cost almost nothing to install.

## npm

npm keeps a shared download cache (`~/.npm/_cacache`), which removes network cost but still extracts per worktree. Use the cache explicitly:

```sh
npm ci --prefer-offline
```

## uv (Python)

uv shares one global cache by default (`~/.cache/uv`). Install in each worktree is fast and mostly cached; there is no per-worktree store to duplicate. Keep `uv.lock` committed so installs reproduce.

## Rust / Cargo

Share the registry source cache, isolate the build target directory:

```sh
# Shared registry cache: set once
# CARGO_HOME=/path/to/shared/cargo-home
```

Do not point `CARGO_TARGET_DIR` at one shared directory across parallel agents: concurrent builds collide. Use a separate target dir per worktree, or a dedicated shared cache tool (sccache) when compile time matters.

## Other toolchains

- Maven/Gradle: share the local repository or Gradle cache via their cache settings; keep `build/` per worktree.
- Go: module cache (`GOMODCACHE`) is shared by default and safe.
- Pip: user-level cache is shared; installs re-extract.

## Cross-platform mechanics

- macOS and Linux: `ln -s` for symlinks; hard links only within the same filesystem.
- Windows: use directory junctions (`mklink /J`) or copies; plain symlinks need privileges.
- Keep the strategy in a shared recipe per repo (package manager + language) instead of re-solving it per task.

The factory setup decides the recipe once; provisioning just applies it.