tequila-django
==============

This repository holds an `Ansible <http://www.ansible.com/home>`_ role
that is installable using ``ansible-galaxy``.  This role contains
tasks used to install and set up a Django web app.  It exists
primarily to support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_.

More complete documenation can be found in `caktus/tequila
<https://github.com/caktus/tequila>`_.


License
-------

This Ansible role is released under the BSD License.  See the `LICENSE
<https://github.com/caktus/tequila-django/blob/master/LICENSE>`_ file for
more details.


Contributing
------------

If you think you've found a bug or are interested in contributing to
this project check out `tequila-django on Github
<https://github.com/caktus/tequila-django>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.


Installation
------------

Create an ``ansible.cfg`` file in your project directory to tell
Ansible where to install your roles (optionally, set the
``ANSIBLE_ROLES_PATH`` environment variable to do the same thing, or
allow the roles to be installed into ``/etc/ansible/roles``) ::

    [defaults]
    roles_path = deployment/roles/

Create a ``requirements.yml`` file in your project's deployment
directory.  It is recommended to include `tequila-common
<https://github.com/caktus/tequila-common>`_, which sets up the
project directory structure and users, and also `tequila-nodejs
<https://github.com/caktus/tequila-nodejs>`_ and `geerlingguy/nodejs
<https://github.com/geerlingguy/ansible-role-nodejs>`_ to install
nodejs and any front-end packages that your project requires ::

    ---
    # file: deployment/requirements.yml
    - src: https://github.com/caktus/tequila-common
      version: v0.8.0

    - src: https://github.com/caktus/tequila-django
      version: v0.9.11

    - src: geerlingguy.nodejs
      version: 4.1.2
      name: nodejs

    - src: https://github.com/caktus/tequila-nodejs
      version: v0.8.0

Run ``ansible-galaxy`` with your requirements file ::

    $ ansible-galaxy install -r deployment/requirements.yml

or, alternatively, run it directly against the url ::

    $ ansible-galaxy install git+https://github.com/caktus/tequila-django

The project then should have access to the ``tequila-django`` role in
its playbooks.


Variables
---------

The following variables are used by the ``tequila-django`` role:

- ``project_name`` **required**
- ``env_name`` **required**
- ``domain`` **required**
- ``additional_domains`` **default:** empty list
- ``is_web`` **default:** ``false`` (**required:** one of ``is_web`` or ``is_worker`` set to ``true``)
- ``is_worker`` **default:** ``false``
- ``python_version`` **default:** ``"2.7"``
- ``root_dir`` **default:** ``"/var/www/{{ project_name }}"``
- ``source_dir`` **default:** ``"{{ root_dir }}/src"``
- ``venv_dir`` **default:** ``"{{ root_dir }}/env"``
- ``ssh_dir`` **default:** ``"/home/{{ project_name }}/.ssh"``
- ``requirements_file`` **default:** ``"{{ source_dir }}/requirements/{{ env_name }}.txt"``
- ``requirements_extra_args`` **default:** ``""``
- ``use_newrelic`` **default:** ``false``
- ``new_relic_license_key`` **required if use_newrelic is true**
- ``cloud_staticfiles`` **default:** ``false``
- ``gunicorn_version`` **optional**
- ``gunicorn_num_workers`` **required**
- ``gunicorn_num_threads`` **optional** (note: gunicorn sets this at ``1`` if ``--threads=...`` is not given)
- ``project_user`` **default:** ``"{{ project_name }}"``
- ``project_settings`` **default:** ``"{{ project_name }}.settings.deploy"``
- ``secret_key`` **required**
- ``db_name`` **default:** ``"{{ project_name }}_{{ env_name }}"``
- ``db_user`` **default:** ``"{{ project_name }}_{{ env_name }}"``
- ``db_host`` **default:** ``'localhost'``
- ``db_port`` **default:** ``5432``
- ``db_password`` **required**
- ``cache_host`` **optional**
- ``broker_host`` **optional**
- ``broker_password`` **optional**
- ``celery_worker_extra_args`` **default:** ``"--loglevel=INFO"``
- ``celery_events`` **default:** ``false``
- ``celery_camera_class`` **default:** ``"django_celery_monitor.camera.Camera"``
- ``static_dir`` **default:** ``"{{ root_dir }}/public/static"``
- ``media_dir`` **default:** ``"{{ root_dir }}/public/media"``
- ``log_dir`` **default:** ``"{{ root_dir }}/log"``
- ``repo`` **required:** dict containing url and branch
- ``source_is_local`` **default:** ``false``
- ``github_deploy_key`` **required if source_is_local is false**
- ``local_project_dir`` **required if source_is_local**
- ``extra_env`` **default:** empty dict
- ``project_subdir`` **default:** ``""`` - if a project's main source
  directory is a subdir of the git repo checkout top directory, e.g.
  manage.py is not in the top directory and you have to cd to a subdirectory
  before running it, then set this to the relative path of that subdirectory.
- ``wsgi_module`` **default:** ``{{ project_name }}.wsgi`` - allow
  configuring an alternate path to the project's wsgi module.

The ``extra_env`` variable is a dict of keys and values that is
desired to be injected into the environment as variables, via the
``envfile.j2`` template, which will be uploaded as a .env file for use
with the django-dotenv library.  Variables will be injected into this
file wrapped in single-quotes, so no additional escaping needs to be
done to make them safe.

Note that if ``source_is_local`` is set to false, a Github checkout
key needs to be provided in the environment secrets file, and that key
needs to be added to the repo's settings within Github.
Alternatively, if ``source_is_local`` is set to true, the user's local
checkout of the repo is rsynced into the environment, with a few
exclusions (.pyc files, the .git directory, the .env file, and the
node_modules directory).

The ``cloud_staticfiles`` variable is to allow for the case where the
Django static files are being collected to an external service, such
as S3.  In that case, we don't want to be running ``collectstatic`` on
every web instance, since they'll be getting in each other's way.
This variable set to ``true`` causes the ``collectstatic`` task to be
run only once.

The ``celery_events`` and ``celery_camera_class`` variables are used
to enable and configure Celery event monitoring using the "snapshots"
system, which allows worker activity to be tracked in a less expensive
way than storing all event history on disk. Setting ``celery_events``
to ``true`` will set up the ``celery events`` command to be run alongside
the other Celery commands. By default this will use the
`django-celery-monitor <https://github.com/jezdez/django-celery-monitor>`_
app as its snapshot "camera", so either ensure that this app is installed
in your project or change ``celery_camera_class`` to a string naming
the alternative camera class to use (e.g. ``myapp.Camera``). For
more on Celery event monitoring, see
`the docs <http://docs.celeryproject.org/en/latest/userguide/monitoring.html>`_.

Optimizations
-------------

You can turn on `SSH pipelining (http://docs.ansible.com/ansible/latest/intro_configuration.html#pipelining)
<http://docs.ansible.com/ansible/latest/intro_configuration.html#pipelining>`_
to speed up ansible commands (by minimizing SSH operations). Add the following
to your project's `ansible.cfg` file ::

    [ssh_connection]
    pipelining = True

**Warning:** this will cause deployments to break if ``securetty`` is used in your server's
``/etc/sudoers`` file.
