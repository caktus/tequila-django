Tequila-django
==============

Changes

v 0.9.21 on Jan 28, 2019
------------------------

* When rsyncing local source to server (when source_is_local is true,
  mainly when using vagrant), exclude deployment dir, and use the
  same ssh as ansible.

v 0.9.20 on Dec 27, 2018
------------------------

* Remove --log-syslog from the supervisor gunicorn command line. Supervisor
  was already logging the gunicorn stdout to syslog and trying to log it twice
  was failing.

v 0.9.19 on Nov 21, 2018
----------------------------

* Add ability to customize Celery app name via ``celery_app`` variable.


v 0.9.18 on Sep 26, 2018
----------------------------

* Allow a celery beat instance to be deployed and configured
  independently of the celery worker instances.  This is because it is
  desirable to have only one beat instance, generally.

  It is recommended to add a new group to your inventory files,
  e.g. ``[beat]``, that has exactly one instance in it, which may be
  an instance that is also in your ``[worker]`` group.  You may then
  create a new playbook, e.g. ``deployment/playbooks/beat.yml``,
  containing something like::

    ---
    - hosts: beat
      become: yes
      roles:
        - { role: tequila-django, is_celery_beat: true }

  If you go this route, do not forget to add this new beat.yml file to
  the list invoked by your site.yml playbook.  Note that if you
  incorporate this change this way, the tequila-django role will be
  executed multiple times on instances that incorporate these
  differing variants.  Alternatively, one can fold together the
  invocation of tequila-django into a single playbook that uses group
  checking to set the parameters used, like so::

    ---
    - hosts: web:worker:beat
      become: yes
      roles:
        - role: tequila-django
          is_web: "{{ 'web' in group_names }}"
          is_worker: "{{ 'worker' in group_names }}"
          is_celery_beat: "{{ 'beat' in group_names }}"

  This has the advantage of requiring only one loop through the
  tequila-django tasks per server instance.

v 0.9.17 on Sep 11, 2018
------------------------

* Consistently use manage.py and dotenv.sh to invoke Django with
  the same environment.

v 0.9.16 on Aug 6, 2018
-----------------------

* New variable ``project_subdir`` to accomodate projects where
  the Django project (``manage.py`` etc.) are in a subdirectory of
  the repository.
* New variable ``wsgi_module`` to accomodate projects where the
  package of the wsgi module is not ``{{ project_name }}.wsgi``.

v 0.9.15 on July 31, 2018
--------------------------

* Fix syntax error in ``celery.yml``

v 0.9.14 on July 30, 2018
--------------------------

* New variable ``project_port`` to have Django listen on a port
  other than 8000, to help with multi-site deploys.
* Update README with example for SSH agent forwarding.

v 0.9.13 on June 1, 2018
--------------------------

* Add additional variables to enable Celery event monitoring
  with snapshots.

  Per the remarks added to the "Variables" section of the
  README, tequila-django now includes variables that allow
  the user to turn on Celery event monitoring alongside
  other Celery commands. This relies on the ``celery events``
  command introduced in Celery 3.1, and by default it uses
  the ``django-celery-monitor`` app to capture worker events.

v 0.9.12 on May 31, 2018
--------------------------

* Split out the npm tasks into a new role, `tequila-nodejs
  <https://github.com/caktus/tequila-nodejs>`_.  Projects upgrading to
  this version will need to add tequila-nodejs to their
  requirements.yml file while still retaining geerlingguy.nodejs,
  which is a dependency of this new role.  Additionally, the
  playbook/web.yml playbook should be updated to execute
  tequila-nodejs instead of geerlingguy.nodejs, and it should be
  placed immediately after the tequila-django role.  See the new
  example web.yml file in the playbooks directory in the
  `caktus/tequila <https://github.com/caktus/tequila>`_ repo.

v 0.9.11 on March 19, 2018
--------------------------

* Add additional env vars to account for Celery 4's renamed
  configuration settings.

  NOTE: if you are upgrading from Celery 3 to Celery 4, be
  aware of the changes made to Celery's setting names.
  Most relevant to tequila-django, the changed names
  include the environment-variable-dependent
  settings determined by the secrets ``broker_host``
  and ``broker_password``.

  Old setting names will still work after the change, but
  users are encouraged to upgrade as soon as possible.
  Settings can be upgraded automatically using the Celery 4
  command line interface.

  For more details, see the Celery 4 `"What’s new in Celery
  4.0" <http://docs.celeryproject.org/en/latest/whatsnew-4.0.html>`_
  changelog document, in particular the "`For Django
  users and others who want to keep uppercase names"
  <http://docs.celeryproject.org/en/latest/whatsnew-4.0.html#lowercase-setting-names>`_
  section.


v 0.9.10 on Mar 2, 2018
-----------------------

* Move celerybeat's pid file to an in-memory filesystem.


v 0.9.9 on Dec 12, 2017
-----------------------

* Throw a failure if the presence of packages in the project
  package.json ``devDependencies`` object is detected.  Projects will
  need to move their dependencies into the ``dependencies`` object
  instead, or disable the check by setting ``ignore_devdependencies``
  to ``true``.


v 0.9.8 on Nov 27, 2017
-----------------------

* Properly quoting all environment variables.

  Previously, most of the Ansible variables that were dropped into the .env file were not being quoted within that file, making many characters (spaces, characters with special meaning to the shell, etc.) unsafe for use within this file.  The workaround was to double-quote your Ansible variables, but now with this change any such variables need to be identified and the extra quoting removed.


v 0.9.7 on Oct 19, 2017
-----------------------

* Work around for Ansible bug #25431. Store Github deploy key in a fact
  so it's available regardless of result of previous task.


v 0.9.6 on Sep 21, 2017
-----------------------

* Added an ``additional_domains`` variable, to allow for the
  multi-domain case to be supported in the Django settings file.


v 0.9.5 on Sep 13, 2017
-----------------------

* Added a ``cloud_staticfiles`` boolean variable, that determines
  whether to run ``collectstatic`` only once or not.


v 0.9.4 on Sep 6, 2017
----------------------

* Mark the Django migration task to only run once.


v 0.9.3 on Aug 28, 2017
-----------------------

* Allow Git checkout of source tree on Vagrant environments instead
  of only supporting source_is_local=true.

* Ignore .env and node_modules when rsync-ing source tree for
  source_is_local processing.


v 0.9.2 on Aug 17, 2017
-----------------------

* Adjustment to the Django migrate task to improve its speed, and a
  suggestion for a project-wide setting to improve it further.


v 0.9.1 on July 20, 2017
------------------------

* Convert the collectstatic task into a handler.  This is needed so
  that it happens after the ``npm run build`` step, so that the files
  generated from that are included.


v 0.9.0 on July 18, 2017
------------------------

* Remove the nodejs installation and package management in favor of
  the geerlingguy/nodejs Ansible role.

  .. IMPORTANT::

     To upgrade to this version, you will have to make the following
     changes to your deployment files.

     1. Add the geerlingguy/nodejs role to
        deployment/requirements.yml, and bump the version of
        tequila-django::

          ---
          - src: https://github.com/caktus/tequila-django
            version: v0.9.3
            name: tequila-django

          - src: geerlingguy.nodejs
            version: 4.1.2
            name: nodejs
          ...

     #. Install the new role, and make sure that tequila-django gets
        upgraded.  Since ``ansible-galaxy`` does not at this time seem
        to have support for version upgrades, either explicitly remove
        the tequila-django directory from deployment/roles/, or use
        ``ansible-galaxy uninstall tequila-django``, before running
        the command to install the roles from the requirements.yml
        file.

     #. Include the configuration variables for geerlingguy/nodejs in
        your project-wide variables file (usually
        deployment/playbooks/group_vars/all/project.yml)::

          ---
          nodejs_version: "6.x"
          nodejs_install_npm_user: "{{ project_name }}"
          nodejs_package_json_path: "{{ source_dir }}"
          nodejs_config_unsafe_perm: true

        If you previously had anything configured under the variable
        ``global_npm_installs``, rename this variable to
        ``nodejs_npm_global_packages``.  Note that
        ``nodejs_config_unsafe_perm`` has to be set to ``true`` in
        order for the global npm installs to work for
        ``nodejs_install_npm_user`` set to anything other than root.

     #. If you previously had a different version of nodejs installed
        using a .deb package, you should probably uninstall it, and
        remove any PPA source file associated with it (if used).

     #. Modify your deployment/playbooks/web.yml file (or equivalent)
        to include the nodejs role _after_ the tequila-django role::

          ---
          - hosts: web
            become: yes
            roles:
              - tequila-nginx
              - { role: tequila-django, is_web: true }
              - nodejs
