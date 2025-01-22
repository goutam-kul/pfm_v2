from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(override=True)

# Access variables
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

print(MAIL_PASSWORD)
print(MAIL_USERNAME)