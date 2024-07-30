from django.db import models


from django.db import models

class Estac(models.Model):
    id_estacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    has_new_data = models.BooleanField(default=True)
    ultima_actualizacion = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'estac'

class Alarmas(models.Model):
    id_alarma = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    presionatmosferica = models.FloatField(blank=True, null=True)
    velocidad_del_viento = models.FloatField(blank=True, null=True)
    pluvialidad = models.FloatField(blank=True, null=True)
    estacion = models.ForeignKey('Estac', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarmas'
        
class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(blank=True, null=True)
    alarma = models.ForeignKey(Alarmas, models.DO_NOTHING, blank=True, null=True)
    estacion = models.ForeignKey('Estac', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificaciones'

class Newlectura(models.Model):
    id_lectura = models.AutoField(primary_key=True)
    estacion = models.ForeignKey(Estac, models.DO_NOTHING, blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    presionatmosferica = models.FloatField(blank=True, null=True)
    velocidad_del_viento = models.FloatField(blank=True, null=True)
    direccion_del_viento = models.FloatField(blank=True, null=True)
    pluvialidad = models.FloatField(blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newlectura'


class Sensor(models.Model):
    id_sensor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estacion = models.ForeignKey(Estac, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'

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
    