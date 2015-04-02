import unittest
import tempfile
import sys
import os
import ntpath
import adb

DEST_FOLDER_TARGET = '/data/media/0/Download/'
NON_EXISTING_DIR = '/non-existing-dir/'
dest_folder_host = ''

ADB_COMMAND_PREFIX = 'adb'
ADB_COMMAND_SHELL = 'shell'
ADB_COMMAND_PULL = 'pull'
ADB_COMMAND_PUSH = 'push'
ADB_COMMAND_RM = 'rm -r'
ADB_COMMAND_CHMOD = 'chmod -R 777'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_INSTALL = 'install'
ADB_COMMAND_FORWARD = 'forward'

tmp_file = None
tmp_file_on_target = None

adb_push = None
adb_pull = None

def setUpModule():
    #todo: implement tearDownModule function which will clean generated files
    #from device and host system
    generate_tmp_file()

def generate_tmp_file():
    """Generates temp file and pushes it to target"""
    global tmp_file
    if not tmp_file:
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        print('*** preparing temporary file with name ' + tmp_file.name)
    adb.push(tmp_file.name, DEST_FOLDER_TARGET)

    #gets full path on target for tmp_file
    global tmp_file_on_target
    tmp_file_on_target = (DEST_FOLDER_TARGET + ntpath.basename(tmp_file.name))
    print('*** getting path to tmp_file ' + str(tmp_file.name))

    #gets path to dest_folder_host
    global tmp_file
    global dest_folder_host
    dest_folder_host = os.path.dirname(tmp_file.name)
    print('*** getting path to dest_folder_host ' + dest_folder_host)

class TestPushCommand(unittest.TestCase):
    def test_push_p(self):
        global tmp_file
        result = adb.push(tmp_file.name, DEST_FOLDER_TARGET)
        self.assertEqual(result, True)

    def test_push_n_invalid_1_parameter(self):
        global tmp_file
        result = adb.push(None,DEST_FOLDER_TARGET)
        self.assertEqual(result, False)

    def test_push_n_invalid_2_sparameter(self):
        global tmp_file
        result = adb.push(tmp_file.name,None)
        self.assertEqual(result, False)

    def test_push_n_invalid_source_folder(self):
        global tmp_file
        result = adb.push(NON_EXISTING_DIR, DEST_FOLDER_TARGET)
        self.assertEqual(result, False)

class TestPullCommand(unittest.TestCase):

    def test_pull_p(self):
        global tmp_file_on_target
        global dest_folder_host
        result = adb.pull(tmp_file_on_target, dest_folder_host)
        self.assertEqual(result, True)

    def test_pull_n_invalid_1_parameter(self):
        global dest_folder_host
        result = adb.pull(None, dest_folder_host)
        self.assertEqual(result, False)

    def test_pull_n_invalid_2_parameter(self):
        global tmp_file_on_target
        result = adb.pull(tmp_file_on_target, None)
        self.assertEqual(result, False)

    def test_pull_n_invalid_dest_folder_host(self):
        global tmp_file_on_target
        result = adb.pull(tmp_file_on_target, NON_EXISTING_DIR)
        self.assertEqual(result, False)

class TestExecResultsHandler(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """Prepares full adb commands and their attributes"""
        #assembles "adb push" command
        global tmp_file
        global adb_push
        adb_push = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PUSH, tmp_file.name, \
        DEST_FOLDER_TARGET ]

        #assembles "adb pull" command
        global tmp_file_on_target
        global dest_folder_host
        global adb_pull
        adb_pull = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, tmp_file_on_target, \
        dest_folder_host ]

    def test_exec_result_handler_p_adb_push(self):
        global adb_push
        result = adb.exec_result_handler(adb_push)
        self.assertEqual(result, True)

    def test_exec_result_handler_p_adb_pull(self):
        global adb_pull
        result = adb.exec_result_handler(adb_pull)
        self.assertEqual(result, True)

    def test_exec_result_handler_n_uncomplete_argument(self):
        #4th argument is missing in adb_command
        adb_command = [ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, tmp_file_on_target]
        result = adb.exec_result_handler(adb_command)
        self.assertEqual(result, False)

    def test_exec_result_handler_n_invalid_command_syntax(self):
        #missing ADB_COMMAND_PREFIX
        adb_command = [ADB_COMMAND_PUSH, tmp_file.name, DEST_FOLDER_TARGET ]
        result = adb.exec_result_handler(adb_command)
        self.assertEqual(result, False)

    def test_exec_result_handler_n_missing_argument(self):
        #no argument at all
        adb_command = None
        result = adb.exec_result_handler(adb_command)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()