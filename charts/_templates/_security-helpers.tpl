{{- /*
Common RBAC and Security Context Templates
For use across all Deploy-System-Unified Helm charts
*/}}

{{/*
Create a ServiceAccount for the chart
Usage: {{ include "common.serviceAccount" (dict "context" . "component" "app") }}
*/}}
{{- define "common.serviceAccount" -}}
{{- $fullName := include "common.fullname" .context -}}
{{- $component := .component | default "default" -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ $fullName }}-{{ $component }}
  labels:
    app.kubernetes.io/name: {{ include "common.name" .context }}
    app.kubernetes.io/instance: {{ .context.Release.Name }}
    app.kubernetes.io/component: {{ $component }}
{{- end }}

{{/*
Create a minimal Role for pod operations
Usage: {{ include "common.role" (dict "context" . "component" "app" "rules" $rules) }}
*/}}
{{- define "common.role" -}}
{{- $fullName := include "common.fullname" .context -}}
{{- $component := .component | default "default" -}}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ $fullName }}-{{ $component }}
  labels:
    app.kubernetes.io/name: {{ include "common.name" .context }}
    app.kubernetes.io/instance: {{ .context.Release.Name }}
rules:
  {{- if .rules }}
  {{- toYaml .rules | nindent 2 }}
  {{- else }}
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
  {{- end }}
{{- end }}

{{/*
Create a RoleBinding to link ServiceAccount to Role
Usage: {{ include "common.roleBinding" (dict "context" . "component" "app") }}
*/}}
{{- define "common.roleBinding" -}}
{{- $fullName := include "common.fullname" .context -}}
{{- $component := .component | default "default" -}}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {{ $fullName }}-{{ $component }}
  labels:
    app.kubernetes.io/name: {{ include "common.name" .context }}
    app.kubernetes.io/instance: {{ .context.Release.Name }}
subjects:
  - kind: ServiceAccount
    name: {{ $fullName }}-{{ $component }}
    namespace: {{ .context.Release.Namespace }}
roleRef:
  kind: Role
  name: {{ $fullName }}-{{ $component }}
  apiGroup: rbac.authorization.k8s.io
{{- end }}

{{/*
Create a standard Pod securityContext
Usage: {{ include "common.podSecurityContext" . }}
*/}}
{{- define "common.podSecurityContext" -}}
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  fsGroupChangePolicy: "OnRootMismatch"
  seccompProfile:
    type: RuntimeDefault
{{- end }}

{{/*
Create a standard Container securityContext
Usage: {{ include "common.containerSecurityContext" (dict "readOnly" true "allowPrivilegeEscalation" false) }}
*/}}
{{- define "common.containerSecurityContext" -}}
{{- $readOnly := .readOnly | default false -}}
{{- $allowPrivilegeEscalation := .allowPrivilegeEscalation | default false -}}
securityContext:
  allowPrivilegeEscalation: {{ $allowPrivilegeEscalation }}
  readOnlyRootFilesystem: {{ $readOnly }}
  capabilities:
    drop:
      - ALL
{{- end }}

{{/*
Create a full security context block for a deployment
Usage: {{ include "common.fullSecurityContext" (dict "readOnly" false) }}
*/}}
{{- define "common.fullSecurityContext" -}}
# Pod-level security context
{{ include "common.podSecurityContext" . }}

# Container-level security context (to be included in each container)
# {{ include "common.containerSecurityContext" (dict "readOnly" .readOnly) }}
{{- end }}
