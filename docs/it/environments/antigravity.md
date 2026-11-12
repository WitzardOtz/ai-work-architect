# Profilo dell'ambiente Antigravity

[English](../../../environments/antigravity.md) | [Italiano](antigravity.md)

Ultima revisione: 2026-11-12.

Verifiche precedenti indicano che Antigravity può operare localmente su Windows con filesystem e PowerShell e usare Python/SQLite. Considerarle **evidenze da verificare**, non garanzie permanenti.

Antigravity può anche eseguire agenti remoti nel cloud; il registro delle modifiche del prodotto ne descrive la distribuzione ai piani a pagamento a fine 2026. Stabilire se la conversazione corrente è locale o remota prima di scegliere le risorse: un agente remoto non dispone di filesystem locale, PowerShell o Vault sincronizzato sul dispositivo se non verificato, ed è per AWA un ambiente cloud.

Adattatore preferito:

```text
python scripts/awa_cli.py ...
```

Associazioni consigliate quando verificate:

- filesystem locale e PowerShell: esecuzione locale e accesso al Vault;
- Python: calcolo deterministico e CLI/cache AWA;
- Google Drive per desktop: adattatore filesystem al Vault condiviso;
- sottoagenti: esecuzione `PARALLEL` o `ISOLATE`;
- artefatti Markdown: presentazione del brief di progetto o pacchetto di contesto.

Skill, regole e plugin possono essere globali o specifici del progetto, e le posizioni di configurazione sono cambiate tra le versioni (il registro delle modifiche indica la configurazione per progetto sotto `<project>/.gemini/config.json` nel 2026). Verificare l'inventario installato per lo spazio corrente invece di affidarsi a un percorso ricordato.

Se il Vault è fuori dallo spazio attivo e la modifica diretta è limitata, usare la CLI Python di AWA tramite esecuzione di comandi, invece di scrivere manualmente gli eventi JSON.
