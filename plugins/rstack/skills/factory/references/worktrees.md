# Worktrees

Give each parallel writer its own git worktree. Separate working copies prevent agents from overwriting each other's files during execution, but their changes can still conflict when merged. Worktrees share git objects and repository configuration; they are not a security sandbox. Reduce install costs with package-manager caches, not shared writable dependency trees.

## Create

```sh
git worktree add ../wt-task-42 -b task/42
```

One worktree per task or per agent. Name it after the task or the agent that owns it. Remove it when done:

```sh
git worktree remove ../wt-task-42
```

Keep a small pool of recycled worktrees when tasks are short. Before reuse, stop all workers, inspect tracked and untracked changes, and preserve the previous task's commits and artifacts. Never reset, clean, or remove a worktree containing unreviewed or user-owned work. Assign one writer at a time.

## The sharing rule

Share anything reproducible: package caches, build caches, registry downloads. Never share active state two agents write at once: build output directories inside a worktree, `.git` internals, or the worktree's own dependency tree when a task mutates it.

Isolation boundaries matter more than disk savings. Wrong sharing breaks builds silently; keep correctness on the side of isolation.

## node_modules

Install a separate dependency tree in each worktree using the package manager's shared cache. Matching lockfiles alone do not make a shared `node_modules` safe: install scripts, native builds, workspace links, and tools that write caches there can depend on the working directory.

Only share a dependency tree when it is immutable and the repository has verified that all consumers are read-only and relocatable. Never share it while either worker installs, rebuilds, or patches packages.

## pnpm

Use pnpm's content-addressed store to reuse package downloads across worktrees, while keeping each worktree's dependency links separate. Let pnpm manage links and its store layout; do not hardlink writable source files yourself.

A global virtual store is a separate, version-dependent feature. Check the installed pnpm documentation before enabling it. `virtual-store-dir-max-length` only controls directory-name length; it does not enable a global virtual store. Cached installs still need per-worktree linking and may run build scripts.

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