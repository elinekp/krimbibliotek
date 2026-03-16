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