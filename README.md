# Polo Stats 

This program gives detailed overview of your last trades based on your current poloniex balances

## Installation

1) Clone the repository 
```
git clone https://github.com/araa47/PoloniexProfit.git 
```

2) Cd into the repository 
```
cd PoloniexProfit 
```

3) You can either follow A OR B 

#### A: System Install 

1) Install to usr/local python library

```
sudo pip install -r requirements.txt 
```

#### B: Virtual Environment Install 

1) Cd to a directory outside

```
cd ..
```

2) Create a virtualenviroment , here i have named mine pypolo

```
virtualenv pypolo 
```

3) Activate the virtualenvironment

```
source pypolo/bin/activate
```

4) Cd into the project
```
cd PoloniexProfit 
```
5) Now locally install the requirements
```
pip install -r requirements.txt
```



## API Key Configuration 

1) Open sample_apikey.py and enter your poloniex api key and secret 

2) Rename the file to apikey.py 

## Running 

In order to run the simple program, you need to give it a single parameter which is the amount of time between updates. In this example I have set my time to 2 seconds. 

```
python stats.py -l 2

```
## Mock Output

![Image of Output](outputexample.png)

## Extra Details 

1) Currently the program only calculates BTC to other currency trades 

2) The program only works on the latest trade history. For example: You bought some ripple at 0.00011 and sold at 0.00021. Next you buy more ripple at 0.15. The program will only calculate your gains from the last trade. However your total gain can be seen by checking your total portfolio value. 