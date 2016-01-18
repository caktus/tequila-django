import argparse
import os
import os.path
from subprocess import check_call

import tequila

# TODO: Provide a way to pass additional arguments to ansible-playbook

INVENTORY_FILE_TEMPLATE = """# Inventory file for environment {envname}
dbserver1 ansible_ssh_host="1.2.3.4"
generalpurpose1 ansible_ssh_host="1.2.3.5" ansible_user="user2"
generalpurpose2 ansible_ssh_host="1.2.3.6"

[db]
dbserver1

[worker]
generalpurpose1
generalpurpose2

[web]
generalpurpose1
generalpurpose2
"""

SECRETS_FILE_TEMPLATE = """---
# Secrets file for environment {envname}
# Put password in .vaultpassword then encrypt using:
#  ansible-vault encrypt {filename}
# and edit using
#  ansible-vault edit {filename}
password: noway
"""


def touch(filename, content):
    """
    Create an empty file at `filename` but only if it
    doesn't already exist. Also creates any necessary
    intermediate directories.
    """
    if not os.path.exists(filename):
        fullpath = os.path.abspath(filename)
        directory = os.path.dirname(fullpath)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        f = open(filename, "w")
        f.write(content)
        f.close()


def main():
    tequila_dir = os.path.dirname(tequila.__file__)

    tequila_roles_dir = os.path.join(tequila_dir, 'roles')
    if not os.path.exists(tequila_roles_dir):
        raise Exception("Something is wrong, tequila roles were expected to be at "
                        "%s but they're not" % tequila_roles_dir)
    os.environ['ANSIBLE_ROLES_PATH'] = 'roles:%s' % tequila_roles_dir

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "envname",
        help="Required: name of the environment to deploy, e.g. 'staging' or 'production'",
    )
    parser.add_argument(
        "--newenv",
        action='store_true',
        help="Create the files for the environment specified as `envname` if they "
             "don't already exist, then exit.",
    )
    parser.add_argument(
        "--inventory",
        "-i",
        action='store',
        help="Use a different inventory file than the default."
    )
    args = parser.parse_args()
    envname = args.envname

    inventory_file = 'inventory/{}'.format(envname)
    if args.inventory:
        inventory_file = args.inventory
    global_vars_file = 'inventory/group_vars/all'
    env_vars_file = 'inventory/group_vars/{}'.format(envname)
    global_secrets_file = 'inventory/secrets/all'
    env_secrets_file = 'inventory/secrets/{}'.format(envname)
    password_file = '.vaultpassword-{envname}'.format(envname=envname)

    if args.newenv:
        print("Creating new environment {!r}".format(envname))
        touch(inventory_file,
              INVENTORY_FILE_TEMPLATE.format(envname=envname))
        touch(env_vars_file,
              "---\n# Variables file for environment {}\nfoo: bar\n".format(envname))
        touch(env_secrets_file, SECRETS_FILE_TEMPLATE
              .format(envname=envname, filename=env_secrets_file))
        return

    if not os.path.exists(inventory_file):
        print("ERROR: No inventory file found at {!r}, is {!r} a valid environment?".format(inventory_file, envname))
        return
    if not os.path.exists(env_vars_file):
        print("ERROR: No vars file found at {!r}, is {!r} a valid environment?".format(env_vars_file, envname))
        return

    playbook_options = [
        '--become',
        '-i', inventory_file,
        '-e', 'tequila_dir=%s' % tequila_dir,
        '-e', 'env_name=%s' % envname,
        '-e', 'local_project_dir=%s' % os.getcwd(),
    ]

    if os.path.exists(password_file):
        playbook_options.extend(['--vault-password-file', password_file])
        for secrets_file in [global_secrets_file, env_secrets_file]:
            if os.path.exists(secrets_file):
                playbook_options.extend(['-e', '@' + secrets_file])
            else:
                print("WARNING: Found {}, but no secrets file at {}".format(password_file, secrets_file))
    else:
        print("WARNING: No {} file found, will not use any secrets.".format(password_file))

    command = ['ansible-playbook'] + playbook_options + ['%s/deploy.yml' % tequila_dir]

    print("Invoking ansible: {}".format(command))

    check_call(command)
