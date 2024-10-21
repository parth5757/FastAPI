import sys
sys.path.append("d:/FastAPI/NSE_Stock/backend")
from main import Return_Hello



name = input("Enter name")

print(Return_Hello.give_name(name))