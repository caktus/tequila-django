tequila-django
==============

This repository holds an `Ansible <http://www.ansible.com/home>`_ role
that is installable using ``ansible-galaxy``.  This role contains
tasks used to install and set up a Django web app.  It exists
primarily to support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_.


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
directory ::

    ---
    # file: deployment/requirements.yml
    - src: https://github.com/caktus/tequila-django
      version: 0.1.0

Run ``ansible-galaxy`` with your requirements file ::

    $ ansible-galaxy install -r deployment/requirements.yml

or, alternatively, run it directly against the url ::

    $ ansible-galaxy install git+https://github.com/caktus/tequila-django

The project then should have access to the ``tequila-django`` role in
its playbooks.


Variables
---------

The following variables are made use of by the ``tequila-django``
role:

- ``project_name`` **required**
- ``env_name`` **required**
- ``domain`` **required**
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
- ``static_dir`` **default:** ``"{{ root_dir }}/public/static"``
- ``media_dir`` **default:** ``"{{ root_dir }}/public/media"``
- ``log_dir`` **default:** ``"{{ root_dir }}/log"``
- ``repo`` **required:** dict containing url and branch
- ``source_is_local`` **default:** ``false``
- ``github_deploy_key`` **required if source_is_local is false**
- ``local_project_dir`` **required if source_is_local**
- ``global_npm_installs`` **default:** empty list
- ``extra_env`` **default:** empty dict

The ``global_npm_installs`` variable is a list of dicts, with required
key ``name`` for the package name, and optional key ``version`` for
the desired version to install.  This is needed for the less or sass
packages, to make them available where supervisord and gunicorn can
find them.

The ``extra_env`` variable is a dict of keys and values that is
desired to be injected into the environment as variables, via the
``envfile.j2`` template.
