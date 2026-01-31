# Local CI mirror

This folder provides a lightweight, reproducible local mirror of the GitHub Actions jobs used by the repository.

Goals:
- Reproduce `style-enforcement` and `detect-secrets` jobs locally
- Produce the same artifacts (compliance report and detect-secrets scan files) so debugging is easier
- Be fast and easy to iterate on (Docker-based)

Prerequisites:
- Docker installed and running
- Optional: `make` to run the convenience target

Quick start (Docker):

1. Build the local CI image:

   docker build -t dsu-ci-local .ci-local

2. Run the local CI container (writes artifacts to the host `./artifacts` directory):

   docker run --rm -v "$(pwd)":/home/ci/workspace -w /home/ci/workspace -e CI=true dsu-ci-local

This runs both the style enforcement and detect-secrets scans and writes artifacts to `projects/deploy-system-unified/ci-artifacts/`.

Run individual jobs:

- Run only style enforcement:
  docker run --rm -v "$(pwd)":/home/ci/workspace -w /home/ci/workspace -e CI=true dsu-ci-local /bin/bash -c "./.ci-local/run-local-ci.sh style"

- Run only detect-secrets:
  docker run --rm -v "$(pwd)":/home/ci/workspace -w /home/ci/workspace -e CI=true dsu-ci-local /bin/bash -c "./.ci-local/run-local-ci.sh detect-secrets"

Notes:
- The container uses an Ubuntu base to match the GitHub Actions runner environment.
- The container installs Python, pip, `detect-secrets==1.3.0`, and `jq` to match the workflow.
- The `run-local-ci.sh` script mirrors the steps performed by the real workflows and writes the same artifacts.

If you prefer a host-run (no Docker), run:

  ./projects/deploy-system-unified/.ci-local/run-local-ci.sh all

(You may need to install `python3`, `python3-pip`, and `jq` locally.)
