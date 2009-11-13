#!/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import StringIO
from tomtom import Tomtom
import mox

import tomtom
import test_data

class AcceptanceTests(unittest.TestCase):
    """
    Acceptance tests: what is the expected behaviour from the
    user point of view.
    """
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.old_argv = sys.argv

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.argv = self.old_argv

    def test_no_argument(self):
        """ Acceptance: Application called without arguments should print a list of the last 10 notes """
        sys.argv = ["unused_prog_name", ]
        tomtom.main()
        self.assertEquals(test_data.expected_list + "\n", sys.stdout.getvalue())

    def test_only_note_name(self):
        """ Acceptance: Only note name is passed as argument : display the note """
        sys.argv = ["unused_prog_name", "TODO"]
        tomtom.main()
        self.assertEquals(test_data.expected_note_content + "\n", sys.stdout.getvalue())

    def test_note_does_not_exist(self):
        """ Acceptance: Specified note non-existant should display an error message """
        sys.argv = ["unused_prog_name", "unexistant"]
        tomtom.main()
        self.assertEquals("Note named \"unexistant\" not found.\n", sys.stdout.getvalue())

    def test_full_list(self):
        """ Acceptance: -l argument should produce a list of all articles """
        sys.argv = ["unused_prog_name", "-l"]
        tomtom.main()
        self.assertEquals(test_data.expected_list + test_data.list_appendix + "\n", sys.stdout.getvalue())

    def test_search(self):
        """ Acceptance: -s argument should execute a case independant search within all notes """
        sys.argv = ["unused_prog_name", "-s", "john doe"]
        tomtom.main()
        self.assertEquals(test_data.search_results + "\n", sys.stdout.getvalue())

    def test_search_specific_notes(self):
        """ Acceptance: Giving a space separated list of note names should restrict search within those notes """
        sys.argv = ["unused_prog_name", "-s", "python", "dell 750", "python-work", "OpenSource Conference X"]
        tomtom.main()
        self.assertEquals(test_data.specific_search_results + "\n", sys.stdout.getvalue())

class TestListing(unittest.TestCase):
    """
    Tests in relation to code that handles the notes and lists them.
    """
    def setUp(self):
        """setup a mox factory"""
        self.m = mox.Mox()

    def test_list_notes(self):
        """Listing receives a list of notes"""
        tt = Tomtom()
        fake_list = self.m.CreateMock(list)

        self.m.StubOutWithMock(tt, "listing")
        self.m.StubOutWithMock(tt, "get_all_notes")
        tt.get_all_notes().AndReturn(fake_list)
        tt.listing(fake_list)
        
        self.m.ReplayAll()

        tt.list_all_notes()

        self.m.VerifyAll()

if __name__ == "__main__":
    unittest.main()

