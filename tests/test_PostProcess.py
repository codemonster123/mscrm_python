from sys import path
from pathlib import Path; 
path.append(str(Path(__file__).parent.parent)+'/src/')

from smtp.IncidentRepository import IncidentRepository
from smtp.Incident import Incident
from smtp.PostProcessInitContext import PostProcessInitContext
from smtp.PostProcess import PostProcess
import pytest
from unittest.mock import patch
from pprint import pprint

@patch('csv.writer')
def test_initialization_valid(mock_cvs_writer):
    ctx = PostProcessInitContext('success.log','failed.log')
    PostProcess(ctx)

def test_mark_as_sent_not_initialized():
    with patch.object(PostProcess, '__init__', lambda self, ctx: None):
        with pytest.raises(Exception) as ex_info:
            pp = PostProcess(PostProcessInitContext(success_log_filename='success.log',failed_log_filename='failed.log'))
            pp.mark_as_sent(Incident('incidentid', 'some@email.com', 'contact_name',
                                     'title', 'prior_status', 'status', 'ticketnumber'))
        assert 'no attribute' in ex_info.value.args[0]

def test_mark_as_sent_success_log_not_initialized():
    with patch.object(PostProcess, '__init__', lambda self, ctx: None):
        with pytest.raises(Exception) as ex_info:
            pp = PostProcess(PostProcessInitContext(success_log_filename='success.log',failed_log_filename='failed.log'))
            pp.__setattr__('success_log_filename','')
            pp.mark_as_sent(Incident('incidentid', 'some@email.com', 'contact_name',
                                     'title', 'prior_status', 'status', 'ticketnumber'))
        assert 'not initialized' in ex_info.value.args[0]


@patch('csv.writer')
def test_mark_as_sent_success(mock_csv_writer):
    pp = PostProcess(PostProcessInitContext(success_log_filename='success.log',failed_log_filename='failed.log'))
    pp.mark_as_sent(Incident('incidentid', 'some@email.com', 'contact_name',
                                'title', 'prior_status', 'status', 'ticketnumber'))
    mock_csv_writer.return_value.writerow.assert_called()  



@patch('csv.writer')
def test_mark_as_failed_to_send(mock_csv_writer):
    pp = PostProcess(PostProcessInitContext(success_log_filename='success.log',failed_log_filename='failed.log'))
    pp.mark_as_failed_to_send(Incident('incidentid', 'some@email.com', 'contact_name',
                                'title', 'prior_status', 'status', 'ticketnumber'),
                                Exception('test'))
    mock_csv_writer.return_value.writerow.assert_called()  

def test_mark_as_failed_to_send_not_initialized():
    with patch.object(PostProcess, '__init__', lambda self, ctx: None):
        with pytest.raises(Exception) as ex_info:
            pp = PostProcess(PostProcessInitContext(success_log_filename='success.log',failed_log_filename='failed.log'))
            pp.__setattr__('failed_log_filename','')
            pp.mark_as_failed_to_send(Incident('incidentid', 'some@email.com', 'contact_name',
                                     'title', 'prior_status', 'status', 'ticketnumber'),
                                     Exception('test'))
        assert 'not initialized' in ex_info.value.args[0]