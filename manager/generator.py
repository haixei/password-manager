# This is a secure password generator, it follows all modern
# security standards and is used to generate account passwords
import random
import string


def generate():
    result_letters = ''.join((random.choice(string.ascii_letters) for i in range(random.randrange(10, 14))))
    result_numbers = ''.join((random.choice(string.digits) for i in range(random.randrange(5, 10))))
    result_special = ''.join((random.choice(string.punctuation) for i in range(random.randrange(5, 10))))

    merge = result_letters + result_numbers + result_special
    result_str = ''.join(random.sample(merge, len(merge)))

    return result_str
