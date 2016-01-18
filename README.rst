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
  (with no extension).  The inventory file is an ``ini``-format file.

  The purpose of the inventory file is to specify which hosts are serving which
  roles in the deploy, *and* how to connect to them. To do this, servers should be
  added to the groups "db", "worker", and "web", as appropriate, and variables
  such as ``ansible_ssh_host`` and ``ansible_ssh_user`` can be set on individual
  hosts.

  Also - *very important* - there must be a group named the same as the environment,
  that contains all hosts for that environment. That way, any variables that we
  put into ``inventory/group_vars/<envname>`` will get applied to all the
  environment's servers by Ansible.

  Example::

      # file: inventory/staging

      # Put all staging servers into this group. We can also
      # give the servers convenient "names" here, and then use
      # ansible_ssh_host and other variables to tell Ansible how
      # to connect to them.
      [staging]
      server1 ansible_ssh_host=ec2-gibberish.more.long.domain
      server2 ansible_ssh_host=ec2-gibberish2.more.long.domain

      [web]
      server1

      [db]
      server2

      [worker]
      # no workers yet for this project

  TBD: Update that list as we add more groups?  Probably better to flesh out this
  part of the documentation in much greater detail somewhere other than this
  README.

* Put any variables that should be set for the whole project in a YAML file
  named ``$(PWD)/inventory/group_vars/all``.  E.g.::

      vi $(PWD)/inventory/group_vars/all

  and it'll look something like this::

      ---
      # file: inventory/group_vars/all
      project_name: our_neat_project
      python_version: 3.4
      less_version: 2.1.0
      postgres_version: 9.3

* Put any variables that should be set for the entire environment in a YAML file
  named ``$(PWD)/inventory/group_vars/<envname>``.  E.g.::

      vi $(PWD)/inventory/group_vars/staging

  example::

      ---
      # file: inventory/group_vars/staging
      domain: project-staging.domain.com
      repo:
        url: git@github.com:caktus/caktus-website.git
        branch: develop

* For any variables whose values need to be kept secret (e.g. passwords), declare
  them in the appropriate ``$(PWD)/inventory/group_vars/<filename>`` too, but set their value to
  ``{{ secret_<varname> }}``.  E.g. if the variable is DB_PASSWORD, put this in
  the environment variable file::

      DB_PASSWORD: {{ secret_DB_PASSWORD }}

* Then, set the actual values of the ``secret_<varname>`` variables in a YAML file named
  ``$(PWD)/inventory/secrets/<envname>`` and encrypt it using the `Ansible
  vault <http://docs.ansible.com/ansible/playbooks_vault.html>`_, e.g.::

      ansible-vault edit $(PWD)/inventory/secrets/staging

  (This two-step approach to secret variables is an
  `Ansible best practice <http://docs.ansible.com/ansible/playbooks_best_practices.html#variables-and-vaults>`_).

* Put the passwords for the Ansible vault in files named ``.vaultpassword-<envname>``.
  Be *sure* that (1) they do not get added to version control, and (2) they
  are not public (e.g. set permissions to 0600).  E.g.::

      echo ".vaultpassword*" >>.gitignore
      echo "password" >.vaultpassword-staging
      chmod 600 .vaultpassword-staging

* TODO: Add instructions here for the FIRST deploy. It might need to run
  as root or ubuntu or whatever the initial user the server has set up
  is.

* Run ``deploy <envname>`` to update servers.  E.g.::

    deploy staging

  or::

    deploy production

Where to set variables
----------------------

Ansible supports setting variables in many places. Let's try to agree on some
common practices for our projects:

* Variables that are global to the project go in ``inventory/group_vars/all``::

    ---
    # file: inventory/group_vars/all
    project_name: our_project

* Variables that apply to all servers in an environment go in
  ``inventory/group_vars/<envname>``::

    ---
    # file: inventory/group_vars/staging
    domain: project-staging.example.com

* Variables whose values should be secret should be declared in the same
  files as other variables, depending on their scope, but their value
  should be set to ``{{ secret_<varname> }}``::

    ---
    # file: inventory/group_vars/staging
    DB_PASSWORD: {{ secret_DB_PASSWORD }}

* For each secret variable mentioned in ``inventory/group_vars/<FILENAME>``,
  declare its actual value in ``inventory/secrets/<FILENAME>``.  E.g.
  if DB_PASSWORD is set to ``{{ secret_DB_PASSWORD }}`` in
  ``inventory/group_vars/staging``, then in ``inventory/secrets/staging``
  we would expect to see::

      ---
      # file: inventory/secrets/staging
      secret_DB_PASSWORD: "value of password"

* Variables telling Ansible how to connect to a particular host go into
  the inventory file, on the same line as the first mention of that host.

TODO for this README
--------------------

TODO: Create more detailed documentation, including which groups to use and
what variables need to be set, and lots of examples of the whole process

TODO: document that setting force_ssl False will make port 80 also serve
Django rather than redirecting to https.

TODO: add hstore & postgis

TODO: document that setting source_is_local True will sync the project
files from the current directory instead of pulling them from git.
