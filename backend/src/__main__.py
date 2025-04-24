from loguru import logger

from src.pipeline import run_pipeline


def main():
    """Entry point for the pipeline."""
    logger.info("Starting pipeline")
    query = "machine learning"
    for event in run_pipeline(query):
        if event.type == "step":
            logger.info(f"Step: {event.step} - {event.message}")
        elif event.type == "result":
            logger.info(f"Result: {event.data}")
        else:
            logger.warning(f"Unknown event type: {event.type}")


if __name__ == "__main__":
    main()
