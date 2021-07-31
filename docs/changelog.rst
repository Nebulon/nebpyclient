Change Log
==========

A log of changes by version and date.

Version 1.0.1
-------------

Version 1.0.1 has no externally visible changes on top of version 1.0.0.

Version 1.0.2
-------------

Version 1.0.2 has no externally visible changes on top of version 1.0.1.

Version 1.0.3
-------------

Version 1.0.3 has no externally visible changes on top of version 1.0.3.

Version 1.0.6
-------------

Version 1.0.6 includes the following externally visible 
changes on top of version 1.0.3.

Changed Classes
~~~~~~~~~~~~~~~

TokenResponse Changes
#####################

The following changes were made to the ``TokenResponse`` class.

- Property ``must_send_target_dns`` was introduced.

Version 1.0.7
-------------

Version 1.0.7 includes the following externally visible 
changes on top of version 1.0.6.

Changed Classes
~~~~~~~~~~~~~~~

SupportCase Changes
###################

The following changes were made to the ``SupportCase`` class.

- Property ``alert_id`` was introduced.

Version 1.0.8
-------------

Version 1.0.8 has no externally visible changes on top of version 1.0.7.

Version 1.0.10
--------------

Version 1.0.10 includes the following externally visible 
changes on top of version 1.0.8.

Changed Classes
~~~~~~~~~~~~~~~

SupportCaseAttachment Changes
#############################

The following changes were made to the ``SupportCaseAttachment`` class.

- Property ``file_link`` was retired.

Version 1.0.11
--------------

Version 1.0.11 includes the following externally visible 
changes on top of version 1.0.10.

Changed Classes
~~~~~~~~~~~~~~~

NebPyClient Changes
###################

The following changes were made to the ``NebPyClient`` class.

- Function ``set_ntp_servers`` was retired.
- Function ``shutdown_spu`` was retired.

Version 1.0.13
--------------

Version 1.0.13 includes the following externally visible 
changes on top of version 1.0.11.

Changed Classes
~~~~~~~~~~~~~~~

NebPyClient Changes
###################

The following changes were made to the ``NebPyClient`` class.

- Function ``update_volume`` was retired.

New Classes
~~~~~~~~~~~

The following classes were introduced in this version. Some
are replacements of previously retired classes. Please review
the API reference for details.

- Class ``UpdateVolumeInput`` was introduced.

Version 2.0.1
-------------

Version 2.0.1 includes the following externally visible 
changes on top of version 1.0.13.

Enumerations
~~~~~~~~~~~~
- Property ``Recovery`` was retired in enum ``NebPackageType``.
- Property ``Lab`` was retired in enum ``ResourceType``.
- Enumeration ``SnapConsistencyLevel`` was retired.

Changed Classes
~~~~~~~~~~~~~~~

Alert Changes
#############

The following changes were made to the ``Alert`` class.

- Property ``id`` was retired.
- Property ``action_operation`` was introduced.
- Property ``action_params`` was introduced.
- Property ``event_id`` was introduced.
- Property ``incident_id`` was introduced.
AuditLogEntry Changes
#####################

The following changes were made to the ``AuditLogEntry`` class.

- Property ``component_name`` was introduced.

AuditLogFilter Changes
######################

The following changes were made to the ``AuditLogFilter`` class.

- Property ``user_uuid`` was introduced.

CreateNPodTemplateInput Changes
###############################

The following changes were made to the ``CreateNPodTemplateInput`` class.

- Property ``shared_volume`` was retired.
- Property ``shared_lun`` was introduced.
- Function ``__init__`` changed from

  ``name, saving_factor, mirrored_volume, boot_volume, os, volume_size_bytes, shared_volume, boot_volume_size_bytes, boot_image_url, app, note, snapshot_schedule_template_uuids, volume_count`` to

  ``name, saving_factor, mirrored_volume, boot_volume, os, volume_size_bytes, shared_lun, boot_volume_size_bytes, boot_image_url, app, note, snapshot_schedule_template_uuids, volume_count``

CreateSupportCaseInput Changes
##############################

The following changes were made to the ``CreateSupportCaseInput`` class.

- Property ``resource_type_other`` was introduced.

DeleteKeyValueInput Changes
###########################

The following changes were made to the ``DeleteKeyValueInput`` class.

- Property ``npod_group_uuid`` was retired.
- Property ``npod_uuid`` was introduced.
- Function ``__init__`` changed from

  ``resource_type, npod_group_uuid, resource_uuid, key`` to

  ``resource_type, npod_uuid, resource_uuid, key``

GraphQLParam Changes
####################

The following changes were made to the ``GraphQLParam`` class.

- Property ``no_log`` was introduced.

HostFilter Changes
##################

The following changes were made to the ``HostFilter`` class.

- Property ``npod_uuid`` was introduced.

IPInfoState Changes
###################

The following changes were made to the ``IPInfoState`` class.

- Property ``display_interface_names`` was introduced.
- Property ``link_active`` was introduced.

KeyValueFilter Changes
######################

The following changes were made to the ``KeyValueFilter`` class.

- Property ``npod_group_uuid`` was retired.
- Property ``npod_uuid`` was introduced.
- Function ``__init__`` changed from

  ``resource_type, npod_group_uuid, resource_uuid, key`` to

  ``resource_type, npod_uuid, resource_uuid, key``

LoginResults Changes
####################

The following changes were made to the ``LoginResults`` class.

- Property ``change_password`` was introduced.
- Property ``need_two_factor_authentication`` was introduced.

NPod Changes
############

The following changes were made to the ``NPod`` class.

- Property ``creation_time`` was introduced.
- Property ``recommended_package`` was introduced.

NPodFilter Changes
##################

The following changes were made to the ``NPodFilter`` class.

- Property ``npod_base_template_uuid`` was introduced.
- Property ``npod_group_uuid`` was introduced.
- Property ``npod_template_uuid`` was introduced.
- Property ``spu_serial`` was introduced.

NPodTemplateFilter Changes
##########################

The following changes were made to the ``NPodTemplateFilter`` class.

- Property ``only_last_version`` was introduced.

NebPyClient Changes
###################

The following changes were made to the ``NebPyClient`` class.

- Function ``abort_spu_firmware`` was retired.
- Function ``get_npod_group_count`` was retired.
- Function ``get_update_packages`` was retired.
- Function ``get_user_group_count`` was retired.
- Function ``get_users_count`` was retired.
- Function ``send_npod_debug_info`` was retired.
- Function ``send_spu_debug_info`` was retired.
- Function ``abort_update_spu_firmware`` was retired.
- Function ``cancel_custom_diagnostics`` was retired.
- Function ``cancel_support_case_attachment`` was retired.
- Function ``collect_debug_info`` was retired.
- Function ``delete_support_case_attachment`` was retired.
- Function ``get_audit_log`` was retired.
- Function ``get_available_packages`` was retired.
- Function ``create_clone`` changed from

  ``name, volume_uuid`` to

  ``create_clone_input``

- Function ``create_datacenter`` changed from

  ``name, address, contacts, note`` to

  ``create_input``

- Function ``create_lun`` changed from

  ``volume_uuid, lun_id, host_uuids, spu_serials, local`` to

  ``lun_input``

- Function ``create_npod`` changed from

  ``name, npod_group_uuid, spus, npod_template_uuid, note, timezone, ignore_warnings`` to

  ``create_npod_input, ignore_warnings``

- Function ``create_npod_group`` changed from

  ``name, note`` to

  ``create_npod_group_input``

- Function ``create_npod_template`` changed from

  ``name, saving_factor, mirrored_volume, boot_volume, os, volume_size_bytes, shared_volume, boot_volume_size_bytes, boot_image_url, app, note, snapshot_schedule_template_uuids, volume_count`` to

  ``create_npod_template_input``

- Function ``create_rack`` changed from

  ``name, row_uuid, note, location`` to

  ``create_rack_input``

- Function ``create_rbac_policy`` changed from

  ``role_uuid, scopes`` to

  ``create_rbac_policy_input``

- Function ``create_rbac_role`` changed from

  ``name, description, rights`` to

  ``create_rbac_role_input``

- Function ``create_room`` changed from

  ``datacenter_uuid, name, note, location`` to

  ``create_room_input``

- Function ``create_row`` changed from

  ``name, room_uuid, note, location`` to

  ``create_row_input``

- Function ``create_snapshot_schedule_template`` changed from

  ``name, name_pattern, schedule, expiration_seconds, retention_seconds, ignore_boot_volumes`` to

  ``create_template_input``

- Function ``create_support_case`` changed from

  ``subject, description, priority, issue_type, spu_serial, resource_type, resource_id`` to

  ``create_input``

- Function ``create_user`` changed from

  ``name, password, email, user_group_uuid, first_name, last_name, note, mobile_phone, business_phone, inactive, policy_uuids, send_notification, time_zone`` to

  ``create_user_input``

- Function ``create_user_group`` changed from

  ``name, policy_uuids, note`` to

  ``create_user_group_input``

- Function ``create_volume`` changed from

  ``name, size_bytes, npod_uuid, mirrored, owner_spu_serial, backup_spu_serial, force, ignore_warnings`` to

  ``create_volume_input``

- Function ``create_webhook`` changed from

  ``definition`` to

  ``create_webhook_input``

- Function ``delete_datacenter`` changed from

  ``uuid, cascade`` to

  ``uuid, delete_input``

- Function ``delete_key_value`` changed from

  ``resource_type, npod_group_uuid, resource_uuid, key`` to

  ``delete_key_value_input``

- Function ``delete_luns`` changed from

  ``volume_uuid, lun_uuids, host_uuids`` to

  ``batch_delete_lun_input``

- Function ``delete_room`` changed from

  ``uuid, cascade`` to

  ``uuid, delete_room_input``

- Function ``delete_row`` changed from

  ``uuid, cascade`` to

  ``uuid, delete_row_input``

- Function ``get_hosts`` changed from

  ``page, h_filter, sort`` to

  ``page, host_filter, sort``

- Function ``get_key_values`` changed from

  ``kv_filter`` to

  ``key_value_filter``

- Function ``get_npod_recipes`` changed from

  ``npod_uuid, recipe_uuid, completed`` to

  ``npod_recipe_filter``

- Function ``get_physical_drive_updates`` changed from

  ``page, pd_filter, sort`` to

  ``page, pd_updates_filter, sort``

- Function ``get_user_groups`` changed from

  ``page, ug_filter, sort`` to

  ``page, user_group_filter, sort``

- Function ``get_webhooks`` changed from

  ``page, wh_filter, sort`` to

  ``page, webhook_filter, sort``

- Function ``locate_physical_drive`` changed from

  ``wwn, duration_seconds`` to

  ``locate_pd_input``

- Function ``replace_spu`` changed from

  ``npod_uuid, previous_spu_serial, new_spu_info, sset_uuid`` to

  ``replace_spu_input``

- Function ``set_key_value`` changed from

  ``resource_type, npod_group_uuid, resource_uuid, key, value`` to

  ``upsert_key_value_input``

- Function ``set_npod_timezone`` changed from

  ``uuid, timezone`` to

  ``uuid, set_npod_timezone_input``

- Function ``set_vsphere_credentials`` changed from

  ``npod_uuid, username, password, url`` to

  ``npod_uuid, credentials_input``

- Function ``test_webhook`` changed from

  ``uuid, create, update`` to

  ``test_webhook_input``

- Function ``update_datacenter`` changed from

  ``uuid, name, address, contacts, note`` to

  ``uuid, update_input``

- Function ``update_host`` changed from

  ``uuid, name, rack_uuid, note`` to

  ``uuid, host_input``

- Function ``update_npod_group`` changed from

  ``uuid, name, note`` to

  ``uuid, update_npod_group_input``

- Function ``update_npod_template`` changed from

  ``name, volume_size_bytes, saving_factor, mirrored_volume, shared_volume, boot_volume, boot_volume_size_bytes, boot_image_url, os, app, note, snapshot_schedule_template_uuids, volume_count`` to

  ``update_npod_template_input``

- Function ``update_physical_drive_firmware`` changed from

  ``accept_eula, npod_uuid, spu_serial`` to

  ``update_pd_firmware_input``

- Function ``update_rack`` changed from

  ``uuid, row_uuid, name, note, location`` to

  ``uuid, update_rack_input``

- Function ``update_rbac_policy`` changed from

  ``uuid, scopes`` to

  ``uuid, update_rbac_policy_input``

- Function ``update_rbac_role`` changed from

  ``uuid, name, description, rights`` to

  ``uuid, update_rbac_role_input``

- Function ``update_room`` changed from

  ``uuid, name, note, location`` to

  ``uuid, update_room_input``

- Function ``update_row`` changed from

  ``uuid, room_uuid, name, note, location`` to

  ``uuid, update_row_input``

- Function ``update_snapshot_schedule_template`` changed from

  ``uuid, name, name_pattern, schedule, expiration_seconds, retention_seconds, ignore_boot_volumes`` to

  ``uuid, update_template_input``

- Function ``update_support_case`` changed from

  ``case_number, subject, description, priority, status, contact_user_uuid, improvement_suggestion, comment`` to

  ``case_number, update_input``

- Function ``update_user`` changed from

  ``uuid, name, password, note, email, user_group_uuids, first_name, last_name, mobile_phone, business_phone, inactive, policy_uuids, send_notification, time_zone`` to

  ``uuid, update_user_input``

- Function ``update_user_group`` changed from

  ``uuid, name, policy_uuids, note`` to

  ``uuid, update_user_group_input``

- Function ``update_volume`` changed from

  ``uuid, update_input`` to

  ``uuid, update_volume_input``

- Function ``update_webhook`` changed from

  ``uuid, updates`` to

  ``uuid, update_webhook_input``

PackageInfo Changes
###################

The following changes were made to the ``PackageInfo`` class.

- Property ``package_deprecated`` was retired.
- Property ``release_unix`` was retired.
- Property ``lts_version`` was introduced.
- Property ``offline`` was introduced.
- Property ``release_date`` was introduced.
- Property ``support_state`` was introduced.

PhysicalDrive Changes
#####################

The following changes were made to the ``PhysicalDrive`` class.

- Property ``state_display`` was retired.
- Property ``update_failure`` was introduced.

PhysicalDriveFilter Changes
###########################

The following changes were made to the ``PhysicalDriveFilter`` class.

- Property ``spu_serial`` was introduced.

PhysicalDriveUpdate Changes
###########################

The following changes were made to the ``PhysicalDriveUpdate`` class.

- Property ``eula_url`` was introduced.

RBACPolicySort Changes
######################

The following changes were made to the ``RBACPolicySort`` class.

- Property ``name`` was retired.
- Property ``role_name`` was introduced.
- Function ``__init__`` changed from

  ``name`` to

  ``role_name``

ReplaceSpuInput Changes
#######################

The following changes were made to the ``ReplaceSpuInput`` class.

- Property ``npod_uuid`` was retired.
- Property ``sset_uuid`` was retired.
- Function ``__init__`` changed from

  ``npod_uuid, previous_spu_serial, new_spu_info, sset_uuid`` to

  ``previous_spu_serial, new_spu_info``

Spu Changes
###########

The following changes were made to the ``Spu`` class.

- Property ``lun_uuids`` was retired.
- Property ``physical_drive_wwns`` was retired.
- Property ``recovery_version`` was introduced.
- Property ``version_package_names`` was introduced.

SpuFilter Changes
#################

The following changes were made to the ``SpuFilter`` class.

- Property ``host_ioc_wwn`` was introduced.
- Property ``npod_uuid`` was introduced.
- Property ``storage_ioc_wwn`` was introduced.

SupportCase Changes
###################

The following changes were made to the ``SupportCase`` class.

- Property ``origin`` was introduced.
- Property ``resource_name`` was introduced.
- Property ``resource_type_other`` was introduced.

SupportCaseFilter Changes
#########################

The following changes were made to the ``SupportCaseFilter`` class.

- Property ``contact_uuid`` was retired.
- Property ``contact_id`` was introduced.
- Property ``resource_type`` was introduced.
- Property ``resource_type_other`` was introduced.
- Function ``__init__`` changed from

  ``number, status, issue_type, contact_uuid`` to

  ``number, status, issue_type, contact_id, resource_type, resource_type_other``

UpdateNPodTemplateInput Changes
###############################

The following changes were made to the ``UpdateNPodTemplateInput`` class.

- Property ``shared_volume`` was retired.
- Property ``shared_lun`` was introduced.
- Function ``__init__`` changed from

  ``name, volume_size_bytes, saving_factor, mirrored_volume, shared_volume, boot_volume, boot_volume_size_bytes, boot_image_url, os, app, note, snapshot_schedule_template_uuids, volume_count`` to

  ``name, volume_size_bytes, saving_factor, mirrored_volume, shared_lun, boot_volume, boot_volume_size_bytes, boot_image_url, os, app, note, snapshot_schedule_template_uuids, volume_count``

UpdateRoomInput Changes
#######################

The following changes were made to the ``UpdateRoomInput`` class.

- Property ``datacenter_uuid`` was introduced.

UpdateStateSpu Changes
######################

The following changes were made to the ``UpdateStateSpu`` class.

- Property ``waiting_for_scheduled`` was introduced.

UpdateUserGroupInput Changes
############################

The following changes were made to the ``UpdateUserGroupInput`` class.

- Property ``user_uuids`` was introduced.

UpsertKeyValueInput Changes
###########################

The following changes were made to the ``UpsertKeyValueInput`` class.

- Property ``npod_group_uuid`` was retired.
- Property ``npod_uuid`` was introduced.
- Function ``__init__`` changed from

  ``resource_type, npod_group_uuid, resource_uuid, key, value`` to

  ``resource_type, npod_uuid, resource_uuid, key, value``

UpsertVsphereCredentialsInput Changes
#####################################

The following changes were made to the ``UpsertVsphereCredentialsInput`` class.

- Property ``enable_vmhost_affinity`` was introduced.

User Changes
############

The following changes were made to the ``User`` class.

- Property ``change_password_reason`` was introduced.

UserFilter Changes
##################

The following changes were made to the ``UserFilter`` class.

- Property ``inactive`` was introduced.

UserGroup Changes
#################

The following changes were made to the ``UserGroup`` class.

- Property ``custom`` was introduced.

Volume Changes
##############

The following changes were made to the ``Volume`` class.

- Property ``lun_uuids`` was retired.
- Property ``snapshot_uuids`` was retired.

VolumeFilter Changes
####################

The following changes were made to the ``VolumeFilter`` class.

- Property ``natural_backup_spu_serial`` was introduced.
- Property ``natural_owner_spu_serial`` was introduced.
- Property ``parent_name`` was introduced.
- Property ``sync_state`` was introduced.

VsphereCredentials Changes
##########################

The following changes were made to the ``VsphereCredentials`` class.

- Property ``enable_vmhost_affinity`` was introduced.

Retired Classes
~~~~~~~~~~~~~~~

The following classes were removed in this version. Please
review the New Classes section for possible replacements.

- Class ``BatchDeleteLunInput`` was retired.
- Class ``CreateLunInput`` was retired.
- Class ``Dimm`` was retired.
- Class ``IntFilter`` was retired.
- Class ``Lun`` was retired.
- Class ``LunFilter`` was retired.
- Class ``LunList`` was retired.
- Class ``LunSort`` was retired.
- Class ``TokenResponse`` was retired.
- Class ``UpdatePackages`` was retired.
- Class ``UuidFilter`` was retired.

New Classes
~~~~~~~~~~~

The following classes were introduced in this version. Some
are replacements of previously retired classes. Please review
the API reference for details.

- Class ``AvailablePackagesFilter`` was introduced.
- Class ``AvailablePackagesSort`` was introduced.
- Class ``BatchDeleteLUNInput`` was introduced.
- Class ``CreateLUNInput`` was introduced.
- Class ``DIMM`` was introduced.
- Class ``DeleteSupportCaseAttachmentInput`` was introduced.
- Class ``DeleteVolumeInput`` was introduced.
- Class ``LUN`` was introduced.
- Class ``LUNFilter`` was introduced.
- Class ``LUNList`` was introduced.
- Class ``LUNSort`` was introduced.
- Class ``NPodRecommendedPackage`` was introduced.
- Class ``PackageInfoList`` was introduced.
- Class ``UUIDFilter`` was introduced.
