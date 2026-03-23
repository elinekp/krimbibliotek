# Modelleringsregler — fase 1

Dette dokumentet beskriver praktiske katalogiseringsregler for hvordan entiteter og relasjoner skal brukes i fase 1.

Målet er å sikre konsistent registreringspraksis innenfor den valgte datamodellen.

---

## 1. Work og Expression

### Oversettelser

En oversettelse registreres som **ny Expression** av samme `Work`.

Eksempel:

- `Work`: originalverket
- `Expression`: engelsk tekst
- `Expression`: norsk oversettelse

### Lydbok

En lydbok registreres som **ny Expression** av samme `Work`.

Tekst og lydbok av samme språk regnes som **ulike Expressions**, fordi de representerer ulike realiseringer av verket.

Eksempel:

- `Expression (nor, text)`
- `Expression (nor, spoken_word)`

### Flere Expressions med samme språk og samme type

Det er tillatt å ha flere `Expressions` innenfor samme `Work` med samme:

- `language_code`
- `expression_type`

Dette kan være aktuelt ved for eksempel:

- sterkt reviderte tekster
- forkortede versjoner
- andre særskilte realiseringer

Slike tilfeller må vurderes faglig og håndteres gjennom katalogiseringspraksis, ikke gjennom teknisk unik constraint.

### Filmatisering

En filmatisering registreres som **nytt Work**.

### Grafisk adaptasjon

En grafisk adaptasjon registreres som **nytt Work**.

### Sterkt revidert tekst

Sterkt reviderte tekster må vurderes konkret.

Dette avgjøres gjennom katalogiseringsfaglig skjønn og ikke gjennom databasen alene.

---

## 2. Expression

### Språk

Språk registreres på `Expression`-nivå.

Språk kodes med verdier fra **LOC Language Vocabulary**.

Eksempler:

- `eng`
- `nor`
- `ger`
- `fre`

### Realiseringstype

Realiseringstype registreres i feltet `expression_type`.

Dette beskriver hvordan verket er realisert.

Eksempler:

- `text`
- `spoken_word`
- `moving_image`
- `still_image`

Feltet kan senere mappes til **RDA Content Type**.

### Bidrag på Expression-nivå

Roller som gjelder realiseringen av verket registreres på `Expression`.

Eksempler:

- oversetter
- innleser

---

## 3. Manifestation

### Manifestation som utgavenivå

`Manifestation` representerer den konkrete publiserte utgaven av en `Expression`.

Forskjeller i publiseringsform og utgave registreres som ulike `Manifestations`, ikke som nye `Expressions`.

### Eksempler på ulike Manifestations

Følgende registreres normalt som ulike `Manifestations` av samme `Expression`:

- hardcover
- paperback
- epub
- pdf

### Identifikatorer på Manifestation

Følgende identifikatorer registreres på `Manifestation` i fase 1:

- `isbn`
- `nb_sesamid`

`nb_sesamid` brukes som navn for Nasjonalbibliotekets identifikator i modellen.

### Forlag

Forlag hører til `Manifestation`-nivået.

Forlag modelleres via `Contribution / Agent`, ikke som eget tekstfelt i fase 1.

### Serier på utgavenivå

Forlagsserier registreres på `Manifestation`-nivå.

Narrative serier registreres derimot på `Work`-nivå.

---

## 4. Work

### Sjanger og appellfaktorer

Sjanger og appellfaktorer registreres på `Work`-nivå.

Disse beskriver fortellingen og ikke en bestemt utgave eller realisering.

### Karakterer

Karakterer registreres på `Work`-nivå.

I fase 1 registreres primært sentrale karakterer med tydelig navigasjonsverdi.

### Verkrelasjoner

Relasjoner mellom verk registreres gjennom `WorkRelationship`.

Eksempler:

- adaptasjon
- inspirert av
- videreføring av
- basert på

---

## 5. Kommentar om grensetilfeller

Databasen avgjør ikke automatisk hva som er nytt `Work` versus ny `Expression`.

Ved tvilstilfeller skal vurderingen dokumenteres og følge disse modelleringsreglene, ikke løses gjennom ad hoc-praksis.