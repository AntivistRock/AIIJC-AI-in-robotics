from pybullet import GUI

import engine
import model


def main():

    i_model = model.Model()

    env = engine.Environment(i_model, GUI)
    env.run(10000)


if __name__ == "__main__":
    main()
