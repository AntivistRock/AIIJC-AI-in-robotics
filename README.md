# AIIJC AI in robotics
### Описание:
This repository contains developments of AIIJC robotics track

### Инструкция по скачиванию и установке:

1) Сначала склонируйте репозиторий
```console
$ git clone https://github.com/AntivistRock/AIIJC-AI-in-robotics.git
$ cd AIIJC-AI-in-robotics
```

2) Создйте виртуальное окружение
```console
$ python -m virtualenv venv

in linux:
$ source ./venv/bin/activate

in windows:
$ venv\Scripts\activate
```

4) Установите необходимые библиотеки
```console
$ pip install -r requirements.txt
```

5) И запустите симуляцию
```console
$ python "./source/main.py"
```

### Полезные ссылки:
* [Семинар Тинькофф по Reinforce](https://colab.research.google.com/drive/1U3-rixEJSEO7oNbjKVjFIEjVt0DiDiYs?usp=sharing)
* [Семинар Тинькофф по Actor Critic](https://colab.research.google.com/drive/1SFdsiSNGcisU51-28a2dZyO_k5g2PNKR?usp=sharing)
* [Захват предметов роботом Kuka в pybullet с помощью OpenAI gym](https://github.com/mahyaret/kuka_rl)
* [Интересные мысли про RL-эвристики при обучении манипулятора](https://hackernoon.com/using-reinforcement-learning-to-build-a-self-learning-grasping-robot-ld2m31w1)
* [Как импортнуть .obj модель в pybullet](https://towardsdatascience.com/simulate-images-for-ml-in-pybullet-the-quick-easy-way-859035b2c9dd)
* [Захват предметов с помощью ur5 и манипулятора](https://github.com/lzylucy/graspGripper)
