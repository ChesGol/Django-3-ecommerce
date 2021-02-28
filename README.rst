# Instruction:
 Install Poetry:
    1.https://python-poetry.org/docs/#installation
    2.poetry --version

# Configure Poetry to store virtual environment in project directory:
    1.poetry config virtualenvs.in-project true
    2.poetry config --list

# Clone project:
    1.Open IDE that you use. (Remember that you must have installed git)
    2.Type in terminal: git clone https://github.com/ChesGol/Django-3-ecommerce.git to clone project.
    3.Or you can download project and open in your IDE.
# Steps to run server:
    Go to project root directory and type in terminal:
                    1.poetry install
                    2.python manage.py makemigrations
                    3.python manage.py migrate
                    4.python manage.py runserver
