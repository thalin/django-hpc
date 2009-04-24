from django.db import models
 
import uuid
 
class UUIDField(models.CharField):
    """
        A field which stores a UUID value in hex format. This may also have
        the Boolean attribute 'auto' which will set the value on initial save to a
        new UUID value (calculated using the UUID1 method). Note that while all
        UUIDs are expected to be unique we enforce this with a DB constraint.

        Credit for this field goes to David Cramer.
        See:
            http://www.davidcramer.net/code/420/improved-uuidfield-in-django.html
        for additional details.
    """
    __metaclass__ = models.SubfieldBase
 
    def __init__(self, version=4, node=None, clock_seq=None, namespace=None, auto=False, name=None, *args, **kwargs):
        assert(version in (1, 3, 4, 5), "UUID version %s is not supported." % (version,))
        self.auto = auto
        self.version = version
        # Set this as a fixed value, we store UUIDs in text.
        kwargs['max_length'] = 32
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version in (3, 5):
            self.namespace, self.name = namespace, name
        super(UUIDField, self).__init__(*args, **kwargs)
 
    def _create_uuid(self):
        if self.version == 1:
            args = (self.node, self.clock_seq)
        elif self.version in (3, 5):
            args = (self.namespace, self.name)
        else:
            args = ()
        return getattr(uuid, 'uuid%s' % (self.version,))(*args)
 
    def db_type(self):
        return 'char'
 
    def pre_save(self, model_instance, add):
        """ see CharField.pre_save
            This is used to ensure that we auto-set values if required.
        """
        value = getattr(model_instance, self.attname, None)
        if not value and self.auto:
            # Assign a new value for this attribute if required.
            value = self._create_uuid()
            setattr(model_instance, self.attname, value)
        return value
 
    def to_python(self, value):
        if not value: return
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value
 
    def get_db_prep_save(self, value):
        if not value: return
        assert(isinstance(value, uuid.UUID))
        return value.hex
 
    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, uuid.UUID))
        return unicode(value)
