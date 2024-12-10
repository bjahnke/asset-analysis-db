CREATE TABLE public.peak (
    start bigint NOT NULL,
    "end" bigint NOT NULL,
    type bigint NOT NULL,
    lvl bigint NOT NULL,
    stock_id bigint NOT NULL,
    CONSTRAINT "bar_number_FK01" FOREIGN KEY (start) REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "bar_number_FK02" FOREIGN KEY ("end") REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "stock_id_FK01" FOREIGN KEY (stock_id) REFERENCES public.stock(id)
);

ALTER TABLE public.peak OWNER TO bjahnke71;