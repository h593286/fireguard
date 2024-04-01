class User():
    def __init__(self, id, username, first_name,last_name,realm_roles,client_roles):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.realm_roles = realm_roles
        self.client_roles = client_roles
