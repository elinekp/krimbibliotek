# Data Dictionary — Krimbiblioteket

Dette dokumentet er et teknisk oppslagsverk for tabeller og felter i datamodellen for Krimbiblioteket.

Formålet er å gi en kort, presis og konsistent beskrivelse av:
- hvilke tabeller som finnes
- hva tabellene representerer
- hvilke felter som inngår i fase 1
- hva feltene betyr
- hvordan nøkler og referanser brukes

Dette dokumentet er ikke hovedkilde for:
- arkitekturbeslutninger
- modellinvarianter
- praktiske modelleringsregler
- designresonnement
- prosjektstatus

Ved konflikt gjelder disse dokumentene foran:
1. `ADR.md`
2. `model_invariants.md`
3. `modelling_rules_phase1.md`

Dette dokumentet skal primært beskrive **hva som finnes i modellen**, ikke begrunne hvorfor.


---

## 1. Hvordan dokumentasjonen er strukturert

Hver tabell beskrives med:
- kort formål
- nivå i modellen
- fase-1-felter
- korte feltdefinisjoner
- nøkler og referanser
- eventuelle korte merknader

Følgende begreper brukes konsekvent:
- **PK** = primærnøkkel
- **FK** = fremmednøkkel
- **obligatorisk** = feltet skal ha verdi i fase 1
- **valgfri** = feltet kan være tomt i fase 1
- **kontrollert kode** = verdi fra lokalt, stabilt vokabular


---

## 2. Work

### Formål
Representerer verkets abstrakte/intellektuelle identitet.

### Nivå
WEMI: Work

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for verket |
| `title_preferred` | string | ja | Foretrukket tittel for verket |
| `wikidata_id` | string | nei | Ekstern identifikator til Wikidata når kjent |

### Nøkler og referanser
- PK: `id`

### Merknad
`Work` er overordnet nivå for blant annet sjanger, appellfaktorer, karakterer og verkrelasjoner.

### Merknad
`title_preferred` er foretrukket navneform i fase 1, ikke full nomen-struktur.

---

## 3. Expression

### Formål
Representerer en realisering av et verk, for eksempel språkversjon eller realiseringstype.

### Nivå
WEMI: Expression

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for expression |
| `work` | UUID / FK | ja | Referanse til tilhørende `Work` |
| `language_code` | string | ja | Språkkode for expression |
| `expression_type` | string / kontrollert kode | ja | Type realisering, for eksempel tekst eller lydbok |

### Nøkler og referanser
- PK: `id`
- FK: `work` → `Work.id`

### Merknad
Flere `Expressions` kan tilhøre samme `Work`.


---

## 4. Manifestation

### Formål
Representerer den konkrete publiserte utgaven.

### Nivå
WEMI: Manifestation

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for manifestation |
| `isbn` | string | nei | ISBN for utgaven når kjent |
| `publication_year` | integer | nei | Utgivelsesår |
| `edition_statement` | string | nei | Utgaveangivelse slik den vises eller registreres |
| `nb_sesamid` | string | nei | Nasjonalbibliotekets SESAM-identifikator når kjent |

### Nøkler og referanser
- PK: `id`

### Merknad
Kobling til `Expression` skjer via `ExpressionManifestation`, ikke via direkte felt på `Manifestation`.


---

## 5. Item

### Formål
Representerer det individuelle eksemplaret.

### Nivå
WEMI: Item

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for item |
| `manifestation` | UUID / FK | ja | Referanse til tilhørende `Manifestation` |
| `shelf_location` | string | nei | Hylleplassering eller lokal plassering |
| `provenance_notes` | text | nei | Fritekstnotat om proveniens eller eksemplarhistorikk |

### Nøkler og referanser
- PK: `id`
- FK: `manifestation` → `Manifestation.id`

### Merknad
`Item` brukes bare for copy-specific informasjon i fase 1.


---

## 6. ExpressionManifestation

### Formål
Koblingstabell mellom `Expression` og `Manifestation`.

### Nivå
Kobling mellom WEMI-nivåene Expression og Manifestation

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for koblingen |
| `expression` | UUID / FK | ja | Referanse til `Expression` |
| `manifestation` | UUID / FK | ja | Referanse til `Manifestation` |
| `is_primary` | boolean | nei | Marker om dette er primærkoblingen for manifestasjonen |

### Nøkler og referanser
- PK: `id`
- FK: `expression` → `Expression.id`
- FK: `manifestation` → `Manifestation.id`
- Unik kombinasjon: (`expression`, `manifestation`)

### Merknad
En `Manifestation` kan ha maks én primærkobling.


---

## 7. Series

### Formål
Representerer en serie som egen entitet.

### Nivå
Støtteentitet i modellen

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for serien |
| `title` | string | ja | Foretrukket tittel/navn på serien |
| `series_type` | string / kontrollert kode | ja | Serietype i fase 1 |

### Nøkler og referanser
- PK: `id`

### Merknad
I fase 1 brukes serietyper for narrative serier og forlagsserier.


---

## 8. SeriesMembership

### Formål
Kobling mellom `Series` og enten `Work` eller `Manifestation`.

### Nivå
Koblingstabell

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for medlemskapet |
| `series` | UUID / FK | ja | Referanse til `Series` |
| `work` | UUID / FK | nei | Referanse til `Work` når medlemskapet gjelder verk |
| `manifestation` | UUID / FK | nei | Referanse til `Manifestation` når medlemskapet gjelder utgave |
| `part_number` | integer | nei | Strukturelt serienummer når dette kan uttrykkes numerisk |
| `part_display` | string | nei | Visningsform for del-/nummerinformasjon |

### Nøkler og referanser
- PK: `id`
- FK: `series` → `Series.id`
- FK: `work` → `Work.id`
- FK: `manifestation` → `Manifestation.id`

### Merknad
Nøyaktig én av `work` eller `manifestation` skal være satt.


---

## 9. Character

### Formål
Representerer en fiktiv karakter som egen entitet.

### Nivå
Work-relatert støtteentitet

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for karakter |
| `name` | string | ja | Foretrukket navn på karakteren |

### Nøkler og referanser
- PK: `id`

### Merknad
`name` er foretrukket navneform i fase 1, ikke full nomen-struktur.

---

## 10. WorkCharacter

### Formål
Koblingstabell mellom `Work` og `Character`.

### Nivå
Koblingstabell

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for koblingen |
| `work` | UUID / FK | ja | Referanse til `Work` |
| `character` | UUID / FK | ja | Referanse til `Character` |

### Nøkler og referanser
- PK: `id`
- FK: `work` → `Work.id`
- FK: `character` → `Character.id`
- Unik kombinasjon: (`work`, `character`)


---

## 11. WorkRelationship

### Formål
Representerer en retningsbestemt relasjon mellom to verk.

### Nivå
Work-nivå

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for relasjonen |
| `source_work` | UUID / FK | ja | Utgående verk i relasjonen |
| `target_work` | UUID / FK | ja | Inngående verk i relasjonen |
| `relation_type` | string / kontrollert kode | ja | Type verkrelasjon |

### Nøkler og referanser
- PK: `id`
- FK: `source_work` → `Work.id`
- FK: `target_work` → `Work.id`

### Merknad
Selvrelasjon er ikke tillatt.


---

## 12. Agent

### Formål
Representerer en aktør, enten person eller kollektiv agent.

### Nivå
Støtteentitet

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for agent |
| `name` | string | ja | Foretrukket navn på agenten i fase 1 |
| `agent_type` | string / kontrollert kode | ja | Type agent. I fase 1 brukes `person` eller `collective_agent` |
| `wikidata_id` | string | nei | Ekstern identifikator til Wikidata når kjent |

### Nøkler og referanser
- PK: `id`

### Merknad
- `name` er foretrukket navneform i fase 1, ikke full nomen-struktur
- `viaf_id` inngår ikke som eget fase-1-felt
- rikere struktur for variantnavn, pseudonymer og andre appellasjoner utsettes til senere modellering


---

## 13. Role

### Formål
Kontrollert vokabular for roller brukt i `Contribution`.

### Nivå
Støtteentitet / kontrollert vokabular

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `code` | string | ja | Stabil lokal kode for rollen |
| `label` | string | ja | Leserrettet etikett for rollen |

### Nøkler og referanser
- PK: `code`


---

## 14. Contribution

### Formål
Representerer en rollebasert kobling mellom `Agent` og én målentitet i modellen.

### Nivå
Koblingstabell

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for bidraget |
| `agent` | UUID / FK | ja | Referanse til `Agent` |
| `role` | string / FK | ja | Referanse til `Role` |
| `work` | UUID / FK | nei | Målfelt når bidraget gjelder `Work` |
| `expression` | UUID / FK | nei | Målfelt når bidraget gjelder `Expression` |
| `manifestation` | UUID / FK | nei | Målfelt når bidraget gjelder `Manifestation` |
| `item` | UUID / FK | nei | Målfelt når bidraget gjelder `Item` |

### Nøkler og referanser
- PK: `id`
- FK: `agent` → `Agent.id`
- FK: `role` → `Role.code`
- FK: `work` → `Work.id`
- FK: `expression` → `Expression.id`
- FK: `manifestation` → `Manifestation.id`
- FK: `item` → `Item.id`

### Merknad
Nøyaktig én av `work`, `expression`, `manifestation` eller `item` skal være satt.


---

## 15. Genre

### Formål
Kontrollert sjangervokabular på Work-nivå.

### Nivå
Work-relatert kontrollert vokabular

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `code` | string | ja | Stabil lokal kode for sjangeren |
| `label` | string | ja | Foretrukket etikett for sjangeren |
| `parent_genre` | string / FK | nei | Referanse til overordnet sjanger |

### Nøkler og referanser
- PK: `code`
- FK: `parent_genre` → `Genre.code`

### Merknad
Hierarki er eksplisitt støttet i fase 1.


---

## 16. WorkGenre

### Formål
Koblingstabell mellom `Work` og `Genre`.

### Nivå
Koblingstabell

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for koblingen |
| `work` | UUID / FK | ja | Referanse til `Work` |
| `genre` | string / FK | ja | Referanse til `Genre` |

### Nøkler og referanser
- PK: `id`
- FK: `work` → `Work.id`
- FK: `genre` → `Genre.code`
- Unik kombinasjon: (`work`, `genre`)


---

## 17. AppealFactor

### Formål
Kontrollert vokabular for appellfaktorer på Work-nivå.

### Nivå
Work-relatert kontrollert vokabular

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `code` | string | ja | Stabil lokal kode for appellfaktoren |
| `label` | string | ja | Foretrukket etikett for appellfaktoren |
| `parent_appeal_factor` | string / FK | nei | Referanse til overordnet appellfaktor |
| `definition` | text | nei | Definisjon av appellfaktoren |
| `scope_note` | text | nei | Omfangsnote eller brukskommentar |

### Nøkler og referanser
- PK: `code`
- FK: `parent_appeal_factor` → `AppealFactor.code`

### Merknad
Synonymer inngår ikke som operativ fase-1-struktur.


---

## 18. WorkAppealFactor

### Formål
Koblingstabell mellom `Work` og `AppealFactor`.

### Nivå
Koblingstabell

### Fase-1-felter

| Felt | Type | Obligatorisk | Beskrivelse |
|---|---|---:|---|
| `id` | UUID | ja | Primærnøkkel for koblingen |
| `work` | UUID / FK | ja | Referanse til `Work` |
| `appeal_factor` | string / FK | ja | Referanse til `AppealFactor` |

### Nøkler og referanser
- PK: `id`
- FK: `work` → `Work.id`
- FK: `appeal_factor` → `AppealFactor.code`
- Unik kombinasjon: (`work`, `appeal_factor`)


---

## 19. Dokumentets videre bruk

Dette dokumentet bør oppdateres når:
- nye tabeller fryses for fase 1
- fase-1-felter endres
- navn på felter endres
- kontrollert vokabular får nye obligatoriske felt

Dette dokumentet bør ikke brukes til å:
- diskutere alternative modeller
- begrunne arkitekturvalg i lengden
- samle åpne spørsmål
- beskrive roadmap eller neste steg