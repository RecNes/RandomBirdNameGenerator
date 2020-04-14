import string, random
uni=string.ascii_letters+string.digits+string.punctuation
print(repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))])))
