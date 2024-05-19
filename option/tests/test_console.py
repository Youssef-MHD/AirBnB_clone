#!/usr/bin/python3
"""Module for testing the HBNBCommand Class"""

import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """Test the HBNBCommand Console"""

    def setUp(self):
        """Set up the test environment"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down the test environment"""
        pass

    def capture_output(self, command):
        """Capture the output of a command"""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd(command)
            return output.getvalue()

    def test_help(self):
        """Test the help command"""
        expected_output = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update\n
"""
        self.assertEqual(expected_output.strip(), self.capture_output("help").strip())

    def test_do_quit(self):
        """Test the quit command"""
        self.assertEqual("", self.capture_output("quit"))
        self.assertEqual("", self.capture_output("quit garbage"))

    def test_do_EOF(self):
        """Test the EOF command"""
        self.assertEqual("\n", self.capture_output("EOF"))
        self.assertEqual("\n", self.capture_output("EOF garbage"))

    def test_do_emptyline(self):
        """Test the emptyline command"""
        self.assertEqual("", self.capture_output("\n"))
        self.assertEqual("", self.capture_output("                     \n"))

    def test_do_all(self):
        """Test the all command"""
        # Add appropriate assertion once implementation is done
        pass

    # Add more test cases for other commands: count, show, create, update, destroy


if __name__ == "__main__":
    unittest.main()

