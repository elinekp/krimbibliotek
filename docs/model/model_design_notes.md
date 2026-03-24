# Work-nivået i modellen

Dette notatet dokumenterer begrunnelsene bak hvordan Work er modellert i fase 1 av prosjektet.

## Hvorfor Work er holdt minimal

Work representerer den **konseptuelle identiteten** til et verk.

Mange katalogsystemer fyller Work-nivået med et stort antall metadatafelt, men i dette prosjektet er Work bevisst holdt svært enkel i første fase.

Følgende hensyn ligger bak beslutningen:

- redusere kompleksitet i tidlig utvikling
- unngå å modellere felter som senere viser seg å høre hjemme på Expression
- gjøre det lettere å etablere stabile katalogiseringsregler

Work fungerer derfor primært som **ankeret i WEMI-strukturen**.

## Hvorfor sjanger og appellfaktorer ligger på Work

Sjanger og appellfaktorer beskriver **selve fortellingen**, ikke en spesifikk utgave.

For eksempel:

- en norsk oversettelse av en roman
- en lydbokversjon
- en ny paperbackutgave

vil normalt ha samme sjanger og samme appellstruktur.

Derfor er disse koblet til Work i stedet for Expression eller Manifestation.

## Hvorfor karakterer kobles til Work

Kriminallitteratur er ofte karakterdrevet.

Ved å koble karakterer til Work blir det mulig å:

- navigere biblioteket etter karakterer
- koble karakterer på tvers av forfattere (f.eks. pastisjer)
- analysere karakterunivers på tvers av utgaver

Dette gir en mer fleksibel modell for litterær formidling.

## Hvorfor Work kan eksistere uten Expression

Et Work kan registreres før konkrete uttrykk er katalogisert.

Dette gjør det mulig å:

- registrere verk på konseptnivå
- legge til Expression senere
- modellere verk som eksisterer uavhengig av spesifikke utgaver

Denne beslutningen samsvarer med prinsippene i LRM.

## Hvorfor Work vs Expression ikke løses i databasen

Grensen mellom Work og Expression er i praksis et **katalogiseringsspørsmål**, ikke et databaseproblem.

Eksempler som krever faglig vurdering:

- sterkt reviderte tekster
- grafiske adaptasjoner
- dramatiseringer
- forkortede utgaver

Disse vurderingene vil derfor bli definert i dokumentet:

```
Lokale modelleringsregler for fase 1
```

Databasen implementerer strukturen, mens katalogiseringsreglene definerer praksisen.

## Hvorfor språk ligger på Expression

Språk beskriver realiseringen av et verk, ikke selve verket.

Et verk kan eksistere i flere språkversjoner, som alle representerer ulike Expressions.

Eksempel:

```
Work
 ├ Expression (eng)
 ├ Expression (nor)
 └ Expression (ger)
```

Derfor er språk modellert på Expression-nivå.

## Hvorfor tekst og lydbok er ulike Expressions

En lydbok er ikke bare en distribusjonsform av en tekst, men en egen realisering av verket.

Lydboken innebærer blant annet:

- innlesning
- performativ tolkning
- egne bidragsytere (innleser)

Derfor modelleres tekst og lydbok som ulike Expressions.

## Hvorfor Expression kan ha flere forekomster med samme språk

Flere Expressions med samme språk og realiseringstype kan forekomme i situasjoner som:

- sterkt reviderte tekster
- forkortede versjoner
- alternative realiseringer

Datamodellen begrenser derfor ikke slike situasjoner.

I stedet håndteres disse gjennom **lokale modelleringsregler.**

## Hvorfor Manifestation representerer bibliografisk identitet på utgavenivå

`Manifestation` brukes til å modellere den konkrete publiserte utgaven av en `Expression`.

Dette nivået brukes til å skille mellom ulike utgaver og publiseringsformer av samme realisering, for eksempel:

- hardcover
- paperback
- epub
- pdf

Disse forskjellene representerer ikke nye `Expressions`, men nye `Manifestations`.

Dette gjør skillet mellom `Expression` og `Manifestation` tydelig:

- `Expression` = hvordan verket er realisert
- `Manifestation` = hvordan denne realiseringen er publisert

## Hvorfor ISBN ligger på Manifestation

ISBN identifiserer en konkret utgave og hører derfor til `Manifestation`-nivået.

ISBN identifiserer ikke verket som abstrakt idé og heller ikke realiseringen som sådan.

## Hvorfor NB-identifikatoren lagres som nb_sesamid

I fase 1 lagres Nasjonalbibliotekets identifikator som `nb_sesamid`.

Dette er valgt for å være presis om hvilken NB-identifikator feltet faktisk representerer, og for å unngå uklarhet rundt et mer generelt `nb_id`.

Siden denne identifikatoren peker til en konkret bibliografisk post eller utgave, hører den til `Manifestation`-nivået.

## Hvorfor forlag modelleres via Contribution / Agent fra start

Forlag hører til `Manifestation`-nivået fordi forlag er knyttet til den konkrete utgaven, ikke til `Work` eller `Expression`.

Prosjektet velger å modellere forlag via `Contribution / Agent` allerede i fase 1, i stedet for å bruke et enkelt tekstfelt.

Dette gir:

- mer konsekvent rollemodell
- bedre autoritetskontroll
- mindre oppryddingsarbeid senere

Ulempen er høyere registreringsfriksjon i fase 1, men dette er vurdert som akseptabelt for å beskytte modellen strukturelt.

## Hvorfor Item holdes på eksemplarnivå

`Item` representerer det individuelle fysiske eksemplaret i samlingen.

I fase 1 holdes `Item` bevisst på rent eksemplarnivå. Det betyr at `Item` brukes til data som gjelder det konkrete eksemplaret, ikke til bibliografiske data om utgaven.

Eksempler på data som hører til `Item`:

- hylleplassering
- proveniens
- lokale eksemplarnotater
- senere eventuelt tilstand og utlånsrelaterte opplysninger

Eksempler på data som ikke hører til `Item`:

- ISBN
- `nb_sesamid`
- utgivelsesår
- utgaveinformasjon som beskriver selve publikasjonen

Slike data hører til `Manifestation`, fordi de beskriver den bibliografiske identiteten på utgavenivå.

Dette skillet er viktig for å unngå at samme type informasjon registreres både på `Manifestation` og `Item`, noe som ville gi overlapp, inkonsistens og dyr opprydding senere.

## Hvorfor proveniens i fase 1 håndteres enkelt

Proveniens beskriver et eksemplars eier- og historieforløp.

Dette kan for eksempel omfatte:

- tidligere eiere
- gaveopplysninger
- samlingstilknytning
- ex libris
- dedikasjoner
- stempler eller andre spor på eksemplaret

I fase 1 håndteres proveniens normalt gjennom feltet:

- `provenance_notes`

Dette er valgt for å holde registreringen enkel i første fase.

Samtidig åpner modellen for at `Contribution` også kan kobles til `Item` når proveniens eller eierskap er viktig nok til å struktureres, for eksempel ved navngitte tidligere eiere eller givere.

Valget i fase 1 er derfor:

- enkel proveniens registreres som fritekst
- strukturert proveniens brukes bare når det gir tydelig merverdi

## Hvorfor `is_first_edition` ikke brukes på Item

Et eget felt som `is_first_edition` brukes ikke på `Item`.

Om et eksemplar tilhører første utgave, fremgår dette gjennom vanlig utgaveinformasjon på `Manifestation`-nivå.

Prosjektet legger derfor ikke inn et eget boolsk felt for dette, verken på `Item` eller som særskilt behov i fase 1.

Dersom prosjektet senere ønsker å registrere copy-specific bibliografiske særtrekk på eksemplarnivå, må dette vurderes som en egen problemstilling og modelleres med mer presis semantikk enn `is_first_edition`.

# Hvorfor serier modelleres som egne entiteter

Dette notatet dokumenterer begrunnelsene bak hvordan `Series` og `SeriesMembership` er modellert i fase 1 av prosjektet.

## Hvorfor Series er en egen entitet

Serier representerer ikke bare en tekststreng, men en gjenbrukbar og navigerbar struktur i modellen.

Ved å modellere `Series` som egen entitet blir det mulig å:

- gjenbruke samme serie på tvers av flere verk eller utgaver
- skille tydelig mellom selve serien og det enkelte medlemskapet
- støtte flere serietyper uten å miste struktur
- bygge navigasjon og filtrering på serie senere

Dette er viktig fordi prosjektet allerede skal støtte minst to ulike seriekonsepter:

- narrative serier
- forlagsserier

## Hvorfor series_type er obligatorisk

Samme tabell brukes i fase 1 til både narrative serier og forlagsserier.

For å unngå uklar semantikk må hver `Series`-post derfor ha en eksplisitt type.

I fase 1 brukes et lite og lukket vokabular:

- `narrative`
- `publisher_series`

Dette gir en stram modell med lav risiko for lokal variasjon i verdier, og gjør det enklere å validere data og bygge spørringer senere.

Andre serietyper utsettes til senere fase.

## Hvorfor SeriesMembership er en egen koblingsentitet

Serietilknytning er ikke bare en enkel mange-til-mange-relasjon.

Et medlemskap i en serie kan også ha egne egenskaper, særlig:

- rekkefølge
- nummerering for visning
- eventuell fremtidig kontekst

Derfor modelleres serietilknytning gjennom en egen entitet:

`SeriesMembership`

Dette gjør det mulig å holde selve serien adskilt fra opplysninger som gjelder ett bestemt medlemskap.

## Hvorfor serier kan ligge på ulike nivåer i modellen

Prosjektet har skilt mellom to hovedtyper serie i fase 1:

- narrative serier
- forlagsserier

Disse hører ikke til samme nivå i WEMI-strukturen.

Narrative serier beskriver verkets fortellingsmessige tilknytning og hører derfor til `Work`.

Forlagsserier beskriver en konkret utgave- eller publiseringskontekst og hører derfor til `Manifestation`.

Dette gjør det mulig at samme bok kan ha:

- en narrativ serie på `Work`
- en forlagsserie på `Manifestation`

uten at disse blandes sammen.

## Hvorfor én rad i SeriesMembership peker til enten Work eller Manifestation

Én rad i `SeriesMembership` representerer én konkret serietilknytning.

For å holde modellen entydig skal en medlemskapsrad derfor peke til:

- enten `Work`
- eller `Manifestation`

Aldri begge samtidig.

Hvis én rad kunne peke til begge nivåer, ville det bli uklart hva medlemskapet faktisk beskriver.

Derfor er modellen strammet slik at hver rad uttrykker én type tilknytning.

## Hvorfor duplikatmedlemskap ikke tillates

Samme serie skal ikke kunne registreres flere ganger mot samme mål.

Det betyr at prosjektet beskytter mot:

- samme `Series` koblet flere ganger til samme `Work`
- samme `Series` koblet flere ganger til samme `Manifestation`

Dette er valgt fordi slike duplikater normalt ikke uttrykker ny informasjon, men heller registreringsfeil eller inkonsistent praksis.

Derfor håndheves dette som databasekrav, ikke bare som anbefalt praksis.

## Hvorfor part_number og part_display ligger på medlemskapet

Nummerering er ikke en egenskap ved serien som abstrakt entitet, men ved forholdet mellom serien og et bestemt verk eller en bestemt manifestasjon.

Derfor ligger:

- `part_number`
- `part_display`

på `SeriesMembership`, ikke på `Series`.

Dette gjør det mulig at samme serie kan brukes mot mange mål med ulik eller manglende nummerering.

## Hvorfor nummerering er valgfri i fase 1

Ikke alle serietilknytninger har kjent, stabil eller normaliserbar nummerering.

Modellen må derfor tåle:

- serietilknytning uten nummer
- nummerering bare som visningsstreng
- ulik verdi for sortering og visning

Derfor er både `part_number` og `part_display` valgfrie i fase 1.

Dette gir nok fleksibilitet uten å utvide modellen unødvendig.

## Hvorfor flere serieutvidelser utsettes

Fase 1 holder seriemodellen bevisst stram.

Følgende er utsatt:

- `context_note`
- variantnavn på `Series`
- seriehierarki som `parent_series`
- flere `series_type`-verdier enn de to grunnleggende

Dette er nyttige utvidelser, men ikke nødvendige for å beskytte grunnstrukturen nå.

Målet i fase 1 er å få på plass en liten, tydelig og stabil seriemodell som kan utvides senere uten ombygging av kjernen.