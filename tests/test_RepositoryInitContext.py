from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.RepositoryInitContext import RepositoryInitContext
from pytest import raises

def test_server_invalid():
    # Make sure server parameter is not missing
    with raises(ValueError) as ex_info:
        RepositoryInitContext(server='',database='database',username='username',password='password')
    assert 'Server is missing' in ex_info.value.args[0]

def test_database_invalid():
    # Make sure server parameter is not missing
    with raises(ValueError) as ex_info:
        RepositoryInitContext(server='server',database='',username='username',password='password')
    assert 'Database is missing' in ex_info.value.args[0]

def test_username_invalid():
    # Make sure server parameter is not missing
    with raises(ValueError) as ex_info:
        RepositoryInitContext(server='server',database='database',username='',password='password')
    assert 'Username is missing' in ex_info.value.args[0]

def test_password_invalid():
    # Make sure server parameter is not missing
    with raises(ValueError) as ex_info:
        RepositoryInitContext(server='server',database='database',username='username',password='')
    assert 'Password is missing' in ex_info.value.args[0]
