-- Seed data for spockpm
-- This is a placeholder seed file
CREATE TABLE IF NOT EXISTS public.test_table (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO public.test_table (name) VALUES ('test')
ON CONFLICT DO NOTHING;