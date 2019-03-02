import argparse
import random


def random_quality():
    rand = random.randint(1, 101)
    # 8%
    if rand <= 8:
        quality = 1
    # 36%
    elif 8 < rand <= 43:
        quality = 2
    # 39%
    elif 43 < rand <= 82:
        quality = 3
    # 15%
    elif 82 < rand <= 97:
        quality = 5
    # 2%
    else:
        quality = 45
    return quality


def do_spin(items):
    quality = random_quality()
    item = random.choice(items)
    return "{item} 5 {quality} 1".format(item=item, quality=quality)


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            "{} is an invalid positive int value".format(value)
        )
    return ivalue


def do_multiple_spins(value):
    ivalue = check_positive(value)
    with open('items.txt') as f:
        items = f.read().splitlines()

    output = []
    for i in range(ivalue):
        output.append(do_spin(items))

    return ' | \n\n'.join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spins", type=int, help="The number of spins"
    )
    args = parser.parse_args()

    print(do_multiple_spins(args.spins))
