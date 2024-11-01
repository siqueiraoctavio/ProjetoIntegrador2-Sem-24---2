--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

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

--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    "CNPJ" character varying NOT NULL,
    "Primeiro_Nome" character varying,
    "Segundo_Nome" character varying,
    "Email" character varying,
    "Telefone" character varying,
    "Estado" character varying,
    "Cidade" character varying,
    "Bairro" character varying,
    "Rua" character varying,
    "Numero" character varying
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: compras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.compras (
    "Obra_OS" character varying,
    "Ordem_de_Compras" character varying NOT NULL,
    "Materia_prima" character varying,
    "Consumiveis" character varying,
    "Miscelanea" character varying
);


ALTER TABLE public.compras OWNER TO postgres;

--
-- Name: obras; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.obras (
    "OS" character varying NOT NULL,
    "Primeiro_Nome_Contato" character varying,
    "Segundo_Nome_Contato" character varying,
    "Valor" double precision,
    "Estado_Obra" character varying,
    "Cidade_Obra" character varying,
    "Bairro_Obra" character varying,
    "Rua_Obra" character varying,
    "Numero_Obra" character varying,
    "CNPJ_Cliente" character varying
);


ALTER TABLE public.obras OWNER TO postgres;

--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes ("CNPJ", "Primeiro_Nome", "Segundo_Nome", "Email", "Telefone", "Estado", "Cidade", "Bairro", "Rua", "Numero") FROM stdin;
23.456.789/0001-81	Maria	Oliveira	maria.oliveira@pisoselevadosbrasil.com	(21) 99876-5432	RJ	Rio de Janeiro	Copacabana	Rua Barata Ribeiro	450
12.345.678/0001-90	Carlos	Souza	carlos.souza@pisoselevados.com	(11) 98765-4321	SP	S├úo Paulo	Bela Vista	Av. Paulista	1234
\.


--
-- Data for Name: compras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.compras ("Obra_OS", "Ordem_de_Compras", "Materia_prima", "Consumiveis", "Miscelanea") FROM stdin;
1	1	Estruturas de a├ºo para piso	Parafusos e fixadores	Placas de piso elevado
2	2	Placas de concreto para piso elevado	Espumas e adesivos	Perfis met├ílicos
3	3	Perfis met├ílicos	Selantes e fitas	Tapetes antiderrapantes
4	4	Estruturas de alum├¡nio	Lixas e lubrificantes	Caixas de passagem para cabos
5	5	Placas de vidro para piso	Selantes para vidro	Estruturas niveladoras
\.


--
-- Data for Name: obras; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.obras ("OS", "Primeiro_Nome_Contato", "Segundo_Nome_Contato", "Valor", "Estado_Obra", "Cidade_Obra", "Bairro_Obra", "Rua_Obra", "Numero_Obra", "CNPJ_Cliente") FROM stdin;
1	Marcelo	Silva	45000	SP	Campinas	Cambu├¡	Rua dos Alecrins	987	12.345.678/0001-90
4	Jo├úo	Alves	60000	RJ	Niter├│i	Icara├¡	Av. Roberto Silveira	1200	23.456.789/0001-81
2	Renata	Carvalho	38500	SP	Ribeir├úo Preto	Jardim Calif┬órnia	Avenida Caramuru	455	12.345.678/0001-90
3	Felipe	Mendes	52750	SP	Sorocaba	Centro	Rua da Penha	210	12.345.678/0001-90
5	Ana	Martins	72300	RJ	Petr├│polis	Realengo	Rua do Imperador	800	23.456.789/0001-81
\.


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY ("CNPJ");


--
-- Name: compras compras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compras
    ADD CONSTRAINT compras_pkey PRIMARY KEY ("Ordem_de_Compras");


--
-- Name: obras obras_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obras
    ADD CONSTRAINT obras_pkey PRIMARY KEY ("OS");


--
-- Name: compras compras_Obra_OS_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compras
    ADD CONSTRAINT "compras_Obra_OS_fkey" FOREIGN KEY ("Obra_OS") REFERENCES public.obras("OS");


--
-- Name: obras obras_CNPJ_Cliente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.obras
    ADD CONSTRAINT "obras_CNPJ_Cliente_fkey" FOREIGN KEY ("CNPJ_Cliente") REFERENCES public.clientes("CNPJ");


--
-- PostgreSQL database dump complete
--

