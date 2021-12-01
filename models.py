import json


class Paintings:
    def __init__(self):
        try:
            with open("paintings.json", "r") as f:
                self.paintings = json.load(f)
        except FileNotFoundError:
            self.paintings = []

    def all(self):
        return self.paintings

    def get(self, id):
        painting = [painting for painting in self.all() if painting['id'] == id]
        if painting:
            return painting[0]
        return []

    def create(self, data):
        self.paintings.append(data)
        self.save_all()

    def save_all(self):
        with open("paintings.json", "w") as f:
            json.dump(self.paintings, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.paintings[id] = data
        self.save_all()

    def delete(self, id):
        todo = self.get(id)
        if todo:
            self.todos.remove(todo)
            self.save_all()
            return True
        return False

    def update(self, id, data):
        todo = self.get(id)
        if todo:
            index = self.todos.index(todo)
            self.todos[index] = data
            self.save_all()
            return True
        return False


paintings = Paintings()