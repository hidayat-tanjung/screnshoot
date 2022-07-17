import pyscreenshot


banner = """ 
     [!] mouse_listener
     [!] By : X3NUX
     [!] www.niasxploit.com
"""
print(banner)

image = pyscreenshot.grab()

image.show()
image.save("123.png")