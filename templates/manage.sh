# Shell script to run a management command
cd {{ source_dir }}
./dotenv.sh {{ venv_dir }}/bin/python {{ source_dir }}/manage.py $@
