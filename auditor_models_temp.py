from core.data.model import *
from core.data.model.audit import *
from core.data.model.auth import *


'''
audit_answer        Answer
audit_auditdata     AuditData
audit_auditpoint    AuditPoint

# audit_point         Point
# audit_section       Section

# auth_group          Group

#auth_group<>permission     GroupPermission
# auth_location       Location
# auth_permission     Permission
# auth_user           User
# auth_user<>group    UserGroup
'''

__flush_order__ = (User, Group, UserGroup, Permission, GroupPermission,
                   Location, Section, Point, Answer, AuditData, AuditPoint)


def __sequence_dummy__(??):
    """Generate dummy records across all tables on the source server in
order to acquire the correct destination autoincr id sequence."""