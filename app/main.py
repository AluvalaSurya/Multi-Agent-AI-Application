import subprocess
import time
import requests

from dotenv import load_dotenv

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

BACKEND_URL = "http://127.0.0.1:9999/docs"


def wait_for_backend(timeout=30):
    """
    Wait until the FastAPI backend is ready.
    """
    logger.info("Waiting for backend to become available...")

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(BACKEND_URL, timeout=2)

            if response.status_code == 200:
                logger.info("Backend is ready.")
                return True

        except requests.exceptions.RequestException:
            pass

        time.sleep(1)

    return False


def main():
    backend_process = None
    frontend_process = None

    try:
        logger.info("Starting backend service...")

        backend_process = subprocess.Popen(
            [
                "uvicorn",
                "app.backend.api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "9999",
            ]
        )

        if not wait_for_backend():
            raise CustomException(
                "Backend failed to start within 30 seconds."
            )

        logger.info("Starting frontend service...")

        frontend_process = subprocess.Popen(
            [
                "streamlit",
                "run",
                "app/frontend/ui.py",
            ]
        )

        # Wait until Streamlit exits
        frontend_process.wait()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")

    except Exception as e:
        logger.exception("Application startup failed.")
        raise CustomException(
            "Failed to start application.",
            error_detail=e
        )

    finally:
        logger.info("Stopping services...")

        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            frontend_process.wait()

        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            backend_process.wait()

        logger.info("Application stopped.")


if __name__ == "__main__":
    main()
