ID = 1
name = "This person"
print(name)


def say(something):
    print(name, 'says', something)


from animal.pet import name as pet_name, run as pet_run


def have():
    print(name, 'has', pet_name)
