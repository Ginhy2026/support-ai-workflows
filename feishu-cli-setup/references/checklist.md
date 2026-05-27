# Feishu CLI Readiness Checklist

Use this checklist to diagnose whether `supportman` can automatically search Feishu documents and wiki pages.

## Required State

| Item | Required result |
|---|---|
| Node.js | Installed and available as `node` |
| lark-cli | Installed and available as `lark-cli` or `lark-cli.cmd` |
| Login identity | User OAuth login, not shared App Secret |
| Token status | Valid |
| Required scope | `search:docs:read` |
| Search command | `lark-cli drive +search` works |
| Document access | User can access the target knowledge base documents |

## Windows Notes

- PowerShell may block `lark-cli.ps1` because scripts are disabled.
- Prefer `lark-cli.cmd` when that happens.
- If `npm.ps1` is blocked, use `npm.cmd` or run from Command Prompt.

## macOS/Linux Notes

- `lark-cli` should normally resolve from PATH after global npm install.
- If not found, check npm global bin path.

## Readiness Levels

- Ready: CLI installed, logged in, `search:docs:read` granted, test search succeeds.
- Partially ready: CLI exists but login or scope is missing.
- Not ready: Node.js or CLI missing.
- Blocked by access: CLI works but the user lacks access to the target Feishu documents.
