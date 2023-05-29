import unittest
from ..commands import *
from ..tools.document_tools import del_last_line, write_after



cgignore_path = os.path.join(main_folder_path, "cgignore")
cgfolder_path = os.path.join(main_folder_path, "cgfolder")


class TestMerge(unittest.TestCase):

    def test_is_ignore(self):
        try:
            self.assertFalse(merge.is_ignore("test_file"))
            with open(cgignore_path, 'a') as cgignore:
                cgignore.write("test_file")
            self.assertTrue(merge.is_ignore("test_file"))

        except : pass

        del_last_line(cgignore_path)

    def test_update_folder_path_list(self):
        try :
            self.assertFalse("test_folder" in folder_path_list)

            with open(cgfolder_path, "a") as cgfolder:
                cgfolder.write("test_folder")

            merge.update_folder_path_list()
            folder_path = os.path.join(main_folder_path, "test_folder")
            self.assertTrue(folder_path in folder_path_list)
        except : pass
        del folder_path_list[-1]
        del_last_line(cgfolder_path)


    def test_script_in_order(self):
        for i in range(20):
            with open(os.path.join(main_folder_path, src_path, f"script_{i}.py"), 'w') as script:
                script.write(f"Test blabla order : {i}")

        for i, file_name in enumerate(merge.script_in_order()):
            try:
                self.assertEqual(file_name, f"script_{i}.py")
            except : pass
            os.remove(os.path.join(src_path, file_name))


    def test_copy_files(self):
        test_file_path = os.path.join(os.path.abspath("."), "test_file")

        with open(test_file_path, 'w') as test_file:
            test_file.write("test")

        test_file_path_copy = test_file_path + "_copy"
        merge.copy_files(test_file_path, test_file_path_copy)

        try :
            with open(test_file_path_copy, "r") as test_file_copy:
                self.assertEqual(test_file_copy.readline(), "test\n")    
        except: pass
        os.remove(test_file_path)
        os.remove(test_file_path_copy)


        






