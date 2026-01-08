import time
import pyautogui as pg


# ===================== CONSTANTS =====================
RETRY_TIMEOUT = 10          # seconds
RETRY_INTERVAL = 0.5        # seconds


# ===================== CORE FUNCTIONS =====================
def _locate_with_retry(image_path: str, confidence: float, grayscale: bool = True):
    """
    Tries to locate an image on screen within a timeout.
    Raises RuntimeError if image is not found.
    """
    start_time = time.time()

    while time.time() - start_time < RETRY_TIMEOUT:
        try:
            location = pg.locateOnScreen(
                image_path,
                confidence=confidence,
                grayscale=grayscale
            )

            if location:
                return location

        except pg.ImageNotFoundException:
            pass  # Safe to ignore and retry

        except Exception as e:
            raise RuntimeError(f"Unexpected error while locating '{image_path}': {e}")

        time.sleep(RETRY_INTERVAL)

    # Screenshot for debugging
    pg.screenshot(f"error_{image_path}")

    raise RuntimeError(
        f"Image '{image_path}' not found on screen after {RETRY_TIMEOUT} seconds"
    )


def CrossLocation():
    """Locate the cross (close / clear) button."""
    return _locate_with_retry(
        image_path="cross.png",
        confidence=0.9,
        grayscale=True
    )


def SearchBarLocation():
    """Locate WhatsApp search bar."""
    return _locate_with_retry(
        image_path="SearchBar.png",
        confidence=0.8,
        grayscale=True
    )
