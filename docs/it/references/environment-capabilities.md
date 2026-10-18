# Modello delle capacità dell'ambiente

[English](../../../references/environment-capabilities.md) | [Italiano](environment-capabilities.md)

## Distinzione fondamentale

**La conoscenza è globale; la disponibilità è locale.**

AWA non deve equiparare «una risorsa esiste da qualche parte» a «la risorsa è utilizzabile qui».

Tre livelli:

1. **Base di conoscenza delle risorse**: osservazioni globali su modelli, strumenti, skill e schemi di esecuzione.
2. **Profilo delle capacità dell'ambiente**: capacità effettive per una coppia `device_id × environment_id`.
3. **Variazioni della sessione**: autorizzazioni, unità montate e connettori temporanei che possono cambiare a ogni sessione.

## Profilo dell'ambiente

Campi tipici; le chiavi tecniche restano in inglese:

```json
{
  "environment_key": "MY-PC__antigravity-local",
  "device_id": "MY-PC",
  "environment_id": "antigravity-local",
  "last_verified": "...",
  "capabilities": {
    "python": {"status": "AVAILABLE", "version": "..."},
    "filesystem": {"status": "AVAILABLE"},
    "google_drive_vault": {"status": "AVAILABLE"},
    "subagents": {"status": "AVAILABLE"},
    "skill:foo": {"status": "AVAILABLE"}
  }
}
```

Stati concreti quando possibile: `AVAILABLE` (disponibile), `UNAVAILABLE` (non disponibile), `NOT_YET_GRANTED` (non ancora autorizzato), `UNKNOWN` (sconosciuto), `STALE` (da aggiornare).

## Verifica delle capacità

Non chiedere all'utente ciò che si può accertare deterministicamente.

Esempi:

- `python --version`;
- `git --version`;
- verifica di un percorso filesystem;
- verifica dell'unità/cartella Drive;
- inventario delle skill installate;
- controllo dello stato di un connettore.

Memorizzare temporaneamente i fatti stabili. Ripetere le verifiche solo per dati obsoleti o rilevanti alla decisione.

## Scelta tra ambienti

Regola concettuale:

```text
Requisiti del task
∩ conoscenza globale delle risorse
∩ disponibilità dell'ambiente corrente
= piano locale fattibile
```

Se il piano ideale non è fattibile localmente:

1. Verificare ambienti alternativi noti.
2. Se esiste un ambiente migliore verificato, consigliare `HANDOFF_TO_ENVIRONMENT`; riutilizzare piano/checkpoint/log accessibili e produrre un Handoff Pack solo se la destinazione necessita di contesto o accessi mancanti.
3. Altrimenti adattare localmente il piano.

Non scegliere un altro ambiente solo perché un vecchio profilo indicava una capacità disponibile tempo fa. Rispettare `last_verified` e il livello di fiducia.
