# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Errors(models.Model):
    ivoid = models.TextField()
    url = models.TextField()
    svc_type = models.TextField()
    date = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    section = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'errors'
        verbose_name = 'error'
        verbose_name_plural = 'errors'
        indexes = [ # add indexes 
            models.Index(fields=['date']),
            models.Index(fields=['svc_type']),
            models.Index(fields=['ivoid']),
            models.Index(fields=['url']),
        ]

class Services(models.Model):
    ivoid = models.TextField()
    url = models.TextField()
    title = models.TextField(blank=True, null=True)
    short_name = models.TextField(blank=True, null=True)
    date_insert = models.TextField(blank=True, null=True)
    date_update = models.TextField(blank=True, null=True)
    vor_status = models.TextField(blank=True, null=True)
    vor_created = models.TextField(blank=True, null=True)
    vor_updated = models.TextField(blank=True, null=True)
    contact_name = models.TextField(blank=True, null=True)
    contact_email = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    xsi_type = models.TextField(blank=True, null=True)
    spec = models.TextField(blank=True, null=True)
    specv = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    val_mode = models.TextField(blank=True, null=True)
    result_vot = models.TextField(blank=True, null=True)
    result_spec = models.TextField(blank=True, null=True)
    nb_warn = models.IntegerField(blank=True, null=True)
    nb_err = models.IntegerField(blank=True, null=True)
    nb_fatal = models.IntegerField(blank=True, null=True)
    days_same = models.IntegerField(blank=True, null=True)
    nb_fail = models.IntegerField(blank=True, null=True)
    provenance = models.TextField(blank=True, null=True)
    standard_id = models.TextField(blank=True, null=True)
    svc_type = models.TextField()

    class Meta:
        managed = True
        db_table = 'services'
        verbose_name = 'service'
        verbose_name_plural = 'services'
        unique_together = (('ivoid', 'url'),)
        indexes = [ # add indexes on fields that can be searched via datatables searchbox
            models.Index(fields=['title']),
            models.Index(fields=['short_name']),
            models.Index(fields=['result_vot']),
            models.Index(fields=['result_spec']),
        ]


