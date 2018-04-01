import pickle


class Context(object):

    def __init__(self, project=None, entity=None, step=None, task=None, workfile=None, user=None):
        self.project = project
        self.entity = entity
        self.step = step
        self.task = task
        self.workfile = workfile
        self.user = user


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
        context_dict={}
        context_dict['project']=self.project
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