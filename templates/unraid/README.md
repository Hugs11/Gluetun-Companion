# Gluetun Companion Unraid template

This folder contains Unraid DockerMan templates for installing Gluetun Companion
before it is published in Community Applications.

- `gluetun-companion.xml` is the upstream-ready template. It points to the
  `Aerya` package and `main` branch, and is the file to keep for the eventual
  upstream merge / Community Applications submission.
- `gluetun-companion-fork-test.xml` is the temporary Hugs11 fork template used
  to test this feature branch before the upstream merge.

## Image

The fork-test template points to the fork image:

```text
ghcr.io/hugs11/gluetun-companion:feat-protonvpn-port-forwarding
```

Before using it, publish the image from the fork by running the
`Build & publish Docker images` workflow manually on the
`feat/protonvpn-port-forwarding` branch. The workflow also publishes the sidecar
image with the same branch tag, and the template seeds `SIDECAR_IMAGE` to that
matching sidecar.

When the feature is merged upstream, replace the image/template URLs with the
upstream `aerya` package and `main` branch before submitting to Community
Applications.

## Manual install options for the fork test template

Private Community Applications install:

```sh
mkdir -p /boot/config/plugins/community.applications/private/gluetun-companion
wget -O /boot/config/plugins/community.applications/private/gluetun-companion/gluetun-companion.xml \
  https://raw.githubusercontent.com/Hugs11/Gluetun-Companion/feat/protonvpn-port-forwarding/templates/unraid/gluetun-companion-fork-test.xml
```

Then open **Apps -> Private Apps** and install Gluetun Companion.

DockerMan user-template install:

```sh
wget -O /boot/config/plugins/dockerMan/templates-user/my-gluetun-companion.xml \
  https://raw.githubusercontent.com/Hugs11/Gluetun-Companion/feat/protonvpn-port-forwarding/templates/unraid/gluetun-companion-fork-test.xml
```

Then open **Docker -> Add Container** and select the template.

## Unraid-specific notes

- Generate `SECRET_KEY` once with `openssl rand -hex 32`, paste it in the
  template, and keep it unchanged for the life of the instance.
- The container intentionally runs as root. Gluetun Companion must read and
  write DockerMan templates under
  `/boot/config/plugins/dockerMan/templates-user`, which are root-owned and
  typically mode `600` on Unraid. Exposing `PUID`/`PGID` would be misleading
  unless the user also changes host permissions manually.
- The Docker socket mount is required for sidecar benchmarks, Docker event
  monitoring and recreating running containers attached to Gluetun's network
  namespace.
- The DockerMan templates mount is required for persistent Unraid switches:
  Companion writes Gluetun environment changes back to the Gluetun XML template
  before recreating the container.
- The WebUI entry uses `[PORT:8765]`, the container port, so Unraid follows any
  host-port remap made by the user.
