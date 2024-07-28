

CREATE OR REPLACE FUNCTION update_estac_status() RETURNS void AS $$
BEGIN
    -- Update has_new_data to false for all stations initially
    UPDATE estac
    SET has_new_data = FALSE;

    -- Update has_new_data to true for stations that have received new data in the last 5 minutes
    UPDATE estac
    SET has_new_data = TRUE
    WHERE id_estacion IN (
        SELECT DISTINCT estacion_id
        FROM newlectura
        WHERE hora >= NOW() - INTERVAL '5 minutes'
    );
END;
$$ LANGUAGE plpgsql;