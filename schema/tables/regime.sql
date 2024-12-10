CREATE TABLE public.regime (
    start bigint NOT NULL,
    "end" bigint NOT NULL,
    rg double precision NOT NULL,
    type text NOT NULL,
    stock_id bigint NOT NULL,
    CONSTRAINT "bar_number_FK01" FOREIGN KEY (start) REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "bar_number_FK02" FOREIGN KEY ("end") REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "stock_id_FK01" FOREIGN KEY (stock_id) REFERENCES public.stock(id)
);

ALTER TABLE public.regime OWNER TO bjahnke71;