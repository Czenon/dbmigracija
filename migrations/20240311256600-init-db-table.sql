CREATE TABLE IF NOT EXISTS public.cats
(
    id integer NOT NULL DEFAULT nextval('cats_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    age integer NOT NULL,
    CONSTRAINT cats_pkey PRIMARY KEY (id)
)