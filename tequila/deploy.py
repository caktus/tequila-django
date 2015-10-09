import argparse
import os
from subprocess import check_call

import tequila


def main():
    tequila_dir = os.path.dirname(tequila.__file__)

    tequila_roles_dir = os.path.join(tequila_dir, 'roles')
    if not os.path.exists(tequila_roles_dir):
        raise Exception("Something is wrong, tequila roles were expected to be at "
                        "%s but they're not" % tequila_roles_dir)
    os.environ['ANSIBLE_ROLES_PATH'] = 'roles:%s' % tequila_roles_dir

    parser = argparse.ArgumentParser()
    parser.add_argument("envname")
    args = parser.parse_args()
    envname = args.envname

    check_call(
        ['ansible-playbook',
         '-i', 'inventory/%s' % envname,
         '-e', '@inventory/group_vars/%s' % envname,
         '-e', 'tequila_dir=%s' % tequila_dir,
         '-e', 'env_name=%s' % envname,
         '%s/deploy.yml' % tequila_dir,
         ]
    )
