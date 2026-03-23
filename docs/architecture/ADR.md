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
* nb_sesamid

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

# ADR-009

## Primærnøkler implementeres som UUID

### Context

Systemet vil over tid integrere data fra eksterne kilder (Wikidata, Nasjonalbiblioteket, VIAF) og kan senere bli utvidet med API-er eller distribuerte datastrømmer. I slike scenarier kan tradisjonelle auto-increment-nøkler skape problemer ved datasammenslåing eller migrasjoner.

### Decision

Alle hovedentiteter i databasen bruker **UUID som primærnøkkel**.

Dette gjelder blant annet:

- Work
- Expression
- Manifestation
- Item
- Agent
- Character
- Series
- Contribution
- SeriesMembership
- WorkRelationship

### Consequences

Fordeler

- robust ved import og sammenslåing av data
- stabil identitet uavhengig av database
- kompatibelt med Linked Data-tenkning og URI-baserte identifikatorer

Ulemper

- mindre lesbare nøkler for mennesker
- noe større indekser

Beslutningen anses som **arkitekturkritisk og stabil**.

---

# ADR-010

## Relasjonspolicy: `SET_NULL`

### Context

Under utvikling av katalogsystemet vil entiteter kunne endres eller fjernes underveis i modellering og datavask. Aggressiv kaskadesletting kan i slike situasjoner føre til utilsiktet datatap.

### Decision

Alle relasjoner i fase 1 bruker:

```
on_delete = SET_NULL
```

Dette innebærer at relasjoner blir nullstilt dersom en relatert entitet slettes.

### Consequences

Fordeler

- beskytter mot utilsiktet sletting av store datamengder
- tryggere under modellutvikling og datarensing

Ulemper

- kan etterlate null-relasjoner som må ryddes manuelt

Relasjonspolicyen kan senere justeres (f.eks. til `CASCADE`) dersom praksis tilsier det.

---

# ADR-011

## Kardinalitet mellom Work og Expression

### Context

I WEMI-modellen representerer Work den abstrakte ideen bak et verk, mens Expression representerer realiseringen av denne ideen (tekst, lyd, film osv.).

I et praktisk katalogsystem må det avklares om et Work alltid må ha minst én Expression.

### Decision

Kardinaliteten implementeres som:

```
Work → 0..n Expression
Expression → 1 Work
```

Det betyr at:

- et Work kan eksistere uten Expression
- en Expression må alltid tilhøre ett Work

### Consequences

Fordeler

- støtter konseptuelle verk som registreres før konkrete realiseringer
- samsvarer med LRM-modellen

Ulemper

- det kan oppstå Work-poster uten Expression dersom registrering ikke fullføres

Dette anses som en **grunnleggende strukturregel i modellen**.

---

# ADR-012

## Expression representerer realiseringstype (content type)

### Context

I WEMI/LRM representerer Expression hvordan et verk realiseres. Ulike realiseringer av samme verk – for eksempel tekst og lydbok – er ikke bare forskjellige utgaver, men ulike uttrykk for verket.

Systemet trenger derfor et felt som beskriver **hvilken type realisering** en Expression representerer.

### Decision

Expression får feltet:

```
expression_type
```

Dette feltet beskriver realiseringstypen, for eksempel:

```
text
spoken_word
moving_image
still_image
```
Dette feltet kan senere mappes til **RDA Content Type.**

### Consequences

Fordeler

- gjør det mulig å skille tekst, lydbok og andre realiseringer
- kompatibelt med RDA/LRM-modellen
- gjør det mulig å knytte roller som oversetter eller innleser korrekt

Ulemper

- krever et kontrollert vokabular for realiseringstyper

Beslutningen anses som **arkitekturkritisk.**

---

# ADR-013

## Språk registreres på Expression

### Context

Oversettelser representerer nye realiseringer av et verk. Språk er derfor en egenskap ved Expression, ikke Work eller Manifestation.

Systemet må derfor registrere språk på Expression-nivå.

### Decision

Expression får feltet:

```
language_code
```

Språk kodes etter **LOC Language Vocabulary**, som baserer seg på ISO-639-2 bibliografiske koder.

Eksempler:

```
eng
nor
ger
fre
```

### Consequences

Fordeler

- følger bibliotekfaglig praksis
- kompatibelt med MARC og Linked Data
- mulig å koble senere til URI-er fra id.loc.gov

Ulemper

- tretegnskoder i stedet for kortere ISO-639-1

Beslutningen anses som **arkitekturkritisk.**

---

# ADR-014

## Tekst og lydbok er ulike Expressions

### Context

Et verk kan realiseres både som tekst og som lydbok. Disse representerer ulike realiseringer av verket og kan ha ulike bidragsytere (for eksempel innleser).

Det må derfor avklares om dette skal modelleres som ulike Expressions eller kun som ulike Manifestations.

### Decision

Tekst og lydbok modelleres som **ulike Expressions.**

Eksempel:

```
Work
 ├ Expression (eng, text)
 └ Expression (eng, spoken_word)
```

### Consequences

Fordeler

- korrekt modellering av realiseringstype
- gjør det mulig å knytte innleser til riktig nivå
- kompatibelt med RDA Content Type

Ulemper

- flere Expressions per Work

Beslutningen anses som **strukturkritisk.**

---

# ADR-015

## Manifestation representerer bibliografisk identitet på utgavenivå

### Context

Det måtte avklares hva Manifestation konkret representerer i modellen, og hvilke typer forskjeller som skal føre til ny Manifestation.

I prosjektet er det viktig å skille tydelig mellom:

- Expression som realisering av et verk
- Manifestation som den konkrete publiserte utgaven

Det måtte også avklares hvor identifikatorer som ISBN og NB-identifikator skal ligge, og hvordan forlag skal modelleres.

### Decision

Manifestation representerer **bibliografisk identitet på utgavenivå**.

Dette innebærer at følgende modelleres som ulike Manifestations av samme Expression:

- hardcover
- paperback
- epub
- pdf

Følgende felter plasseres på Manifestation-nivå i fase 1:

- `isbn`
- `nb_sesamid`
- `publication_year`

Forlag hører til `Manifestation`-nivået og modelleres fra start via `Contribution / Agent`.

Carrier/media type forstås prinsipielt som et Manifestation-attributt, men konkret felt for dette utsettes til senere fase.

### Consequences

Fordeler

- tydelig skille mellom Expression og Manifestation
- korrekt modellering av konkrete utgaver
- ISBN og NB-identifikator plasseres på riktig nivå
- konsekvent rollemodell ved at forlag håndteres via Contribution / Agent

Ulemper

- høyere registreringsfriksjon i fase 1 enn ved rene tekstfelt
- enkelte praktiske utgivelsesattributter må komme senere

Beslutningen anses som arkitekturkritisk og stabil.

---

# ADR-016

## Item holdes på rent eksemplarnivå

### Context

Prosjektet måtte avklare hva `Item` konkret skal representere i modellen, og hvilke typer data som hører hjemme der.

Det var særlig behov for å skille tydelig mellom:

- bibliografiske data som beskriver en publisert utgave
- eksemplarspesifikke data som gjelder ett fysisk objekt i samlingen

Det måtte også avklares hvordan proveniens skulle håndteres i fase 1, og om et felt som `is_first_edition` skulle brukes på `Item`.

### Decision

`Item` holdes på rent eksemplarnivå.

Dette innebærer at `Item` brukes til data som gjelder det konkrete fysiske eksemplaret, for eksempel:

- `shelf_location`
- `provenance_notes`
- andre lokale eksemplarnotater

Bibliografiske utgavedata skal ikke ligge på `Item`.

Eksempler på data som ikke hører til `Item`:

- ISBN
- `nb_sesamid`
- utgivelsesår
- utgaveinformasjon

Slike data hører til `Manifestation`.

I fase 1 håndteres proveniens normalt gjennom:

- `provenance_notes`

Samtidig kan `Contribution` brukes på `Item` når proveniens eller eierskap er viktig nok til å struktureres.

Feltet `is_first_edition` brukes ikke på `Item`.

Prosjektet innfører heller ikke et eget boolsk felt for dette på `Manifestation`, siden vanlig utgaveinformasjon anses som tilstrekkelig.

### Consequences

Fordeler

- tydelig skille mellom bibliografisk nivå og eksemplarnivå
- mindre risiko for dobbeltføring og inkonsistens
- enklere fase-1-modell
- mulig å utvide senere med mer strukturert proveniens uten å bryte grunnmodellen

Ulemper

- mindre strukturert proveniens i første fase
- enkelte copy-specific bibliografiske særtrekk må eventuelt håndteres senere

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
4. Item
5. Series
6. Agent
7. Contribution
8. Character
9. Genre / AppealFactor


