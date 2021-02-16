def collocation_2_color(collocation):
    if 0 <= collocation < 10:
        return "brown"
    elif 100 <= collocation <= 400:
        return "celeste"
    elif 500 <= collocation <= 519:
        return "red"
    elif 520 <= collocation <= 590:
        return "yellow"
    elif 600 <= collocation <= 620:
        return "green"
    elif 621 <= collocation <= 621.3:
        return "orange"
    elif 621.4 <= collocation <= 621.9:
        return "blue"
    elif 622 <= collocation <= 628:
        return "pink"
    elif 629 <= collocation <= 699:
        return "olive"
    elif 700 <= collocation <= 900:
        return "purple"
    else:
        return "black"
