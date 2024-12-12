CREATE TABLE public.stock_data (
    id serial PRIMARY KEY,
    bar_number serial NOT NULL,
    close double precision NOT NULL,
    stock_id bigint NOT NULL,
    open double precision NOT NULL,
    high double precision NOT NULL,
    low double precision NOT NULL,
    volume bigint NOT NULL
);

-- ALTER TABLE public.stock_data OWNER TO bjahnke71;