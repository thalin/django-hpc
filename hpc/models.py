from datetime import datetime

from django.db import models
from django.utils.encoding import smart_str, smart_unicode

from hpc.fields import UUIDField
from hpc.exceptions import HPCError

class HPCJob(models.Model):
    '''
    This model represents an HPC job.  To use this model you must inherit from
    this class, and at least override the run_job method.  The run_job method
    MUST return a string that is the command line of the process you want to
    schedule on the cluster.

    You may also override the setup and cleanup methods which are run before
    and after the run_job method, respectively.
    '''
    uuid = UUIDField(auto=True)
    processing = models.BooleanField(editable=False)
    completed = models.BooleanField(editable=False)
    error = models.BooleanField(editable=False)
    error_msg = models.TextField(editable=False, blank=True)
    debug_msg = models.TextField(editable=False, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return smart_str(self.uuid)

    def __unicode__(self):
        return smart_unicode(self.uuid)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        super(HPCJob, self).save(*args, **kwargs)

    def setup(self):
        '''
        Set up environment for job submission.

        Here is where you would copy files around etc.
        '''
        pass

    def cleanup(self):
        '''
        Clean up the after execution.

        You should remove any files created by your process, or at least move
        them to a more permanent storage space in this function.
        '''
        pass

    def run_job(self):
        '''
        Figure out and return the job submission command line.
        '''
        NIEStr = "You must define this function for your job to be submitted."
        raise NotImplementedError(NIEStr)
