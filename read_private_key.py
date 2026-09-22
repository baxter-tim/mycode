from getpass import getpass

key = getpass("API key: ")
print("Key supplied." if key.strip() else "No key supplied.")
