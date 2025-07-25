from setuptools import setup, find_packages

setup(
    name="pokergto",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "easyocr",
        "numpy",
        "requests",
        "pyautogui",
        "keyboard"
    ],
    entry_points={
        'console_scripts': [
            'pokergto=main:main',
        ],
    },
)
