# VARIABLE_REFERENCE_Security

## Security Variables

### `security/access`
- [`ssh_match_rules`](security_access#sshmatchrules)
- [`access_admin_user`](security_access#accessadminuser)
- [`access_admin_password_hash`](security_access#accessadminpasswordhash)
- [`access_admin_password_enforce`](security_access#accessadminpasswordenforce)
- [`access_admin_password_placeholders`](security_access#accessadminpasswordplaceholders)

### `security/advanced`
- [`advanced_security_hardening_enabled`](security_advanced#advancedsecurityhardeningenabled)
- [`ssh_randomize_port`](security_advanced#sshrandomizeport)
- [`ssh_random_port_range_start`](security_advanced#sshrandomportrangestart)
- [`ssh_random_port_range_end`](security_advanced#sshrandomportrangeend)
- [`ssh_random_port_file_dest`](security_advanced#sshrandomportfiledest)
- [`ssh_rsync_destination`](security_advanced#sshrsyncdestination)
- [`ssh_key_rotation_enabled`](security_advanced#sshkeyrotationenabled)
- [`ssh_key_rotation_interval_days`](security_advanced#sshkeyrotationintervaldays)
- [`tmux_session_for_deployment`](security_advanced#tmuxsessionfordeployment)
- [`tmux_session_name`](security_advanced#tmuxsessionname)
- [`encryption_method`](security_advanced#encryptionmethod)

### `security/audit_integrity`
- [`security_audit_integrity_store_keys`](security_audit_integrity#securityauditintegritystorekeys)
- [`security_audit_integrity_output_dir`](security_audit_integrity#securityauditintegrityoutputdir)
- [`security_audit_integrity_vault_encrypt_id`](security_audit_integrity#securityauditintegrityvaultencryptid)

### `security/file_integrity`
- *No variables defined in defaults/main.yml*

### `security/firejail`
- [`firejail_enable_gpu`](security_firejail#firejailenablegpu)

### `security/hardening`
- [`security_hardening_enabled`](security_hardening#securityhardeningenabled)
- [`security_enable_ufw`](security_hardening#securityenableufw)
- [`security_enable_fail2ban`](security_hardening#securityenablefail2ban)
- [`security_enable_auto_updates`](security_hardening#securityenableautoupdates)
- [`security_kernel_hardening`](security_hardening#securitykernelhardening)

### `security/hardware_isolation`
- [`hardware_isolation_iommu_enabled`](security_hardware_isolation#hardwareisolationiommuenabled)
- [`hardware_isolation_iommu_vendor`](security_hardware_isolation#hardwareisolationiommuvendor)
- [`hardware_isolation_iommu_pt`](security_hardware_isolation#hardwareisolationiommupt)
- [`hardware_isolation_dma_protection_enabled`](security_hardware_isolation#hardwareisolationdmaprotectionenabled)
- [`hardware_isolation_blacklist_modules`](security_hardware_isolation#hardwareisolationblacklistmodules)
- [`hardware_isolation_acs_override`](security_hardware_isolation#hardwareisolationacsoverride)

### `security/ips`
- [`ips_fail2ban_sshd_maxretry`](security_ips#ipsfail2bansshdmaxretry)
- [`ips_fail2ban_sshd_bantime`](security_ips#ipsfail2bansshdbantime)
- [`ips_fail2ban_sshd_findtime`](security_ips#ipsfail2bansshdfindtime)
- [`ips_fail2ban_sshd_enabled`](security_ips#ipsfail2bansshdenabled)
- [`ips_fail2ban_caddy_enabled`](security_ips#ipsfail2bancaddyenabled)
- [`ips_fail2ban_caddy_maxretry`](security_ips#ipsfail2bancaddymaxretry)
- [`ips_fail2ban_caddy_bantime`](security_ips#ipsfail2bancaddybantime)

### `security/kernel`
- [`kernel_profile`](security_kernel#kernelprofile)
- [`kernel_enable_iommu`](security_kernel#kernelenableiommu)
- [`kernel_restrict_dma`](security_kernel#kernelrestrictdma)
- [`kernel_hugepages_enabled`](security_kernel#kernelhugepagesenabled)

### `security/mac_apparmor`
- *No variables defined in defaults/main.yml*

### `security/resource_protection`
- [`resource_min_ram_mb`](security_resource_protection#resourceminrammb)
- [`resource_default_tasks_max`](security_resource_protection#resourcedefaulttasksmax)
- [`resource_default_memory_max`](security_resource_protection#resourcedefaultmemorymax)

### `security/sandboxing`
- [`sandboxing_enabled`](security_sandboxing#sandboxingenabled)
- [`sandboxing_install_bubblewrap`](security_sandboxing#sandboxinginstallbubblewrap)
- [`sandboxing_policy_dir`](security_sandboxing#sandboxingpolicydir)
- [`sandboxing_use_seccomp`](security_sandboxing#sandboxinguseseccomp)
- [`sandboxing_use_landlock`](security_sandboxing#sandboxinguselandlock)
- [`sandboxing_profiles`](security_sandboxing#sandboxingprofiles)

### `security/scanning`
- [`security_scanning_enable`](security_scanning#securityscanningenable)
- [`security_scanning_install_tools`](security_scanning#securityscanninginstalltools)
- [`security_package_mapping`](security_scanning#securitypackagemapping)
- [`security_scanning_extra_packages`](security_scanning#securityscanningextrapackages)
- [`security_scanning_optional_tools`](security_scanning#securityscanningoptionaltools)
- [`security_scanning_critical_tools`](security_scanning#securityscanningcriticaltools)
- [`security_scanning_rkhunter_warning_threshold`](security_scanning#securityscanningrkhunterwarningthreshold)
- [`security_scanning_aide_change_threshold`](security_scanning#securityscanningaidechangethreshold)
- [`security_scanning_lynis_issue_threshold`](security_scanning#securityscanninglynisissuethreshold)
- [`security_scanning_checkov_issue_threshold`](security_scanning#securityscanningcheckovissuethreshold)

### `security/sshd`
- [`security_sshd_backup_config`](security_sshd#securitysshdbackupconfig)
- [`security_sshd_disable_weak_keys`](security_sshd#securitysshddisableweakkeys)
- [`security_sshd_use_strong_ciphers`](security_sshd#securitysshdusestrongciphers)
- [`security_sshd_allow_tcp_forwarding`](security_sshd#securitysshdallowtcpforwarding)
- [`security_sshd_allow_agent_forwarding`](security_sshd#securitysshdallowagentforwarding)
- [`security_sshd_allow_x11_forwarding`](security_sshd#securitysshdallowx11forwarding)
- [`security_sshd_permit_root_login`](security_sshd#securitysshdpermitrootlogin)
- [`security_sshd_password_authentication`](security_sshd#securitysshdpasswordauthentication)
- [`security_sshd_config_path`](security_sshd#securitysshdconfigpath)
- [`security_sshd_enable_trusted_group_exceptions`](security_sshd#securitysshdenabletrustedgroupexceptions)
- [`security_sshd_trusted_groups`](security_sshd#securitysshdtrustedgroups)

