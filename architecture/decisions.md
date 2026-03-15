# Architecture Decision Log (ADR)

Dette dokumentet registrerer viktige arkitekturvalg i prosjektet **Krimbiblioteket**.
Hensikten er å dokumentere *hva som ble besluttet og hvorfor*, slik at beslutningene kan forstås senere.

Formatet følger en enkel ADR-struktur:

* Context
* Decision
* Consequences

---

# ADR-001

## WEMI som kjernemodell

### Context

Prosjektet ønsker å følge etablerte bibliotekfaglige modeller og støtte avansert bibliografisk struktur. En enkel boktabell ville ikke støtte:

* oversettelser
* adaptasjoner
* samlingsverk
* flere utgaver
* ulike medier

### Decision

Systemet implementerer LRM-inspirert struktur:

```
Work → Expression → Manifestation → Item
```

Dette er prosjektets **fundamentale datamodell**.

### Consequences

Fordeler:

* korrekt bibliografisk modell
* støtte for oversettelser og adaptasjoner
* fleksibilitet for flere medier

Ulemper:

* mer kompleks modell
* flere relasjoner i databasen

Beslutningen anses som **arkitekturkritisk og stabil**.

---

# ADR-002

## Expression–Manifestation modellert som M2M

### Context

Mange manifestasjoner inneholder flere verk eller uttrykk.

Eksempler:

* omnibus
* samlingsverk
* antologier

En enkel 1-til-mange-relasjon ville ikke støtte dette.

### Decision

Expression og Manifestation kobles via en mellomtabell:

```
ExpressionManifestation
```

Tabellen inneholder foreløpig:

* position
* context_note

### Consequences

Fordeler:

* støtter samlingsverk
* støtter omnibus
* fleksibel modell

Ulemper:

* mer kompleks enn enkel FK

---

# ADR-003

## Generisk bidragssystem (Agent / Role / Contribution)

### Context

Bibliografiske relasjoner mellom personer og verk kan være mange:

* forfatter
* oversetter
* illustratør
* innleser
* redaktør
* forlag

En modell med separate felter for hver rolle ville blitt lite fleksibel.

### Decision

Bidrag modelleres gjennom tre tabeller:

```
Agent
Role
Contribution
```

Contribution kan kobles til:

* Work
* Expression
* Manifestation
* Item

### Consequences

Fordeler:

* fleksibel rollemodell
* kompatibel med RDA/Relator codes
* enkel utvidelse

Ulemper:

* mer kompleks spørring

---

# ADR-004

## Serie kan knyttes til Work eller Manifestation

### Context

Serier kan representere ulike konsepter:

Narrative serier:

* Sherlock Holmes
* Hercule Poirot

Forlagsserier:

* Penguin Crime Classics
* Gyldendal Krim

Disse hører til ulike nivåer i modellen.

### Decision

`SeriesMembership` kan kobles til:

* Work
* Manifestation

### Consequences

Fordeler:

* korrekt modellering av forlagsserier
* korrekt modellering av narrativ serie

Ulemper:

* litt mer kompleks datamodell

---

# ADR-005

## Karakterer som egne entiteter

### Context

Kriminallitteratur er ofte sterkt karakterdrevet.

Navigasjon basert på karakterer er en viktig formidlingsmulighet.

### Decision

Karakterer modelleres som egen entitet:

```
Character
```

Relasjon:

```
Work ↔ Character
```

### Consequences

Fordeler:

* mulig å navigere etter karakter
* mulig å koble karakterer på tvers av forfattere

Ulemper:

* karaktermodell kan bli mer kompleks senere

---

# ADR-006

## Kun sentrale identifikatorer i fase 1

### Context

Det finnes mange eksterne identifikatorer:

* Wikidata
* VIAF
* NB
* ISBN
* ISNI
* ORCID

En generell modell for identifikatorer ville gjøre systemet mer komplekst.

### Decision

I fase 1 brukes **egne felter for de viktigste identifikatorene**.

Eksempler:

* wikidata_id
* viaf_id
* isbn
* nb_id

### Consequences

Fordeler:

* enklere implementasjon
* enklere spørringer

Ulemper:

* mindre fleksibelt enn generell identifikatorstruktur

Generell modell kan legges til senere.

---

# ADR-007

## Workflow-felter utsatt

### Context

Felter som:

* is_locked
* is_manually_verified
* metadata_provenance

tilhører arbeidsflyt og staging.

### Decision

Disse feltene implementeres **ikke i fase 1**.

### Consequences

Fordeler:

* enklere modell
* mindre kompleksitet i første versjon

Ulemper:

* må legges til senere når staging bygges

---

# ADR-008

## Lokale modelleringsregler etableres

### Context

Mange bibliografiske beslutninger kan ikke løses kun gjennom databasedesign.

Eksempler:

* når noe er nytt Work
* når noe er nytt Expression
* når noe er ny Manifestation

### Decision

Prosjektet etablerer et internt dokument:

```
Lokale modelleringsregler for fase 1
```

### Consequences

Fordeler:

* konsistent registreringspraksis
* lettere å forstå datamodellen senere

---

# Fremtidige ADR-temaer

Følgende temaer vil sannsynligvis kreve nye ADR-beslutninger senere:

* ekstern identifikatorstruktur
* tittelmodell
* navnevarianter
* Expression-utvidelser
* staging-system
* metadata-proveniens
* anbefalingssystem

---

## En liten anbefaling til slutt

Neste naturlige steg i arbeidet vårt vil være:

**systematisk gjennomgang av hver tabell**, i denne rekkefølgen:

1. Work
2. Expression
3. Manifestation
4. Series
5. Agent
6. Contribution
7. Character
8. Genre / AppealFactor


