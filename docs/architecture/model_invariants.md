# Model Invariants — Krimbiblioteket

Dette dokumentet beskriver harde modellregler for datamodellen i Krimbiblioteket.

Invariants i dette dokumentet skal ikke brytes av applikasjonslogikk, migrasjoner, importløp eller senere utvidelser uten at det er tatt en eksplisitt arkitekturbeslutning.

Dokumentet beskriver:
- strukturelle regler
- kardinalitet
- XOR-regler
- unike kombinasjoner
- nivåplassering som er frosset i fase 1

Dokumentet beskriver ikke:
- begrunnelser og designresonnement
- praktiske katalogiseringsregler
- roadmap, neste steg eller prosjektstatus


---

## 1. WEMI-strukturen er grunnlaget for modellen

Datamodellen bygger på WEMI-strukturen:

`Work → Expression → Manifestation → Item`

Dette betyr:
- `Work` representerer verkets abstrakte/intellektuelle nivå
- `Expression` representerer realiseringen av et verk
- `Manifestation` representerer den konkrete utgaven
- `Item` representerer det individuelle eksemplaret

Ingen entiteter skal hoppe over nivåer i denne kjernen.

Ikke tillatt:
- direkte modellering av `Work → Manifestation` som erstatning for `Expression`
- direkte modellering av `Work → Item`
- direkte modellering av `Expression → Item`


---

## 2. Work kan eksistere uten Expression

Kardinalitet:
- `Work → 0..n Expression`
- `Expression → 1 Work`

Regel:
- Et `Work` kan eksistere uten noen registrert `Expression`
- En `Expression` kan ikke eksistere uten å tilhøre nøyaktig ett `Work`


---

## 3. Expression–Manifestation modelleres som M2M via ExpressionManifestation

Relasjonen mellom `Expression` og `Manifestation` modelleres gjennom en eksplisitt koblingstabell:

`ExpressionManifestation`

Kardinalitet:
- `Expression → 0..n ExpressionManifestation`
- `Manifestation → 1..n ExpressionManifestation`

Regler:
- En `Manifestation` kan ikke eksistere uten minst én kobling til `Expression` via `ExpressionManifestation`
- En `Expression` kan forekomme i flere `Manifestations`
- En `Manifestation` kan kobles til flere `Expressions`
- Direkte 1:M-modell mellom `Expression` og `Manifestation` skal ikke brukes som gjeldende hovedstruktur i databasen

Normalmønsteret i praksis kan ofte være:
- én `Manifestation` til én `Expression`
- én `Expression` til flere `Manifestations`

Dette endrer ikke den formelle modellinvarianten: relasjonen er M2M


---

## 4. ExpressionManifestation er en eksplisitt koblingstabell med egen identitet

`ExpressionManifestation` er en egen tabell i modellen.

Regler:
- tabellen skal ha egen `id`
- hver rad skal koble nøyaktig én `expression` og nøyaktig én `manifestation`
- samme kombinasjon av `expression` og `manifestation` kan ikke registreres flere ganger

Unik regel:
- unik per (`expression`, `manifestation`)


---

## 5. ExpressionManifestation bruker primærkobling med maksimum én primær per Manifestation

`ExpressionManifestation` har i fase 1 feltet:

- `is_primary`

Regler:
- en `Manifestation` kan ha maks én primærkobling
- flere primærkoblinger for samme `Manifestation` er ikke tillatt
- det er tillatt at en `Manifestation` ikke har primærkobling

Dette betyr:
- vanlige utgaver skal normalt ha én primærkobling
- antologier og enkelte samleutgaver kan ha ingen primærkobling

Databasekrav:
- det skal ikke være mulig å registrere mer enn én rad med `is_primary = true` for samme `manifestation`


---

## 6. Item må alltid tilhøre én Manifestation

Kardinalitet:
- `Manifestation → 0..n Item`
- `Item → 1 Manifestation`

Regel:
- Et `Item` kan ikke eksistere uten å tilhøre nøyaktig én `Manifestation`


---

## 7. Hovedentiteter bruker UUID som primærnøkkel

Hovedentiteter i modellen bruker UUID som primærnøkkel.

Dette gjelder minst:
- `Work`
- `Expression`
- `Manifestation`
- `Item`
- `Series`
- `SeriesMembership`
- `Character`
- `WorkCharacter`
- `WorkRelationship`
- `Agent`
- `Contribution`
- `ExpressionManifestation`
- `WorkGenre`
- `WorkAppealFactor`

Regel:
- primærnøkler på disse entitetene skal ikke erstattes av auto-increment som hovedidentitet

Unntak:
- kontrollerte vokabularentiteter kan bruke stabile koder som primær identitet der dette er besluttet, for eksempel `Role`, `Genre` og `AppealFactor`


---

## 8. Kontrollerte semantiske kategorier representeres med stabile lokale koder

I fase 1 skal kontrollerte semantiske kategorier representeres med stabile lokale koder.

Dette gjelder blant annet:
- `expression_type`
- `series_type`
- `relation_type`
- `Role.code`
- `Genre.code`
- `AppealFactor.code`

Regler:
- modellen skal ikke basere slike semantiske kategorier på ukontrollert fritekst
- kodene skal være stabile over tid
- kodene skal kunne mappes entydig til relevante eksterne vokabularer senere


---

## 9. Eksterne URI-er lagres normalt ikke direkte i operative tabeller i fase 1

Regel:
- operative tabeller i fase 1 skal normalt ikke være avhengige av direkte lagring av eksterne URI-er som bærende modellmekanisme

Dette utelukker ikke eksplisitt støtte for enkelte identifikatorfelt der dette er besluttet.

Eksempel:
- `wikidata_id` er støttet i fase 1 der dette er definert
- generell URI-basert identifikatorstruktur er ikke en invariant i fase 1


---

## 10. Agent er egen entitet, komprimert i fase 1 men semantisk tro mot LRM

`Agent` er en egen entitet i modellen.

I fase 1 komprimeres LRM-underklassene `Person` og `Collective Agent` til én operativ `Agent`-tabell med kontrollert typefelt.

Regler:
- `Agent` brukes for både personer og kollektive agenter
- `Agent` skal ha `id`, `name` og `agent_type`
- `agent_type` er obligatorisk og kontrollert
- gyldige fase-1-verdier for `agent_type` er:
  - `person`
  - `collective_agent`
- `wikidata_id` er tillatt som fase-1-identifikator
- roller skal ikke ligge direkte på `Agent`

Konsekvens:
- rolle uttrykkes i relasjon, ikke som attributt på agenten
- fase-1-modellen er operativt komprimert, men semantisk tilpasset LRM/RDA
- modellen skal ikke låses til en snevrere kategori som bare `organization`, siden `collective_agent` i LRM er bredere enn dette

---

## 11. Fase-1-attributter skal kunne migreres til senere LRM-entiteter uten semantisk brudd

Når et fase-1-attributt representerer informasjon som i LRM/RDA mer presist hører hjemme i egen entitet eller relasjon, skal attributtet behandles som en midlertidig operativ representasjon.

Dette gjelder særlig framtidig støtte for:
- `Nomen`
- `Place`
- `Time-span`

Regler:
- slike fase-1-felt skal være atomiske
- slike fase-1-felt skal ha klar og avgrenset semantikk
- slike fase-1-felt skal ikke blande flere opplysningstyper i samme verdi
- slike fase-1-felt skal ikke brukes som erstatning for senere identitets- eller autoritetsstruktur
- navngivning og bruk skal gjøre senere migrering til egen entitet mulig uten semantisk brudd

Konsekvens:
- fase 1 kan bruke enklere operative felt
- modellen skal likevel ikke designes på en måte som gjør senere innføring av `Nomen`, `Place` eller `Time-span` vanskelig eller tvetydig

---

## 12. Role er egen kontrollert entitet

`Role` er egen entitet for kontrollerte agentroller.

Regler:
- `Role` brukes sammen med `Contribution`
- `Role` ligger ikke direkte på `Agent`
- `Role` skal ha:
  - `code`
  - `label`
- `code` er stabil lokal kode og fungerer som primær identitet for rollen


---

## 13. Contribution modellerer agentroller eksplisitt

`Contribution` er koblingstabellen for agentroller i modellen.

Regler:
- `Contribution` kobler én `Agent` til nøyaktig én målentitet og én rolle
- `agent` er obligatorisk
- `role` er obligatorisk

I fase 1 kan `Contribution` kobles til nøyaktig én av:
- `work`
- `expression`
- `manifestation`
- `item`


---

## 14. Contribution har XOR-regel for målentitet

For hver rad i `Contribution` gjelder:

- nøyaktig én av `work`, `expression`, `manifestation` eller `item` skal være satt
- flere målentiteter samtidig er ikke tillatt
- ingen målentitet er heller ikke tillatt

Dette er en hard XOR-regel og skal håndheves teknisk


---

## 15. Contribution skal være unik per målentitet + agent + rolle

Samme agent skal ikke kunne registreres flere ganger med samme rolle mot samme målentitet.

Unik regel:
- samme kombinasjon av målentitet + `agent` + `role` kan ikke registreres flere ganger

Dette gjelder uansett hvilket nivå målentiteten ligger på


---

## 16. Contribution på Item brukes for strukturert proveniens, ikke sirkulasjon

Når `Contribution` brukes på `Item` i fase 1, gjelder dette copy-specific relasjoner som:
- tidligere eier
- giver
- annen navngitt proveniensaktør

Regel:
- `Contribution` på `Item` skal ikke brukes for aktiv låner, utlånshistorikk eller annen sirkulasjonslogikk i fase 1


---

## 17. Series er egen entitet med kontrollert series_type

`Series` er egen entitet i modellen.

Regler:
- hver `Series` skal ha egen `id`
- `series_type` er obligatorisk
- `series_type` er kontrollert kode

I fase 1 er følgende serietyper gyldige:
- `narrative`
- `publisher_series`

Andre serietyper er ikke del av fase-1-modellen


---

## 18. SeriesMembership er eksplisitt koblingstabell mellom Series og enten Work eller Manifestation

`SeriesMembership` er egen koblingstabell.

Regler:
- hver rad skal koble én `Series` til enten ett `Work` eller én `Manifestation`
- tabellen skal ha egen `id`

Dette innebærer:
- medlemskapet ligger på `Work`-nivå for narrative serier
- medlemskapet ligger på `Manifestation`-nivå for forlagsserier


---

## 19. SeriesMembership har XOR-regel mellom Work og Manifestation

For hver rad i `SeriesMembership` gjelder:

- nøyaktig én av `work` eller `manifestation` skal være satt
- begge samtidig er ikke tillatt
- begge tomme er ikke tillatt

Dette er en hard XOR-regel og skal håndheves teknisk


---

## 20. SeriesMembership skal være unikt per serie og målentitet

Duplikatkoblinger er ikke tillatt.

Unike regler:
- samme kombinasjon av `series` og `work` kan ikke registreres flere ganger
- samme kombinasjon av `series` og `manifestation` kan ikke registreres flere ganger


---

## 21. Character er egen Work-nivåentitet

`Character` er egen entitet i modellen.

Regler:
- karakterer hører til på `Work`-nivå
- karakterer skal ikke kobles direkte til `Expression`
- karakterer skal ikke kobles direkte til `Manifestation`
- karakterer skal ikke kobles direkte til `Item`

I fase 1 har `Character`:
- `id`
- `name`


---

## 22. WorkCharacter er eksplisitt koblingstabell mellom Work og Character

`WorkCharacter` er en eksplisitt koblingstabell.

Regler:
- tabellen skal ha egen `id`
- hver rad kobler nøyaktig ett `Work` og én `Character`
- koblingen skal bare gå mellom `Work` og `Character`

Unik regel:
- samme kombinasjon av `work` og `character` kan ikke registreres flere ganger


---

## 23. WorkRelationship modellerer bare Work-til-Work-relasjoner

`WorkRelationship` er egen entitet for intellektuelle relasjoner mellom verk.

Regler:
- `WorkRelationship` kobler bare `Work` til `Work`
- relasjonen er retningsbestemt
- `relation_type` er obligatorisk og kontrollert
- selvrelasjon er ikke tillatt

Unik regel:
- samme kombinasjon av `source_work`, `target_work` og `relation_type` kan ikke registreres flere ganger


---

## 24. Genre er kontrollert Work-taksonomi

`Genre` er egen entitet i modellen.

Regler:
- `Genre` hører til på `Work`-nivå
- `Genre` bruker stabile lokale koder i fase 1
- hierarki er eksplisitt i fase 1 gjennom `parent_genre`
- `Genre` skal ha:
  - `code`
  - `label`
  - `parent_genre`

`code` fungerer som stabil primær identitet for sjangeren


---

## 25. WorkGenre er eksplisitt koblingstabell mellom Work og Genre

`WorkGenre` er egen koblingstabell.

Regler:
- tabellen skal ha egen `id`
- koblingen går bare mellom `Work` og `Genre`
- samme kombinasjon av `work` og `genre` kan ikke registreres flere ganger

Unik regel:
- unik per (`work`, `genre`)


---

## 26. AppealFactor er kontrollert Work-vokabular

`AppealFactor` er egen entitet i modellen.

Regler:
- `AppealFactor` hører til på `Work`-nivå
- `AppealFactor` bruker stabile lokale koder i fase 1
- hierarki er eksplisitt i fase 1 gjennom `parent_appeal_factor`
- `AppealFactor` skal ha:
  - `code`
  - `label`
  - `parent_appeal_factor`
  - `definition`
  - `scope_note`

`code` fungerer som stabil primær identitet for appellfaktoren


---

## 27. WorkAppealFactor er eksplisitt koblingstabell mellom Work og AppealFactor

`WorkAppealFactor` er egen koblingstabell.

Regler:
- tabellen skal ha egen `id`
- koblingen går bare mellom `Work` og `AppealFactor`
- samme kombinasjon av `work` og `appeal_factor` kan ikke registreres flere ganger

Unik regel:
- unik per (`work`, `appeal_factor`)


---

## 28. Språk registreres på Expression

Regel:
- språk skal registreres på `Expression`-nivå
- språk skal ikke registreres som bærende modellattributt på `Work`, `Manifestation` eller `Item`

Dette følger av at språk i modellen er knyttet til verkets realisering


---

## 29. Realiseringstype registreres på Expression

Regel:
- realiseringstype registreres på `Expression`
- `expression_type` er kontrollert kode
- ulike realiseringstyper, som tekst og lydbok, skal kunne skilles som ulike `Expressions`


---

## 30. Flere Expressions med samme språk og samme realiseringstype er tillatt

Regel:
- modellen tillater flere `Expressions` innenfor samme `Work` med samme kombinasjon av `language_code` og `expression_type`

Det skal derfor ikke finnes en hard unik constraint som forbyr dette på `Expression`-nivå


---

## 31. Manifestation representerer bibliografisk identitet på utgavenivå

Regel:
- `Manifestation` representerer utgavenivået i modellen
- bibliografiske forskjeller på utgavenivå skal ikke presses ned på `Item`

Typiske forskjeller som kan representere ulike `Manifestations`:
- hardcover
- paperback
- epub
- pdf


---

## 32. Item representerer eksemplarnivå, ikke utgavenivå

Regel:
- `Item` representerer individuelle eksemplarer
- copy-specific informasjon skal ligge på `Item`, ikke på `Manifestation`
- bibliografisk utgaveinformasjon skal ikke flyttes ned til `Item`


---

## 33. Proveniens kan ligge på Item som fritekst eller strukturert relasjon

Regel:
- `Item` kan bruke `provenance_notes` for enkel proveniens
- når proveniens modelleres strukturert mot agent, skal dette gjøres gjennom `Contribution` på `Item`

Dette endrer ikke regelen om at sirkulasjonslogikk ikke inngår i fase 1


---

## 34. Relasjonspolicy i fase 1 er SET_NULL

Der fase-1-modellen bruker nullable relasjoner som del av designet, er relasjonspolicy i fase 1:

`SET_NULL`

Regel:
- sletting av referert rad skal ikke automatisk føre til cascading sletting som bryter hovedprinsippet for fase-1-modellen, med mindre en eksplisitt arkitekturbeslutning senere endrer dette


---

## 35. Grensen mellom Work, Expression og Manifestation endres ikke av lokale enkelttilpasninger

Regel:
- databasen skal ikke utvides ad hoc for å omgå skillet mellom `Work`, `Expression` og `Manifestation`
- grensetilfeller håndteres gjennom modelleringsregler, ikke ved å bryte kjernestrukturen

Dette beskytter modellens nivådeling over tid


---

## 36. Endring av en invariant krever eksplisitt arkitekturbeslutning

Hvis en foreslått modellendring:
- endrer nivåplassering
- bryter en kardinalitetsregel
- bryter en XOR-regel
- opphever en unik kombinasjon
- endrer den grunnleggende WEMI-strukturen
- endrer rollen til en kontrollert entitet

da skal dette behandles som en arkitekturendring, ikke som en lokal dokumentjustering.