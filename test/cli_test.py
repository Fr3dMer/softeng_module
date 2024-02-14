"""***************************************************************************
File          : cli_test.py
About         : Test cli is working as expected 
Author        : Freddie Mercer
Date modified : 2023-12-20
***************************************************************************"""

import pytest
import src.cli as cli_obj


def test_cli_obj_valid_args():
    # Test case for making sure all args wo
    args = ["-p", 
            "1", 
            "-r", 
            "rcode", 
            "-pid", 
            "patientID", 
            "-sid", 
            "sampleID", 
            "-b37", 
            "test", 
            "-b38", 
            "test"]
    cli = cli_obj.cli_obj(args)

    assert cli.args.panel_id == 1
    assert cli.args.rcode == "rcode"
    assert cli.args.patientID == "patientID"
    assert cli.args.sampleID == "sampleID"
    assert cli.args.bed37 == "test"
    assert cli.args.bed38 == "test"


def test_cli_obj_invalid_combination_args():
    # Test case for invalid combination of arguments
    args = ["-p", "1", "-r", "rcode", "-sid", "sampleID"]

    with pytest.raises(SystemExit):
        cli = cli_obj.cli_obj(args)


def test_cli_obj_no_sampleid():
    # Test case for not providing sampple_id wiht rcode
    args = ["-pid", "patientID"]

    with pytest.raises(SystemExit):
        cli = cli_obj.cli_obj(args)


def test_cli_obj_no_patientid():
    # Test case for not providing patientID with sampleID
    args = ["-p", "1", "-r", "rcode", "-sid", "sampleID"]

    with pytest.raises(SystemExit):
        cli = cli_obj.cli_obj(args)
