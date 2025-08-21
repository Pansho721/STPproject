class User:
    def __init__(self, nombre, password, role="user"):
        self.nombre = nombre
        self.password = password  # De preferencia, hasheada
        self.role = role

    def verify_password(self, input_password):
        return self.password == input_password  # Idealmente usar hash

    def has_role(self, role):
        return self.role == role  