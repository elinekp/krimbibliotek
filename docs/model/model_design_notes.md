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