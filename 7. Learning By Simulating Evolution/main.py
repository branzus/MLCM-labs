import genetic
import dp
import json


def load_dataset(filename):

    x = json.load(open(filename, "r"))
    return x




if __name__ == "__main__":
    a = load_dataset("testset_100.json")
    print(dp.solve(*a))
    print(genetic.solve(*a, 1000, 50, 0.8, 0.15, 0.5))
    print(genetic.solve(*a, 50, 1000, 0.8, 0.15, 0.05))
    print(genetic.solve(*a, 50, 1000, 0.6, 0.3, 0.1))
