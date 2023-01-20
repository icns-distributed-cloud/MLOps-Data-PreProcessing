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
    data_root_directory: str = '.'
    pre_data_root_directory: str = '.'

    backend_url: str = '163.180.117.186'
    backend_port: int = 18088


@dataclass
class ProdConfig(Config):
    project_reload: bool = False
    data_root_directory: str = '.'
    pre_data_root_directory: str = '.'
    # origin_data_root_directory: str = 'data.icnslab.net/origin'
    # pre_data_root_directory: str = 'data.icnslab.net/pre'

    backend_url: str = '163.180.117.186'
    backend_port: int = 18088


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig)
    return config.get(environ.get('API_ENV', 'local'))





