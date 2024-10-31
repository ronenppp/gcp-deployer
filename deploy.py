import sys

from deployers import get_deployer


def run():
    deployer = get_deployer(sys.argv)
    if deployer and deployer.validate_input():
        print(f'The following deployment method was selected: {deployer}')
        deployer.deploy()


# python -m deploy api-sources-intercom-new_contact -i 10 -m 256
if __name__ == '__main__':
    run()

