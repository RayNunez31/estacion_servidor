CREATE OR REPLACE FUNCTION check_alarms()
RETURNS TRIGGER AS $$
DECLARE
    alarma RECORD;
    exceeded BOOLEAN := FALSE;
BEGIN
    -- Loop through all alarms for the station
    FOR alarma IN
        SELECT * FROM alarmas WHERE estacion_id = NEW.estacion_id
    LOOP
        -- Check if any value exceeds the threshold
        IF (alarma.temperatura IS NOT NULL AND NEW.temperatura > alarma.temperatura) OR
           (alarma.humedad IS NOT NULL AND NEW.humedad > alarma.humedad) OR
           (alarma.presionatmosferica IS NOT NULL AND NEW.presionatmosferica > alarma.presionatmosferica) OR
           (alarma.velocidad_del_viento IS NOT NULL AND NEW.velocidad_del_viento > alarma.velocidad_del_viento) OR
           (alarma.direccion_del_viento IS NOT NULL AND NEW.direccion_del_viento > alarma.direccion_del_viento) OR
           (alarma.pluvialidad IS NOT NULL AND NEW.pluvialidad > alarma.pluvialidad) THEN
            exceeded := TRUE;
            INSERT INTO notificaciones (mensaje, fecha, alarma_id)
            VALUES (FORMAT('Alarma %s activada.', alarma.nombre), CURRENT_TIMESTAMP, alarma.id_alarma);
        END IF;
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;