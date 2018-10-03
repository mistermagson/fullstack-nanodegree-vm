from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, CategoryItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


user1 = User(name="Magson", email="magson@gmail.com")
#Menu for UrbanBurger
category1 = Category(name = "Sports",  user=user1)

session.add(user1)
session.add(category1)

for x in range(0, 5):
    categoryItem = CategoryItem(title = "Tenis %s" % x, description = "Dolor sit amet", user=user1, category = category1)
    session.add(categoryItem)
session.commit()


user1 = User(name="Fulano", email="fulano@gmail.com")
#Menu for UrbanBurger
category1 = Category(name = "Kitchen",  user=user1)

session.add(user1)
session.add(category1)

for x in range(0, 4):
    categoryItem = CategoryItem(title = "Frier %s" % x, description = "Loren Ipsum", user=user1, category = category1)
    session.add(categoryItem)
session.commit()

user1 = User(name="Ciclano", email="fulano@gmail.com")
#Menu for UrbanBurger
category1 = Category(name = "XXX",  user=user1)

session.add(user1)
session.add(category1)

for x in range(0, 3):
    categoryItem = CategoryItem(title = "YYY %s" % x, description = "Loren Ipsum", user=user1, category = category1)
    session.add(categoryItem)
session.commit()


print "added category items!"
