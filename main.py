# mohmmed:
# adham:
# arwa:
# habiba:
# aya:

class User:
    # eldoctor mkansh kateb password bs m7tagenha fe el login
    def __init__(self, user_id, name, role, email, __password):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email
        self.__password = __password
        self.logged_in = False

    def login(self, email, password):
        if email == self.email and password == self.password:
            print("logged in sucessfully")
            #3aizen n3ml option eno y create account
        else:
            print("invalid email or password")

    def logout(self):
        self.logged_in = False
        print("loged out sucessfully")

    def view_dashboard(self):
        print(f"Dashboard of : {self.name}")
        print(f"user data: /n Name: {self.name} /n role: {self.role} /n Id: {self.user_id} /n Email: {self.email}")
