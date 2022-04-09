from webargs import fields
"""Old version: changed automatically from R on 2022-04-08 17:23:46"""
#TestEndemGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
#TestExotGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
#TestThreatGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
#ListEndemGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
#ListExotGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
#ListThreatGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
#ListTaxGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
#TaxGetArgs={'canonicalname': fields.Str(required=False), 'cd_tax': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
#ListReferencesGetArgs={'format': fields.Str(required=False), 'onlyEndem': fields.Bool(required=False), 'onlyExot': fields.Bool(required=False), 'onlyThreat': fields.Bool(required=False)}
#ManageTaxoPostArgs={'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'rank': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
#ManageTaxoDeleteArgs={'cd_tax': fields.Int(required=True), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
#ManageTaxoPutArgs={'cd_tax': fields.Int(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'cd_ref': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'rank': fields.Str(required=False), 'reference': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'status': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
#ManageEndemPostArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
#ManageEndemDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
#ManageEndemPutArgs={'cd_tax': fields.Int(required=True), 'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
#ManageExotPostArgs={'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
#ManageExotDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
#ManageExotPutArgs={'cd_tax': fields.Int(required=True), 'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
#ManageThreatPostArgs={'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
#ManageThreatDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
#ManageThreatPutArgs={'cd_tax': fields.Int(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
#ManageRefPutArgs={'cd_ref': fields.Int(required=True), 'link': fields.List(fields.Str(),required=False), 'reference': fields.Str(required=False)}
#ManageRefDeleteArgs={'cd_ref': fields.Int(required=True), 'mergeInto': fields.Int(required=False)}
#CleanDbDeleteArgs={'ref_no_status': fields.Bool(required=False), 'status_no_ref': fields.Bool(required=False), 'syno_no_tax': fields.Bool(required=False), 'tax_no_status': fields.Bool(required=False)}
#PerformancePutArgs={'analysis': fields.Bool(required=True), 'vacuum': fields.Bool(required=True)}
#UserGetArgs={'create_token': fields.Bool(required=False)}
#UserPostArgs={'password': fields.Str(required=True), 'username': fields.Str(required=True)}
#UserDeleteArgs={}
#UserPutArgs={'newPassword': fields.Str(required=True)}
#AdminUsersGetArgs={'format': fields.Str(required=False)}
#AdminUsersDeleteArgs={'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
#AdminUsersPutArgs={'grant_admin': fields.Bool(required=False), 'grant_edit': fields.Bool(required=False), 'grant_user': fields.Bool(required=False), 'newPassword': fields.Str(required=False), 'revoke_admin': fields.Bool(required=False), 'revoke_edit': fields.Bool(required=False), 'revoke_user': fields.Bool(required=False), 'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
##Multiple versions:
#ListTestEndemGetArgs={'list':fields.List(fields.Nested(TestEndemGetArgs))}
#ListTestExotGetArgs={'list':fields.List(fields.Nested(TestExotGetArgs))}
#ListTestThreatGetArgs={'list':fields.List(fields.Nested(TestThreatGetArgs))}
#ListManageTaxoPostArgs={'list':fields.List(fields.Nested(ManageTaxoPostArgs))}
#ListManageTaxoPutArgs={'list':fields.List(fields.Nested(ManageTaxoPutArgs))}
#ListManageTaxoDeleteArgs={'list':fields.List(fields.Nested(ManageTaxoDeleteArgs))}
#ListManageExotPutArgs={'list':fields.List(fields.Nested(ManageExotPutArgs))}
#ListManageExotPostArgs={'list':fields.List(fields.Nested(ManageExotPostArgs))}
#ListManageExotDeleteArgs={'list':fields.List(fields.Nested(ManageExotDeleteArgs))}
#ListManageEndemPutArgs={'list':fields.List(fields.Nested(ManageEndemPutArgs))}
#ListManageEndemPostArgs={'list':fields.List(fields.Nested(ManageEndemPostArgs))}
#ListManageEndemDeleteArgs={'list':fields.List(fields.Nested(ManageEndemDeleteArgs))}
#ListManageThreatPutArgs={'list':fields.List(fields.Nested(ManageThreatPutArgs))}
#ListManageThreatPostArgs={'list':fields.List(fields.Nested(ManageThreatPostArgs))}
#ListManageThreatDeleteArgs={'list':fields.List(fields.Nested(ManageThreatDeleteArgs))}
TestEndemGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
TestExotGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
TestThreatGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ListEndemGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListExotGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListThreatGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListTaxGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
TaxGetArgs={'canonicalname': fields.Str(required=False), 'cd_tax': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ListReferencesGetArgs={'format': fields.Str(required=False), 'onlyEndem': fields.Bool(required=False), 'onlyExot': fields.Bool(required=False), 'onlyThreat': fields.Bool(required=False)}
ManageTaxoPostArgs={'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'min_gbif_conf': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'rank': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageTaxoDeleteArgs={'cd_tax': fields.Int(required=True), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ManageTaxoPutArgs={'cd_tax': fields.Int(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'cd_ref': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'min_gbif_conf': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'rank': fields.Str(required=False), 'reference': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'status': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageEndemPostArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'min_gbif_conf': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageEndemDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageEndemPutArgs={'cd_tax': fields.Int(required=True), 'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageExotPostArgs={'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'min_gbif_conf': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageExotDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageExotPutArgs={'cd_tax': fields.Int(required=True), 'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageThreatPostArgs={'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'min_gbif_conf': fields.Int(required=False), 'no_gbif': fields.Bool(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'rank': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageThreatDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageThreatPutArgs={'cd_tax': fields.Int(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageRefPutArgs={'cd_ref': fields.Int(required=True), 'link': fields.List(fields.Str(),required=False), 'reference': fields.Str(required=False)}
ManageRefDeleteArgs={'cd_ref': fields.Int(required=True), 'mergeInto': fields.Int(required=False)}
CleanDbDeleteArgs={'ref_no_status': fields.Bool(required=False), 'status_no_ref': fields.Bool(required=False), 'syno_no_tax': fields.Bool(required=False), 'tax_no_status': fields.Bool(required=False)}
PerformancePutArgs={'analysis': fields.Bool(required=True), 'vacuum': fields.Bool(required=True)}
UserGetArgs={'create_token': fields.Bool(required=False)}
UserPostArgs={'password': fields.Str(required=True), 'username': fields.Str(required=True)}
UserDeleteArgs={}
UserPutArgs={'newPassword': fields.Str(required=True)}
AdminUsersGetArgs={'format': fields.Str(required=False)}
AdminUsersDeleteArgs={'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
#Multiple versions:
ListTestEndemGetArgs={'list':fields.List(fields.Nested(TestEndemGetArgs))}
ListTestExotGetArgs={'list':fields.List(fields.Nested(TestExotGetArgs))}
ListTestThreatGetArgs={'list':fields.List(fields.Nested(TestThreatGetArgs))}
ListManageTaxoPostArgs={'list':fields.List(fields.Nested(ManageTaxoPostArgs))}
ListManageTaxoPutArgs={'list':fields.List(fields.Nested(ManageTaxoPutArgs))}
ListManageTaxoDeleteArgs={'list':fields.List(fields.Nested(ManageTaxoDeleteArgs))}
ListManageExotPutArgs={'list':fields.List(fields.Nested(ManageExotPutArgs))}
ListManageExotPostArgs={'list':fields.List(fields.Nested(ManageExotPostArgs))}
ListManageExotDeleteArgs={'list':fields.List(fields.Nested(ManageExotDeleteArgs))}
ListManageEndemPutArgs={'list':fields.List(fields.Nested(ManageEndemPutArgs))}
ListManageEndemPostArgs={'list':fields.List(fields.Nested(ManageEndemPostArgs))}
ListManageEndemDeleteArgs={'list':fields.List(fields.Nested(ManageEndemDeleteArgs))}
ListManageThreatPutArgs={'list':fields.List(fields.Nested(ManageThreatPutArgs))}
ListManageThreatPostArgs={'list':fields.List(fields.Nested(ManageThreatPostArgs))}
ListManageThreatDeleteArgs={'list':fields.List(fields.Nested(ManageThreatDeleteArgs))}
AdminUsersPutArgs={'grant_admin': fields.Bool(required=False), 'grant_edit': fields.Bool(required=False), 'grant_user': fields.Bool(required=False), 'newPassword': fields.Str(required=False), 'revoke_admin': fields.Bool(required=False), 'revoke_edit': fields.Bool(required=False), 'revoke_user': fields.Bool(required=False), 'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
