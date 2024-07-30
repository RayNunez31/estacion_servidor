CREATE OR REPLACE FUNCTION update_estac_status()
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
	-- Establecer la zona horaria a "America/Santo_Domingo"
    PERFORM set_config('TimeZone', 'America/Santo_Domingo', true);
    UPDATE estac
    SET has_new_data = (
        SELECT COUNT(*) > 0
        FROM newlectura
        WHERE estacion_id = estac.id_estacion
          AND hora >= NOW() - INTERVAL '1 minute'
    );
END;
$$;