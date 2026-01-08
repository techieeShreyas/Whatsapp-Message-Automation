import time
import pyautogui as pygui
import pyperclip
from PIL import Image
from io import BytesIO
import win32clipboard

from ImageLocations import CrossLocation, SearchBarLocation
from DbConnection import numbers

# ===================== CONFIG =====================
WHATSAPP_START_DELAY = 2
SEARCH_DELAY = 1
SEND_DELAY = 1

IMAGE_CONFIDENCE = 0.7
NO_CHAT_IMAGE = "nochats.png"
ATTACHMENT_IMAGE = "bachpankartLogo.png"
MESSAGE_FILE = "Message.txt"

COUNTRY_CODE = "+91"
CLICK_X, CLICK_Y = 382, 472

CONTACTS = numbers


# ===================== GLOBAL STATE =====================
on_whatsapp = []
not_on_whatsapp = []


# ===================== UTILITY FUNCTIONS =====================
def load_message(file_path: str) -> str:
    """Load message text from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise RuntimeError(f"Message file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read message file: {e}")


def is_image_present(image_path: str, confidence: float = IMAGE_CONFIDENCE) -> bool:
    """Check if an image exists on the screen."""
    try:
        location = pygui.locateOnScreen(image_path, confidence=confidence)
        return location is not None
    except pygui.ImageNotFoundException:
        return False
    except Exception as e:
        print(f"[ERROR] Image detection failed: {e}")
        return False


def copy_image_to_clipboard(image_path: str) -> None:
    """Copy image to Windows clipboard."""
    try:
        image = Image.open(image_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")

        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    except FileNotFoundError:
        print(f"[ERROR] Image not found: {image_path}")
    except Exception as e:
        print(f"[ERROR] Failed to copy image to clipboard: {e}")


def open_whatsapp() -> None:
    """Launch WhatsApp desktop."""
    pygui.press("win")
    time.sleep(0.3)

    pygui.write("whatsapp", interval=0.15)
    time.sleep(0.3)

    pygui.press("enter")
    time.sleep(WHATSAPP_START_DELAY)


def search_contact(contact: str, search_bar, cross) -> None:
    """Search contact in WhatsApp."""
    pygui.click(pygui.center(cross), interval=0.2)
    pygui.click(pygui.center(search_bar), interval=0.4)

    pygui.write(f"{COUNTRY_CODE}{contact}", interval=0.25)
    time.sleep(SEARCH_DELAY)

    pygui.click(CLICK_X, CLICK_Y, interval=0.4)
    pygui.press("enter")
    time.sleep(1.5)


def send_message_and_attachment(message: str) -> None:
    """Send text, emoji, and image."""
    pyperclip.copy(message)
    pygui.hotkey("ctrl", "v")

    copy_image_to_clipboard(ATTACHMENT_IMAGE)
    time.sleep(0.3)

    pygui.hotkey("ctrl", "v")
    time.sleep(0.8)

    pygui.press("enter")
    time.sleep(SEND_DELAY)


def close_whatsapp(cross) -> None:
    """Close WhatsApp safely."""
    pygui.click(pygui.center(cross), interval=0.2)
    pygui.hotkey("alt", "f4")
