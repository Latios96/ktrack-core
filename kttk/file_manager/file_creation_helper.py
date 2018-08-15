import os

import ktrack_api
from kttk import template_manager


class FileCreationHelper(object):
    """
    Class containing helper methods for file creation
    """

    def __init__(self, engine):
        self._engine = engine

    def _context_is_valid_for_file_creation(self, context):
        """
        Validates given context for file creation. Is valid if contains project, entity, task and step
        :param context:
        :return: True if context is valid else false
        """
        has_project = context.project != None
        has_entity = context.entity != None
        has_task = context.task != None
        has_step = context.step != None

        if has_project and has_entity and has_task and has_step:
            return True
        else:
            missing = []

            if not has_project:
                missing.append('project')

            if not has_entity:
                missing.append('entity')

            if not has_task:
                missing.append('task')

            if not has_step:
                missing.append('step')

            raise ValueError("Invalid context: Missing {}".format(", ".join(missing)))

    def _get_highest_workfile(self, context):
        """
        Checks for exisitng workfiles for context.task. If there is one, will return the one with highest version_number.
        If not, will return None
        :param context:
        :return: workfile with highest version number if exists, else None
        """
        kt = ktrack_api.get_ktrack()
        # get all workfiles for task
        workfiles = kt.find("workfile", [['entity', 'is', context.task]])

        # no tasks exist, so return None
        if len(workfiles) == 0:
            return None

        # else search for highest version number, return this one
        return max(workfiles, key=lambda workfile: workfile['version_number'])

    def _create_new_workfile(self, context):
        """
        Creates a new worfile, used when no workfile to create from exists
        :param workfile:
        :return:
        """
        return self._create_workfile_from(context, {'version_number': 0})

    def _create_workfile_from(self, context, workfile, comment=""):
        """
        Creates a new workfile based on given workfile. Will increase version number. Workfile and context have to match for project etc.
        :param context:
        :return: the new workfile
        """
        # initial version number is 1
        version_number = workfile['version_number'] + 1 if workfile['version_number'] else 1

        # get template for file name
        workfile_file_name_template = template_manager.get_route_template('workfile_file_name')
        tokens = context.get_avaible_tokens()
        tokens['dcc_extension'] = self._engine.file_extension
        tokens['dcc_name'] = self._engine.name
        tokens['version'] = version_number

        # format template for file name
        workfile_file_name = template_manager.format_template(workfile_file_name_template, tokens)

        # get and format template for workfile folder
        workfile_location_template = template_manager.get_route_template(
            'dcc_scenes_location_{}_{}'.format(context.entity['type'], self._engine.name.lower()))
        workfile_location = template_manager.format_template(workfile_location_template, tokens)

        # combine location and name to workfile path
        path = os.path.join(workfile_location, workfile_file_name)

        workfile_data = {}
        workfile_data['project'] = context.project
        workfile_data['entity'] = context.task
        workfile_data['version_number'] = version_number
        workfile_data['comment'] = comment

        if len(workfile.keys()) > 1:
            workfile_data['created_from'] = workfile

        workfile_data['name'] = workfile_file_name
        workfile_data['path'] = path

        # create new workfile
        kt = ktrack_api.get_ktrack()
        new_workfile = kt.create('workfile', workfile_data)  # todo register path for workfile

        # return newly created workfile
        return new_workfile

    def _get_template_file_path(self):
        """
        Returns formatted template file based on context
        :return:
        """
        template_file_template = template_manager.get_route_template("template_file_dcc")

        tokens = {'dcc_extension': self._engine.file_extension}

        return template_manager.format_template(template_file_template, tokens)
