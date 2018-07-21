import getpass
import pickle

import ktrack_api
from kttk import template_manager


class Context(object):
    # todo create context_changed signal / callback
    def __init__(self, project=None, entity=None, step=None, task=None, workfile=None, user=None):
        self.project = project
        self.entity = entity
        self.step = step # step is a simple string
        self.task = task
        self.workfile = workfile
        self.user = user

        if not self.user:
            self.user = {'name': getpass.getuser()} # todo find user with name in database

    def __repr__(self):
        # multi line repr
        msg = []
        msg.append("  Project: %s" % str(self.project))
        msg.append("  Entity: %s" % str(self.entity))
        msg.append("  Step: %s" % str(self.step))
        msg.append("  Task: %s" % str(self.task))
        msg.append("  User: %s" % str(self.user))

        return "<Sgtk Context: \n%s>" % ("\n".join(msg))

    def as_dict(self):
        """
        Converts this context into a dictionary
        :return: this context as dict
        """
        context_dict = {}
        context_dict['project'] = self.project
        context_dict['entity'] = self.entity
        context_dict['step'] = self.step
        context_dict['task'] = self.task
        context_dict['workfile'] = self.workfile
        context_dict['user'] = self.user

        return context_dict

    @classmethod
    def from_dict(cls, context_dict):
        """
        Constructs a new Context from given dictionary
        :param context_dict:
        :return: a new Context object
        """
        return Context(project=context_dict.get('project'),
                       entity=context_dict.get('entity'),
                       step=context_dict.get('step'),
                       task=context_dict.get('task'),
                       workfile=context_dict.get('workfile'),
                       user=context_dict.get('user'))

    def serialize(self):
        """
        Serializes this context to a pickle string
        :return:
        """
        return pickle.dumps(self.as_dict())

    @classmethod
    def deserialize(cls, string):
        return cls.from_dict(pickle.loads(string))

    def get_avaible_tokens(self):
        avaible_tokens = {}

        if self.project:
            avaible_tokens['project_name'] = self.project['name']

        # make sure to query all fields from ktrack, because we might only have id and type

        kt = ktrack_api.get_ktrack()

        if self.entity:
            entity = kt.find_one(self.entity['type'], self.entity['id'])
            avaible_tokens['code'] = entity['code']

            if entity['type'] == 'asset':
                avaible_tokens['asset_type'] = entity['asset_type']

        if self.step:
            avaible_tokens['step'] = self.step

        if self.task:
            avaible_tokens['task_name'] = self.task['name']

        if self.workfile:
            workfile = kt.find_one('workfile', self.workfile['id'])

            avaible_tokens['work_file_name'] = workfile['name']
            avaible_tokens['work_file_path'] = workfile['path']
            avaible_tokens['work_file_comment'] = workfile['comment']
            avaible_tokens['version'] = "v{}".format("{}".format(workfile['version_number']).zfill(3))

        if self.user:
            user = kt.find_one('user', self.user['id'])
            avaible_tokens['user_name'] = user['name']

        avaible_tokens['project_root'] = template_manager.get_route_template('project_root')

        return avaible_tokens
