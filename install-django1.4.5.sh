#update repository
sudo apt update
sudo add-apt-repository universe
sudo apt install python2
curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
sudo python2 get-pip.py
pip install Django==1.4.5
pip --version
 sudo apt-get autoremove