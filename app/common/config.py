from dataclasses import dataclass, asdict
from os import path, environ


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    '''
    기본 Configuration 
    '''

    BASE_DIR = base_dir


@dataclass
class LocalConfig(Config):
    project_reload: bool = True
    origin_data_root_directory: str = 'data/origin'
    pre_data_root_directory: str = 'data/pre'


@dataclass
class ProdConfig(Config):
    project_reload: bool = False
    origin_data_root_directory: str = 'data/origin'
    pre_data_root_directory: str = 'data/pre'
    # origin_data_root_directory: str = 'data.icnslab.net/origin'
    # pre_data_root_directory: str = 'data.icnslab.net/pre'


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig)
    return config.get(environ.get('API_ENV', 'local'))





