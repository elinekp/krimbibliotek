# Model Invariants — Krimbiblioteket

Dette dokumentet beskriver grunnleggende regler i datamodellen som ikke skal brytes av applikasjonslogikk, migrasjoner eller fremtidige utvidelser.

Formålet er å beskytte modellens struktur over tid.

Disse reglene er mer stabile enn vanlig dokumentasjon og bør bare endres dersom arkitekturen endres eksplisitt.

---

# 1. WEMI-strukturen er grunnlaget for systemet

Datamodellen følger strukturen:

`Work → Expression → Manifestation → Item`

Betydning:

- `Work` representerer den abstrakte ideen bak et verk
- `Expression` representerer realiseringen (tekst, lyd, film osv.)
- `Manifestation` representerer den konkrete publiserte utgaven
- `Item` representerer det individuelle eksemplaret i samlingen

Ingen entiteter skal hoppe over nivåer i denne strukturen.

Ikke tillatt:

- `Work → Manifestation`
- `Work → Item`

Tillatt:

- `Work → Expression → Manifestation → Item`

---

# 2. Work kan eksistere uten Expression

Kardinaliteten er:

`Work → 0..n Expression`  
`Expression → 1 Work`

Et `Work` kan eksistere uten `Expression`, men en `Expression` kan ikke eksistere uten et `Work`.

---

# 3. Manifestation må alltid tilhøre en Expression

Kardinaliteten er:

`Expression → 0..n Manifestation`  
`Manifestation → 1 Expression`

En `Manifestation` kan ikke eksistere uten en `Expression`.

---

# 4. Item må alltid tilhøre en Manifestation

Kardinaliteten er:

`Manifestation → 0..n Item`  
`Item → 1 Manifestation`

Et `Item` kan ikke eksistere uten en `Manifestation`.

---

# 5. Alle hovedentiteter bruker UUID som primærnøkkel

Dette gjelder blant annet:

- `Work`
- `Expression`
- `Manifestation`
- `Item`
- `Agent`
- `Character`
- `Series`
- `Contribution`
- `WorkRelationship`

Formålet er å sikre stabile identifikatorer uavhengig av databaseinstans eller datamigrasjoner.

---

# 6. Relasjonspolicy i fase 1

Alle relasjoner bruker:

`on_delete = SET_NULL`

Dette beskytter mot utilsiktet kaskadesletting under utvikling og datavask.

Relasjonspolicyen kan revideres senere dersom praksis tilsier det.

---

# 7. Sjanger og appellfaktorer beskriver Work

Sjanger og appellfaktorer modelleres på `Work`-nivå.

Dette skyldes at disse egenskapene beskriver fortellingen og ikke en bestemt utgave.

---

# 8. Karakterer knyttes til Work

Karakterer kobles til `Work`.

Dette gjør det mulig å:

- navigere biblioteket etter karakterer
- koble karakterer på tvers av forfattere
- modellere pastisjer og videreføringer

---

# 9. Narrative serier knyttes til Work

Serier som representerer fortellingsuniverser knyttes til `Work`.

Eksempler:

- Sherlock Holmes
- Hercule Poirot
- Harry Hole

Forlagsserier knyttes derimot til `Manifestation`.

---

# 10. Relasjoner mellom verk modelleres eksplisitt

Relasjoner mellom verk modelleres gjennom entiteten `WorkRelationship`.

En enkel selvrefererende M2M brukes ikke, fordi relasjonstype må lagres.

---

# 11. Grensen mellom Work og Expression styres av katalogiseringsregler

Databasen implementerer strukturen, men avgjør ikke automatisk hva som er:

- nytt `Work`
- nytt `Expression`

Dette defineres i dokumentet `Lokale modelleringsregler for fase 1`.

---

# 12. Språk registreres på Expression

Språk registreres på `Expression`-nivå fordi oversettelser representerer nye realiseringer av et verk.

Språk kodes etter `LOC Language Vocabulary`.

Eksempler:

- `eng`
- `nor`
- `ger`
- `fre`

---

# 13. Realiseringstype registreres på Expression

`Expression` inneholder feltet `expression_type`.

Dette beskriver realiseringstypen, for eksempel:

- `text`
- `spoken_word`
- `moving_image`
- `still_image`

Feltet kan senere mappes til `RDA Content Type`.

---

# 14. Tekst og lydbok er ulike Expressions

Tekst og lydbok modelleres som separate `Expressions`, fordi de representerer ulike realiseringer av et verk.

Eksempel:

- `Expression (nor, text)`
- `Expression (nor, spoken_word)`

---

# 15. Flere Expressions med samme språk og samme realiseringstype er tillatt

Datamodellen tillater flere `Expressions` innenfor samme `Work` med samme:

- `language_code`
- `expression_type`

Dette håndteres gjennom lokale modelleringsregler, ikke ved streng unik constraint.

---

# 16. Manifestation representerer bibliografisk identitet på utgavenivå

`Manifestation` beskriver den konkrete publiserte utgaven av en `Expression`.

Forskjeller som følgende modelleres som ulike `Manifestations` av samme `Expression`:

- hardcover
- paperback
- epub
- pdf

---

# 17. Identifikatorer på Manifestation i fase 1

Følgende sentrale identifikatorer lagres på `Manifestation` i fase 1:

- `isbn`
- `nb_sesamid`

Mer generell identifikatorstruktur er utsatt.

---

# 18. Forlag hører til Manifestation-nivået

Forlag modelleres på `Manifestation`-nivå og representeres fra start via `Contribution / Agent`.

Ikke som eget tekstfelt i fase 1.

---

# 19. Modellen er designet for å tåle følgende bibliografiske situasjoner

Datamodellen skal kunne håndtere:

- oversettelser
- lydbøker
- filmatiseringer
- grafiske adaptasjoner
- samlingsverk
- antologier
- omnibusutgaver
- verk i flere serier
- karakterer på tvers av forfattere

---

## Bruk av dette dokumentet

Dette dokumentet fungerer som en referanse for utvikling og migrasjoner.

Før større modellendringer bør følgende spørsmål stilles:

> Bryter denne endringen en modell-invariant?

Hvis svaret er ja, må beslutningen vurderes som en arkitekturendring.