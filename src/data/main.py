from kismetclient import Kismetclient

def main():
    k = Kismetclient('192.168.1.69')
    print(k.getDevices('phy-IEEE802.11'))

if __name__ == "__main__":
    main()
