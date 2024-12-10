CREATE TABLE public.floor_ceiling (
    test double precision NOT NULL,
    fc_val double precision NOT NULL,
    fc_date bigint NOT NULL,
    rg_ch_date bigint NOT NULL,
    rg_ch_val double precision NOT NULL,
    type bigint NOT NULL,
    stock_id bigint NOT NULL,
    CONSTRAINT "bar_number_FK02" FOREIGN KEY (fc_date) REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "bar_number_FK03" FOREIGN KEY (rg_ch_date) REFERENCES public.timestamp_data(bar_number),
    CONSTRAINT "stock_id_FK01" FOREIGN KEY (stock_id) REFERENCES public.stock(id)
);

ALTER TABLE public.floor_ceiling OWNER TO bjahnke71;