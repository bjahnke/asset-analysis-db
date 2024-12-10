CREATE TABLE public.stock_data (
    bar_number bigint NOT NULL,
    close double precision NOT NULL,
    stock_id bigint NOT NULL,
    open double precision NOT NULL,
    high double precision NOT NULL,
    low double precision NOT NULL,
    volume bigint NOT NULL,
    CONSTRAINT "bar_number_FK01" FOREIGN KEY (bar_number) REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "stock_id_FK02" FOREIGN KEY (stock_id) REFERENCES public.stock(id)
);

ALTER TABLE public.stock_data OWNER TO bjahnke71;