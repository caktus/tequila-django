Tequila
=======

This repository holds a collection of roles for deployments using
`Ansible <http://www.ansible.com/home>`_.  These exist primarily to
support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_.


License
-------

These playbooks are released under the BSD License.  See the `LICENSE
<https://github.com/caktus/tequila/blob/master/LICENSE>`_ file for
more details.


Contributing
------------

If you think you've found a bug or are interested in contributing to this project
check out `tequila on Github <https://github.com/caktus/tequila>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.

How to use
----------

* Create & activate a virtualenv for your project.
* Add a SPECIFIC tagged version of tequila to your project requirements, e.g.
  in ``requirements.txt``::

    git+https://github.com/caktus/tequila.git@0.0.1

  This is so once you have Tequila working with the version you have pinned,
  updates to Tequila won't be applied until you're ready to test them and
  make sure things still work.

* Install the tequila package into your virtualenv, e.g.::

    pip install -r requirements.txt

* In your project's top-level directory (which will be the current directory
  when you run deploys), create an ``inventory`` directory.
* For each environment (e.g. `staging`, `production`), create a new `Ansible
  inventory file <http://docs.ansible.com/ansible/intro_inventory.html>`_
  in the ``inventory`` directory, named the same as the environment
  (with no extension).  E.g.::

      vi $(PWD)/inventory/staging

  The purpose of the inventory file is to specify which hosts are serving which
  roles in the deploy, and how to connect to them. To do this, servers should be
  added to the groups "db", "worker", and "web", as appropriate.

  TBD: Update that list as we add more groups?  Probably better to flesh out this
  part of the documentation in much greater detail somewhere other than this
  README.

* Put any variables that should be set for the entire environment in a YAML file
  named ``$(PWD)/inventory/group_vars/<envname>``.  E.g.::

      vi $(PWD)/inventory/group_vars/staging

* Put any variables that need to be kept secret in a YAML file named
  ``$(PWD)/inventory/secrets/<envname>`` and encrypt it using the `Ansible
  vault <http://docs.ansible.com/ansible/playbooks_vault.html>`_, e.g.::

      ansible-vault edit $(PWD)/inventory/secrets/staging

* Put the password for the Ansible vault in a file named ``.vaultpassword``.
  Be *sure* that (1) it does not get added to version control, and (2) it
  is not public (e.g. set permissions to 0600 or something).  E.g.::

      echo ".vaultpassword" >>.gitignore
      echo "password" >.vaultpassword
      chmod 600 .vaultpassword

* Run ``deploy --envname=<envname>`` to update servers.  E.g.::

    deploy --envname=staging

  or::

    deploy --envname=production

TODO: Create more detailed documentation, including which groups to use and
what variables need to be set, and lots of examples of the whole process
