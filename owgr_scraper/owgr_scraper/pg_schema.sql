--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

-- Started on 2018-12-16 02:02:35

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 198 (class 1259 OID 16606)
-- Name: CurrentTournaments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CurrentTournaments" (
    name text NOT NULL,
    tour text,
    field_strength real,
    points real
);


ALTER TABLE public."CurrentTournaments" OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 16565)
-- Name: PlayerEvents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PlayerEvents" (
    player_id text NOT NULL,
    event_id text NOT NULL,
    finish text,
    points real,
    adj_points real,
    weight real,
    week integer,
    year integer,
    tour text,
    event_name text
);


ALTER TABLE public."PlayerEvents" OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16573)
-- Name: Players; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Players" (
    player_id text NOT NULL,
    player_name text NOT NULL,
    current_rank integer
);


ALTER TABLE public."Players" OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 16665)
-- Name: RankingUpdatedDate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."RankingUpdatedDate" (
    date date
);


ALTER TABLE public."RankingUpdatedDate" OWNER TO postgres;

--
-- TOC entry 2706 (class 2606 OID 16613)
-- Name: CurrentTournaments CurrentTournaments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CurrentTournaments"
    ADD CONSTRAINT "CurrentTournaments_pkey" PRIMARY KEY (name);


--
-- TOC entry 2699 (class 2606 OID 16572)
-- Name: PlayerEvents PlayerEvents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PlayerEvents"
    ADD CONSTRAINT "PlayerEvents_pkey" PRIMARY KEY (player_id, event_id);


--
-- TOC entry 2702 (class 2606 OID 16669)
-- Name: Players player_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Players"
    ADD CONSTRAINT player_id_pk PRIMARY KEY (player_id) INCLUDE (player_id);


--
-- TOC entry 2704 (class 2606 OID 16582)
-- Name: Players player_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Players"
    ADD CONSTRAINT player_id_unique UNIQUE (player_id) INCLUDE (player_id);


--
-- TOC entry 2700 (class 1259 OID 16588)
-- Name: fki_player_id_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_player_id_fk ON public."PlayerEvents" USING btree (player_id);


--
-- TOC entry 2707 (class 2606 OID 16583)
-- Name: PlayerEvents player_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PlayerEvents"
    ADD CONSTRAINT player_id_fk FOREIGN KEY (player_id) REFERENCES public."Players"(player_id);


-- Completed on 2018-12-16 02:02:36

--
-- PostgreSQL database dump complete
--

