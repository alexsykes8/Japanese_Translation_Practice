from Main.user import user
from list_management import list_management

def main():
    currentUser = user()
    currentUser.login("test2")

if __name__ == "__main__":
    main()