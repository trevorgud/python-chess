To install dependencies and run the game:

```
apt-get install python3 python3-pip python3-tk
python3 -m pip install -U numpy pygame
./chess.py
```

To package the game into an executable using pyinstaller:

if pyinstaller is not already installed then install it.
```
pip install pyinstaller
pyinstaller --onefile chess.spec
```
