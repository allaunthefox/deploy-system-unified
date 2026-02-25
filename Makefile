.PHONY: lint lint-markdown test test-x86 test-arm64 molecule-precheck refresh-dependencies check-dependencies

lint:
	ansible-lint .

lint-markdown:
	@echo "Markdown linting not explicitly configured in environment, skipping."

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
	@git diff --exit-code requirements.txt requirements-dev.txt || (echo "Error: Requirements files are out of sync. Run 'make refresh-dependencies' and commit changes." && exit 1)
	@echo "Dependencies are up-to-date."

test: test-x86

test-x86:
	@echo "Running x86_64 GPU Slicing tests..."
	molecule test -s gpu_slicing

test-arm64:
	@echo "Running ARM64 GPU Slicing tests (Requires QEMU/ARM hardware)..."
	molecule test -s gpu_slicing_arm64
