---
name: mcp-integration
description: Install, authenticate, verify, and maintain MCP servers.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, integration, oauth, tools, verification]
    related_skills: [hermes-agent, github, google-workspace]
---

# MCP Integration

Use this skill whenever adding, repairing, or auditing Model Context Protocol servers. The goal is a usable, authenticated, verified connection—not merely a config entry.

## Always-On Rules

- Treat catalog availability as discovery, not proof of authentication, authorization, or zero cost.
- Verify every server name and endpoint against the Hermes catalog or the provider's official documentation; never invent an MCP name.
- Do not report a server as installed or ready unless `hermes mcp list` shows it and `hermes mcp test` succeeds.
- Keep credentials in a credential manager or protected environment. Never print, paste, or commit tokens in chat, logs, or skill files.
- For OAuth servers, complete an interactive login before calling the integration ready. An unauthenticated config entry is pending, not working.
- Prefer catalog installation for approved servers. Use manual `hermes mcp add` only when the official provider supplies a supported URL or stdio command.
- After a successful probe, use `hermes mcp configure <name>` to enable only the tools required by the task; avoid broad write permissions by default.
- A new Hermes session may be required before newly discovered MCP tools appear.

## Procedure

1. **Inventory first**
   Run `hermes mcp catalog` and `hermes mcp list`. Record the requested server's transport, auth method, tool scope, and account or subscription requirements.

2. **Choose the installation path**
   - Approved catalog server: `hermes mcp install <name>`.
   - Official HTTP/SSE server: `hermes mcp add <name> --url <endpoint> --auth oauth` or the provider-documented auth mode.
   - Official stdio server: `hermes mcp add <name> --command <command> --args <args...>`, with credentials resolved from a protected source.

3. **Authenticate when required**
   For OAuth, run `hermes mcp login <name> --flow browser` or `--flow device` in an interactive session. Do not save an unauthenticated endpoint merely to make a later test pass.

4. **Verify the connection**
   Run `hermes mcp list` and `hermes mcp test <name>`. Confirm the transport, tool count, and status. If discovery succeeds but the provider requires account access, report the exact pending authorization step.

5. **Minimize tool scope**
   Run `hermes mcp configure <name>` after authentication. Enable read-only tools for research and only enable write/delete tools after explicit user approval.

6. **Report exact state**
   Distinguish `installed and connected`, `installed but OAuth pending`, `not in catalog`, and `connection failed`. Never collapse these states into “available.”

## Pitfalls

- A catalog install can succeed while its probe fails because no OAuth token is cached; complete login before claiming readiness.
- A cancelled interactive prompt means the server was not added; do not treat the command's exit status as installation success.
- HTTP 401/403 usually means credentials or scopes are missing, not that the MCP transport is broken.
- Do not call a server “free” solely because it appears in the catalog; verify provider pricing and account requirements.
- Do not enable all tools for a write-capable server when a read-only subset is sufficient.
- Do not confuse a related plugin (for example, a meeting plugin) with an MCP connector for a different product.
- Do not expose a token in a shell command, process list, config diff, or diagnostic transcript.

## Verification Checklist

- [ ] Catalog or official endpoint verified
- [ ] Authentication method identified
- [ ] Server appears in `hermes mcp list`
- [ ] `hermes mcp test <name>` passes
- [ ] Tool scope reviewed and pruned
- [ ] User-facing report names any remaining OAuth or permission step

See `references/oauth-and-catalog.md` for reusable server-pattern examples and the auth-state decision table.
