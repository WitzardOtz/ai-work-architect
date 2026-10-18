# Profilo dell'ambiente Antigravity

[English](../../../environments/antigravity.md) | [Italiano](antigravity.md)

Verifiche precedenti indicano che Antigravity può operare localmente su Windows con filesystem e PowerShell e usare Python/SQLite. Considerarle **evidenze da verificare**, non garanzie permanenti.

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

Le skill possono essere globali o specifiche dello spazio di lavoro; verificare l'inventario installato per lo spazio corrente.

Se il Vault è fuori dallo spazio attivo e la modifica diretta è limitata, usare la CLI Python di AWA tramite esecuzione di comandi, invece di scrivere manualmente gli eventi JSON.
