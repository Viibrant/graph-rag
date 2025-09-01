compose := docker compose -f infra/compose.yml
gpu_compose := $(compose) -f infra/compose.gpu.yml

.PHONY: up down clean logs qdrant up-full up-app up-worker once-worker \
        rebuild-api rebuild-worker rebuild-all

# Default: dev = CPU only
up: ; $(compose) --profile core up -d
down: ; $(compose) down
clean: ; $(compose) down -v
logs: ; $(compose) logs -f

# Shorthands
qdrant: ; $(compose) --profile core up -d qdrant
up-app: ; $(compose) --profile core --profile app up -d
up-worker: ; $(compose) --profile core --profile worker up -d

# Full stack: switch between CPU/GPU depending on USE_GPU
up-full:
ifeq ($(USE_GPU),1)
	$(gpu_compose) --profile core --profile redis-local --profile app --profile worker up -d
else
	$(compose) --profile core --profile redis-local --profile app --profile worker up -d
endif

# One-off worker run
once-worker:
	$(compose) run --rm worker uv run -- python -c "from src.worker import run_worker_once; print('processed:', run_worker_once())"

# Rebuild commands
rebuild-api:
	$(compose) build api
	$(compose) up -d api

rebuild-worker:
	$(compose) build worker
	$(compose) up -d worker

rebuild-all:
	$(compose) build
	$(compose) up -d
