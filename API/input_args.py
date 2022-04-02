from webargs import fields
#"""Old version: changed automatically from R on 2022-04-01 19:37:49"""
#getListArgs = {'childrenOf':fields.Str(required=False),'format':fields.Str(required=False)}
#
#getListRefArgs = {'format':fields.Str(required=False), 'onlyEndem':fields.Bool(required=False),'onlyExot':fields.Bool(required=False),'onlyThreat':fields.Bool(required=False)}
#
#taxReconArgs = {'cd_tax': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False), 'canonicalname': fields.Str(required=False)}
#
#taxInputArgs = {'gbifkey':fields.Int(required=False), 'scientificname':fields.Str(required=False), 'canonicalname':fields.Str(required=False), 'authorship':fields.Str(required=False), 'syno':fields.Bool(required=False), 'rank': fields.Str(required=False), 'parentgbifkey':fields.Int(required=False), 'parentcanonicalname':fields.Str(required=False), 'parentscientificname':fields.Str(required=False), 'synogbifkey':fields.Int(required=False), 'synocanonicalname':fields.Str(required=False), 'synoscientificname':fields.Str(required=False) }
#
## TODO: check, for link, how to authorize some of the element of a list to be None and how to force the link and ref_citation to be of the same size
#
#newUserArgs = {'username':fields.Str(required=False), 'password':fields.Str(required=False)}
#
#modifyUserAdminArgs={'grant_user':fields.Bool(required=False),'grant_edit':fields.Bool(required=False),'grant_admin':fields.Bool(required=False),'revoke_user':fields.Bool(required=False),'revoke_edit':fields.Bool(required=False),'revoke_admin':fields.Bool(required=False),'newPassword':fields.Str(required=False)}
#modifyUserAdminArgs.update(newUserArgs)
#
#modifyPw={'newPassword':fields.Str(required=True)}
#
#inputThreatArgs={'threatstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
#inputThreatArgs.update(taxInputArgs)
#
#
#inputEndemArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(), required = False), 'comments': fields.Str(required=False)}
#inputEndemArgs.update(taxInputArgs)
#
#inputExotArgs={'is_alien':fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'occ_observed': fields.Bool(required=False),'cryptogenic': fields.Bool(required=False), 'ref_citation':fields.List(fields.Str(),required=True), 'link': fields.List(fields.Str(),required=False), 'comments': fields.Str(required=False)}
#inputExotArgs.update(taxInputArgs)
TestEndemGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
TestExotGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
TestThreatGetArgs={'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ListEndemGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListExotGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListThreatGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
ListTaxGetArgs={'childrenOf': fields.Str(required=False), 'format': fields.Str(required=False)}
TaxGetArgs={'canonicalname': fields.Str(required=False), 'cd_tax': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ListReferencesGetArgs={'onlyEndem': fields.Bool(required=False), 'onlyExot': fields.Bool(required=False), 'onlyThreat': fields.Bool(required=False)}
ManageTaxoPostArgs={'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageTaxoDeleteArgs={'cd_tax': fields.Int(required=True), 'canonicalname': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'scientificname': fields.Str(required=False)}
ManageTaxoPutArgs={'cd_tax': fields.Int(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'cd_ref': fields.Int(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'reference': fields.Str(required=False), 'scientificname': fields.Str(required=False), 'status': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageEndemPostArgs={'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageEndemDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageEndemPutArgs={'cd_tax': fields.Int(required=True), 'endemstatus': fields.Str(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageExotPostArgs={'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageExotDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageExotPutArgs={'cd_tax': fields.Int(required=True), 'is_alien': fields.Bool(required=True), 'is_invasive': fields.Bool(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageThreatPostArgs={'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'authorship': fields.Str(required=False), 'canonicalname': fields.Str(required=False), 'comments': fields.Str(required=False), 'gbifkey': fields.Int(required=False), 'link': fields.List(fields.Str(),required=False), 'parentcanonicalname': fields.Str(required=False), 'parentgbifkey': fields.Int(required=False), 'parentscientificname': fields.Str(required=False), 'priority': fields.Str(required=False), 'replace_comment': fields.Bool(required=False), 'scientificname': fields.Str(required=False), 'syno': fields.Bool(required=False), 'synocanonicalname': fields.Str(required=False), 'synogbifkey': fields.Int(required=False), 'synoscientificname': fields.Str(required=False)}
ManageThreatDeleteArgs={'cd_tax': fields.Int(required=True), 'cd_ref': fields.Int(required=False), 'delete_status': fields.Bool(required=False)}
ManageThreatPutArgs={'cd_tax': fields.Int(required=True), 'ref_citation': fields.List(fields.Str(),required=True), 'threatstatus': fields.Str(required=True), 'comments': fields.Str(required=False), 'link': fields.List(fields.Str(),required=False), 'replace_comment': fields.Bool(required=False)}
ManageRefPutArgs={'cd_ref': fields.Int(required=True), 'link': fields.List(fields.Str(),required=False), 'reference': fields.Str(required=False)}
ManageRefDeleteArgs={'cd_ref': fields.Int(required=True),'mergeInto': fields.Int(required=False)}
CleanDbDeleteArgs={'ref_no_status': fields.Bool(required=False), 'status_no_ref': fields.Bool(required=False), 'syno_no_tax': fields.Bool(required=False), 'tax_no_status': fields.Bool(required=False)}
PerformancePutArgs={'analysis': fields.Bool(required=True), 'vacuum': fields.Bool(required=True)}
UserGetArgs={'create_token': fields.Bool(required=False)}
UserPostArgs={'password': fields.Str(required=True), 'username': fields.Str(required=True)}
UserDeleteArgs={}
UserPutArgs={'newPassword': fields.Str(required=True)}
AdminUsersGetArgs={'format': fields.Str(required=False)}
AdminUsersDeleteArgs={'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
AdminUsersPutArgs={'grant_admin': fields.Bool(required=False), 'grant_edit': fields.Bool(required=False), 'grant_user': fields.Bool(required=False), 'newPassword': fields.Str(required=False), 'revoke_admin': fields.Bool(required=False), 'revoke_edit': fields.Bool(required=False), 'revoke_user': fields.Bool(required=False), 'uid': fields.Int(required=False), 'username': fields.Str(required=False)}
