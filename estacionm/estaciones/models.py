from django.db import models


class Estac(models.Model):
    nombre = models.CharField(db_column='Nombre', blank=True, null=True)  # Field name made lowercase.
    id_estacion = models.BigIntegerField(db_column='Id_Estacion', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estac'


class Mediclima(models.Model):
    id_med = models.BigIntegerField(db_column='Id_Med', primary_key=True)  # Field name made lowercase. The composite primary key (Id_Med, Id_Estacion, Fecha_Med_Lec) found, that is not supported. The first column is selected.
    velvient = models.FloatField(db_column='VelVient', blank=True, null=True)  # Field name made lowercase.
    direcvien = models.IntegerField(db_column='DirecVien', blank=True, null=True)  # Field name made lowercase.
    id_estacion = models.ForeignKey(Estac, models.DO_NOTHING, db_column='Id_Estacion')  # Field name made lowercase.
    pluvi = models.FloatField(db_column='Pluvi', blank=True, null=True)  # Field name made lowercase.
    fecha_med_lec = models.DateTimeField(db_column='Fecha_Med_Lec')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MediClima'
        unique_together = (('id_med', 'id_estacion', 'fecha_med_lec'),)


class Sensorgen(models.Model):
    presionat = models.FloatField(db_column='PresionAt', blank=True, null=True)  # Field name made lowercase.
    id_estacion = models.OneToOneField(Estac, models.DO_NOTHING, db_column='Id_Estacion', primary_key=True)  # Field name made lowercase. The composite primary key (Id_Estacion, Fecha_Lec_Sen, Id_Sensor) found, that is not supported. The first column is selected.
    fecha_lec_sen = models.DateTimeField(db_column='Fecha_Lec_Sen')  # Field name made lowercase.
    temperatura = models.FloatField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    humedad = models.FloatField(db_column='Humedad', blank=True, null=True)  # Field name made lowercase.
    id_sensor = models.BigIntegerField(db_column='Id_Sensor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SensorGen'
        unique_together = (('id_estacion', 'fecha_lec_sen', 'id_sensor'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Medicionescombinadas(models.Model):
    velvient = models.FloatField(blank=True, null=True)
    direcvien = models.IntegerField(blank=True, null=True)
    id_estacion = models.BigIntegerField(blank=True, null=True)
    pluvi = models.FloatField(blank=True, null=True)
    fecha_med_lec = models.DateTimeField(blank=True, null=True)
    presionat = models.FloatField(blank=True, null=True)
    fecha_lec_sen = models.DateTimeField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    id_sensor = models.BigIntegerField(blank=True, null=True)
    id_med = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'medicionescombinadas'
        unique_together = (('id_estacion', 'fecha_med_lec', 'fecha_lec_sen', 'id_sensor'),)