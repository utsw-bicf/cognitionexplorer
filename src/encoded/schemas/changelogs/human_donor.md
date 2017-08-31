## Changelog for human_donor.json

### Schema version 10

* *fraternal_twin* and *identical_twin* fields were collapsed into *twin* field
* *twin_type* property was added to allow specification of the twin type if it is known, it requires *twin*
* *ethnicity* values are no longer free text but are selected from an enumerated list
* *life_stage* value 'postnatal' was removed and donors were collapsed into 'newborn'
* *life_stage* value 'fetal' were removed and donors were collapsed into 'embryonic'
* *children* property is now a calculated property using the parent fields of other objects. It should no longer be submitted

### Schema version 9

* *status* values "proposed" and "preliminary" were removed
* *status* and *dbxrefs* values are restricted to DCC access only
* *mutagen* property is restricted to model organisms only

### Schema version 8

* *alternate_accessions* now must match accession format, "ENCDO..." or "TSTDO..."
