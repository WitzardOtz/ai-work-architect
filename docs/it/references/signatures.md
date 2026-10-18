# Caratteristiche del task (Task Signature)

[English](../../../references/signatures.md) | [Italiano](signatures.md)

La Signature descrive il problema, mai la soluzione proposta. Chiavi e valori tecnici restano invariati tra le lingue.

## Dimensioni principali

- `operation`: acquire / transform / analyse / produce / validate — acquisire, trasformare, analizzare, produrre, verificare.
- `input_regime`: text / structured_data / code / image / audio / mixed — tipo di input.
- `grounding_regime`: self_contained / project_corpus / external / proprietary / live — base informativa.
- `inference_depth`: minimal / compositional / multi_step / hypothesis_level — profondità del ragionamento.
- `context_scale`: local / bounded / large / corpus_scale — scala del contesto.
- `verifiability_regime`: deterministic / empirical / source_grounded / inferential / aesthetic — modalità di verifica.
- `error_consequence`: low / medium / high / critical — conseguenze dell'errore.

## Dimensioni estese

Usarle solo quando modificano la scelta delle risorse:

- aggiornamento delle informazioni;
- incertezza conoscitiva;
- accoppiamento del contesto;
- modalità dell'output;
- contratto dell'output;
- interazione con lo stato.

La maggior parte dei valori va dedotta, non chiesta all'utente.
