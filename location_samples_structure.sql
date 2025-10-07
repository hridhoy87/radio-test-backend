--
-- PostgreSQL database dump
--

\restrict B8m4e3ZHLFg5mbL1gGWGo6cOiLKfp7f6dt4fLHtd18WyLMtgCdR2M1dXCp7NSCW

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

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
-- Name: location_samples; Type: TABLE; Schema: public; Owner: radio_user
--

CREATE TABLE public.location_samples (
    server_id uuid NOT NULL,
    client_id character varying NOT NULL,
    lat double precision NOT NULL,
    lon double precision NOT NULL,
    acc double precision NOT NULL,
    sample_date character varying NOT NULL,
    sample_time character varying NOT NULL,
    captured_at_utc bigint NOT NULL,
    provider character varying NOT NULL,
    freq character varying NOT NULL,
    rf_pwr character varying NOT NULL,
    comm_state character varying NOT NULL,
    "user" character varying NOT NULL,
    station character varying NOT NULL,
    device_id character varying NOT NULL,
    received_at timestamp without time zone NOT NULL,
    processed boolean NOT NULL,
    sync boolean DEFAULT false,
    attempt_count integer DEFAULT 0,
    last_error text,
    synced_at_utc bigint
);


ALTER TABLE public.location_samples OWNER TO radio_user;

--
-- Name: location_samples location_samples_pkey; Type: CONSTRAINT; Schema: public; Owner: radio_user
--

ALTER TABLE ONLY public.location_samples
    ADD CONSTRAINT location_samples_pkey PRIMARY KEY (server_id);


--
-- Name: ix_location_samples_client_id; Type: INDEX; Schema: public; Owner: radio_user
--

CREATE UNIQUE INDEX ix_location_samples_client_id ON public.location_samples USING btree (client_id);


--
-- Name: ix_location_samples_device_id; Type: INDEX; Schema: public; Owner: radio_user
--

CREATE INDEX ix_location_samples_device_id ON public.location_samples USING btree (device_id);


--
-- PostgreSQL database dump complete
--

\unrestrict B8m4e3ZHLFg5mbL1gGWGo6cOiLKfp7f6dt4fLHtd18WyLMtgCdR2M1dXCp7NSCW

