from __future__ import print_function
import DirectoryModule as dm
import FileModule as fm
import os


class Tree_Structure:
    def __init__(self, root_name, tree_structure, path):
        self.__root_name = root_name
        self.__tree_structure = tree_structure
        self.__path = path

    @property
    def tree_structure(self):
        return self.__tree_structure

    @tree_structure.setter
    def tree_structure(self, tree):
        self.__tree_structure = tree

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @staticmethod
    def generateTreeStructure(path):

        tree_map = {}

        for root, dir, file in os.walk(path):
            tree_files_in_path = []

            for i in dir:
                path_to_dir = root + '\\' + i
                directory_temp = dm.Directory(i, path_to_dir, os.path.getmtime(path_to_dir))
                tree_files_in_path.append(directory_temp)

            for j in file:
                path_to_file = root + '\\' + j
                file_temp = fm.File(j, path_to_file, os.path.getmtime(path_to_file))
                tree_files_in_path.append(file_temp)

            tree_map[root] = tree_files_in_path

        return tree_map

    def printTree(self):
        for key, values in self.__tree_structure.items():
            print(key, end=' -> ')

            for list_element in values:
                print(list_element.name, end=', ')

            print()

    @staticmethod
    def compareTreeStructures(old_tree_map, new_tree_map):

        # here are stored all files that changed since the last tree scan
        files_to_update = []
        # here are stored all dirs from the old tree, to later see if there are any new dirs
        # all_old_keys = []

        for key, list in old_tree_map.items():

            # list of elements in this dir from new tree
            list_new = new_tree_map.get(key, None)

            # break if dir not found in the new tree (was deleted or renamed)
            if list_new is None:
                continue

            # store here all of the dirs that were in the old tree
            # all_old_keys.append(key)

            for file in list:

                # see if the file from old tree is also in new tree, if it
                # hasnt been deleted
                file_new = next((x for x in list_new if x.name == file.name), None)
                # else, skip this file
                if not file_new:
                    continue

                # skip if the element is a directory, not a file
                if type(file_new) is dm.Directory:
                    continue

                # see, if the file has been modified, if so, add it to files_to_update
                if file_new.last_mod_date != file.last_mod_date:
                    files_to_update.append(file_new) # TODO: error here, adds files that have not been changed

            # get all files in the directory from new tree
            only_files_in_directory = [file for file in list_new if type(file) is fm.File]

            # compare old and new lists of files in a dir and get all new files (if any)
            new_files = [file for file in only_files_in_directory if file not in list]

            # if any new files have been found, add them to files_to_update
            if len(new_files) > 0:
                files_to_update += new_files

        # now, look for new directories (if any)
        all_new_dirs_paths = [key for key in new_tree_map.keys() if
                              key not in old_tree_map.keys()]

        # do if found some new dirs
        if len(all_new_dirs_paths) > 0:

            # run through all directories and create Directory objects
            for dir in all_new_dirs_paths:
                # create Directory.name
                dir_name = (dir.split('\\'))[-1]

                # create new Directory(name, path, last_mod_date)
                new_dir = dm.Directory(dir_name, '\\'.join(dir.split('\\')[:-1]).encode('utf-8'), os.path.getmtime(dir))

                # add to files_to_update
                files_to_update.append(new_dir)

        # return the list of all new or modified objects from new tree
        return files_to_update
