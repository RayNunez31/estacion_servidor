CREATE OR REPLACE FUNCTION notify_data_update() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('data_update', row_to_json(NEW)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER newlectura_update
AFTER INSERT OR UPDATE ON newlectura
FOR EACH ROW EXECUTE FUNCTION notify_data_update();