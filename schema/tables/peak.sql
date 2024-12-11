CREATE TABLE public.peak (
    start serial NOT NULL,
    "end" serial NOT NULL,
    type bigint NOT NULL,
    lvl bigint NOT NULL,
    stock_id serial NOT NULL
);

-- ALTER TABLE public.peak OWNER TO bjahnke71;