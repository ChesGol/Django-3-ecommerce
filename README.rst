Instruction:
# Install Poetry:
    https://python-poetry.org/docs/#installation
    poetry --version

# Configure Poetry to store virtual environment in project directory:
    poetry config virtualenvs.in-project true
    poetry config --list

# Clone project:
    open IDE that you use
    type in terminal: https://gitlab.com/PythonLT2/eshop.git to clone project
    or you can download project from https://gitlab.com/PythonLT2/eshop and open in your IDE

# Steps to run server:
    Go to project root directory
    In terminal type :
                    poetry install
                    python manage.py makemigrations
                    python manage.py migrate
                    python manage.py runserver
