import pyautogui as pygui
import time
# from DbConnection import updateDB
from Automation_Functions import load_message, open_whatsapp, SearchBarLocation, CrossLocation, search_contact, is_image_present, send_message_and_attachment, close_whatsapp, WHATSAPP_START_DELAY, SEARCH_DELAY, SEND_DELAY, IMAGE_CONFIDENCE, NO_CHAT_IMAGE, ATTACHMENT_IMAGE, COUNTRY_CODE, CLICK_X, CLICK_Y, MESSAGE_FILE, CONTACTS 


CONTACTS = ["9211864298", "8962589175", "9711520093", "7838070318", "8285315856", "9369242751"]
# ===================== MAIN PROGRAM =====================
def main():
    print(f"Start time: {time.time()}")
    count=0
    on_whatsapp=[]
    not_on_whatsapp=[]
    try:
        message = load_message(MESSAGE_FILE)
        print("Message loaded successfully.")
        open_whatsapp()
        print("Whatspp opened successfully.")

        search_bar = SearchBarLocation()
        pygui.click(pygui.center(search_bar), interval=.03)
        time.sleep(.5)
        cross = CrossLocation()

        print("Location located successfully.")

        pygui.click(pygui.center(search_bar), interval=0.4)
        time.sleep(1)

        for contact in CONTACTS:
            print(f"[INFO] Processing contact: {contact}")

            search_contact(contact, search_bar, cross)
            count+=1

            if is_image_present(NO_CHAT_IMAGE):
                print("[INFO] Contact NOT on WhatsApp")
                not_on_whatsapp.append(int(contact))
            else:
                print("[INFO] Contact IS on WhatsApp")
                pygui.click(CLICK_X, CLICK_Y, interval=0.4)
                pygui.press("enter")

                send_message_and_attachment(message)
                on_whatsapp.append(int(contact))
            if count == 5:
                # updateDB(on_whatsapp, not_on_whatsapp)
                on_whatsapp=[]
                not_on_whatsapp=[]
                count=0

            time.sleep(0.7)

        print("\n[✔] Program executed successfully.")

    except Exception as e:
        # DB updation if any error occured
        print("Inside Exception block. An error is occured.")
        print(f"[FATAL ERROR] Program terminated: {e}")
    finally:
        # updateDB(on_whatsapp, not_on_whatsapp)
        on_whatsapp=[]
        not_on_whatsapp=[]
        close_whatsapp(cross)
        print(f"End time: {time.time()}")

# ===================== ENTRY POINT =====================
if __name__ == "__main__":
    main()
