import random


def ip_networks():
    return str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))


if __name__ == '__main__':
    print ip_networks()