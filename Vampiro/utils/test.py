from faker import Faker

from ..models.UserModel import User, Role
from ..database.mysql import db

# Create a Faker instance
fake = Faker()

def generate_test_db(num_users=100):
    """
    Generates a test database with the specified number of users
    """
    # Create the users
    for _ in range(num_users):
        # Generate fake data for the user
        name = fake.name()
        email = fake.email()
        password = fake.password()
        room = fake.random_int(min=200, max=500)

        # Create the user
        user = User(name=name, email=email, password=password, room=room)
        
        # Assign role based on user index
        if _ < num_users/2:
            role = Role.query.filter_by(name="visitor").first()
            user.role = role
        else:
            role = Role.query.filter_by(name="player").first()
            user.role = role
        
        #Confirm all users
        user.confirmed_at = fake.date_time_this_decade()

        #Print on screen
        print(room, password)

        db.session.add(user)

    # Commit the changes to the database
    db.session.commit()

# Call the function to generate the test database
generate_test_db()