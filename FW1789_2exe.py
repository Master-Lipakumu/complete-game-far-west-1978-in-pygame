import os
import sys
import fnmatch
import glob
import shutil
import operator
from cx_Freeze import setup, Executable
import cx_Freeze
import pygame
from modulefinder import Module

try:
    from cx_Freeze import setup, Executable
    import pygame
    import sys
    import os
    from modulefinder import Module
except ImportError as e:
    raise SystemExit("Unable to load module. %s" % e)
 
# Hack which fixes the pygame mixer and pygame font
origIsSystemDLL = getattr(cx_Freeze.build_exe, 'isSystemDLL', None)

def isSystemDLL(pathname):
    # Checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
        return 0
    if origIsSystemDLL:
        return origIsSystemDLL(pathname)
    return 0
cx_Freeze.build_exe.isSystemDLL = isSystemDLL # Override the default function with this one

class pygame2exe(Executable):
    def copy_extensions(self, extensions):
        # Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
 
        # Add font to list of extensions to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        Executable.copy_extensions(self, extensions)

# Specify the options for cx_Freeze
class BuildExe:
    def __init__(self):
        self.script = "FW1789_V001.py"
        self.project_name = "FW1789_V001"
        self.project_url = "about:none"
        self.project_version = "0.0.1"
        self.author_name = "Master Lipakumu"
        self.author_email = "kristalservice2018@gmail.com"
        self.copyright = "Copyright (c) 2024 Mona Technology. All rights reserved."
        self.project_description = "Far West 1789, a shooter multi player network game."
        self.icon_file = os.path.join("Images", "favicon.ico")
        self.extra_datas = ["background", "fonts_western", "Images", "Sounds"]
        self.extra_modules = ['pygame']
        self.zipfile_name = None
        self.dist_dir ='dist'

    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)

    def find_data_files(self, srcdir, *wildcards, **kw):
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = os.path.join(dirname, wc)
                for f in files:
                    filename = os.path.join(dirname, f)
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append((dirname, names))

        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            for root, dirs, files in os.walk(srcdir):
                walk_helper((file_list, wildcards), root, files)
        else:
            walk_helper((file_list, wildcards), srcdir, os.listdir(srcdir))
        return file_list

    def run(self):
        if os.path.isdir(self.dist_dir):
            shutil.rmtree(self.dist_dir)

        # Spécifiez le chemin de l'icône à utiliser pour l'exécutable
        icon_path = os.path.join("Images", "favicon.ico")

        extra_datas = ["freesansbold.ttf", "FW1789.cfg", "hiscore.json"]
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))

        try:
            setup(
                version=self.project_version,
                description=self.project_description,
                name=self.project_name,
                url=self.project_url,
                author=self.author_name,
                author_email=self.author_email,
                executables=[Executable(self.script, base='Win32GUI', icon=icon_path)],
                options={
                    'build_exe': {
                        'optimize': 2,
                        'packages': self.extra_modules,
                        'include_files': self.extra_datas
                    }
                },
                zipfile=self.zipfile_name,
                data_files=extra_datas,
                dist_dir=self.dist_dir
            )
            print("La création de l'exécutable a été effectuée avec succès!")
        except Exception as e:
            print(f"Erreur lors de la création de l'exécutable : {str(e)}")

        # Supprimer seulement si le dossier existe
        if os.path.isdir('build'):
            print("Le dossier 'build' n'a pas été supprimé car il existe déjà.")
        else:
            print("Le dossier 'build' n'existe pas.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('build')
    BuildExe().run()


"""import os
import sys
import fnmatch
import glob
import shutil
import operator
from cx_Freeze import setup, Executable
import cx_Freeze
import pygame
from modulefinder import Module

try:
    from cx_Freeze import setup, Executable
    import pygame
    import sys
    import os
    from modulefinder import Module
except ImportError as e:
    raise SystemExit("Unable to load module. %s" % e)
 
# Hack which fixes the pygame mixer and pygame font
origIsSystemDLL = getattr(cx_Freeze.build_exe, 'isSystemDLL', None)

def isSystemDLL(pathname):
    # Checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
        return 0
    if origIsSystemDLL:
        return origIsSystemDLL(pathname)
    return 0
cx_Freeze.build_exe.isSystemDLL = isSystemDLL # Override the default function with this one

class pygame2exe(Executable):
    def copy_extensions(self, extensions):
        # Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
 
        # Add font to list of extensions to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        Executable.copy_extensions(self, extensions)

# Specify the options for cx_Freeze
class BuildExe:
    def __init__(self):
        self.script = "FW1789_V001.py"
        self.project_name = "FW1789_V001"
        self.project_url = "about:none"
        self.project_version = "0.0.1"
        self.license = "none"
        self.author_name = "Master Lipakumu"
        self.author_email = "kristalservice2018@gmail.com"
        self.copyright = "Copyright (c) 2024 Mona Technology. All rights reserved."
        self.project_description = "Far West 1789, a shooter multi player network game."
        self.icon_file = os.path.join("Images", "favicon.ico")
        self.extra_datas = ["background", "fonts_western", "Images", "Sounds"]
        self.extra_modules = ['pygame']
        self.exclude_modules = []
        self.exclude_dll = ['']
        self.extra_scripts = []
        self.zipfile_name = None
        self.dist_dir ='dist'

    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)

    def find_data_files(self, srcdir, *wildcards, **kw):
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = os.path.join(dirname, wc)
                for f in files:
                    filename = os.path.join(dirname, f)
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append((dirname, names))

        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            for root, dirs, files in os.walk(srcdir):
                walk_helper((file_list, wildcards), root, files)
        else:
            walk_helper((file_list, wildcards), srcdir, os.listdir(srcdir))
        return file_list

    def run(self):
        if os.path.isdir(self.dist_dir):
            shutil.rmtree(self.dist_dir)

        if self.icon_file is None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(path, 'pygame.ico')

        extra_datas = ["freesansbold.ttf","FW1789.cfg", "hiscore.json"]
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))

        setup(
            version=self.project_version,
            description=self.project_description,
            name=self.project_name,
            url=self.project_url,
            author=self.author_name,
            author_email=self.author_email,
            license=self.license,
            executable=[Executable(self.script)],
            windows=[{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options={
                'build_exe': {
                    'optimize': 2,
                    'bundle_files': 1,
                    'compressed': True,
                    'excludes': self.exclude_modules,
                    'packages': self.extra_modules,
                    'dll_excludes': self.exclude_dll,
                    'includes': self.extra_scripts,
                    'include_files': self.extra_datas
                }
            },
            zipfile=self.zipfile_name,
            data_files=extra_datas,
            dist_dir=self.dist_dir
        )

        if os.path.isdir('build'):
            shutil.rmtree('build')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('build')
    BuildExe().run()"""