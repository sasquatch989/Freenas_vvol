"""Usage: python fn_vvol --size <> :"""
import freenas
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--size',
                       metavar='size', type=int,
                       help='Integer size in GB <ex: 10 />',
                       default=10)
args = argparser.parse_args()



def main():
    """Workflow, new vm get new dataset, volumes created, dataset_name = vm_name"""
    auth = freenas.auth_conf()
    api = freenas.Freenas(freenas.hostname, auth)
    api.create_zvol(int(args.size))
    api.assoc_target(api.create_target(), api.create_extent())


if __name__ == '__main__':
    main()


