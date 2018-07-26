import getpass
import pickle

import ktrack_api
from kttk import template_manager, user_manager


class InvalidEntityException(Exception):

    def __init__(self, type_missing, id_missing):
        super(InvalidEntityException, self).__init__(
            "Entity is invalid: type missing: {}, id missing: {}".format(type_missing, id_missing))


class InvalidStepException(Exception):

    def __init__(self, step):
        super(InvalidStepException, self).__init__("Invalid step, {} is not a non-empty string, its {}!".format(step, type(step)))


# todo make them contain only type and id
# todo step should be taken from task if task is provided
class Context(object):
    # todo add docs
    """
    Context is immutable!!!
    """

    # todo create context_changed signal / callback
    def __init__(self, project=None, entity=None, step=None, task=None, workfile=None, user=None):
        # project
        self._validate_entity_dict(project)
        self._project = project

        # entity
        self._validate_entity_dict(entity)
        self._entity = entity

        # step
        self._validate_step(step)
        self._step = step

        # task
        self._validate_entity_dict(task)
        self._task = task

        # workfile
        self._validate_entity_dict(workfile)
        self._workfile = workfile

        # user
        self._validate_entity_dict(user)
        self._user = user

    @property
    def project(self):
        return self._project

    @property
    def entity(self):
        return self._entity

    @property
    def step(self):
        return self._step

    @property
    def task(self):
        return self._task

    @property
    def workfile(self):
        return self._workfile

    @property
    def user(self):
        return self._user

    @staticmethod
    def _validate_step(step):
        """
        Validates the given step. A step can be null or string or unicode, but not empty string
        :param step: step to validate
        :return: True if step is valid, raises InvalidStepException if not
        """
        if step is not None:
            if isinstance(step, str) or isinstance(step, unicode):
                if len(step) >0:
                    return True
            raise InvalidStepException(step)
        else:
            return True

    @staticmethod
    def _validate_entity_dict(entity_dict):
        # type: (dict) -> bool
        """
        Validates the given entity dict. Should have at least a type and a id and they are not None
        :param dic:
        :return: true if entity has type and id, otherwise invalid entity Exception is thrown
        """
        if entity_dict is not None:
            has_type = entity_dict.get("type")
            has_id = entity_dict.get("id")

            if has_type and has_id:
                return True
            else:
                raise InvalidEntityException(not has_type, not has_id)
        else:
            return True

    def __repr__(self):
        # multi line repr
        msg = []
        msg.append("  Project: %s" % str(self.project))
        msg.append("  Entity: %s" % str(self.entity))
        msg.append("  Step: %s" % str(self.step))
        msg.append("  Task: %s" % str(self.task))
        msg.append("  User: %s" % str(self.user))

        return "<Sgtk Context: \n%s>" % ("\n".join(msg))

    def _entity_dicts_equal(self, left, right):
        """
        Tests if two entity dicts are equal. They are equal if both type and id match or both are None
        :param left:
        :param right:
        :return:
        """
        if left == right == None:
            return True
        if left == None or right == None:
            return False
        return left["type"] == right["type"] and left["id"] == right["id"]

    def __eq__(self, other):
        """
        Tests if two context are equal. Contexts are considered equal, if both type and id attributes of containing entities
        match and step string matches
        :param other:
        :return:
        """

        if not isinstance(other, Context):
            return NotImplemented

        # test project
        if not self._entity_dicts_equal(self.project, other.project):
            return False

        # test entity
        if not self._entity_dicts_equal(self.entity, other.entity):
            return False

        # test step
        if not self.step == other.step:
            return False

        # test task
        if not self._entity_dicts_equal(self.task, other.task):
            return False

        # test workfile
        if not self._entity_dicts_equal(self.workfile, other.workfile):
            return False

        # test user
        if not self._entity_dicts_equal(self.user, other.user):
            return False

        return True

    def __ne__(self, other):
        """
        Test if this Context instance is not equal to the other Context instance

        :param other:   The other Context instance to compare with
        :returns:       True if self != other, False otherwise
        """
        is_equal = self.__eq__(other)
        if is_equal is NotImplemented:
            return NotImplemented
        return not is_equal

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

    def copy_context(self, project=0, entity=0, step=0, task=0, workfile=0, user=0):
        """
        Copy util. Returns a new context instance, will contain values from this context if not overriden by keyword args
        Note: We use 0 here instead of None, so we can override with None
        :param self:
        :param project:
        :param entity:
        :param step:
        :param task:
        :param workfile:
        :param user:
        :return:
        """
        _project = self.project
        if project != 0:
            _project = project

        _entity = self.entity
        if entity != 0:
            _entity = entity

        _step = self.step
        if step != 0:
            _step = step

        _task = self.task
        if task != 0:
            _task = task

        _workfile = self.workfile
        if workfile != 0:
            _workfile = workfile

        _user = self.user
        if user != 0:
            _user = user

        return Context(_project, _entity, _step, _task, _workfile, _user)
