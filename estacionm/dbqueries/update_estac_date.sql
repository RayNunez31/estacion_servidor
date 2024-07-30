CREATE OR REPLACE FUNCTION actualizar_fecha_ultima_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    -- Configura el timezone a 'America/Santo_Domingo'
    PERFORM set_config('TimeZone', 'America/Santo_Domingo', true);

    -- Actualiza el campo ultima_actualizacion en la tabla estac
    UPDATE estac
    SET ultima_actualizacion = CURRENT_TIMESTAMP
    WHERE id_estacion = NEW.estacion_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;