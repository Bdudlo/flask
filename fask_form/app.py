import flask
import os

class Person:
    def __init__(self, first_name, last_name, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

    def to_string(self):
        return f"{self.first_name};{self.last_name};{self.age};{self.gender}\n"

app = flask.Flask(__name__)

# Ścieżka do pliku bazy danych
db_file_path = os.path.join(os.path.dirname(__file__), 'db/base.csv')

# Lista przechowująca obiekty Person
persons_list = []

# Funkcja wczytująca dane z pliku do listy
def load_from_file():
    persons_list.clear()
    if os.path.exists(db_file_path):
        with open(db_file_path, 'r') as f:
            for line in f.readlines():
                data = line.strip().split(';')
                if len(data) == 4:
                    person = Person(data[0], data[1], data[2], data[3])
                    persons_list.append(person)

# Funkcja zapisująca dane z listy do pliku
def save_to_file():
    with open(db_file_path, 'w') as f:
        for person in persons_list:
            f.write(person.to_string())

@app.route('/')
def home():
    load_from_file()
    return flask.render_template("index.html", list_values=persons_list)

@app.route('/add', methods=['POST'])
def add_user():
    try:
        person_data = flask.request.form
        new_person = Person(person_data['imie'], person_data['nazwisko'], person_data['wiek'], person_data['plec'])

        # Dodaj nową osobę do listy
        persons_list.append(new_person)

        # Zapisz listę do pliku
        save_to_file()

        return flask.redirect('/')
    except Exception as e:
        return f'Błąd podczas dodawania osoby: {str(e)}'

@app.route('/del/<int:index>', methods=['POST'])
def deletef(index):
    try:
        # Usuń osobę z listy na podstawie indeksu
        deleted_person = persons_list.pop(index)

        # Zapisz listę do pliku po usunięciu osoby
        save_to_file()

        return flask.redirect('/')
    except Exception as e:
        return f'Błąd podczas usuwania osoby: {str(e)}'

@app.route('/edit/<int:index>', methods=['GET'])
def editform(index):
    try:
        # Pobierz dane osoby na podstawie indeksu
        person = persons_list[index]

        return flask.render_template("edit.html", index=index, person=person)
    except Exception as e:
        return f'Błąd podczas edycji osoby: {str(e)}'

@app.route('/updatedb/<int:index>', methods=['POST'])
def updatedb(index):
    try:
        person_data = flask.request.form
        updated_person = Person(person_data['imie'], person_data['nazwisko'], person_data['wiek'], person_data['plec'])

        # Zaktualizuj dane osoby na podstawie indeksu
        persons_list[index] = updated_person

        # Zapisz listę do pliku po aktualizacji osoby
        save_to_file()

        return flask.redirect('/')
    except Exception as e:
        return f'Błąd podczas aktualizacji osoby: {str(e)}'

if __name__ == "__main__":
    app.run(debug=True)