class Puppy:
    n_puppies = 0

    # define __new__
    def __new__(cls):
        if cls.n_puppies < 10:
            cls.n_puppies += 1
            return cls.__init__(cls)
        return None
