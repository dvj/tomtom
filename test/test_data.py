# -*- coding: utf-8 -*-
"""test data for tomtom"""
import os
import dbus
from tomboy_utils import TomboyNote

# To obtain modification dates for notes and corresponding real dates:
# With tomboy being a dbus interface to the Tomboy application:
# >>> [(datetime.fromtimestamp(tomboy.GetNoteChangeDate(url)),tomboy.GetNoteChangeDate(url)) for url in l]
expected_list = \
"""2009-11-09 | addressbook  (pim)
2009-11-02 | TODO-list  (reminders, pim)
2009-11-02 | Bash  (reminders)
2009-10-22 | dell 750  (projects)
2009-10-22 | python-work
2009-10-18 | TDD
2009-10-18 | OpenSource Conference X
2009-10-03 | business contacts  (pim)
2009-10-01 | japanese  (reminders)
2009-09-19 | Webpidgin  (projects)"""

list_appendix = \
"""2009-09-19 | conquer the world  (projects)
2009-09-19 | recipes
2009-09-19 | R&D  (reminders)"""

search_results = \
"""addressbook : 5 : John Doe (cell) - 555-5512
business contacts : 7 : John Doe Sr. (office) - 555-5534"""

specific_search_results = \
"""dell 750 : 9 : python-libvirt - libvirt Python bindings
python-work : 2 : to use a python buildbot for automatic bundling
OpenSource Conference X : 15 : oops, and don't forget to talk about python"""

search_no_argument_error = "Error: You must specify a pattern to perform a search"

note_contents_from_dbus = {
    "addressbook": """addressbook

Momma Chicken - 444-1919
Père Noël - 464-6464
Nakamura Takeshi - 01-20-39-48-57
G.I. Jane (pager) - 555-1234
John Doe (cell) - 555-5512""",
    "TODO-list": """TODO-list

Build unit tests for tomtom
Chew up some gum
Play pool with the queen of england""",
    "Bash": """Bash

something""",
    "dell 750": """dell 750

$ apt-cache search lxc
libclxclient-dev - Development file for libclxclient
libclxclient3 - X Window System C++ access library
lxc - Linux containers userspace tools
libvirt-bin - the programs for the libvirt library
libvirt-dev - development files for the libvirt library
libvirt-doc - documentation for the libvirt library
libvirt0-dbg - library for interfacing with different virtualization systems
python-libvirt - libvirt Python bindings
libopencascade-ocaf-6.3.0 - OpenCASCADE CAE platform shared library""",
    "python-work": """python-work

I need to ask Shintarou to prepare things
to use a python buildbot for automatic bundling
for the project.""",
    "TDD": """TDD

something""",
    "OpenSource Conference X": """OpenSource Conference X

Lorem ipsum vix ei inermis epicurei mnesarchum, quod graeci facete vis cu, sumo libris pro no. Quod vocibus rationibus ex mea, nam dicta tantas cetero et. Nulla aperiam nostrud ad est, id qui exerci feugiat rationibus, in sed affert facete eripuit. Ei nam oratio aperiri epicurei. His te kasd adipisci dissentiunt, laudem putant fabellas nam in. Homero causae scaevola sit cu.

Mea ea puto malis mediocrem, ad dolorem expetenda iracundia vis. Cibo graece tamquam an mel, ne qui omnes aliquid tibique, has at tale sale vidit. Solum porro at per, usu denique officiis perfecto te. Has puto rebum impedit ex, duo modus diceret fastidii cu.

Nibh impedit posidonium pro ea, sint quidam aperiam per ea, est laudem accommodare eu. Eos brute deserunt eu, no sit novum ignota detraxit, duo facer doctus ei. Qui in impedit ocurreret quaerendum, mei ad noluisse legendos torquatos, facete discere neglegentur ius ex. Nam ei legere vulputate constituto, ut pri virtute ancillae iracundia, vis et sanctus perfecto imperdiet. Te erant aeque dignissim sed, nibh ubique instructior ex vel. Ne docendi democritum scripserit has, vis ut elitr equidem, agam invidunt prodesset id vis.

At vix facete scaevola. Ad erat explicari persequeris mei, et mei nullam fierent vulputate. Et oratio rationibus complectitur duo, an sit nominati consequuntur. Ea cum nulla scaevola dignissim, aeterno utroque interpretaris in sit. Altera vivendum lobortis quo an, vitae dolore iisque per et.

Eum novum mucius propriae in, brute repudiare at quo. Mel elitr vidisse epicuri te, vim sonet accusam ancillae ut, his no movet maiorum instructior. Hinc eligendi corrumpit usu et, nam ne dolor aperiri, vix novum virtute ut. Nam et modus nihil exerci, te minim omittantur theophrastus eum.

Te paulo vivendum accusamus cum, autem feugait salutatus an sit. Ex pro dicam virtute periculis, at sit odio solum interpretaris. Rebum nostrud legendos ad ius, ad feugait consetetur dissentias pri. Te iudico timeam percipit eum, has ex postea democritum theophrastus, ad ipsum ancillae pri. Te vis harum simul liberavisse, nihil fuisset dissentiunt eos no, in illud legimus percipit sed. Nam agam debitis placerat id, adversarium liberavisse his an.

Mea elit munere nonummy at, ei sed sint nonummy consetetur, iudicabit efficiendi no sit. Sea ne appareat tractatos voluptatum, posse dicat hendrerit cum at, duo fabellas rationibus reprehendunt an. Sit an homero laudem labores, et oblique blandit aliquyam vel. No per officiis quaestio expetendis, vero omnium offendit mel in, sit no consulatu adolescens adipiscing. Quo id saepe elaboraret delicatissimi, eripuit ornatus utroque per ut, putant quodsi definitiones et nam.

oops, and don't forget to talk about python""",
    "business contacts": """business contacts

Elvis Presley - 111-1111
Kurosaki Ichigo - 444-5555
God Himself (cell) - 999-9999
Mother Theresa - 000-0000
Pidgeon in a Box - 918-3874
Donald E. Knuth - 101-2020
John Doe Sr. (office) - 555-5534
Mister Anderson (secretary) - 123-4567
Python McClean - 777-7777""",
    "japanese": """japanese

something""",
    "Webpidgin": """Webpidgin

something""",
    "conquer the world": """conquer the world

something""",
    "recipes": """recipes

something""",
    "R&D": """R&D

something""",
}

display_no_note_name_error = "Error: You need to specify a note name to display it"

full_list_of_notes = [
    TomboyNote(
        uri="note://tomboy/b332eb31-8139-4351-9f5d-738bf64ce172",
        title="addressbook",
        date=dbus.Int64(1257805144L),
        tags=["pim", ]
    ),
    TomboyNote(
        uri="note://tomboy/30ae533a-2789-4789-a409-16a6f65edf54",
        title="TODO-list",
        date=dbus.Int64(1257140572L),
        tags=["reminders", "pim"]
    ),
    TomboyNote(
        uri="note://tomboy/4652f914-85dd-487d-b614-188242f52241",
        title="Bash",
        date=dbus.Int64(1257138697L),
        tags=["reminders", ]
    ),
    TomboyNote(
        uri="note://tomboy/5815160c-7143-4c56-9c5f-007acca375ad",
        title="dell 750",
        date=dbus.Int64(1256265529L),
        tags=["projects", ]
    ),
    TomboyNote(
        uri="note://tomboy/89277e3b-bdb7-4cfe-a42c-7c8b207370fd",
        title="python-work",
        date=dbus.Int64(1256257835L),
        tags=[]
    ),
    TomboyNote(
        uri="note://tomboy/bece0d43-19ba-41cf-92b5-7b30a5411a0c",
        title="TDD",
        date=dbus.Int64(1255898778L),
        tags=[]
    ),
    TomboyNote(
        uri="note://tomboy/1a1994da-1b98-41d2-8eab-26e8581fc391",
        title="OpenSource Conference X",
        date=dbus.Int64(1255890996L),
        tags=[]
    ),
    TomboyNote(
        uri="note://tomboy/21612e71-e2ec-4afb-82bb-7e663e58e88c",
        title="business contacts",
        date=dbus.Int64(1254553804L),
        tags=["pim", ]
    ),
    TomboyNote(
        uri="note://tomboy/8dd14cf8-4766-4122-8178-192cdc0e99dc",
        title="japanese",
        date=dbus.Int64(1254384931L),
        tags=["reminders", ]
    ),
    TomboyNote(
        uri="note://tomboy/c0263232-c3b8-45a8-bfdc-7cb8ee4b2a5d",
        title="Webpidgin",
        date=dbus.Int64(1253378270L),
        tags=["projects", ]
    ),
    TomboyNote(
        uri="note://tomboy/ea6f4c7f-1b82-4835-9aa2-2df002d788f4",
        title="conquer the world",
        date=dbus.Int64(1253342190L),
        tags=["projects", ]
    ),
    TomboyNote(
        uri="note://tomboy/461fb1a2-1e02-4447-8891-c3c6fcbb26eb",
        title="recipes",
        date=dbus.Int64(1253340981L),
        tags=[]
    ),
    TomboyNote(
        uri="note://tomboy/5df0fd74-cbdd-4cf3-bb08-7a7f09997afd",
        title="R&D",
        date=dbus.Int64(1253340600L),
        tags=["reminders", ]
    ),
]

help_usage = """Usage: app_name (-h|--help) [action]
       app_name <action> [-h|--help] [options]"""

help_more_details = """For more details, use option -h"""

help_action_list = os.linesep.join([
    help_usage,
    "",
    """Options depend on what action you are taking. To obtain details on options for a particular action, combine -h or --help and the action name.

Here is a list of all the available actions:
  list
  display
  search""",
])

help_details_list = """Usage: app_name list [-h|-a]

Options:
  -h, --help  show this help message and exit
  -a, --all   List all the notes"""

help_details_display = """Usage: app_name display [-h] [note_name ...]

Options:
  -h, --help  show this help message and exit"""

help_details_search = """Usage: app_name search [-h] <search_pattern> [note_name ...]

Options:
  -h, --help  show this help message and exit"""

