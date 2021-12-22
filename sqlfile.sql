--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: body_measurement; Type: TABLE; Schema: public; Owner: danielteshager
--

CREATE TABLE public.body_measurement (
    id integer NOT NULL,
    weight double precision NOT NULL,
    height double precision NOT NULL,
    user_id integer
);


ALTER TABLE public.body_measurement OWNER TO danielteshager;

--
-- Name: body_measurement_id_seq; Type: SEQUENCE; Schema: public; Owner: danielteshager
--

CREATE SEQUENCE public.body_measurement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.body_measurement_id_seq OWNER TO danielteshager;

--
-- Name: body_measurement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: danielteshager
--

ALTER SEQUENCE public.body_measurement_id_seq OWNED BY public.body_measurement.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: danielteshager
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    full_name character varying,
    nick_name character varying,
    age integer
);


ALTER TABLE public."user" OWNER TO danielteshager;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: danielteshager
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO danielteshager;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: danielteshager
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: body_measurement id; Type: DEFAULT; Schema: public; Owner: danielteshager
--

ALTER TABLE ONLY public.body_measurement ALTER COLUMN id SET DEFAULT nextval('public.body_measurement_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: danielteshager
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: body_measurement; Type: TABLE DATA; Schema: public; Owner: danielteshager
--

COPY public.body_measurement (id, weight, height, user_id) FROM stdin;
1	80	100	1
2	100	1	1
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: danielteshager
--

COPY public."user" (id, full_name, nick_name, age) FROM stdin;
1	Dan	D	22
\.


--
-- Name: body_measurement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: danielteshager
--

SELECT pg_catalog.setval('public.body_measurement_id_seq', 2, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: danielteshager
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: body_measurement body_measurement_pkey; Type: CONSTRAINT; Schema: public; Owner: danielteshager
--

ALTER TABLE ONLY public.body_measurement
    ADD CONSTRAINT body_measurement_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: danielteshager
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: body_measurement body_measurement_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: danielteshager
--

ALTER TABLE ONLY public.body_measurement
    ADD CONSTRAINT body_measurement_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

