# Model Design Notes — Krimbiblioteket

Dette dokumentet samler designbetraktninger, forklarende resonnement og faglige nyanser knyttet til datamodellen i Krimbiblioteket.

Det er ikke prosjektets normative hovedkilde.

Formålet er å dokumentere:
- hvorfor modellen er tenkt som den er
- hvilke avveininger som ligger bak viktige valg
- hvilke framtidige utvidelser modellen prøver å holde åpne
- hvilke produkt- og arkitekturretninger som påvirker modelltenkningen

Dette dokumentet skal ikke brukes som eneste kilde for:
- harde modellregler
- databasekrav
- kardinalitet og XOR-regler
- endelige fase-1-beslutninger
- prosjektstatus eller arbeidsrekkefølge

Normativt innhold hører primært hjemme i:
- `ADR.md`
- `model_invariants.md`
- `modelling_rules_phase1.md`

Dette dokumentet kan gjerne være mer resonnerende, mer forklarende og mer åpent om framtidige muligheter.


---

## 1. Overordnet designretning

Krimbiblioteket er tenkt som mer enn en tradisjonell katalog.

Målet er å bygge en struktur som både kan:
- støtte presis bibliografisk modellering
- gi god navigasjon for brukere
- tåle framtidige utvidelser uten at kjernen må tegnes om

Prosjektet prøver derfor å balansere to hensyn:

1. en stram bibliografisk kjerne som er mulig å bygge og vedlikeholde i fase 1  
2. en modell som på sikt kan støtte rikere formidling, relasjoner, kuratering og utforsking

Denne spenningen går igjen i mange av designvalgene:
- hvorfor WEMI beholdes
- hvorfor kontrollerte koder brukes tidlig
- hvorfor noen ting bevisst utsettes
- hvorfor enkelte koblingstabeller får egen identitet


---

## 2. Hvorfor WEMI beholdes som kjerne

WEMI-strukturen gjør det mulig å skille mellom ulike typer bibliografiske forskjeller som ellers lett ville blitt blandet sammen.

Den viktigste gevinsten er at modellen kan uttrykke forskjellen mellom:
- verkets identitet
- verkets realisering
- den publiserte utgaven
- det konkrete eksemplaret

Dette er særlig viktig i et prosjekt som skal tåle:
- oversettelser
- lydbøker
- ulike utgaveformer
- forlagsserier
- strukturert proveniens
- verkrelasjoner
- karaktersporing og andre navigasjonslag

Uten dette skillet ville modellen raskt blitt enklere i starten, men dyrere å rydde opp i senere.

Ulempen er at modellen blir mer krevende å forstå og bruke, særlig i grensetilfeller. Derfor er prosjektet også avhengig av egne modelleringsregler ved siden av selve databasedesignet.


---

## 3. Hvorfor Work, Expression, Manifestation og Item holdes tydelig fra hverandre

En gjennomgående designambisjon er å unngå semantisk overlapp mellom nivåene.

Hvis samme type informasjon kan legges flere steder, oppstår det fort:
- dobbeltregistrering
- inkonsistente data
- uklare søkeflater
- dyr opprydding senere

Derfor er nivåene tenkt med tydelige hovedroller:

- `Work` for verkets innholdsmessige og intellektuelle identitet
- `Expression` for språk og realiseringsform
- `Manifestation` for bibliografisk utgaveidentitet
- `Item` for eksemplarspesifikke forhold

Dette skillet er ikke bare teoretisk. Det beskytter også framtidig funksjonalitet, fordi brukergrensesnitt, søk og importløp senere kan bygges på mer forutsigbare data.


---

## 4. Hvorfor grenseoppganger ikke kan løses i databasen alene

Databasen kan håndheve struktur, men ikke alltid semantisk tolkning.

Den kan for eksempel ikke alene avgjøre:
- når noe er nytt `Work`
- når noe er ny `Expression`
- når noe er ny `Manifestation`

Dette er et grunnleggende trekk ved prosjektet, ikke en midlertidig svakhet.

Derfor er dokumentasjonen delt i flere lag:
- databasen beskytter struktur
- invariants fryser harde regler
- modelleringsreglene styrer praktisk bruk
- designnotatene forklarer hvorfor valgene er tatt

Dette er en bevisst arkitektur for dokumentasjon, ikke bare en praktisk nødløsning.


---

## 5. Hvorfor Expression–Manifestation beholdes som M2M

Valget om å modellere `Expression`–`Manifestation` som M2M via `ExpressionManifestation` gjør modellen mer kompleks enn en enkel 1:M-løsning.

Likevel er dette valgt fordi prosjektet ønsker å tåle bibliografiske situasjoner som ellers blir vanskelige eller kunstige å modellere, særlig:
- samlingsverk
- antologier
- omnibusutgaver
- samleutgaver med flere uttrykk i samme utgivelse
- samme realisering publisert i flere utgaver

Dette er et klassisk tilfelle der prosjektet prioriterer strukturell robusthet over maksimal enkelhet i fase 1.

Fordelen er at modellen tåler mer fra start.

Ulempen er at det krever:
- egen koblingstabell
- mer bevisst registreringspraksis
- forklaring av normalmønster versus særtilfeller

Det er derfor viktig å forstå at M2M her ikke betyr at alle registreringer blir kompliserte. Normalmønsteret i praksis vil fortsatt ofte være enkelt. Men modellen er ikke låst til bare det enkle tilfellet.


---

## 6. Hvorfor ExpressionManifestation har egen identitet

At `ExpressionManifestation` har egen `id` kan virke tungt for en ren koblingstabell.

Valget er likevel fornuftig i dette prosjektet av flere grunner:
- det gir konsistens med andre koblingstabeller
- det gjør tabellen lettere å utvide senere
- det gjør det enklere å referere til selve koblingen dersom nye egenskaper kommer
- det passer bedre med en modell som forventes å vokse over tid

Dette er ikke strengt nødvendig i alle systemer, men i denne modellen er det et valg som beskytter framtidig utvikling.

Det samme mønsteret er derfor også brukt i tabeller som:
- `WorkGenre`
- `WorkAppealFactor`
- `WorkCharacter`

Prosjektet prioriterer her intern konsistens over minimalisme.


---

## 7. Hvorfor språk og realiseringstype ligger på Expression

Språk og realiseringstype er lagt på `Expression` fordi de beskriver hvordan verket faktisk kommer til uttrykk, ikke hva verket er som abstrakt identitet.

Dette gjør det mulig å uttrykke forskjeller som:
- originaltekst versus oversettelse
- tekst versus lydbok
- andre realiseringsformer av samme verk

Det gjør også at `Work` kan holdes relativt rent som bærer av verkidentitet, uten å bli overbelastet med egenskaper som egentlig tilhører realiseringen.

En viktig konsekvens av dette er at samme `Work` kan ha flere `Expressions` som ligner hverandre sterkt. Det kan gi noen vanskelige grensetilfeller, men det er likevel bedre enn å tvinge slike forskjeller inn på feil nivå.


---

## 8. Hvorfor Manifestation holdes som bibliografisk utgavenivå

`Manifestation` er ment å bære den bibliografiske identiteten på utgavenivå.

Dette er viktig fordi mange forskjeller som brukere og bibliotekarer bryr seg om, ikke handler om nytt verk eller ny realisering, men om konkret publisert utgave:
- hardcover
- paperback
- epub
- pdf
- ulike utgivere eller publiseringskontekster

Ved å holde dette tydelig på `Manifestation` unngår prosjektet at slike variasjoner enten:
- presses opp på `Expression`, der de ikke hører hjemme
- eller ned på `Item`, der de blir copy-specific på feil måte

Dette gir en ryddigere modell og bedre grunnlag for både bibliografisk arbeid og framtidig visning.


---

## 9. Hvorfor forlag modelleres via Agent og Contribution

Prosjektet har valgt å modellere forlag via `Agent` og `Contribution` i stedet for å bruke et enkelt tekstfelt på `Manifestation`.

Fordeler:
- mer konsekvent rollemodell
- bedre gjenbruk av aktørdata
- lettere overgang til rikere autoritetsarbeid senere
- mindre opprydding når modellen blir mer moden

Ulemper:
- høyere registreringsfriksjon i fase 1
- større behov for konsekvent praksis rundt agentnavn

Dette er et bevisst valg der prosjektet aksepterer litt mer kompleksitet i starten for å beskytte modellens struktur senere.


---

## 10. Hvorfor Item holdes stramt på eksemplarnivå

`Item` holdes med vilje smalt i fase 1.

Det brukes for forhold som faktisk gjelder det individuelle eksemplaret, for eksempel:
- hylleplassering
- proveniens
- lokale eksemplarnotater

Dette er gjort for å beskytte skillet mellom:
- bibliografisk identitet
- copy-specific informasjon

Hvis bibliografiske egenskaper flyttes ned på `Item`, oppstår det fort uklarhet om hva som gjelder alle eksemplarer av en utgave, og hva som gjelder ett bestemt eksemplar.

Dette gjelder også små fristelser i registreringsarbeidet, som å legge utgaverelatert informasjon på itemnivå fordi den er “lett tilgjengelig der”. Modellen prøver bevisst å motstå slike snarveier.


---

## 11. Hvorfor proveniens i fase 1 håndteres pragmatisk

Proveniens er viktig for prosjektet, men fase 1 prøver likevel å holde registreringskostnaden nede.

Derfor er hovedlinjen:
- enkel proveniens kan registreres som fritekst
- strukturert proveniens brukes når det gir tydelig merverdi

Denne pragmatiske linjen er viktig av to grunner.

For det første:
ikke all proveniens er verdt å modellere tungt fra start.

For det andre:
prosjektet ønsker å holde døren åpen for rikere proveniensmodellering senere, uten å gjøre fase 1 uforholdsmessig tung.

At `Contribution` også kan brukes på `Item`, gjør at modellen allerede nå kan håndtere navngitte tidligere eiere, givere eller andre copy-specific aktører når det faktisk er nyttig.

Dette er et godt eksempel på prosjektets generelle strategi:
ikke bygge alt nå, men heller ikke stenge for det.


---

## 12. Hvorfor `is_first_edition` ikke brukes på Item

Prosjektet har valgt å ikke bruke et eget felt som `is_first_edition` på `Item`.

Begrunnelsen er at førsteutgave i utgangspunktet er et spørsmål om utgaveidentitet, altså noe som hører hjemme på `Manifestation`-nivå, ikke på eksemplarnivå.

Hvis prosjektet senere ønsker å uttrykke copy-specific bibliografiske særtrekk på eksemplarnivå, bør dette modelleres med mer presis semantikk enn et generelt boolsk felt.

Dette er et bevisst nei til en løsning som virker enkel, men som egentlig blander nivåene.


---

## 13. Hvorfor sjanger ligger på Work

Sjanger beskriver først og fremst verkets innholdsmessige og fortellingsmessige karakter.

Derfor er `Genre` lagt på `Work`-nivå.

Dette gjør det mulig å:
- beskrive samme verk konsistent på tvers av utgaver og realiseringer
- støtte flere sjangre per verk
- bygge navigasjon, filtrering og utforsking rundt verkets innhold

En alternativ løsning kunne vært å registrere sjanger på utgavenivå eller som løs tagging, men det ville gitt svakere semantisk kontroll og dårligere grunnlag for videre utvikling.


---

## 14. Hvorfor AppealFactor ligger på Work

Appellfaktorer beskriver leseropplevelse, stemning, fortellingsdriv og andre trekk ved verket slik det oppleves som fortelling.

Derfor er `AppealFactor` også lagt på `Work`-nivå.

Dette har flere fordeler:
- appellfaktorer kan brukes på tvers av utgaver
- vokabularet kan bygges som et eget kontrollert lag
- det gir grunnlag for framtidig lesersørvis, anbefaling og navigasjon

Samtidig er dette et område med mer tolkningsrom enn tradisjonell bibliografisk katalogisering. Derfor er det ekstra viktig at modellen ikke bare lagrer appellfaktorer, men også kan støtte definisjoner og omfangsnoter.

Dette er grunnen til at `definition` og `scope_note` er tatt med allerede i fase 1.


---

## 15. Hvorfor sjanger og appellfaktor holdes adskilt

Prosjektet prøver å holde tydelig skille mellom:
- hva et verk er
- hvordan det oppleves
- hva det handler om

Grovt sagt:
- sjanger beskriver form og fortellingstype
- appellfaktor beskriver leseopplevelse og fortellingskarakter
- tematikk er noe annet igjen

I praksis vil grensene ofte være porøse.

Nettopp derfor er det viktig å holde vokabularene adskilt, selv om de noen ganger kan oppleves som overlappende. Hvis de kollapser inn i hverandre, blir både registreringspraksis og brukergrensesnitt raskt uklarere.

Dette er et område der modelleringsreglene blir minst like viktige som selve tabellstrukturen.


---

## 16. Hvorfor hierarki støttes i Genre og AppealFactor

Både `Genre` og `AppealFactor` er designet slik at hierarki kan uttrykkes eksplisitt.

Dette er viktig fordi prosjektet ikke bare trenger flate etiketter, men også:
- overordnede og underordnede kategorier
- mer presis navigasjon
- mulighet for framtidig utvidelse uten å bryte eksisterende struktur

Hierarki er derfor ikke bare en “ekstra finesse”, men et grep som gjør vokabularene mer robuste over tid.

Samtidig er hierarkiet i fase 1 holdt enkelt:
- ett eksplisitt parent-felt
- ingen mer avansert tesauruslogikk


---

## 17. Hvorfor synonymer utsettes, men ikke glemmes

Prosjektet ser et klart framtidig behov for synonymer, særlig på appellfaktorsiden.

Likevel er synonymer utsatt i fase 1.

Grunnen er at en god synonymstruktur fort blir mer enn bare “noen ekstra tekststrenger”. Den kan få betydning for:
- søk
- vedlikehold
- tvetydighetshåndtering
- presentasjon
- eventuell mapping mot andre vokabularer

Å utsette dette er derfor ikke et tegn på at behovet er lite, men på at prosjektet ønsker å gjøre det ordentlig senere.

Samtidig prøver modellen å være kompatibel med en senere utvidelse, for eksempel gjennom en framtidig tabell som:
- `AppealFactorAltLabel`

Dette er en typisk fase-1-strategi i prosjektet:
utsett funksjonalitet, men ikke blokker for den.


---

## 18. Hvorfor Character er en egen entitet

Prosjektet ønsker å støtte navigasjon og forbindelser som ikke bare går via forfatter, tittel og serie, men også via fiktive figurer.

Derfor er `Character` modellert som egen entitet.

Dette åpner blant annet for:
- navigasjon via gjennomgående karakterer
- kobling av verk på tvers av forfattere
- støtte for pastisjer, videreføringer og andre karakterbaserte forbindelser

At karakterer holdes på `Work`-nivå er viktig, fordi karakteren tilhører verkets fortellingsidentitet, ikke en bestemt utgave.


---

## 19. Hvorfor Character holdes enkel i fase 1

Selv om karakterer er viktige for formidling og navigasjon, er `Character` bevisst holdt enkel i fase 1.

Foreløpig brukes bare:
- `id`
- `name`

Dette er gjort for å:
- få på plass den viktigste navigasjonsstrukturen
- unngå at karaktermodellen blir et eget stort delprosjekt
- lære mer om faktisk bruk før modellen utvides

Det betyr også at framtidige behov som variantnavn, notater, identifikatorer eller relasjonstyper mellom karakterer og verk ennå ikke er modellert.

Dette er akseptabelt så lenge prosjektet er bevisst på begrensningen.


---

## 20. Hvorfor WorkCharacter er en ren kobling i fase 1

`WorkCharacter` er holdt som en enkel kobling uten ekstra metadata.

Dette er valgt fordi hovedbehovet i fase 1 er å uttrykke at en karakter forekommer i et verk.

Mer avanserte spørsmål er utsatt, for eksempel:
- karakterrolle
- betydningsgrad
- note
- kilde
- usikkerhet

Fordelen er en enkel og tydelig modell.

Ulempen er at noen nyanser går tapt i første omgang.

Prosjektet har vurdert dette som en god avgrensning i fase 1.


---

## 21. Hvorfor serier modelleres som egne entiteter

Serier representerer ikke bare en tekststreng, men en gjenbrukbar og navigerbar struktur.

Ved å modellere `Series` som egen entitet blir det mulig å:
- gjenbruke samme serie på tvers av flere verk eller utgaver
- skille mellom selve serien og det konkrete medlemskapet
- støtte flere serietyper uten å miste struktur
- bygge navigasjon og filtrering på serie senere

Dette er viktig fordi prosjektet allerede i fase 1 trenger å skille mellom minst to seriekonsepter:
- narrative serier
- forlagsserier


---

## 22. Hvorfor series_type er obligatorisk

Når samme serietabell brukes for ulike seriekonsepter, blir typeangivelsen viktig for semantisk klarhet.

At `series_type` er obligatorisk, gjør det mulig å:
- validere data tydeligere
- styre nivåplassering mer konsekvent
- bygge spørringer og grensesnitt med mindre tvetydighet

I fase 1 er vokabularet med vilje holdt stramt.

Det gir mindre fleksibilitet på kort sikt, men også mindre risiko for at like tilfeller registreres ulikt.


---

## 23. Hvorfor serier kan ligge på ulike nivåer

Prosjektet har skilt mellom to hovedtyper serier i fase 1:
- narrative serier
- forlagsserier

Disse hører ikke hjemme på samme nivå i WEMI-strukturen.

Narrative serier beskriver verkets fortellingsmessige tilknytning og hører derfor til `Work`.

Forlagsserier beskriver en konkret publiserings- eller utgavekontekst og hører derfor til `Manifestation`.

Dette gjør modellen mer presis, men også mer krevende enn en løsning der “serie” bare er ett generelt felt.


---

## 24. Hvorfor SeriesMembership er en egen koblingsentitet

Serietilknytning er ikke bare en ren M2M-relasjon.

Et medlemskap i en serie kan også ha egne egenskaper, særlig:
- nummerering
- visningsform
- senere eventuelt annen kontekst

Derfor er `SeriesMembership` modellert som egen entitet.

Dette gjør det mulig å holde selve serien adskilt fra opplysninger som gjelder et bestemt medlemskap.


---

## 25. Hvorfor part_number og part_display ligger på medlemskapet

Nummerering er ikke en egenskap ved serien som abstrakt størrelse, men ved forholdet mellom serien og et bestemt verk eller en bestemt manifestasjon.

Derfor ligger:
- `part_number`
- `part_display`

på `SeriesMembership`, ikke på `Series`.

Dette gir bedre semantisk presisjon og mer fleksibilitet i visning og sortering.


---

## 26. Hvorfor WorkRelationship er eksplisitt og retningsbestemt

Relasjoner mellom verk er ikke bare “koblet eller ikke koblet”.

Prosjektet ønsker å uttrykke hva slags forhold som finnes mellom to verk, og i hvilken retning det forstås.

Derfor er `WorkRelationship` modellert som eksplisitt relasjonsentitet med kontrollert relasjonstype.

Dette gjør det mulig å uttrykke forbindelser som:
- adaptasjon
- inspirert av
- videreføring
- basert på

Samtidig krever dette strengere praksis, fordi retning og relasjonstype må brukes konsekvent for at dataene skal bli meningsfulle.


---

## 27. Hvorfor Agent er samlet for personer og kollektive agenter

Prosjektet har valgt én samlet `Agent`-entitet i fase 1.

Dette er en bevisst operativ komprimering av LRM-strukturen, der `Agent` er superklasse for:
- `Person`
- `Collective Agent`

I databasen modelleres dette foreløpig som:
- én `Agent`-tabell
- ett kontrollert felt `agent_type`

I fase 1 brukes:
- `person`
- `collective_agent`

Hvorfor dette er valgt:
- det gir en enklere og mer konsekvent relasjonsmodell
- samme bidragsstruktur kan brukes på tvers av aktørtyper
- det reduserer behovet for parallelle tabeller og særlogikk i en tidlig prosjektfase

Hvorfor dette ikke er formulert som `person` + `organization`:
- LRM bruker `collective agent`, ikke `organization`, som overordnet kategori
- `collective_agent` er bredere og mer semantisk presist
- kategorien kan omfatte blant annet organisasjoner, familier, konferanser, grupper, regjeringer og andre navngitte kollektive enheter

Konsekvensen er at modellen i fase 1 er enklere enn full LRM-subklassestruktur, men ikke semantisk frakoblet LRM/RDA.

Dette gjør det også lettere å splitte ut egne tabeller senere dersom prosjektet på et senere tidspunkt trenger tydelig ulike attributtsett for personer og kollektive agenter.


---

## 28. Hvorfor rolle ligger i relasjonen, ikke på Agent

At rolle ligger i `Contribution` og ikke på `Agent`, er et grunnleggende designvalg.

En aktør har ikke én rolle i seg selv. Rollen oppstår i forhold til noe:
- forfatter av et verk
- oversetter av en expression
- forlag for en manifestation
- giver til et item

Dette er en klassisk relasjonell fordel ved modellen.

Det gjør også at samme aktør kan ha flere roller uten at agentposten må dupliseres eller forvrenges.


---

## 29. Hvorfor Contribution får bred anvendelse i modellen

`Contribution` brukes på flere nivåer i modellen fordi prosjektet ønsker en konsekvent måte å uttrykke aktør + rolle + målentitet på.

Dette gir en samlet relasjonslogikk for:
- verkroller
- realiseringsroller
- utgaveroller
- strukturert proveniens

Fordelen er høy intern konsistens.

Ulempen er at registreringspraksisen må være tydelig, ellers kan samme type rolle bli lagt på feil nivå.


---

## 30. Hvorfor `wikidata_id` støttes tidlig, men generell identifikatorstruktur utsettes

Prosjektet ønsker å støtte minst én praktisk ekstern identifikator i fase 1, og `wikidata_id` er valgt som den viktigste.

Dette gir en nyttig kobling mot et bredt eksternt økosystem uten å kreve at hele modellen fra start bygges rundt omfattende identifikator- og URI-strukturer.

Samtidig er mer generell identifikatorstruktur utsatt fordi den lett kan trekke med seg:
- flere felter
- uklare prioriteringer
- større autoritetsarbeid
- behov for mer omfattende governance

Dette er derfor et eksempel på selektiv tidlig støtte heller enn full identifikatorstrategi.


---

## 31. Hvorfor `Nomen`, `Place` og `Time-span` ikke modelleres som egne entiteter i fase 1

IFLA LRM modellerer `Nomen`, `Place` og `Time-span` som egne entiteter.

Prosjektet velger likevel å ikke innføre full struktur for disse i fase 1.

Dette er et pragmatisk avgrensningsvalg, ikke en faglig avvisning av LRM.

Hvorfor de utsettes:
- fase 1 trenger en byggbar og håndterbar kjerne
- full støtte for appellasjoner, steder og tidsutstrekninger ville utvide modell- og registreringsarbeidet betydelig
- flere av de konkrete bruksområdene for disse entitetene er relevante, men ikke nødvendige for første operative versjon

Dette gjelder særlig:
- variantnavn, pseudonymer og alternative titler (`Nomen`)
- strukturert stedsmodellering (`Place`)
- generisk modellering av tidsutstrekninger (`Time-span`)

Prosjektet ønsker likevel å holde disse utvidelsene åpne.

Derfor skal fase-1-felt som midlertidig representerer slike opplysninger:
- være atomiske
- være semantisk avgrensede
- ikke blande flere typer informasjon i samme verdi
- navngis og brukes slik at senere migrering til egne entiteter kan skje uten semantisk brudd

Dette betyr at fase 1 kan bruke enklere operative tekst- eller årsfelt, men ikke på en måte som låser modellen bort fra senere LRM-nær utvidelse.

---

## 32. Hvorfor fase-1-navn og titler må forstås som foretrukne visningsformer

Når prosjektet i fase 1 bruker felt som `name` eller foretrukket tittel, skal disse forstås som operative visningsformer.

De er ikke en full modellering av LRM-entiteten `Nomen`.

Det betyr blant annet at fase 1 foreløpig ikke forsøker å modellere:
- variantnavn
- pseudonymer
- alternative titler
- autoriserte tilgangspunkter
- komplette appellasjonsnettverk mellom entitet og navneformer

Denne avgrensningen er valgt for å holde fase 1 enkel.

Samtidig er det viktig at slike felt ikke behandles som om de var full identitetsstruktur.

Dette har flere konsekvenser:
- tekstlikhet alene må ikke brukes som endelig identitetslogikk
- ett fase-1-navn betyr ikke at entiteten bare har én gyldig appellasjon
- senere nomen-støtte må kunne legges til uten at eksisterende felt må omfortolkes

Denne tankegangen gjelder særlig for:
- `Agent.name`
- `Character.name`
- foretrukne tittel- eller navnefelt på andre entiteter

---

## 33. Hvorfor VIAF er utsatt

At `viaf_id` ikke er med som eget fase-1-felt, betyr ikke at VIAF er uviktig.

Det betyr at prosjektet ikke ønsker å låse fase 1 til en bredere identifikatorstrategi før det faktisk er nødvendig.

Dette gir en strammere start og mindre modellstøy.

Samtidig holdes muligheten åpen for at VIAF eller andre identifikatorer kan komme senere når behovet er tydeligere.


---

## 34. Hvorfor kontrollerte koder prioriteres før direkte eksterne URI-er

Prosjektet har valgt å bruke stabile lokale koder i fase 1 for sentrale semantiske kategorier.

Dette gjelder blant annet:
- roller
- relasjonstyper
- expression_type
- series_type
- sjanger
- appellfaktorer

Dette valget gjør fase 1 enklere å kontrollere og lettere å få konsistent.

Samtidig bevarer det en viktig linked-data-retning, fordi kodene er ment å kunne mappes entydig til eksterne vokabularer senere.

Dette er en mellomposisjon mellom:
- helt lokal semantikk uten interoperabilitet
- full URI-basert modell fra første dag

Prosjektet har vurdert denne mellomposisjonen som mest realistisk og mest robust i tidlig fase.


---

## 35. Hvorfor workflow-felter er utsatt fra kjernemodellen

Prosjektet ser et sannsynlig framtidig behov for arbeidsflyt knyttet til:
- staging
- verifisering
- låsing
- kvalitetssikring
- intern redigering

Likevel er slike workflow-felter holdt utenfor fase-1-kjernen.

Grunnen er at disse feltene tilhører arbeidsprosess og styring av datainnhenting, ikke den bibliografiske kjernemodellen.

Å holde dette utenfor kjernen gir:
- tydeligere bibliografisk modell
- mindre risiko for at arbeidsflytlogikk griper inn i grunnstrukturen
- lettere framtidig skille mellom datalag og arbeidsflater

Dette betyr ikke at slike behov er små. Tvert imot kan de bli viktige senere. Men prosjektet ønsker ikke å la dem definere kjernemodellen for tidlig.


---

## 36. Lagdelt kildestrategi som designretning

Prosjektet ser for seg en framtidig lagdelt kildestrategi.

Tanken er at data i systemet over tid kan komme fra flere nivåer, for eksempel:
- importerte bibliografiske grunnposter
- lokale kuraterte tilføyninger
- autoritetsnære koblinger
- formidlings- og navigasjonslag

Dette er ikke ferdig implementert modellarkitektur i fase 1.

Det er en designretning som påvirker hvordan modellen tenkes:
- kjernen bør være stabil
- senere lag bør kunne legges til uten å bryte kjernen
- systemet bør tåle at ulike datatyper har ulik grad av autoritet og kuratering

Denne retningen er viktig for å forstå hvorfor modellen både er stram i kjernen og åpen i periferien.


---

## 37. Staging som framtidig arbeidslag

Staging er ikke en del av den normative fase-1-modellen, men framstår som en sannsynlig framtidig komponent.

Et framtidig staging-lag kan være relevant for:
- import og mellomlagring
- kvalitetssikring før publisering
- sammenstilling av data fra flere kilder
- kontroll før noe blir del av den operative katalogstrukturen

Dette er viktig fordi prosjektet trolig ikke bare skal håndtere manuelt registrerte data, men også mer sammensatte dataløp over tid.

At staging ikke er med nå, betyr derfor ikke at tanken er forlatt. Den er bare holdt utenfor kjernemodellen.


---

## 38. Offentlig portal og administrativ flate som ulike behov

Prosjektet peker mot et framtidig skille mellom minst to ulike brukerflater:
- en offentlig portal for utforsking, søk og formidling
- en administrativ flate for registrering, kvalitetssikring og intern kontroll

Dette skillet er viktig fordi de to flatene har ulike behov:
- offentlig portal trenger god navigasjon, relasjonsvisning og formidling
- administrativ flate trenger presisjon, kontroll og arbeidsflyt

Modellen prøver å være et felles fundament for begge, uten at én av flatene helt får definere strukturen alene.


---

## 39. Det “levende biblioteket” som produktidé

Tanken om et “levende bibliotek” er en viktig produktidé i prosjektet.

Med dette menes et bibliotek som ikke bare presenterer statiske katalogposter, men som gjør det mulig å bevege seg gjennom forbindelser som:
- relaterte verk
- serier
- karakterer
- sjanger
- appellfaktorer
- ulike uttrykk og utgaver

Denne idéen forklarer mye av prosjektets vilje til å modellere flere relasjonstyper og navigerbare entiteter allerede i fase 1, selv når enklere løsninger kunne vært valgt.

Det er likevel viktig å forstå at dette foreløpig er en designretning og produktvisjon, ikke en ferdig implementert funksjonalitet.


---

## 40. Hvorfor fase 1 bevisst holder igjen enkelte ting

Flere ting er bevisst utsatt i fase 1:
- generell identifikatorstruktur
- rike autoritetsdata
- variantnavn flere steder
- synonymstruktur
- mer avansert relasjonsmetadata
- workflow-felter
- sirkulasjonslogikk
- mer detaljerte koblingstyper i noen koblingstabeller

Dette er ikke tilfeldig.

Prosjektet prøver å gjøre fase 1 smal nok til å være gjennomførbar, men rik nok til at videre utvikling ikke krever at grunnmodellen veltes.

Med andre ord:
fase 1 er ikke “minimum mulig modell”, men en selektivt beskyttet kjerne.


---

## 41. Hva slags type prosjekt dette egentlig er

Krimbiblioteket er ikke bare et katalogprosjekt og ikke bare et formidlingsprosjekt.

Det er et hybridprosjekt som prøver å kombinere:
- bibliografisk presisjon
- kuratert modellering
- framtidig navigasjon og utforsking
- gradvis utvidbarhet

Denne prosjektkarakteren er viktig å ha med seg når man vurderer modellvalg. Mange valg som kan virke “for store” for en enkel katalog, gir mer mening når målet også er å bygge grunnlag for et rikere litterært og formidlingsorientert system.


---

## 42. Hvordan dette dokumentet bør brukes videre

Dette dokumentet bør brukes når prosjektet trenger å:
- forklare hvorfor et valg ble tatt
- bevare resonnement som ikke bør ligge i ADR eller invariants
- skille mellom fase-1-kjerne og framtidig retning
- dokumentere hva modellen prøver å beskytte på lengre sikt

Det bør ikke brukes som eneste sannhetskilde for konkrete modellregler.

Hvis noe i dette dokumentet kommer i konflikt med:
- `ADR.md`
- `model_invariants.md`
- `modelling_rules_phase1.md`

skal de normative dokumentene ha forrang.