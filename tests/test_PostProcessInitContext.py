from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.PostProcessInitContext import PostProcessInitContext
from pytest import raises

def test_success_log_filename_invalid():
    # Make sure success_log_filename is not missing
    with raises(ValueError) as ex_info:
        PostProcessInitContext(success_log_filename='', failed_log_filename='failed.log')
    assert 'missing' in ex_info.value.args[0]

def test_failed_log_filename_invalid():
    # Make sure failed_log_filename is not missing
    with raises(ValueError) as ex_info:
        PostProcessInitContext(success_log_filename='success.log', failed_log_filename='')
    assert 'missing' in ex_info.value.args[0]

def test_initialization_valid():
    ctx = PostProcessInitContext(success_log_filename='success.log', failed_log_filename='failed.log')
    assert ctx.failed_log_filename == 'failed.log'
    assert ctx.success_log_filename == 'success.log'