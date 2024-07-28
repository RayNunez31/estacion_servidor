from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Newlectura, Alarmas, Notificaciones

@receiver(post_save, sender=Newlectura)
def check_alarms(sender, instance, **kwargs):
    # Get all alarms for the related station
    alarms = Alarmas.objects.filter(estacion=instance.estacion)
    
    for alarma in alarms:
        # Check if any value exceeds the threshold
        if (alarma.temperatura and instance.temperatura > alarma.temperatura) or \
           (alarma.humedad and instance.humedad > alarma.humedad) or \
           (alarma.presionatmosferica and instance.presionatmosferica > alarma.presionatmosferica) or \
           (alarma.velocidad_del_viento and instance.velocidad_del_viento > alarma.velocidad_del_viento) or \
           (alarma.direccion_del_viento and instance.direccion_del_viento > alarma.direccion_del_viento) or \
           (alarma.pluvialidad and instance.pluvialidad > alarma.pluvialidad):
            
            # Create a notification
            Notificaciones.objects.create(
                mensaje=f'Alarma {alarma.nombre} activada.',
                fecha=timezone.now(),
                alarma=alarma
            )