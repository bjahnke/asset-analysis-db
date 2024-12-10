BEGIN;

-- Create the view to dynamically include st_px and en_px
CREATE OR REPLACE VIEW public.peak_with_prices AS
SELECT 
    p.start,
    p."end",
    p.type,
    p.lvl,
    s1.close AS st_px,
    s2.close AS en_px,
    p.stock_id
FROM 
    public.peak p
JOIN 
    public.stock_data s1 ON p.start = s1.bar_number
JOIN 
    public.stock_data s2 ON p."end" = s2.bar_number;

COMMIT;
