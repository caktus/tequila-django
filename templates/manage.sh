# Shell script to run a management command
cd {{ source_dir }}/{{ project_subdir }}
./dotenv.sh {{ venv_dir }}/bin/python {{ source_dir }}/{{ project_subdir }}/manage.py $@
