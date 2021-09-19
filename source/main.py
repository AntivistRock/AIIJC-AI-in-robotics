import model
import engine

from pybullet import GUI


def main():
    agent = model.KettleModel()
    env = engine.Environment(agent)

    env.run(5)

    input()


if __name__ == "__main__":
    main()
