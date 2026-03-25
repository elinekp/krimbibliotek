# Modelleringsregler — fase 1

Dette dokumentet beskriver praktisk modellerings- og registreringspraksis for fase 1 i Krimbiblioteket.

Formålet er å sikre konsistent bruk av datamodellen i tilfeller der databasen alene ikke avgjør hvordan noe bør registreres.

Dette dokumentet beskriver:
- hvordan modellen brukes i praksis
- hvordan nivåvalg håndteres i tvilstilfeller
- hvordan kontrollerte koder og vokabularer brukes i fase 1
- hvordan grensetilfeller skal forstås innenfor den fryste modellen

Dette dokumentet beskriver ikke:
- arkitekturbeslutninger og beslutningshistorikk
- harde invariants og databasekrav
- roadmap eller prosjektstatus
- lange designresonnementer


---

## 1. Overordnet praksis i fase 1

### 1.1 Bruk den fryste modellen, ikke lokale snarveier

Når et tilfelle er vanskelig, skal det løses innenfor den vedtatte modellen.

Det betyr blant annet:
- ikke hopp over nivåer i WEMI-strukturen
- ikke legg inn midlertidige fritekstløsninger der modellen allerede har en strukturert løsning
- ikke utvid tabeller ad hoc for å håndtere enkelttilfeller

Hvis et tilfelle ikke passer tydelig innenfor disse reglene, er det et modelleringsspørsmål som må avklares eksplisitt.


### 1.2 Kontrollerte semantiske kategorier registreres med stabile lokale koder

I fase 1 brukes stabile lokale koder for kontrollerte semantiske kategorier.

Dette gjelder blant annet:
- `expression_type`
- `series_type`
- `relation_type`
- `role`
- `Genre.code`
- `AppealFactor.code`

Kodene skal brukes konsekvent og ikke erstattes av fri tekst i operative registreringer.

Eksterne URI-er brukes normalt ikke direkte i operative tabeller i fase 1.


### 1.3 Grensetilfeller løses gjennom praksis, ikke gjennom databasen alene

Databasen avgjør ikke alene:
- hva som er nytt `Work`
- hva som er ny `Expression`
- hva som er ny `Manifestation`

Slike spørsmål må avgjøres gjennom katalogiseringsfaglig vurdering og konsekvent praksis.


---

## 2. Work og Expression

### 2.1 Oversettelser registreres som ny Expression av samme Work

En oversettelse registreres som ny `Expression` av samme `Work`.

Eksempel:
- originaltekst på svensk = én `Expression`
- norsk oversettelse = én annen `Expression`

Språkforskjellen ligger altså på `Expression`-nivå, ikke på `Work`-nivå.


### 2.2 Lydbok registreres som ny Expression av samme Work

En lydbok registreres som ny `Expression` av samme `Work`.

Dette gjelder også når språk er det samme som i tekstutgaven.

Eksempel:
- `Expression (nor, text)`
- `Expression (nor, spoken_word)`

Tekst og innlest lyd behandles altså som ulike realiseringer av samme verk.


### 2.3 Flere Expressions med samme språk og samme type er tillatt

Det er tillatt å ha flere `Expressions` innenfor samme `Work` med samme:
- `language_code`
- `expression_type`

Dette kan være relevant ved for eksempel:
- sterkt reviderte tekster
- forkortede versjoner
- andre særskilte realiseringer som fortsatt ikke vurderes som nytt `Work`

Slike tilfeller skal håndteres gjennom faglig vurdering, ikke gjennom forenklede tekniske antakelser om at kombinasjonen må være unik.


### 2.4 Filmatisering registreres som nytt Work

En filmatisering registreres som nytt `Work`.

Den skal ikke registreres som bare en ny `Expression` av bokverket.


### 2.5 Grafisk adaptasjon registreres som nytt Work

En grafisk adaptasjon registreres som nytt `Work`.

Den skal ikke automatisk behandles som bare en annen `Expression` av det opprinnelige verket.


### 2.6 Sterkt reviderte tekster må vurderes konkret

Sterkt reviderte tekster vurderes konkret.

Hovedspørsmålet er om vi fortsatt står i samme verkidentitet, eller om endringen er så stor at det bør registreres som nytt `Work`.

Dette avgjøres ikke av databasen alene.


---

## 3. Expression

### 3.1 Språk registreres på Expression

Språk registreres på `Expression`-nivå.

I fase 1 brukes språkkoder konsekvent som kontrollert verdi.

Eksempler:
- `eng`
- `nor`
- `ger`
- `fre`

Språk skal ikke brukes som bærende klassifisering på `Work`, `Manifestation` eller `Item`.


### 3.2 Realiseringstype registreres i expression_type

Realiseringstype registreres i `expression_type`.

Verdien skal være en stabil lokal kode.

Eksempler:
- `text`
- `spoken_word`
- `moving_image`
- `still_image`

Verdiene skal brukes konsekvent og ikke varieres som fritekst.


### 3.3 Bidrag på Expression-nivå brukes for realiseringsrelaterte roller

Roller som gjelder selve realiseringen av verket, registreres på `Expression`.

Typiske eksempler:
- oversetter
- innleser

Dette skiller slike roller fra:
- verkrelaterte roller på `Work`
- utgaverelaterte roller på `Manifestation`


---

## 4. ExpressionManifestation

### 4.1 Expression–Manifestation brukes via koblingstabellen ExpressionManifestation

I fase 1 modelleres relasjonen mellom `Expression` og `Manifestation` via:

- `ExpressionManifestation`

Dette gjelder også i vanlige enkelttilfeller.

Det skal altså ikke brukes en skjult eller alternativ 1:M-praksis ved registrering.


### 4.2 Normalmønsteret er fortsatt enkelt

Selv om modellen formelt er M2M, er normalmønsteret i praksis ofte:

- én `Manifestation` til én `Expression`
- én `Expression` til flere `Manifestations`

Dette er vanlig mønster, men ikke en tvangstrøye for modellen.


### 4.3 Når flere Expressions kan kobles til samme Manifestation

Flere `Expressions` kan kobles til samme `Manifestation` når utgaven faktisk inneholder flere realiseringer eller verkrealiseringer.

Dette kan være relevant for eksempel ved:
- antologier
- samlingsverk
- omnibusutgaver
- samleutgaver med flere separate uttrykk


### 4.4 is_primary brukes for primærkobling når dette gir mening

Feltet `is_primary` brukes for å markere primærkobling når en slik primærkobling faktisk gir mening.

Praktisk regel:
- vanlige utgaver skal normalt ha én primærkobling
- antologier og enkelte samleutgaver kan ha ingen primærkobling

Det skal aldri legges inn flere primærkoblinger for samme `Manifestation`.


### 4.5 Det som utsettes i ExpressionManifestation skal ikke improviseres inn

Fase 1 inkluderer ikke:
- rekkefølge / sekvens
- koblingstype / relasjonsrolle i koblingen

Slike behov skal ikke løses ved å legge inn improviserte ekstrafelt eller fritekst i tabellen.


---

## 5. Manifestation

### 5.1 Manifestation representerer utgavenivået

`Manifestation` representerer den konkrete publiserte utgaven.

Forskjeller i publiseringsform og utgave registreres normalt som ulike `Manifestations`, ikke som nye `Expressions`.


### 5.2 Typiske ulike Manifestations av samme Expression

Følgende registreres normalt som ulike `Manifestations` av samme `Expression`:
- hardcover
- paperback
- epub
- pdf

Dette er utgave- eller publiseringsnivå, ikke realiseringsnivå.


### 5.3 Identifikatorer på Manifestation i fase 1

I fase 1 registreres følgende identifikatorer på `Manifestation` når de finnes:
- `isbn`
- `nb_sesamid`

Disse brukes som identifikatorer for utgavenivået.


### 5.4 Forlag hører til Manifestation-nivået

Forlag hører til `Manifestation`.

I fase 1 modelleres dette via `Contribution` / `Agent`, ikke som eget fritekstfelt.


### 5.5 Forlagsserier hører til Manifestation-nivået

Når en serie er en forlagsserie, registreres serietilknytningen på `Manifestation`-nivå, ikke på `Work`.

Dette skjer via `SeriesMembership`.


---

## 6. Item

### 6.1 Item brukes bare for eksemplarspesifikke data

`Item` representerer det individuelle eksemplaret.

I fase 1 brukes `Item` bare for data som faktisk gjelder det konkrete eksemplaret.

Eksempler:
- `shelf_location`
- `provenance_notes`
- lokale eksemplarnotater

Bibliografiske forhold ved utgaven skal ikke flyttes ned på `Item`.


### 6.2 Proveniens kan registreres enkelt eller strukturert

I enkle tilfeller er `provenance_notes` tilstrekkelig.

Når proveniens eller annen copy-specific agentrelasjon har tydelig verdi for søk, dokumentasjon eller navigasjon, kan den registreres strukturert via `Contribution` på `Item`.

Typiske tilfeller:
- tidligere eier
- giver
- annen navngitt proveniensaktør


### 6.3 Item brukes ikke for sirkulasjonslogikk i fase 1

Fase 1 inkluderer ikke modellering av:
- aktiv låner
- utlånshistorikk
- annen sirkulasjonslogikk

Slike behov skal ikke bygges inn i `Item` eller `Contribution` i denne fasen.


---

## 7. Work

### 7.1 Sjanger registreres på Work

Sjanger registreres på `Work`-nivå.

Sjanger beskriver fortellingen og verkets innholdsmessige identitet, ikke en bestemt utgave eller realisering.

Samme verk kan ha flere sjangre.


### 7.2 Appellfaktorer registreres på Work

Appellfaktorer registreres på `Work`-nivå.

Appellfaktorer beskriver leseopplevelse og fortellingskarakter, ikke språkversjon eller utgave.

Samme verk kan ha flere appellfaktorer.


### 7.3 Karakterer registreres på Work

Karakterer registreres på `Work`-nivå.

De skal ikke kobles til:
- `Expression`
- `Manifestation`
- `Item`

I fase 1 bør registrering primært brukes for karakterer med tydelig verdi for søk, filtrering eller navigasjon.


### 7.4 Verkrelasjoner registreres mellom Work og Work

Relasjoner mellom verk registreres gjennom `WorkRelationship`.

Dette brukes bare mellom to `Work`-poster.

Eksempler på relasjonstyper kan være:
- adaptasjon av
- inspirert av
- videreføring av
- basert på

Retningsvalg og bruk av relasjonstyper må være konsekvent i praksis.


---

## 8. Genre og WorkGenre

### 8.1 Genre er kontrollert vokabular, ikke fri tagging

`Genre` brukes som kontrollert Work-taksonomi.

I fase 1 brukes:
- `code`
- `label`
- `parent_genre`

Sjanger skal ikke registreres som løs, ukontrollert fritekst når formålet er å uttrykke modellens sjangerstruktur.


### 8.2 WorkGenre brukes for koblingen mellom Work og Genre

Koblingen mellom `Work` og `Genre` går via:
- `WorkGenre`

Samme sjanger skal ikke registreres flere ganger på samme verk.


### 8.3 Hierarki brukes eksplisitt når det er relevant

Sjangervokabularet skal støtte eksplisitt hierarki gjennom `parent_genre`.

Det betyr at over-/underordning skal håndteres i vokabularet, ikke improviseres i etiketter eller notater.


---

## 9. AppealFactor og WorkAppealFactor

### 9.1 AppealFactor brukes som kontrollert Work-vokabular

`AppealFactor` brukes som kontrollert vokabular på `Work`-nivå.

I fase 1 brukes:
- `code`
- `label`
- `parent_appeal_factor`
- `definition`
- `scope_note`

Dette skal brukes som styrt vokabular, ikke som løs fritekstklassifisering.


### 9.2 WorkAppealFactor brukes for koblingen mellom Work og AppealFactor

Koblingen mellom `Work` og `AppealFactor` går via:
- `WorkAppealFactor`

Samme appellfaktor skal ikke registreres flere ganger på samme verk.


### 9.3 Definition og scope_note skal brukes aktivt ved tvilstilfeller

Når appelltermer er vanskelige å skille, skal:
- `definition`
- `scope_note`

brukes som praktisk støtte for konsekvent registrering.

Dette er særlig viktig fordi grensene mellom appellfaktor, sjanger og tematikk ellers kan bli uklare.


### 9.4 Synonymer brukes ikke operativt i fase 1

Synonymer er utsatt som operativ fase-1-funksjonalitet.

Det betyr:
- ingen egen synonymtabell i fase 1
- ingen improvisert synonymhåndtering i operative tabeller

Hvis alternative betegnelser er viktige i praksis, må det håndteres senere i egen struktur.


---

## 10. Character og WorkCharacter

### 10.1 Når Character skal brukes

`Character` brukes når en fiktiv figur skal modelleres som en egen, gjenbrukbar entitet.

Dette er særlig relevant når karakteren:
- går igjen i flere verk
- har tydelig verdi for søk eller navigasjon
- bør behandles som mer enn bare en løs tekstopplysning


### 10.2 Character holdes enkel i fase 1

I fase 1 har `Character` bare:
- `id`
- `name`

Det brukes én foretrukket navneform per karakter.

Variantnavn håndteres ikke som egen struktur i fase 1.


### 10.3 Navnepraksis må være streng

Fordi variantnavn er utsatt, må registreringspraksisen være konsekvent.

Unngå å opprette separate karakterposter for små variasjoner som:
- fullt navn vs. kortform
- alternative stavemåter
- små forskjeller i tegnsetting

Hvis det er tvil om to navn viser til samme karakter, skal dette vurderes eksplisitt før ny post opprettes.


### 10.4 WorkCharacter brukes som ren kobling

Koblingen mellom `Work` og `Character` går via:
- `WorkCharacter`

I fase 1 brukes denne som ren kobling uten ekstra relasjonsmetadata.

Det innføres ikke i fase 1:
- karakterrolle
- prioritet
- note
- kilde
- usikkerhet


---

## 11. Agent, Role og Contribution

### 11.1 Agent brukes for både personer og organisasjoner

`Agent` brukes for både:
- personer
- organisasjoner

I fase 1 har `Agent`:
- `id`
- `name`
- `agent_type`
- `wikidata_id`

`name` forstås som foretrukket navn, ikke som unik identifikator.


### 11.2 Agent type skal brukes konsekvent

`agent_type` er obligatorisk og skal bruke kontrollert verdi.

I fase 1 brukes minst:
- `person`
- `organization`

Verdiene skal ikke erstattes av fritekstvarianter.


### 11.3 wikidata_id kan brukes, VIAF er utsatt

`wikidata_id` kan registreres når den er kjent.

I fase 1 brukes ikke eget felt for `viaf_id`.

Andre identifikatorer og mer generell identifikatorstruktur er utsatt.


### 11.4 Role brukes som kontrollert rollevokabular

`Role` brukes som kontrollert vokabular for agentroller.

I fase 1 har `Role`:
- `code`
- `label`

Rollen skal ligge i relasjonen, ikke på `Agent`.


### 11.5 Contribution brukes for agent + rolle + målentitet

`Contribution` brukes når en `Agent` har en rolle knyttet til en entitet i modellen.

I fase 1 kan `Contribution` kobles til:
- `Work`
- `Expression`
- `Manifestation`
- `Item`

Én rad skal alltid peke til nøyaktig én av disse.


### 11.6 Typisk nivåbruk for Contribution

Som hovedpraksis i fase 1 brukes:
- `Work` for verkrelaterte roller, for eksempel forfatter
- `Expression` for realiseringsrelaterte roller, for eksempel oversetter eller innleser
- `Manifestation` for utgaverelaterte roller, for eksempel forlag
- `Item` for strukturert proveniens når dette gir tydelig merverdi

Ved tvil skal rollen legges på det nivået den faktisk beskriver.


---

## 12. Series og SeriesMembership

### 12.1 Når Series skal brukes

`Series` brukes når en serie skal modelleres som en egen, gjenbrukbar entitet.

I fase 1 brukes `Series` for minst:
- narrative serier
- forlagsserier

Serietilknytning skal ikke reduseres til fritekst når modellen faktisk trenger strukturen.


### 12.2 series_type er obligatorisk og lukket i fase 1

I fase 1 brukes bare:
- `narrative`
- `publisher_series`

Andre serietyper er utsatt.

`character_series` brukes ikke som egen `series_type` i fase 1.


### 12.3 Narrative serier registreres på Work

Når serien uttrykker fortellingsmessig eller verkrelatert tilknytning, registreres den på `Work`-nivå via `SeriesMembership`.


### 12.4 Forlagsserier registreres på Manifestation

Når serien uttrykker publiserings- eller utgaverelatert tilknytning, registreres den på `Manifestation`-nivå via `SeriesMembership`.


### 12.5 part_number og part_display brukes pragmatisk

Når seriemedlemskap har rekkefølge- eller delinformasjon, brukes:
- `part_number` når strukturen er tallmessig og tydelig
- `part_display` når visningsformen bør bevares som tekst

Eksempler:
- `part_number = 1`, `part_display = Del 1`
- `part_number = 2`, `part_display = Bok 2`
- `part_number = null`, `part_display = Del II`
- `part_number = null`, `part_display = null`

Begge felt kan være nyttige samtidig når både sortering og visning er viktig.


### 12.6 Dette gjøres ikke i fase 1

Fase 1 inkluderer ikke:
- `context_note` på `SeriesMembership`
- seriehierarki som `parent_series`
- variantnavn på `Series`
- egne serietyper utover `narrative` og `publisher_series`

Hvis et tilfelle ikke passer rent i fase-1-modellen, skal det løftes som modelleringsspørsmål.


---

## 13. WorkRelationship

### 13.1 WorkRelationship brukes bare mellom verk

`WorkRelationship` brukes bare mellom `Work` og `Work`.

Det brukes ikke for relasjoner mellom:
- `Expression`
- `Manifestation`
- `Item`


### 13.2 Relasjonen er retningsbestemt

Ved registrering må det tas stilling til:
- hva som er `source_work`
- hva som er `target_work`
- hvilken `relation_type` som uttrykker forholdet best

Praksisen må være konsekvent slik at lignende tilfeller registreres på samme måte.


### 13.3 relation_type skal være kontrollert

`relation_type` skal være en stabil lokal kode.

Den skal brukes konsekvent og ikke erstattes av fritekstformuleringer i selve relasjonsfeltet.


### 13.4 Grensetilfeller må håndteres eksplisitt

Ved tvil om en relasjon bør uttrykkes som:
- adaptasjon
- inspirert av
- videreføring
- basert på
- annet vedtatt relasjonsforhold

skal vurderingen gjøres eksplisitt og konsekvent.

Databasen avgjør ikke alene hvilke tolkninger som er riktige.


---

## 14. Praktisk tommelfingerregel for nivåvalg

Bruk denne enkle testrekken når du er i tvil:

- Gjelder dette verkets innholdsmessige identitet?  
  → vurder `Work`

- Gjelder dette språk, realisering eller versjon av verket?  
  → vurder `Expression`

- Gjelder dette den publiserte utgaven eller formatet?  
  → vurder `Manifestation`

- Gjelder dette det konkrete eksemplaret i samlingen?  
  → vurder `Item`

Hvis svaret fortsatt er uklart, er det et modelleringsspørsmål som bør avklares før registrering fortsetter.