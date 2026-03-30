# Architecture Decision Log (ADR)

Dette dokumentet registrerer viktige arkitekturvalg i prosjektet **Krimbiblioteket**.

Hensikten er å dokumentere **hva som er besluttet og hvorfor**, slik at beslutningene kan forstås og etterprøves senere.

Formatet følger en enkel ADR-struktur:

- Context
- Decision
- Consequences

---

# ADR-001

## WEMI som kjernemodell

### Context

Prosjektet ønsker å følge etablerte bibliotekfaglige modeller og støtte avansert bibliografisk struktur.

En enkel boktabell ville ikke støtte blant annet:

- oversettelser
- adaptasjoner
- samlingsverk
- flere utgaver
- ulike medier

### Decision

Systemet implementerer en LRM-inspirert WEMI-struktur:

`Work → Expression → Manifestation → Item`

Dette er prosjektets grunnleggende bibliografiske kjernemodell.

### Consequences

**Fordeler**
- korrekt bibliotekfaglig modell
- støtte for oversettelser, adaptasjoner og flere medier
- tydelig skille mellom abstrakt verk, realisering, utgave og eksemplar

**Ulemper**
- mer kompleks modell
- flere relasjoner i databasen
- høyere registrerings- og modelleringsfriksjon enn i en flat modell

Beslutningen anses som arkitekturkritisk og stabil.

---

# ADR-002

## Expression–Manifestation modelleres som M2M via ExpressionManifestation

### Context

Prosjektet må støtte både det vanlige mønsteret der én `Expression` materialiseres i flere `Manifestations`, og særtilfeller der én `Manifestation` inneholder flere `Expressions`.

Dette gjelder blant annet:

- samlingsverk
- antologier
- samleutgaver / omnibusutgaver
- samme `Expression` i flere `Manifestations`

En ren direkte 1:M-modell ville ikke støtte dette tilstrekkelig.

### Decision

Relasjonen mellom `Expression` og `Manifestation` modelleres gjennom en eksplisitt koblingstabell:

`ExpressionManifestation`

I fase 1 har tabellen følgende felter:

- `id`
- `expression`
- `manifestation`
- `is_primary`

Følgende regler fryses:

- relasjonen er formelt M2M
- samme kombinasjon av `expression` og `manifestation` kan ikke registreres flere ganger
- en `Manifestation` kan ha flere `Expressions`
- samme `Expression` kan forekomme i flere `Manifestations`
- en `Manifestation` kan ha **maks én** primærkobling
- vanlige utgaver skal normalt ha én primærkobling
- antologier og enkelte samleutgaver kan ha ingen primærkobling
- rekkefølge / sekvens utsettes
- koblingstype / relasjonsrolle utsettes

Normalmønsteret i praksis er fortsatt ofte:

- én `Manifestation` til én `Expression`
- én `Expression` til flere `Manifestations`

### Consequences

**Fordeler**
- støtter antologier, samlingsverk og omnibusutgaver
- støtter både vanlige og mer komplekse bibliografiske situasjoner
- gir eksplisitt og utvidbar modellering av en viktig relasjon
- gjør det mulig å markere primærkobling uten å låse alle tilfeller til ett hoveduttrykk

**Ulemper**
- mer kompleks modell enn en enkel FK-løsning
- krever tydelige modelleringsregler for grensen mellom bibliografisk sammenstilling og nytt `Work`
- gir én ekstra koblingstabell i kjernen

---

# ADR-003

## Generisk bidragssystem: Agent / Role / Contribution

### Context

Bibliografiske og samlingsrelaterte relasjoner mellom aktører og entiteter kan være mange og ligge på ulike nivåer i modellen.

Eksempler:

- forfatter på `Work`
- oversetter på `Expression`
- innleser på `Expression`
- forlag på `Manifestation`
- tidligere eier eller giver på `Item`

Separate rollefelter per tabell ville blitt lite fleksibelt og vanskelig å utvide.

### Decision

Bidrag modelleres gjennom tre tabeller:

- `Agent`
- `Role`
- `Contribution`

`Contribution` er koblingstabellen mellom:

- `Agent`
- én målentitet
- én rolle

I fase 1 kan `Contribution` kobles til:

- `Work`
- `Expression`
- `Manifestation`
- `Item`

Én rad i `Contribution` skal peke til **nøyaktig én** av disse målentitetene.

Når `Contribution` brukes på `Item`, er dette i fase 1 primært for strukturert proveniens, for eksempel:

- tidligere eier
- giver
- annen navngitt proveniensaktør

Aktiv låner, utlånshistorikk og annen sirkulasjonslogikk modelleres ikke gjennom `Contribution` i fase 1.

### Consequences

**Fordeler**
- én konsistent modell for bidrag på tvers av nivåer
- roller knyttes til relasjonen, ikke feilaktig til agenten alene
- støtter både personer og organisasjoner
- støtter strukturert proveniens på `Item` når det gir merverdi
- gir godt grunnlag for senere linked-data-mapping og utvidelser

**Ulemper**
- mer kompleks spørring enn egne rollefelter
- flere nullable mål-felter i `Contribution`
- krever tydelige modelleringsregler for bruk av roller og `Item`-bidrag

---

# ADR-004

## Series kan knyttes til Work eller Manifestation

### Context

Serier kan representere ulike konsepter som hører hjemme på ulike nivåer i modellen.

Eksempler:

- narrative serier
- forlagsserier

Det var nødvendig å støtte begge uten å tvinge alle serier inn på samme nivå.

### Decision

`SeriesMembership` kan kobles til:

- `Work`
- `Manifestation`

I fase 1 brukes `Series` for minst to serietyper:

- `narrative`
- `publisher_series`

Dette innebærer at:

- narrative serier ligger på `Work`
- forlagsserier ligger på `Manifestation`

### Consequences

**Fordeler**
- korrekt modellering av ulike serietyper
- tydelig skille mellom fortellingsmessig og publiseringsrelatert serie
- støtter videre formidling og gjenfinning

**Ulemper**
- litt mer kompleks modell
- noen grensetilfeller må styres gjennom modelleringsregler

---

# ADR-005

## Character modelleres som egen entitet på Work-nivå

### Context

Kriminallitteratur er ofte sterkt karakterdrevet, og karakterbasert navigasjon er en viktig formidlingsmulighet.

Det måtte avklares om karakterer skulle være fritekst eller egen gjenbrukbar entitet.

### Decision

Karakterer modelleres som egen entitet:

`Character`

Karakterer kobles til `Work`, ikke til `Expression`, `Manifestation` eller `Item`.

### Consequences

**Fordeler**
- mulig å navigere etter karakter
- mulig å koble karakterer på tvers av verk
- mulig å gjenbruke samme karakter på tvers av forfattere og relaterte verk

**Ulemper**
- krever egen koblingsmodell
- navnevariasjoner må håndteres gjennom registreringspraksis i fase 1
- mer avansert karaktermodell må komme senere dersom behovet oppstår

---

# ADR-006

## Kun sentrale identifikatorer i fase 1

### Context

Det finnes mange eksterne identifikatorer, og en generell identifikatorstruktur ville gjøre systemet mer komplekst i første fase.

Prosjektet måtte avgrense hvilke identifikatorer som faktisk skulle få egne operative felter i fase 1.

### Decision

I fase 1 brukes egne felter for et begrenset sett sentrale identifikatorer.

I den nåværende fase-1-modellen gjelder dette eksplisitt blant annet:

- `wikidata_id`
- `isbn`
- `nb_sesamid`

`wikidata_id` støttes eksplisitt i fase 1 som identifikator på relevante entiteter der dette er valgt.

VIAF og andre identifikatorer utsettes til senere struktur.

### Consequences

**Fordeler**
- enklere implementasjon
- enklere spørringer
- lavere kompleksitet i fase 1

**Ulemper**
- mindre fleksibelt enn en generell identifikatorstruktur
- senere utvidelser krever egen modell eller mappinglag

Generell identifikatorstruktur kan legges til senere.

---

# ADR-007

## Workflow-felter utsatt fra fase 1

### Context

Felter som:

- `is_locked`
- `is_manually_verified`
- `metadata_provenance`

tilhører arbeidsflyt, staging og styring av datainnhenting, ikke den bibliografiske kjernemodellen.

### Decision

Workflow-felter implementeres ikke i fase 1.

### Consequences

**Fordeler**
- enklere modell
- tydeligere skille mellom bibliografisk kjerne og arbeidsflyt
- mindre kompleksitet i første versjon

**Ulemper**
- staging- og verifiseringslogikk må legges til senere
- enkelte arbeidsprosesser må i mellomtiden håndteres uten egne modellfelter

---

# ADR-008

## Lokale modelleringsregler etableres for fase 1

### Context

Mange bibliografiske beslutninger kan ikke løses bare gjennom databasedesign.

Eksempler:

- når noe er nytt `Work`
- når noe er nytt `Expression`
- når noe er ny `Manifestation`
- hvordan særtilfeller og grensetilfeller skal håndteres

### Decision

Prosjektet etablerer et eget dokument for lokale modelleringsregler i fase 1.

### Consequences

**Fordeler**
- konsistent registreringspraksis
- tydeligere skille mellom databasedesign og registreringsregler
- lettere å forstå og videreføre modellen senere

**Ulemper**
- krever vedlikehold av et eget normativt praksisdokument
- databasen alene kan ikke bære all semantikk

---

# ADR-009

## UUID brukes som primærnøkler på hovedentiteter

### Context

Systemet vil over tid kunne integrere data fra eksterne kilder og senere bli utvidet med import, API-er eller migrasjoner.

Tradisjonelle auto-increment-nøkler er mindre robuste i slike scenarier.

### Decision

Hovedentiteter i databasen bruker UUID som primærnøkkel.

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

Koblingstabeller kan også ha egen `id` når dette er valgt som konsekvent mønster i modellen.

### Consequences

**Fordeler**
- stabil identitet på tvers av miljøer og importer
- enklere fremtidig sammenslåing og migrering
- mindre risiko for nøkkelkollisjoner

**Ulemper**
- mindre lesbare nøkler
- noe mer tungvint ved manuell inspeksjon og debugging

---

# ADR-010

## Kontrollerte semantiske kategorier representeres med stabile lokale koder

### Context

Prosjektet bruker flere kontrollerte semantiske kategorier, blant annet:

- språk
- `expression_type`
- `series_type`
- `relation_type`
- rollekoder
- sjangerkoder
- appellfaktorkoder

Prosjektet trenger stabil intern bruk, men ønsker samtidig å kunne mappe til eksterne vokabularer senere.

### Decision

Kontrollerte semantiske kategorier representeres i fase 1 med **stabile lokale koder**.

Kodene skal kunne mappes entydig til relevante eksterne vokabularer eller autoritetsregistre senere.

I fase 1 lagres normalt ikke eksterne URI-er direkte i alle operative tabeller.

### Consequences

**Fordeler**
- stabil og kontrollerbar intern semantikk
- enklere fase-1-modell
- mindre avhengighet av eksterne URI-strukturer i den operative databasen
- godt grunnlag for senere mapping og interoperabilitet

**Ulemper**
- mappinglaget må bygges senere
- man får ikke full linked-data-struktur direkte i fase 1

---

# ADR-011

## Genre modelleres som kontrollert Work-taksonomi

### Context

Sjanger beskriver verkets innhold og fortellingsform, og hører derfor til på `Work`-nivå.

Prosjektet trenger kontrollert sjangerbruk, støtte for flere sjangre per verk og eksplisitt hierarki.

### Decision

`Genre` modelleres som egen entitet med stabile lokale koder.

I fase 1 har `Genre` følgende felter:

- `code`
- `label`
- `parent_genre`

Koblingen mellom `Work` og `Genre` modelleres som egen koblingstabell:

`WorkGenre`

I fase 1 har `WorkGenre` følgende felter:

- `id`
- `work`
- `genre`

Følgende regler fryses:

- `Genre` ligger på `Work`-nivå
- ett `Work` kan ha flere sjangre
- samme kombinasjon av `work` og `genre` kan ikke registreres flere ganger
- hierarki er eksplisitt med i fase 1
- eksterne URI-er utsettes

### Consequences

**Fordeler**
- kontrollert og gjenbrukbar sjangermodell
- støtte for krysskategorisering
- støtte for eksplisitt sjangerhierarki
- godt grunnlag for senere mapping og videreutvikling

**Ulemper**
- krever vedlikehold av eget sjangervokabular
- grensene mot appellfaktor og tematikk må styres gjennom modelleringsregler

---

# ADR-012

## AppealFactor modelleres som kontrollert Work-vokabular

### Context

Appellfaktorer beskriver leseropplevelse og fortellingskarakter, og hører derfor til på `Work`-nivå.

Prosjektet ønsker å støtte appellfaktorer i tråd med lesersørvis-metodikk, med overordnede appellfaktorer og underordnede appelltermer.

### Decision

`AppealFactor` modelleres som egen entitet med stabile lokale koder.

I fase 1 har `AppealFactor` følgende felter:

- `code`
- `label`
- `parent_appeal_factor`
- `definition`
- `scope_note`

Koblingen mellom `Work` og `AppealFactor` modelleres som egen koblingstabell:

`WorkAppealFactor`

I fase 1 har `WorkAppealFactor` følgende felter:

- `id`
- `work`
- `appeal_factor`

Følgende regler fryses:

- `AppealFactor` ligger på `Work`-nivå
- ett `Work` kan ha flere appellfaktorer
- samme kombinasjon av `work` og `appeal_factor` kan ikke registreres flere ganger
- hierarki er eksplisitt med i fase 1
- `definition` og `scope_note` er med i fase 1
- synonymer utsettes som operativ fase-1-funksjonalitet
- modellen skal tåle synonymstruktur senere
- eksterne URI-er utsettes
- prioritet / styrkegrad på koblingen utsettes

### Consequences

**Fordeler**
- støtte for strukturert appellbeskrivelse
- kompatibelt med lesersørvis-orientert vokabulararbeid
- eksplisitt hierarki og definisjonsstøtte fra start
- godt grunnlag for senere synonymforvaltning

**Ulemper**
- krever vedlikehold av eget appellvokabular
- grensene mot sjanger og tematikk må styres i modelleringsreglene
- synonymstruktur må legges til senere dersom den skal brukes operativt

---

---

# ADR-013

## Manifestation kan ha eget title-felt i fase 1

### Context

Under implementasjonen ble det tydelig at `Manifestation` ikke alltid kan identifiseres godt nok bare gjennom ISBN, år og kobling til uttrykk.

Noen utgaver har en egen manifestation-identitet som bør kunne uttrykkes eksplisitt i modellen.

Dette gjelder særlig:
- antologier
- samleutgaver
- manifestasjoner med flere expressions
- andre sammensatte utgivelser

Prosjektet måtte derfor ta stilling til om `Manifestation` skulle kunne ha eget tittelfelt i fase 1.

### Decision

`Manifestation` får eget valgfritt felt:

- `title`

Feltet brukes når utgaven har en egen tittel eller tydelig manifestation-identitet.

Feltet er valgfritt og skal ikke tvinges brukt i vanlige enkelttilfeller der det ikke tilfører presisjon.

### Consequences

**Fordeler**
- bedre bibliografisk presisjon
- bedre brukbarhet i admin og grensesnitt
- tydeligere identifikasjon av sammensatte utgaver

**Ulemper**
- litt rikere manifestation-modell i fase 1
- krever skjønn i registreringspraksis

Valget endrer ikke nivåplasseringen i WEMI.
Et manifestation-spesifikt tittelfelt er fortsatt manifestation-nivå, ikke work- eller expression-nivå.

---

---

# ADR-014

## WorkRelationship registreres med fast retning fra source til target og leses fra target til source

### Context

`WorkRelationship` er en retningsbestemt verkrelasjon.

Under implementasjonen ble det tydelig at feltnavn alene ikke er nok til å sikre konsistent registrering og lesing. Uten en fast regel er det stor risiko for at like relasjoner registreres i motsatt retning.

Prosjektet måtte derfor avklare både semantisk retning og praktisk lesemåte.

### Decision

I fase 1 forstås:

- `source_work` som det primære eller opphavlige verket
- `target_work` som det sekundære eller avledede verket

Relasjonen skal leses slik:

- `target_work` (`relation_type`) `source_work`

Eksempel:
- tegneserieversjonen `adaptation_of` romanverket

Konsekvens for vokabular:
- `relation_type` skal formuleres i denne retningen
- bruk koder som:
  - `adaptation_of`
  - `translation_of`
  - `abridgement_of`
  - `graphic_novelization_of`
- ikke koder som:
  - `adapted_as`
  - `translated_into`
  - `has_adaptation`

### Consequences

**Fordeler**
- konsistent registreringspraksis
- mindre risiko for speilvendte dubletter
- tydeligere semantikk i admin, søk og videre modellarbeid

**Ulemper**
- krever eksplisitt dokumentasjon og brukeropplæring
- er ikke nødvendigvis intuitivt ved første møte med feltnavnene

Denne retningen er en del av den operative fase-1-modellen og skal støttes i dokumentasjon og admin.