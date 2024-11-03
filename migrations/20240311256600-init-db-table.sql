CREATE TABLE IF NOT EXISTS public.cats
(
    id serial NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    age integer NOT NULL,
    CONSTRAINT cats_pkey PRIMARY KEY (id)
);