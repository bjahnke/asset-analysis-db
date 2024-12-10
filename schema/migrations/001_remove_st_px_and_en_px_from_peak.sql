BEGIN;

-- Remove the redundant columns
ALTER TABLE public.peak DROP COLUMN st_px;
ALTER TABLE public.peak DROP COLUMN en_px;

-- Add foreign keys to reference stock_data
ALTER TABLE public.peak 
ADD CONSTRAINT fk_start FOREIGN KEY (start) REFERENCES public.stock_data (bar_number),
ADD CONSTRAINT fk_end FOREIGN KEY ("end") REFERENCES public.stock_data (bar_number);

COMMIT;
