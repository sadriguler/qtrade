from os import getcwd
from os.path import abspath
from os.path import dirname

script_path = abspath(__file__)
dir_path = dirname(script_path)
PROJECT_PATH = f'{dir_path}/..'

DATA_PATH = f'{PROJECT_PATH}/data/' 
DATA_PATH_USER = f'{DATA_PATH}/user_data/'
DATA_PATH_MARKET = f'{DATA_PATH}/market_data/'

YF_ASSET_NAMES = {
    'EURTRY' : 'EURTRY=X',
    'USDTRY' : 'TRY=X',
}