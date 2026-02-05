.PHONY: lint lint-markdown test test-x86 test-arm64

lint:
	ansible-lint .

lint-markdown:
	@echo "Markdown linting not explicitly configured in environment, skipping."

test: test-x86

test-x86:
	@echo "Running x86_64 GPU Slicing tests..."
	molecule test -s gpu_slicing

test-arm64:
	@echo "Running ARM64 GPU Slicing tests (Requires QEMU/ARM hardware)..."
	molecule test -s gpu_slicing_arm64
