--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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
-- Name: compte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.compte (
    id bigint NOT NULL,
    nom_compte character varying(50),
    prenom_compte character varying(50),
    email_compte character varying(100) NOT NULL,
    mdp character varying(50) NOT NULL,
    mdp_crypted character varying(500) NOT NULL,
    tel character varying(50),
    adresse character varying(50),
    adresse_comp character varying(50),
    cp character varying(7),
    ville character varying(50),
    pays character varying(50),
    fonction text
);


ALTER TABLE public.compte OWNER TO postgres;

--
-- Name: compte_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.compte_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.compte_id_seq OWNER TO postgres;

--
-- Name: compte_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.compte_id_seq OWNED BY public.compte.id;


--
-- Name: temperature; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.temperature (
    id bigint NOT NULL,
    degre numeric(5,2) NOT NULL,
    localisation character varying(20) NOT NULL,
    date_temperature date NOT NULL,
    heure time without time zone,
    compte integer NOT NULL
);


ALTER TABLE public.temperature OWNER TO postgres;

--
-- Name: temperature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.temperature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.temperature_id_seq OWNER TO postgres;

--
-- Name: temperature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.temperature_id_seq OWNED BY public.temperature.id;


--
-- Name: compte id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compte ALTER COLUMN id SET DEFAULT nextval('public.compte_id_seq'::regclass);


--
-- Name: temperature id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperature ALTER COLUMN id SET DEFAULT nextval('public.temperature_id_seq'::regclass);


--
-- Data for Name: compte; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.compte (id, nom_compte, prenom_compte, email_compte, mdp, mdp_crypted, tel, adresse, adresse_comp, cp, ville, pays, fonction) FROM stdin;
\.


--
-- Data for Name: temperature; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.temperature (id, degre, localisation, date_temperature, heure, compte) FROM stdin;
\.


--
-- Name: compte_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.compte_id_seq', 1, false);


--
-- Name: temperature_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.temperature_id_seq', 1, false);


--
-- Name: compte compte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compte
    ADD CONSTRAINT compte_pkey PRIMARY KEY (id);


--
-- Name: temperature temperature_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperature
    ADD CONSTRAINT temperature_pkey PRIMARY KEY (id);


--
-- Name: temperature temperature_compte_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.temperature
    ADD CONSTRAINT temperature_compte_fkey FOREIGN KEY (compte) REFERENCES public.compte(id);


--
-- PostgreSQL database dump complete
--

