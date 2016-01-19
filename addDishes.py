from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Cuisine, Base, Dish, User

###connect to the the dabatase
engine = create_engine('sqlite:///cuisinewithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()


# Dish for American Cuisine
cuisine1 = Cuisine(user_id=1, name="American")

session.add(cuisine1)
session.commit()

Dish1 = Dish(user_id=1, name="Beer Chicken Tartar", description="It's got a nice and crisp outside and juicy, tender and moist chicken on the inside.",
                     cuisine=cuisine1)

session.add(Dish1)
session.commit()


Dish2 = Dish(user_id=1, name="Old Monk Sticky Chicken Wings", description="Chicken wings are marinated, roasted and then flambeed with rum.",
                     cuisine=cuisine1)

session.add(Dish2)
session.commit()

Dish3 = Dish(user_id=1, name="Classic American Pancakes", description="Start your day with these classic American pancakes. They are easy to make and can have various toppings like maple syrup or honey or fresh berries- the choice is yours!",
                       cuisine=cuisine1)

session.add(Dish3)
session.commit()

Dish4 = Dish(user_id=1, name="Mint Julep", description="Shake up some bourbon with fresh mint & lime! Voila, you've got yourself a party starter.",
                     cuisine=cuisine1)

session.add(Dish4)
session.commit()

Dish5 = Dish(user_id=1, name="Chilli Burgers with Pepper Relish", description="An American recipe of chilli burgers. A spiced lamb patty slapped between burger buns served with a roasted red bell pepper dip.",
                     cuisine=cuisine1)

session.add(Dish5)
session.commit()

Dish6 = Dish(user_id=1, name="Cola BBQ Sauce", description="A BBQ sauce with a twist! This one has a strong cola flavor. Try out something different.",
                     cuisine=cuisine1)

session.add(Dish6)
session.commit()

Dish7 = Dish(user_id=1, name="Apple Sausage Plait", description="This one's a winter delight! A filling of apples, lime, herbs and sausage meat wrapped in puff pastry.",
                     cuisine=cuisine1)

session.add(Dish7)
session.commit()

Dish8 = Dish(user_id=1, name="Grilled Cheese Sandwich",
                     description="On texas toast with American Cheese", cuisine=cuisine1)

session.add(Dish8)
session.commit()

Dish9 = Dish(user_id=1, name="Sloppy Joes", description="Crusty bread topped with a delicious lamb mince, roasted eggplants and cheddar cheese. Combine this with a beer or some fizzy drink and you're sorted.",
                      cuisine=cuisine1)
session.add(Dish9)
session.commit()


# Dishes for Chinese
cuisine2 = Cuisine(user_id=1, name="Chinese")

session.add(cuisine2)
session.commit()


dish1 = Dish(user_id=1, name="Vegetable Manchow Soup", description="Savour the hot and spicy flavours of this Chinese vegetable manchow soup.",
                     cuisine=cuisine2)

session.add(dish1)
session.commit()

dish2 = Dish(user_id=1, name="Peking Duck",
                     description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", cuisine = cuisine2)

session.add(dish2)
session.commit()

dish3 = Dish(user_id=1, name="Cantonese Chicken Soup", description="An authentic Chinese soup, the Cantonese Soup is a hearty mix of chicken and vegetables chopped into small pieces in piping hot chicken stock",
                    cuisine=cuisine2)

session.add(dish3)
session.commit()

dish4 = Dish(user_id=1, name="Stir Fried Tofu with Rice", description="An easy,vegetarian, Chinese style recipe laden with sam pal oelic and soya sauce which flavors it up!",
                     cuisine=cuisine2)

session.add(dish4)
session.commit()

dish5 = Dish(user_id=1, name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     cuisine=cuisine2)

session.add(dish5)
session.commit()

dish6 = Dish(user_id=1, name="Chilli Fish", description="Boneless pieces of fish, batter fried and doused in a spicy-tangy sauce.",
                     cuisine=cuisine2)

session.add(dish6)
session.commit()


# dishes for french
cuisine3 = Cuisine(user_id=1, name="French")

session.add(cuisine3)
session.commit()


dish1 = Dish(user_id=1, name="Crepe Suzette", description="They're light, fluffy, silky smooth and made using orange juice, rind and water.",
                    cuisine = cuisine3)

session.add(dish1)
session.commit()

dish2 = Dish(user_id=1, name="Spinach and Potato Soup", description="Seasoned with salt, pepper, some cream and a hint of nutmeg, this soup is quick, delicious and perfect for a nippy winter evening.",
                     cuisine = cuisine3)

session.add(dish2)
session.commit()

dish3 = Dish(user_id=1, name="Lobster Thermidor", description="Beautifully cooked lobster meat tossed together with mustard, salt, pepper and cream that comes paired with a delicate sauce made with brandy and egg yolks.",
                     cuisine = cuisine3)

session.add(dish3)
session.commit()

dish4 = Dish(user_id=1, name="Coq Au Vin", description="Get fancy with 'Coq Au Vin', a classic French delicacy! Braise the chicken with red wine, mushrooms, garlic and bacon lardons before throwing in some fresh parsley.",
                     cuisine = cuisine3)

session.add(dish4)
session.commit()

dish5 = Dish(user_id=1, name="Algerienne Fish", description="Fish fillets are marinated in lemon juice, baked and topped with a freshly made tomato sauce.",
                    cuisine = cuisine3)

session.add(dish5)
session.commit()


# dishes for italian
cuisine4 = Cuisine(user_id=1, name="Italian")

session.add(cuisine4)
session.commit()


dish1 = Dish(user_id=1, name="Fettuccine in White Sauce", description="Long strands of fettuccine smeared in a cream-based white sauce and blessed with traces of garlic and capsicum.",
                     cuisine = cuisine4)

session.add(dish1)
session.commit()

dish2 = Dish(user_id=1, name="Meatballs", description="These round, bite-sized and juicy meatballs need only 10 minutes to cook and can be enjoyed with spaghetti, pasta, rice and even as is, doused in a rich and tangy sauce.",
                     cuisine = cuisine4)

session.add(dish2)
session.commit()

dish3 = Dish(user_id=1, name="Risotto-e-Tonno",
                     description="Brown rice, capers, chopped olives, mixed vegetables and fresh lemon juice all come together to create this easy, healthy meal perfect to pack for lunch or a picnic! Top with moist tuna chops, and enjoy it like never before.", cuisine = cuisine4)

session.add(dish3)
session.commit()

dish4 = Dish(user_id=1, name="Deviled Eggs", description="A popular Italian preparation, hard-boiled eggs are filled with a foamy mix of egg yolk, mustard and mayo.",
                    cuisine = cuisine4)

session.add(dish4)
session.commit()

dish5 = Dish(user_id=1, name="Fusilli Tomatina", description="Fusilli pasta cooked in a herb-y, tomato-based, sensational sauce makes an easy and anytime meal.",
                     cuisine = cuisine4)

session.add(dish5)
session.commit()

dish6 = Dish(user_id=1, name="Fritto Misto", description="Munch on these golden snacks made of a host vegetables bathed in flour and fried to perfection.",
                     cuisine = cuisine4)

session.add(dish6)
session.commit()


# dishes for greek
cuisine5 = Cuisine(user_id=1, name="Greek")

session.add(cuisine5)
session.commit()


# dishes for Japanese
cuisine6 = Cuisine(user_id=1, name="Japanese")

session.add(cuisine6)
session.commit()


dish1 = Dish(user_id=1, name="Japanese Soba Noodles", description="Easy to make, these noodles taste delicious when stir-fried with teriyaki sauce. Throw in some veggies like mushrooms and carrots, caramalised pork strips (if you like) or just dunk them in dashi.",
                     cuisine = cuisine6)

session.add(dish1)
session.commit()


print "added menu items!"