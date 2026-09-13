# OAuth and Catalog Patterns

Reference for common MCP server auth states and decision rules.

## Auth-State Decision Table

| State | `hermes mcp list` shows | `hermes mcp test` output | Ready? |
|-------|------------------------|--------------------------|--------|
| Catalog installed, no auth needed | ✓ enabled | ✓ Connected | Yes |
| Catalog installed, OAuth required | ✓ enabled | ✗ no cached tokens | No — run `hermes mcp login <name>` |
| Catalog installed, partial access | ✓ enabled | ✗ HTTP 401/403 | No — check scopes or account access |
| Not in catalog | — | — | No — verify provider URL or use manual add |
| Manual add, unreachable | ✓ enabled | ✗ connection refused | No — check URL/transport/daemon |

## HTTP/SSE Server Add Templates

```bash
hermes mcp add expo --url https://mcp.expo.dev/mcp --auth oauth --connect-timeout 30
hermes mcp add notion --url https://mcp.notion.com/mcp --auth oauth --connect-timeout 30
hermes mcp add linear --url https://mcp.linear.app/mcp --auth oauth --connect-timeout 30
```

## Stdio Server Add Templates

```bash
hermes mcp add github --command npx --args "-y" "@modelcontextprotocol/server-github" --env GITHUB_PERSONAL_ACCESS_TOKEN=$TOKEN
```

## Catalog Install Templates

```bash
hermes mcp install <name>  # from hermes mcp catalog output
```

## After Install

```bash
hermes mcp list           # verify entry exists
hermes mcp test <name>    # verify connectivity and tools
hermes mcp configure <name>  # prune tool scope after successful probe
```

## Notes

- OAuth flows require an interactive browser. Cannot be completed in non-interactive sessions.
- A cancelled interactive prompt means the server was NOT added.
- After auth succeeds, restart Hermes or run `hermes mcp configure <name>` to reload tools.
