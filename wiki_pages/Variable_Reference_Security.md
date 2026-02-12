# Variable_Reference_Security

## Security Variables

### `security/access`
- [`ssh_match_rules`](roles/security_access.md#sshmatchrules)
- [`access_admin_user`](roles/security_access.md#accessadminuser)
- [`access_admin_password_hash`](roles/security_access.md#accessadminpasswordhash)
- [`access_admin_password_enforce`](roles/security_access.md#accessadminpasswordenforce)
- [`access_admin_password_placeholders`](roles/security_access.md#accessadminpasswordplaceholders)

### `security/advanced`
- [`advanced_security_hardening_enabled`](roles/security_advanced.md#advancedsecurityhardeningenabled)
- [`ssh_randomize_port`](roles/security_advanced.md#sshrandomizeport)
- [`ssh_random_port_range_start`](roles/security_advanced.md#sshrandomportrangestart)
- [`ssh_random_port_range_end`](roles/security_advanced.md#sshrandomportrangeend)
- [`ssh_random_port_file_dest`](roles/security_advanced.md#sshrandomportfiledest)
- [`ssh_rsync_destination`](roles/security_advanced.md#sshrsyncdestination)
- [`ssh_key_rotation_enabled`](roles/security_advanced.md#sshkeyrotationenabled)
- [`ssh_key_rotation_interval_days`](roles/security_advanced.md#sshkeyrotationintervaldays)
- [`tmux_session_for_deployment`](roles/security_advanced.md#tmuxsessionfordeployment)
- [`tmux_session_name`](roles/security_advanced.md#tmuxsessionname)
- [`encryption_method`](roles/security_advanced.md#encryptionmethod)

### `security/audit_integrity`
- *No variables defined in defaults/main.yml*

### `security/file_integrity`
- *No variables defined in defaults/main.yml*

### `security/firejail`
- [`firejail_enable_gpu`](roles/security_firejail.md#firejailenablegpu)

### `security/hardening`
- [`security_hardening_enabled`](roles/security_hardening.md#securityhardeningenabled)
- [`security_enable_ufw`](roles/security_hardening.md#securityenableufw)
- [`security_enable_fail2ban`](roles/security_hardening.md#securityenablefail2ban)
- [`security_enable_auto_updates`](roles/security_hardening.md#securityenableautoupdates)
- [`security_kernel_hardening`](roles/security_hardening.md#securitykernelhardening)

### `security/hardware_isolation`
- [`hardware_isolation_iommu_enabled`](roles/security_hardware_isolation.md#hardwareisolationiommuenabled)
- [`hardware_isolation_iommu_vendor`](roles/security_hardware_isolation.md#hardwareisolationiommuvendor)
- [`hardware_isolation_iommu_pt`](roles/security_hardware_isolation.md#hardwareisolationiommupt)
- [`hardware_isolation_dma_protection_enabled`](roles/security_hardware_isolation.md#hardwareisolationdmaprotectionenabled)
- [`hardware_isolation_blacklist_modules`](roles/security_hardware_isolation.md#hardwareisolationblacklistmodules)
- [`hardware_isolation_acs_override`](roles/security_hardware_isolation.md#hardwareisolationacsoverride)

### `security/ips`
- [`ips_fail2ban_sshd_maxretry`](roles/security_ips.md#ipsfail2bansshdmaxretry)
- [`ips_fail2ban_sshd_bantime`](roles/security_ips.md#ipsfail2bansshdbantime)
- [`ips_fail2ban_sshd_findtime`](roles/security_ips.md#ipsfail2bansshdfindtime)
- [`ips_fail2ban_sshd_enabled`](roles/security_ips.md#ipsfail2bansshdenabled)
- [`ips_fail2ban_caddy_enabled`](roles/security_ips.md#ipsfail2bancaddyenabled)
- [`ips_fail2ban_caddy_maxretry`](roles/security_ips.md#ipsfail2bancaddymaxretry)
- [`ips_fail2ban_caddy_bantime`](roles/security_ips.md#ipsfail2bancaddybantime)

### `security/kernel`
- [`kernel_profile`](roles/security_kernel.md#kernelprofile)
- [`kernel_enable_iommu`](roles/security_kernel.md#kernelenableiommu)
- [`kernel_restrict_dma`](roles/security_kernel.md#kernelrestrictdma)
- [`kernel_hugepages_enabled`](roles/security_kernel.md#kernelhugepagesenabled)

### `security/mac_apparmor`
- *No variables defined in defaults/main.yml*

### `security/resource_protection`
- [`resource_min_ram_mb`](roles/security_resource_protection.md#resourceminrammb)
- [`resource_default_tasks_max`](roles/security_resource_protection.md#resourcedefaulttasksmax)
- [`resource_default_memory_max`](roles/security_resource_protection.md#resourcedefaultmemorymax)

### `security/sandboxing`
- [`sandboxing_enabled`](roles/security_sandboxing.md#sandboxingenabled)
- [`sandboxing_install_bubblewrap`](roles/security_sandboxing.md#sandboxinginstallbubblewrap)
- [`sandboxing_policy_dir`](roles/security_sandboxing.md#sandboxingpolicydir)
- [`sandboxing_use_seccomp`](roles/security_sandboxing.md#sandboxinguseseccomp)
- [`sandboxing_use_landlock`](roles/security_sandboxing.md#sandboxinguselandlock)
- [`sandboxing_profiles`](roles/security_sandboxing.md#sandboxingprofiles)

### `security/scanning`
- [`security_scanning_enable`](roles/security_scanning.md#securityscanningenable)
- [`security_scanning_install_tools`](roles/security_scanning.md#securityscanninginstalltools)
- [`security_package_mapping`](roles/security_scanning.md#securitypackagemapping)
- [`security_scanning_extra_packages`](roles/security_scanning.md#securityscanningextrapackages)
- [`security_scanning_optional_tools`](roles/security_scanning.md#securityscanningoptionaltools)
- [`security_scanning_critical_tools`](roles/security_scanning.md#securityscanningcriticaltools)
- [`security_scanning_rkhunter_warning_threshold`](roles/security_scanning.md#securityscanningrkhunterwarningthreshold)
- [`security_scanning_aide_change_threshold`](roles/security_scanning.md#securityscanningaidechangethreshold)
- [`security_scanning_lynis_issue_threshold`](roles/security_scanning.md#securityscanninglynisissuethreshold)
- [`security_scanning_checkov_issue_threshold`](roles/security_scanning.md#securityscanningcheckovissuethreshold)

### `security/sshd`
- [`sshd_backup_config`](roles/security_sshd.md#sshdbackupconfig)
- [`sshd_disable_weak_keys`](roles/security_sshd.md#sshddisableweakkeys)
- [`sshd_use_strong_ciphers`](roles/security_sshd.md#sshdusestrongciphers)
- [`sshd_allow_tcp_forwarding`](roles/security_sshd.md#sshdallowtcpforwarding)
- [`sshd_allow_agent_forwarding`](roles/security_sshd.md#sshdallowagentforwarding)
- [`sshd_allow_x11_forwarding`](roles/security_sshd.md#sshdallowx11forwarding)
- [`sshd_permit_root_login`](roles/security_sshd.md#sshdpermitrootlogin)
- [`sshd_password_authentication`](roles/security_sshd.md#sshdpasswordauthentication)
- [`sshd_config_path`](roles/security_sshd.md#sshdconfigpath)
- [`sshd_enable_trusted_group_exceptions`](roles/security_sshd.md#sshdenabletrustedgroupexceptions)
- [`sshd_trusted_groups`](roles/security_sshd.md#sshdtrustedgroups)

