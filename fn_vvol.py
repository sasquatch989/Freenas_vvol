from freenas import Freenas
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--size', metavar='size', type=int, help='Integer size in GB <ex: 10 />')
args = argparser.parse_args()

#auth = (args.host, args.user, args.pw)

def main():
    api = Freenas(auth)
    zvol_id = api.create_zvol()

    pass

if __name__ == '__main__':
    main()


