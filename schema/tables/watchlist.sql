CREATE TABLE public.watchlist (
    id serial PRIMARY KEY,
    stock_id serial NOT NULL,
    bars bigint NOT NULL
)