# """RIS reader for Talbot"""
# from typing import Optional
# from ..utils import compact, normalize_url
# from ..date_utils import get_date_from_parts
# from ..doi_utils import normalize_doi, doi_from_url
# from ..constants import (
#     RIS_TO_CP_TRANSLATIONS,
#     RIS_TO_DC_TRANSLATIONS,
#     RIS_TO_SO_TRANSLATIONS,
#     TalbotMeta
# )


# def read_ris(data: Optional[str], **kwargs) -> TalbotMeta:
#     """read_ris"""

#     #         read_options = ActiveSupport::HashWithIndifferentAccess.
#     # new(options.except(:doi, :id, :url,
#     # :sandbox, :validate, :ra))

#     meta = ris_meta(data=data)

#     read_options = kwargs or {}

#     if not isinstance(meta, dict):
#         return {"meta": None, "state": "not_found"}

#     ris_type = meta.get("TY", None) or "GEN"
#     schema_org = RIS_TO_SO_TRANSLATIONS.get(ris_type, None) or "CreativeWork"
#     types = compact(
#         {
#             "resourceTypeGeneral": RIS_TO_DC_TRANSLATIONS.get(ris_type, None),
#             "schemaOrg": schema_org,
#             "citeproc": RIS_TO_CP_TRANSLATIONS.get(schema_org, None) or "misc",
#             "ris": ris_type,
#         }
#     )

#     pid = normalize_doi(meta.get("DO", None))  # options[:doi] or

#     # author = wrap(meta.get('AU', None)).map {| a | { 'creatorName' = > a } }

#     date_parts = str(meta.get("PY", None)).split("/")
#     created_date_parts = str(meta.get("Y1", None)).split("/")
#     dates = []
#     if meta.get("PY", None) is not None:
#         dates.append({"date": get_date_from_parts(
#             *date_parts), "dateType": "Issued"})
#     if meta.get("Y1", None) is not None:
#         dates.append(
#             {"date": get_date_from_parts(
#                 *created_date_parts), "dateType": "Created"}
#         )
#     # publication_year = get_date_from_parts(*date_parts).to_s[0..3]

#     # related_identifiers = if meta.fetch('T2', nil).present? & & meta.fetch('SN', nil).present?
#     #                             [{'type' = > 'Periodical',
#     #                                'id'= > meta.fetch('SN', nil),
#     #                                'relatedIdentifierType'= > 'ISSN',
#     #                                'relationType'= > 'IsPartOf',
#     #                                'title' = > meta.fetch('T2', nil)}.compact]
#     #                           else
#     #                             []
#     #                           end
#     if meta.get("T2", None) is not None:
#         container = compact(
#             {
#                 "type": "Journal",
#                 "title": meta.get("T2", None),
#                 "identifier": meta.get("SN", None),
#                 "volume": meta.get("VL", None),
#                 "issue": meta.get("IS", None),
#                 "firstPage": meta.get("SP", None),
#                 "lastPage": meta.get("EP", None),
#             }
#         )
#     else:
#         container = None

#     state = "findable" if meta.get("DO", None) or read_options else "not_found"
#     # subjects = Array.wrap(meta.fetch('KW', nil)).reduce([]) do |sum, subject|
#     #   sum += name_to_fos(subject)

#     #   sum
#     # end

#     return {
#         "pid": pid,
#         "types": types,
#         "doi": doi_from_url(pid),
#         "url": normalize_url(meta.get("UR", None)),
#         'titles': None, # meta.get('T1', nil).present? ? [{ 'title': meta.fetch('T1', nil) }] : nil,
#         'creators': None, #get_authors(author),
#         "publisher": meta.get("PB", "(:unav)"),
#         'publication_year': None, # publication_year,
#         "container": container,
#         # 'related_identifiers': related_identifiers,
#         "dates": dates,
#         # 'descriptions': if meta.fetch('AB', nil).present?
#         #                       [{ 'description': sanitize(meta.fetch('AB')),
#         #                          'descriptionType': 'Abstract' }]
#         #                     end,
#         # 'subjects': subjects,
#         "language": meta.get("LA", None),
#         "state": state,
#     }  # .merge(read_options)


# def ris_meta(data):
#     """ris_meta"""
#     meta = {}
#     if data is None:
#         return meta
#     for line in data.split("\n"):
#         key, value = line.split("-", 1)
#         key = key.strip()
#         value = value.strip()
#         meta[key] = value
#     return compact(meta)


# #         h = Hash.new { |h, k| h[k] = [] }
# #         string.split("\n").each_with_object(h) do |line, _sum|
# #           k, v = line.split('-', 2)
# #           h[k.strip] << v.to_s.strip
# #         end.transform_values(&:unwrap).compact
