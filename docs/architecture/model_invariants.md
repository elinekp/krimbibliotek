Dette dokumentet beskriver **grunnleggende regler i datamodellen** som ikke skal brytes av applikasjonslogikk, migrasjoner eller fremtidige utvidelser.

Formålet er å beskytte modellens struktur over tid.

Disse reglene er mer stabile enn vanlig dokumentasjon og bør bare endres dersom arkitekturen endres eksplisitt.

# 1. WEMI-strukturen er grunnlaget for systemet

Datamodellen følger strukturen:

```
Work → Expression → Manifestation → Item
```

Betydning:

- **Work** representerer den abstrakte ideen bak et verk
- **Expression** representerer realiseringen (tekst, lyd, film osv.)
- **Manifestation** representerer den konkrete publiserte utgaven
- **Item** representerer det individuelle eksemplaret i samlingen

Ingen entiteter skal hoppe over nivåer i denne strukturen.

Eksempler:

Ikke tillatt:

```
Work → Manifestation
Work → Item
```

Tillatt:

```
Work → Expression → Manifestation → Item
```

---

# 2. Expression må alltid tilhøre ett Work

Regel:

```
Expression → 1 Work
```

En Expression kan ikke eksistere uten et Work.

Derimot kan et Work eksistere uten Expression.

```
Work → 0..n Expression
```

Dette gjør det mulig å registrere et verk før konkrete uttrykk registreres.

---

# 3. Manifestation må alltid tilhøre en Expression

Regel:

```
Manifestation → Expression
```

En manifestasjon kan ikke eksistere uten en Expression.

Dette sikrer at alle publiserte utgaver kan spores tilbake til den realiseringen av verket de representerer.

---

# 4. Item må alltid tilhøre en Manifestation

Regel:

```
Item → Manifestation
```

Item representerer et fysisk eller digitalt eksemplar i samlingen.

Et Item kan derfor ikke eksistere uten en Manifestation.

---

# 5. Alle hovedentiteter bruker UUID som primærnøkkel

Dette gjelder blant annet:

- Work
- Expression
- Manifestation
- Item
- Agent
- Character
- Series
- Contribution
- WorkRelationship

Formålet er å sikre stabile identifikatorer uavhengig av databaseinstans eller datamigrasjoner.

---

# 6. Relasjonspolicy i fase 1

Alle relasjoner bruker:

```
on_delete = SET_NULL
```

Dette beskytter mot utilsiktet kaskadesletting under utvikling og datavask.

Relasjonspolicyen kan revideres senere dersom praksis tilsier det.

---

# 7. Sjanger og appellfaktorer beskriver Work

Sjanger og appellfaktorer modelleres på **Work-nivå**.

Dette skyldes at disse egenskapene beskriver fortellingen og ikke en bestemt utgave.

Eksempler:

- oversettelser
- lydbøker
- nye utgaver

skal normalt arve samme sjangerstruktur.

---

# 8. Karakterer knyttes til Work

Karakterer kobles til Work.

Dette gjør det mulig å:

- navigere biblioteket etter karakterer
- koble karakterer på tvers av forfattere
- modellere pastisjer og videreføringer

---

# 9. Narrative serier knyttes til Work

Serier som representerer **fortellingsuniverser** knyttes til Work.

Eksempler:

- Sherlock Holmes
- Hercule Poirot
- Harry Hole

Forlagsserier knyttes derimot til Manifestation.

---

# 10. Relasjoner mellom verk modelleres eksplisitt

Relasjoner mellom verk modelleres gjennom entiteten:

```
WorkRelationship
```

Dette gjør det mulig å beskrive relasjonstyper som:

- adaptasjon
- inspirert av
- videreføring av
- basert på

En enkel selvrefererende M2M brukes ikke, fordi relasjonstype må lagres.

---

# 11. Grensen mellom Work og Expression styres av katalogiseringsregler

Databasen implementerer strukturen, men avgjør ikke automatisk hva som er:

- nytt Work
- nytt Expression

Dette defineres i dokumentet:

```
Lokale modelleringsregler for fase 1
```

---

# 12. Modellen er designet for å tåle følgende bibliografiske situasjoner

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

# 13.Expression må alltid tilhøre ett Work

´´´
Expression → 1 Work
´´´

Et Work kan eksistere uten Expression, men en Expression kan ikke eksistere uten et Work.

# 14. Manifestation må alltid tilhøre en Expression

´´´
Manifestation → 1 Expression
´´´

Dette sikrer at alle publiserte utgaver kan spores tilbake til en bestemt realisering av verket.

# 15. Språk registreres på Expression

Språk registreres på Expression-nivå fordi oversettelser representerer nye realiseringer av et verk.

# 16. Realiseringstype registreres på Expression

Expression inneholder feltet expression_type, som beskriver realiseringstypen (for eksempel tekst eller lydbok).

# 17.Tekst og lydbok er ulike Expressions

Tekst og lydbok modelleres som separate Expressions, fordi de representerer ulike realiseringer av et verk.

---

## Bruk av dette dokumentet

Dette dokumentet fungerer som en **referanse for utvikling og migrasjoner**.

Før større modellendringer bør følgende spørsmål stilles:

> Bryter denne endringen en modell-invariant?
> 

Hvis svaret er ja, må beslutningen vurderes som en **arkitekturendring**.

---
