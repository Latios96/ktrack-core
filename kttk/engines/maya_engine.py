from kttk import template_manager
from kttk.engines.abstract_engine import AbstractEngine

import pymel.core as pm
import maya.cmds as cmds

KTTK_CONTEXT = 'kttk_context'


class MayaEngine(AbstractEngine):


    name = "Maya"  # todo read only
    file_extension = ".mb" # todo read only

    @property
    def qt_main_window(self):
        # local imports because could break app otherwise when running in batch mode
        from shiboken2 import wrapInstance
        from maya import OpenMayaUI
        from PySide2 import QtWidgets

        ptr = OpenMayaUI.MQtUtil.mainWindow()
        return wrapInstance(long(ptr), QtWidgets.QMainWindow)

    def current_file_path(self):  # todo maybe its better to make this a property?
        path = pm.sceneName()

        if path == "":
            return None

        return str(path)

    def open_file(self, file_to_open):
        # call super method to store file_to_open in context
        super(MayaEngine, self).open_file(file_to_open)

        # now open file in maya
        pm.openFile(file_to_open['path'], force=True)

    def open_file_by_path(self, path): # todo add to recent files
        super(MayaEngine, self).open_file_by_path(path)

        # now open file in maya
        pm.openFile(path, force=True)

    def has_unsaved_changes(self):
        return cmds.file(q=True, modified=True)

    def save(self):
        pm.saveFile()
    
    def save_as(self, file_to_save_to):
        # call super for context change
        super(MayaEngine, self).save_as(file_to_save_to)

        # now save the file
        pm.saveAs(file_to_save_to['path'])

    def update_file_for_context(self):
        # check in which context we are
        is_asset = self.context.entity['type'] == 'asset'
        is_shot = self.context.entity['type'] == 'shot'
        is_unsupported_context = is_asset == False and is_shot == False

        # set maya project
        if is_asset:
            maya_workspace_location_template = template_manager.get_route_template('asset_maya_workspace_location')
        elif is_shot:
            maya_workspace_location_template = template_manager.get_route_template('shot_maya_workspace_location')
        elif is_unsupported_context:
            raise Exception("Unsupported context: entity is {}, should be an asset or shot".format(self.context.entity)) # todo create specific exception for this

        # This is handled be workspace.mel:
        # - alembic
        # - sourceimages
        # - renderoutput folder
        # - playblast folder

        # format the workspace location template
        maya_workspace_location = template_manager.format_template(maya_workspace_location_template, self.context.get_avaible_tokens())
        maya_workspace_location = maya_workspace_location.replace("\\", "/")

        # now change to correct location, workspace.mel is is created together with all other folders
        pm.mel.eval(' setProject "{}"'.format(maya_workspace_location))

        # get and format image name template
        image_name_template = template_manager.get_route_template('render_image_file_name')
        image_name = template_manager.format_template(image_name_template, self.context.get_avaible_tokens())

        # set filename for vray
        vray_settings_node = self.__get_vray_settings()
        if vray_settings_node:
            vray_settings_node.fileNamePrefix.set(image_name)

        # set standart fileNamePrefix
        settings_node = self.__get_default_render_globals()
        settings_node.imageFilePrefix.set(image_name)


        # store context in file
        self.serialize_context_to_file()

        # todo set frame rate, frame range and resolution

    def serialize_context_to_file(self):
        pm.fileInfo[KTTK_CONTEXT] = self.context.serialize()

    @staticmethod
    def __get_vray_settings():
        settings_nodes = pm.ls("vraySettings")
        if len(settings_nodes) > 0:
            return settings_nodes[0]

    @staticmethod
    def __get_default_render_globals():
        settings_nodes = pm.ls("defaultRenderGlobals")
        if len(settings_nodes) > 0:
            return settings_nodes[0]

