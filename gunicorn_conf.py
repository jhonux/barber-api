import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1 ))

worker_class = "uvicorn.workers.UvicornWorker"

loglevel = os.getenv("LOG_LEVEL", "info")

timeout = int(os.getenv("TIMEOUT", "120"))