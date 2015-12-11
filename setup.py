#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by: python.exe -m py2exe mygame.py -O -W setup.py


import platform
import os
from distutils.core import setup
import py2exe

class Target(object):
    '''Target is the baseclass for all executables that are created.
    It defines properties that are shared by all of them.
    '''
    def __init__(self, **kw):
        self.__dict__.update(kw)

        # the VersionInfo resource, uncomment and fill in those items
        # that make sense:

        # The 'version' attribute MUST be defined, otherwise no versioninfo will be built:
        # self.version = "1.0"

        # self.company_name = "Company Name"
        # self.copyright = "Copyright Company Name © 2013"
        # self.legal_copyright = "Copyright Company Name © 2013"
        # self.legal_trademark = ""
        # self.product_version = "1.0.0.0"
        # self.product_name = "Product Name"

        # self.private_build = "foo"
        # self.special_build = "bar"

    def copy(self):
        return Target(**self.__dict__)

    def __setitem__(self, name, value):
        self.__dict__[name] = value

RT_BITMAP = 2
RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6

manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="%(level)s"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''



mygame = Target(
    script="D:/project/mygame.py",
    dest_base = "TheGreatRobber",
    icon_resources = [(1,r"D:/project/robber.ico")],
    other_resources = [(RT_MANIFEST, 1, (manifest_template % dict(prog="mygame", level="asInvoker")).encode("utf-8"))]
    )

py2exe_options = dict(
    packages = [],
    optimize=1,
    compressed=True, # uncompressed may or may not have a faster startup
    bundle_files=2,
    dist_dir='D:/dist/',
    )

Battle_folder = 'D:/project/Battle_State/'
Data_folder = 'D:/project/Data/'
Gameover_folder = 'D:/project/Game_Over/'
Mainmap_folder = 'D:/project/Main_Map/'
Npc_folder = 'D:/project/Npc/'
Sound_folder = 'D:/project/Sound/'
Title_folder = 'D:/project/Title/'
Font_folder = 'D:/project/Font/'

if platform.architecture()[0] == '32bit':
    sdl_folder="D:/project/SDL2/x86/"
else:
    sdl_folder = "D:/project/SDL2/x64/"


sdl_dlls = [sdl_folder + file_name for file_name in os.listdir(sdl_folder)]
battle_dlls = [Battle_folder + file_name for file_name in os.listdir(Battle_folder)]
data_dlls = [Data_folder + file_name for file_name in os.listdir(Data_folder)]
gameover_dlls = [Gameover_folder + file_name for file_name in os.listdir(Gameover_folder)]
mainmap_dlls = [Mainmap_folder + file_name for file_name in os.listdir(Mainmap_folder)]
npc_dlls = [Npc_folder + file_name for file_name in os.listdir(Npc_folder)]
sound_dlls = [Sound_folder + file_name for file_name in os.listdir(Sound_folder)]
title_dlls = [Title_folder + file_name for file_name in os.listdir(Title_folder)]
font_dlls = [Font_folder + file_name for file_name in os.listdir(Font_folder)]

setup(name="name",
      windows=[mygame],
      data_files=[('D:/dist/SDL2/x64/', sdl_dlls),('D:/dist/Battle_State/', battle_dlls),('D:/dist/Data/', data_dlls), ('D:/dist/Game_Over/', gameover_dlls),
                  ('D:/dist/Main_Map/', mainmap_dlls),('D:/dist/Npc/', npc_dlls),('D:/dist/Sound/', sound_dlls), ('D:/dist/Title/', title_dlls), ('D:/dist/Font/', font_dlls)], # copy resource to '.' folder
      zipfile=None,
      options={"py2exe": py2exe_options},
      )

