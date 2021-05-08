import argparse

def genereate_keys():
    print()

def config_argparse():
    parser = argparse.ArgumentParser(description='Generates key and signs messages using RSA.')
    parser.add_argument('-k', action = 'store_true', help = 'Generates private key (private.key) and public key (public.key) in keys folder')
    return parser


def main():
    parser = config_argparse()
    arguments = parser.parse_args()

    if (arguments.k):
        generate_keys()

    print('Done! Press Enter to close.')
    input()


if __name__ == '__main__':
    main()