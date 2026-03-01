.PHONY: lint lint-markdown test test-x86 test-arm64 molecule-precheck refresh-dependencies check-dependencies wiki sync-wiki codeql

lint:
	ansible-lint -x internal-error .

codeql:
	@echo "Running local CodeQL security audit..."
	@./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh

security-scan:
	@echo "Running comprehensive local security scan (Bandit, Safety, TruffleHog, Checkov, Trivy, Lynis, RKHunter)..."
	@./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh

lint-markdown:
	@echo "Markdown linting not explicitly configured in environment, skipping."

wiki:
	@echo "Generating wiki pages..."
	@./scripts/generate_wiki.py

sync-wiki: wiki
	@echo "Syncing wiki to GitHub..."
	@./scripts/sync_wiki.sh

molecule-precheck:
	@./scripts/ensure_podman_access.sh || true

refresh-dependencies:
	@echo "Refreshing hashed dependencies via pip-compile..."
	@pip-compile --generate-hashes requirements.in
	@pip-compile --generate-hashes requirements-dev.in
	@echo "Done. Review changes in requirements.txt and requirements-dev.txt"

check-dependencies:
	@echo "Verifying dependency idempotence..."
	@pip-compile --generate-hashes requirements.in
	@pip-compile --generate-hashes requirements-dev.in
	@if git diff --quiet requirements.txt requirements-dev.txt; then \
		echo "Dependencies are up-to-date."; \
	else \
		echo "Dependencies updated, committing changes."; \
		git config user.name "ci-bot"; \
		git config user.email "ci-bot@users.noreply.github.com"; \
		git add requirements.txt requirements-dev.txt; \
		git commit -m "ci: refresh hashed dependencies"; \
	fi

test: test-x86

test-x86:
	@echo "Running x86_64 GPU Slicing tests..."
	molecule test -s gpu_slicing

test-arm64:
	@echo "Running ARM64 GPU Slicing tests (Requires QEMU/ARM hardware)..."
	molecule test -s gpu_slicing_arm64
