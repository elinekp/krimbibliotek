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

---

## 6. Item

### Item som eksemplarnivå

`Item` representerer det individuelle fysiske eksemplaret i samlingen.

I fase 1 brukes `Item` kun til data som gjelder det konkrete eksemplaret, ikke bibliografiske data om utgaven.

Eksempler på data som hører til `Item`:

- `shelf_location`
- `provenance_notes`
- lokale eksemplarnotater

Eksempler på data som **ikke** hører til `Item`:

- ISBN
- `nb_sesamid`
- utgivelsesår
- annen bibliografisk utgaveinformasjon

Slike data hører til `Manifestation`.

### Proveniens

Proveniens brukes om et eksemplars eier- og historieforløp.

Dette kan for eksempel omfatte:

- tidligere eiere
- gaveopplysninger
- samlingstilknytning
- ex libris
- dedikasjoner
- stempler eller andre spor på eksemplaret

I fase 1 registreres proveniens normalt i:

- `provenance_notes`

### Når Contribution kan brukes på Item

`Contribution` kan også brukes på `Item` når proveniens eller eierskap er viktig nok til å struktureres.

Dette kan være aktuelt når:

- tidligere eier er kjent og har tydelig verdi for gjenfinning
- giver bør registreres som navngitt aktør
- samlingshistorikk bør kunne kobles strukturert til agent

I enkle tilfeller er `provenance_notes` tilstrekkelig.

I fase 1 er det akseptabelt å bruke fritekst som hovedpraksis.

### Førsteutgave

`is_first_edition` brukes ikke på `Item`.

Om et eksemplar tilhører første utgave, fremgår dette gjennom vanlig utgaveinformasjon på `Manifestation`-nivå, ikke som eget boolsk felt på `Item`.

Eventuelle copy-specific bibliografiske særtrekk vurderes senere og modelleres ikke særskilt i fase 1.

## 7. Series og SeriesMembership i fase 1

### Når Series skal brukes

`Series` brukes når en serie skal modelleres som en egen, gjenbrukbar entitet i databasen.

I fase 1 brukes `Series` for minst to serietyper:

- narrative serier
- forlagsserier

`Series` skal ikke erstattes av fritekstfelt når formålet er å uttrykke faktisk serietilknytning i modellen.

### Hvordan series_type skal brukes

Hver `Series`-post skal ha en obligatorisk verdi i `series_type`.

I fase 1 er vokabularet lukket og består bare av:

- `narrative`
- `publisher_series`

Bruk:

- `narrative` når serien uttrykker fortellingsmessig eller verkrelatert tilknytning
- `publisher_series` når serien uttrykker utgave- eller publiseringsrelatert tilknytning på manifestasjonsnivå

Andre serietyper utsettes til senere fase.

`character_series` brukes ikke som egen `series_type` i fase 1.

### Valg av nivå for serietilknytning

Serietilknytning skal registreres på det nivået den faktisk hører hjemme.

Bruk:

- `Work` når serien er narrativ og gjelder verket som sådan
- `Manifestation` når serien er knyttet til en bestemt utgave eller publiseringsform

Hovedregel:

- narrative serier registreres via `SeriesMembership` mot `Work`
- forlagsserier registreres via `SeriesMembership` mot `Manifestation`

Samme bok kan derfor ha:

- en narrativ serietilknytning på `Work`
- en forlagsserietilknytning på `Manifestation`

Dette skal registreres som to ulike `SeriesMembership`-rader.

### Hvordan SeriesMembership skal brukes

`SeriesMembership` representerer én konkret kobling mellom en serie og dens mål.

Én rad i `SeriesMembership` skal peke til:

- enten `Work`
- eller `Manifestation`

Aldri begge samtidig.

Det skal heller ikke opprettes rader uten mål.

Samme serie skal ikke registreres flere ganger mot samme mål.

Det betyr:

- maks én rad per (`series`, `work`)
- maks én rad per (`series`, `manifestation`)

### Nummerering i SeriesMembership

Fase 1 skal støtte enkel og praktisk nummerering uten å kreve full normalisering.

Feltene brukes slik:

- `part_number` brukes når nummereringen kan uttrykkes som en enkel sorterbar verdi
- `part_display` brukes når nummereringen bør vises i en bestemt form, eller når den ikke passer rent i `part_number`

Begge felter er valgfrie.

Modellen skal derfor tåle:

- serietilknytning uten nummer
- nummerering bare i `part_display`
- ulik verdi for sortering og visning

Eksempler:

- `part_number = 1`, `part_display = Del 1`
- `part_number = 2`, `part_display = Bok 2`
- `part_number = null`, `part_display = Del II`
- `part_number = null`, `part_display = null`

### Hva som ikke gjøres i fase 1

Fase 1 inkluderer ikke:

- `context_note` på `SeriesMembership`
- seriehierarki som `parent_series`
- variantnavn på `Series`
- egne serietyper utover `narrative` og `publisher_series`

Hvis et serietilfelle ikke passer rent i fase-1-modellen, skal det vurderes som et modelleringsspørsmål, ikke løses ved å utvide databasen ad hoc.