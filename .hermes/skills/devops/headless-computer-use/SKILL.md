---
name: headless-computer-use

description: Run computer_use on headless Linux with persistent Xvfb.
version: 1.0.0
author: Administrator, Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [computer-use, headless, xvfb, x11, automation]
    related_skills: [computer-use, hermes-agent]
---

# Headless Computer Use

Use this when Hermes runs on a headless Linux server but still needs `computer_use`.

## When to Use
- The host has no graphical session (`XDG_SESSION_TYPE=tty`).
- `hermes computer-use doctor` reports missing `DISPLAY` or no X11 reachability.
- You need screenshots, clicks, or typing inside a virtual desktop.

## Procedure
1. **Install Xvfb and X11 utilities**
   ```bash
   sudo apt-get install -y xvfb x11-xserver-utils xauth xdotool
   ```
2. **Create a persistent user service**
   ```bash
   mkdir -p ~/.config/systemd/user
   cat > ~/.config/systemd/user/xvfb.service <<'EOF'
   [Unit]
   Description=Xvfb Virtual X11 Server (Display :99)
   After=graphical-session.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset
   Restart=on-failure
   RestartSec=5
   Environment=DISPLAY=:99

   [Install]
   WantedBy=graphical-session.target
   EOF
   ```
3. **Enable and start it**
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now xvfb.service
   DISPLAY=:99 hermes computer-use doctor
   ```
4. **Inject the display into the gateway**
   ```bash
   mkdir -p ~/.config/systemd/user/hermes-gateway.service.d
   cat > ~/.config/systemd/user/hermes-gateway.service.d/override.conf <<'EOF'
   [Service]
   Environment=DISPLAY=:99
   Environment=XDG_SESSION_TYPE=x11
   Environment=XWAYLAND_DISPLAY=
   EOF
   systemctl --user daemon-reload
   systemctl --user restart hermes-gateway.service
   ```
5. **Verify**
   ```bash
   systemctl --user is-active xvfb.service
   systemctl --user show hermes-gateway.service -p Environment | grep DISPLAY
   DISPLAY=:99 hermes computer-use doctor
   ```

## Use the Tool, Not the CLI Wrapper
`hermes computer-use` is only a management CLI (`install`, `status`, `doctor`, `permissions`).
Actual capture/click/type actions use the `computer_use` tool: `action="capture"`, `mode="vision"` or `"som"`, and optionally `app="xterm"` or another running X11 app.

## Pitfalls
- Xvfb is headless: it captures and controls apps running inside `:99`, not your local desktop.
- Do not start a second `Xvfb :99` while the service is active; stop the old process and clear `/tmp/.X99-lock` only if the lock is stale.
- The gateway must inherit `DISPLAY=:99`; otherwise Telegram-triggered runs will still fail even though a manual `DISPLAY=:99` test works.
- Keep credentials in `~/.hermes/.env`; put only environment settings in systemd overrides.

## Verification Checklist
- [ ] `xvfb.service` is active and enabled
- [ ] `DISPLAY=:99` appears in the gateway environment
- [ ] `hermes computer-use doctor` reports `ax_capability` and `screen_capture_capability` as ✅
- [ ] A real `computer_use(action="capture")` returns a `screenshot_path`
