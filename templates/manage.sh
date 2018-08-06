# Shell script to run a management command
cd {{ django_dir }}
./dotenv.sh {{ venv_dir }}/bin/python {{ django_dir }}/manage.py $@
