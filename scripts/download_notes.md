# Raw data downloads

`data/raw/` is gitignored. Fetch these into it before running the extract scripts.

## MHCLG statutory homelessness — detailed local authority tables

December quarter each year, saved as `TA_<yyyymm>.ods`. Filenames on gov.uk are inconsistent
between releases, so the current links are listed on the
[live tables on homelessness](https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness)
page. The ones used here:

| Save as | Source |
|---|---|
| `TA_201912.ods` | `DetailedLA_201912_revised.ods` |
| `TA_202012.ods` | `DetailedLA_202012_Revised_updated.ods` |
| `TA_202112.ods` | `Detailed_LA_202112_revised.ods` |
| `TA_202212.ods` | `Detailed_LA_202212_revised.ods` |
| `TA_202312.ods` | `Detailed_LA_202312_Revised_No_Dropdowns.ods` |
| `TA_202412.ods` | `Statutory_Homelessness_Detailed_Local_Authority_Data_202412_revised.ods` |
| `TA_202512.ods` | `Statutory_Homelessness_Detailed_Local_Authority_Data_202512.ods` |

## GLA London Plan Annual Monitoring Report 21

```bash
curl -L -o data/raw/AMR21_Housing.xlsx \
  "https://data.london.gov.uk/download/2rjko/0yx/AMR%2021%20Chapter%202%20Housing%20Tables.xlsx"
```
