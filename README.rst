tequila-django
==============

This repository holds an `Ansible <http://www.ansible.com/home>`_ role
that is installable using ``ansible-galaxy``.  This role contains
tasks used to install and set up a Django web app.  It exists
primarily to support the `Caktus Django project template
<https://github.com/caktus/django-project-template>`_.


License
-------

These playbooks are released under the BSD License.  See the `LICENSE
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
    roles_path = roles/

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
- ``python_version`` **default:** ``"2.7"``
- ``root_dir`` **default:** ``"/var/www/{{ project_name }}"``
- ``source_dir`` **default:** ``"{{ root_dir }}/src"``
- ``venv_dir`` **default:** ``"{{ root_dir }}/env"``
- ``ssh_dir`` **default:** ``"/home/{{ project_name }}/.ssh"``
- ``new_relic_license_key`` **optional**
- ``gunicorn_num_workers`` **required**
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
- ``static_dir`` **default:** ``"{{ root_dir }}/public/static"``
- ``media_dir`` **default:** ``"{{ root_dir }}/public/media"``
- ``log_dir`` **default:** ``"{{ root_dir }}/log"``
- ``github_deploy_key`` **required**
- ``repo`` **required:** dict containing url and branch
- ``source_is_local`` **required**
- ``local_project_dir`` **required if source_is_local**
- ``requirements_name`` **default:** ``{'local': 'dev'}``
- ``use_newrelic`` **default:** ``false``
- ``less_version`` **required**
