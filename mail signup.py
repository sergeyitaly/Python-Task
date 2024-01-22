import pyautogui
import sys
import time
import random
import string
import webbrowser
import ctypes
import re
import pyperclip


CF_TEXT = 1
BASE_URL = 'https://account.proton.me/signup?plan=free'
LOGIN_URL = 'https://account.proton.me/login'
TEMP_EMAIL_URL = 'https://dropmail.me/'

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def getClip6digit():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return str(re.findall(r'(\d{6})', (str(value))))
    finally:
        user32.CloseClipboard()

def getMail():
    # Get the HTML content of the page
    html_content = pyperclip.paste()
    # Find the position of "Your temporary email:" in the HTML string
    start_index = html_content.find("Your temporary email:")
    if start_index != -1:
        # Extract the substring after "Your temporary email:"
        email_info = html_content[start_index + len("Your temporary email:"):]
        # Use a regular expression to extract the email name
        match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email_info)
        if match:
            email_name = match.group(1)
            return email_name.strip()

    return ''

        
def randomize(_option_,_length_):

    if _length_ > 0 :

        if _option_ == '-p':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
        elif _option_ == '-s':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        elif _option_ == '-l':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif _option_ == '-n':
            string._characters_='1234567890'
        elif _option_ == '-m':
            string._characters_='JFMASOND'

        if _option_ == '-d':
            random.shuffle
            _generated_info_=random.randint(1,28)
        elif _option_ == '-y':
            random.shuffle
            _generated_info_=random.randint(1950,2000)
        else:
            _generated_info_=''
            random.shuffle
            for _counter_ in range(0,_length_) :
                _generated_info_= _generated_info_ + random.choice(string._characters_)

        return _generated_info_

    else:
        return 'error'

def main():
    # Open temporary email page
    webbrowser.open(TEMP_EMAIL_URL)
    time.sleep(5)

    # Select and copy the email text
    pyautogui.hotkey('ctrl', 'a')  # Select all
    pyautogui.hotkey('ctrl', 'c')  # Copy
    time.sleep(1)  # Add a delay to ensure clipboard update

    # Get temporary email
    temp_email = getMail()
    print("Temporary Email: " + temp_email)
    pyautogui.press('esc')
    time.sleep(3)
    # Generate a unique username with a timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    username = randomize('-s',20) + timestamp
    password = randomize('-p', 16)
    # Open ProtonMail signup page
    webbrowser.open(BASE_URL)
    time.sleep(10)

    # Fill in username and password
    pyautogui.typewrite(username + '\t')
    pyautogui.typewrite('\t')
    print("Username: " + username)
    pyautogui.typewrite(password + '\t' + password + '\t')
    print("Password: " + password)

    # Retype password
    pyautogui.typewrite(password + '\t')
    
    # Submit the form
    pyautogui.typewrite('\n')
    time.sleep(10)

    # Handle temporary email input   
    time.sleep(1)
    pyautogui.typewrite(temp_email)
    time.sleep(1)
    pyautogui.typewrite('\n')
    
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'shift', 'tab')
    verification_code = getClip6digit()
    print("Verification Code:", verification_code)

    # Fill in the verification code on ProtonMail page
    time.sleep(5)
    pyautogui.typewrite(verification_code + '\n')

    print(username + "@proton.me:" + password)

    logfile = open("accLog.txt", "a")
    logfile.write(temp_email+ "\n")
    logfile.write(username + "@proton.me:" + password + "\n" + "\n")
    logfile.close()

if __name__ == "__main__":
    main()
