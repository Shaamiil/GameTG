import random

cartridge = ["боевой", "холостой"]


def create_cartridges(number: int):
    cartridges = []
    for i in range(number):
        cartridges.append(random.choice(cartridge))
    if "боевой" not in cartridges:
        cartridges.append("боевой")
    elif "холостой" not in cartridges:
        cartridges.append("холостой")
    return cartridges

