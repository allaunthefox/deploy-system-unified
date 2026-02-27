{{- /*
CRITICAL SECURITY VALIDATION
Fail deployment if passwords are not set
*/ -}}
{{- if and .Values.postgresql.enabled (empty .Values.postgresql.password) }}
{{- fail "SECURITY ERROR: postgresql.password is required and cannot be empty. Set it via values.yaml or --set postgresql.password=<secure-value>" }}
{{- end }}
{{- if and .Values.redis.enabled (empty .Values.redis.password) }}
{{- fail "SECURITY ERROR: redis.password is required and cannot be empty. Set it via values.yaml or --set redis.password=<secure-value>" }}
{{- end }}
{{- /*
END SECURITY VALIDATION
*/ -}}
