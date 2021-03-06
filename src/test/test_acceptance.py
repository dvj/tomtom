# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2009, Gabriel Filion
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,
#     * this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################
"""Acceptance tests for Tomtom.

This defines the use cases and expected results.

"""
import sys
import os
import mox
import dbus
import pkg_resources

import test_data
from test_utils import *

from tomtom import cli
from tomtom import plugins

class AcceptanceTests(BasicMocking, CLIMocking):
    """Acceptance tests.

    Define what the expected behaviour is from the user's point of view.

    Those tests are meant to verify correct functionality of the whole
    application, so they mock out external library dependencies only.

    """
    def setUp(self):
        """Unit test preparation.

        Mock out the default dbus interaction: that of creating an object that
        establishes contact with Tomboy via dbus.

        """
        super(AcceptanceTests, self).setUp()

        # By default, mock out Tomboy interaction.
        self.mock_out_dbus("Tomboy")

    def tearDown(self):
        """Unit test breakdown.

        Remove mocks and replace what was disturbed so that it doesn't affect
        other tests.

        """
        super(AcceptanceTests, self).tearDown()

        dbus.SessionBus = self.old_SessionBus
        dbus.Interface = self.old_Interface

    def mock_out_dbus(self, application):
        """Mock out dbus interaction with the specified application."""
        self.old_SessionBus = dbus.SessionBus
        self.old_Interface = dbus.Interface
        dbus.SessionBus = self.m.CreateMockAnything()
        dbus.Interface = self.m.CreateMockAnything()
        session_bus = self.m.CreateMockAnything()
        dbus_object = self.m.CreateMockAnything()
        self.dbus_interface = self.m.CreateMockAnything()

        dbus.SessionBus()\
            .AndReturn(session_bus)
        session_bus.get_object(
            "org.gnome.%s" % application,
            "/org/gnome/%s/RemoteControl" % application
        ).AndReturn(dbus_object)
        dbus.Interface(
            dbus_object,
            "org.gnome.%s.RemoteControl" % application
        ).AndReturn(self.dbus_interface)

    def mock_out_listing(self, notes):
        """Create mocks for note listing via dbus.

        Arguments:
            notes -- a list of TomboyNote objects

        """
        self.dbus_interface.ListAllNotes()\
            .AndReturn([n.uri for n in notes])
        for note in notes:
            self.dbus_interface.GetNoteTitle(note.uri)\
                .AndReturn(note.title)
            self.dbus_interface.GetNoteChangeDate(note.uri)\
                .AndReturn(note.date)
            self.dbus_interface.GetTagsForNote(note.uri)\
                .AndReturn(note.tags)

    def mock_out_get_notes_by_names(self, notes):
        """Create mocks for searching for notes by their names.

        Arguments:
            notes -- a list of TomboyNote objects

        """
        for note in notes:
            self.dbus_interface.FindNote(note.title)\
                .AndReturn(note.uri)

        for note in notes:
            self.dbus_interface.GetNoteChangeDate(note.uri)\
                .AndReturn(note.date)
            self.dbus_interface.GetTagsForNote(note.uri)\
                .AndReturn(note.tags)

    def test_no_argument(self):
        """Acceptance: tomtom called without arguments must print usage."""
        # No dbus interaction for this test
        self.remove_mocks()

        sys.argv = ["app_name", ]
        old_docstring = cli.__doc__
        cli.__doc__ = os.linesep.join([
            "command -h",
            "command action",
            "",
            "unused",
            "but fake",
            "help text"
        ])

        self.m.ReplayAll()

        tomtom_cli = cli.CommandLine()
        self.assertRaises(
            SystemExit,
            tomtom_cli.main
        )

        self.m.VerifyAll()

        # Test that usage comes from the script's docstring.
        self.assertEqual(
            (os.linesep * 2).join([
                os.linesep.join( cli.__doc__.splitlines()[:3]),
                test_data.help_more_details
            ]) + os.linesep,
            sys.stderr.getvalue()
        )

        cli.__doc__ = old_docstring

    def test_unknown_action(self):
        """Acceptance: Giving an unknown action name must print an error."""
        # No dbus interaction for this test
        self.remove_mocks()

        self.m.ReplayAll()

        sys.argv = ["app_name", "unexistant_action"]
        tomtom_cli = cli.CommandLine()
        self.assertRaises( SystemExit, tomtom_cli.main )

        self.m.VerifyAll()

        self.assertEqual(
            test_data.unknown_action + os.linesep,
            sys.stderr.getvalue()
        )

    def test_action_list(self):
        """Acceptance: Action "list -n" prints a list of the last n notes."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes[:10])

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "list", "-n", "10"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            test_data.expected_list + os.linesep,
            sys.stdout.getvalue()
        )

    def test_full_list(self):
        """Acceptance: Action "list" alone produces a list of all notes."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes)

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "list"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            os.linesep.join([
                test_data.expected_list,
                test_data.list_appendix
            ]) + os.linesep,
            sys.stdout.getvalue()
        )

    def test_notes_displaying(self):
        """Acceptance: Action "display" prints the content given note names."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        todo = list_of_notes[1]
        python_work = list_of_notes[4]
        separator = os.linesep + "==========================" + os.linesep
        note_lines = test_data.note_contents_from_dbus["TODO-list"]\
                        .splitlines()

        note_lines[0] = \
            "%s  (system:notebook:reminders, system:notebook:pim)" % (
                note_lines[0],
            )

        expected_result_list = [
            os.linesep.join(note_lines),
            test_data.note_contents_from_dbus["python-work"]
        ]

        self.mock_out_get_notes_by_names([todo, python_work])

        self.dbus_interface.GetNoteContents(todo.uri)\
            .AndReturn(test_data.note_contents_from_dbus["TODO-list"])
        self.dbus_interface.GetNoteContents(python_work.uri)\
            .AndReturn(test_data.note_contents_from_dbus["python-work"])

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "display", "TODO-list", "python-work"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            separator.join(expected_result_list) + os.linesep,
            sys.stdout.getvalue()
        )

    def test_note_does_not_exist(self):
        """Acceptance: Specified note non-existant: display an error."""
        self.dbus_interface.FindNote("unexistant")\
            .AndReturn(dbus.String(""))

        self.m.ReplayAll()

        sys.argv = ["app_name", "display", "unexistant"]
        tomtom_cli = cli.CommandLine()
        self.assertRaises(SystemExit, tomtom_cli.main)

        self.assertEquals(
            test_data.unexistant_note_error + os.linesep,
            sys.stderr.getvalue()
        )

        self.m.VerifyAll()

    def test_display_zero_argument(self):
        """Acceptance: Action "display" with no argument prints an error."""
        sys.argv = ["app_name", "display"]

        self.m.ReplayAll()

        tomtom_cli = cli.CommandLine()
        self.assertRaises(
            SystemExit,
            tomtom_cli.main
        )

        self.m.VerifyAll()

        self.assertEquals(
            test_data.display_no_note_name_error + os.linesep,
            sys.stderr.getvalue()
        )

    def test_search(self):
        """Acceptance: Action "search" searches in all notes, case-indep."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes)

        # Forget about the last note (a template)
        for note in list_of_notes[:-1]:
            self.dbus_interface.GetNoteContents(note.uri)\
                .AndReturn(test_data.note_contents_from_dbus[note.title])

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "search", "john doe"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            test_data.search_results + os.linesep,
            sys.stdout.getvalue()
        )

    def test_search_specific_notes(self):
        """Acceptance: Action "search" restricts the search to given notes."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        requested_notes = [
            list_of_notes[3],
            list_of_notes[4],
            list_of_notes[6],
        ]

        self.mock_out_get_notes_by_names(requested_notes)

        for note in requested_notes:
            self.dbus_interface.GetNoteContents(note.uri)\
                .AndReturn(test_data.note_contents_from_dbus[note.title])

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "search", "python"] + \
                [n.title for n in requested_notes]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            test_data.specific_search_results + os.linesep,
            sys.stdout.getvalue()
        )

    def test_search_zero_arguments(self):
        """Acceptance: Action "search" with no argument prints an error."""
        sys.argv = ["unused_prog_name", "search"]

        self.m.ReplayAll()

        tomtom_cli = cli.CommandLine()
        self.assertRaises(
            SystemExit,
            tomtom_cli.main
        )

        self.m.VerifyAll()

        self.assertEquals(
            test_data.search_no_argument_error + os.linesep,
            sys.stderr.getvalue()
        )

    def verify_main_help(self, argument):
        """Test that we actually get the main help."""
        # Remove stubs and reset mocks for dbus that the setUp method
        # constructed as there will be no dbus interaction.
        self.remove_mocks()

        self.m.StubOutWithMock(pkg_resources, "iter_entry_points")

        old_docstring = cli.__doc__
        cli.__doc__ = os.linesep.join([
            "some",
            "non-",
            "useful",
            "but fake",
            "help text "
        ])

        fake_list = [
            "  action1 : this action does something",
            "  action2 : this one too",
            "  action3 : No description available.",
        ]

        fake_plugin_list = [
            self.m.CreateMockAnything(),
            self.m.CreateMockAnything(),
            self.m.CreateMockAnything(),
        ]
        fake_plugin_list[0].name = "action1"
        fake_plugin_list[1].name = "action2"
        fake_plugin_list[2].name = "action3"

        fake_classes = [
            self.m.CreateMock(plugins.ActionPlugin),
            self.m.CreateMock(plugins.ActionPlugin),
            self.m.CreateMock(plugins.ActionPlugin),
        ]
        fake_classes[0].short_description = "this action does something"
        fake_classes[1].short_description = "this one too"
        for fake_class in fake_classes:
            fake_class.__bases__ = ( plugins.ActionPlugin, )

        pkg_resources.iter_entry_points(group="tomtom.actions")\
            .AndReturn( (x for x in fake_plugin_list) )

        for index, entry_point in enumerate(fake_plugin_list):
            fake_class = fake_classes[index]
            entry_point.load()\
                .AndReturn(fake_class)

        self.m.ReplayAll()

        sys.argv = ["app_name", argument]
        tomtom_cli = cli.CommandLine()
        self.assertRaises(
            SystemExit,
            tomtom_cli.main
        )

        self.m.VerifyAll()

        # The help should be displayed using tomtom's docstring.
        self.assertEquals(
            cli.__doc__[:-1] + os.linesep.join(fake_list) + os.linesep,
            sys.stdout.getvalue()
        )

        cli.__doc__ = old_docstring

    def test_help_on_base_level(self):
        """Acceptance: Using "-h" or "--help" alone prints basic help."""
        self.verify_main_help("-h")

    def test_help_action(self):
        """Acceptance: "help" as an action name."""
        self.verify_main_help("help")

    def test_filter_notes_with_templates(self):
        """Acceptance: Using "--with-templates" lists notes and templates."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes)

        self.m.ReplayAll()

        sys.argv = [
            "app_name", "list",
            "--with-templates"
        ]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEqual(
            test_data.expected_list + os.linesep +
                test_data.list_appendix + os.linesep +
                test_data.normally_hidden_template + os.linesep,
            sys.stdout.getvalue()
        )

    def test_filter_notes_by_tags(self):
        """Acceptance: Using "-t" limits the notes by tags."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes)

        self.m.ReplayAll()

        sys.argv = [
            "app_name", "list",
            "-t", "system:notebook:pim",
            "-t", "projects"
        ]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEqual(
            test_data.tag_limited_list + os.linesep,
            sys.stdout.getvalue()
        )

    def test_filter_notes_by_books(self):
        """Acceptance: Using "-b" limits the notes by notebooks."""
        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes)

        self.m.ReplayAll()

        sys.argv = ["app_name", "list", "-b", "pim", "-b", "reminders"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEqual(
            test_data.book_limited_list + os.linesep,
            sys.stdout.getvalue()
        )

    def verify_help_text(self, args, text):
        """Mock out help messages.

        Mimic things to expect the application to exit while printing a
        specified help text.

        Arguments:
            args -- a list of meuh
            text -- the text to verify against

        """
        # No dbus interaction should occur if we get a help text.
        self.remove_mocks()

        sys.argv = args

        # Mock out sys.exit : optparse calls this when help is displayed
        self.m.StubOutWithMock(sys, "exit")
        sys.exit(0).AndRaise(SystemExit)

        self.m.ReplayAll()

        tomtom_cli = cli.CommandLine()
        self.assertRaises(SystemExit, tomtom_cli.main)
        self.assertEquals(
            text + os.linesep,
            sys.stdout.getvalue()
        )

        self.m.VerifyAll()

    def test_help_before_action_name(self):
        """Acceptance: Using "-h" before an action displays detailed help."""
        self.verify_help_text(
            [
                "app_name",
                "-h",
                "list"
            ],
            test_data.help_details_list
        )

    def test_help_pseudo_action_before_action_name(self):
        """Acceptance: Using "-h" before an action displays detailed help."""
        self.verify_help_text(
            [
                "app_name",
                "help",
                "version"
            ],
            test_data.help_details_version
        )

    def test_help_display_specific(self):
        """Acceptance: Detailed help using "-h" after "display" action."""
        self.verify_help_text(
            [
                "app_name",
                "display",
                "--help"
            ],
            test_data.help_details_display
        )

    def test_help_list_specific(self):
        """Acceptance: Detailed help using "-h" after "list" action."""
        self.verify_help_text(
            [
                "app_name",
                "list",
                "--help"
            ],
            test_data.help_details_list
        )

    def test_help_search_specific(self):
        """Acceptance: Detailed help using "-h" after "search" action."""
        self.verify_help_text(
            [
                "app_name",
                "search",
                "--help"
            ],
            test_data.help_details_search
        )

    def test_tomboy_version(self):
        """Acceptance: Get Tomboy's version."""
        self.dbus_interface.Version()\
            .AndReturn(u'1.0.1')

        self.m.ReplayAll()

        # Call function and make assertions here
        sys.argv = ["app_name", "version"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEqual(
            test_data.tomboy_version_output % "Tomboy" + os.linesep,
            sys.stdout.getvalue()
        )

    def test_help_version_specific(self):
        """Acceptance: Detailed help using "-h" after "version" action."""
        self.verify_help_text(
            [
                "app_name",
                "version",
                "--help"
            ],
            test_data.help_details_version
        )

    def test_list_using_gnote(self):
        """Acceptance: Specifying --gnote connects to Gnote."""
        # Reset stubs and mocks. We need to mock out dbus differently.
        self.remove_mocks()

        self.mock_out_dbus("Gnote")

        list_of_notes = test_data.full_list_of_notes(self.m)

        self.mock_out_listing(list_of_notes[:10])

        self.m.ReplayAll()

        sys.argv = ["unused_prog_name", "list", "-n", "10", "--gnote"]
        tomtom_cli = cli.CommandLine()
        tomtom_cli.main()

        self.m.VerifyAll()

        self.assertEquals(
            test_data.expected_list + os.linesep,
            sys.stdout.getvalue()
        )
