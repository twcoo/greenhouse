{{/*
Expand the name of the chart.
*/}}
{{- define "greenhouse.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully-qualified app name.
*/}}
{{- define "greenhouse.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Chart label.
*/}}
{{- define "greenhouse.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels shared across all resources.
*/}}
{{- define "greenhouse.labels" -}}
helm.sh/chart: {{ include "greenhouse.chart" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Selector labels.
Usage: include "greenhouse.selectorLabels" (dict "root" . "component" "backend")
*/}}
{{- define "greenhouse.selectorLabels" -}}
app.kubernetes.io/name: {{ include "greenhouse.name" .root }}
app.kubernetes.io/instance: {{ .root.Release.Name }}
app.kubernetes.io/component: {{ .component }}
{{- end }}

{{/*
Build a fully-qualified image reference, honoring global.imageRegistry.
Usage: include "greenhouse.image" (dict "root" . "image" .Values.backend.image)
*/}}
{{- define "greenhouse.image" -}}
{{- $registry := .root.Values.global.imageRegistry | trimSuffix "/" }}
{{- if $registry }}
{{- printf "%s/%s:%s" $registry .image.repository .image.tag }}
{{- else }}
{{- printf "%s:%s" .image.repository .image.tag }}
{{- end }}
{{- end }}

{{/*
imagePullSecrets block for a specific component.
Usage: include "greenhouse.imagePullSecrets" (dict "secrets" .Values.backend.imagePullSecrets)
*/}}
{{- define "greenhouse.imagePullSecrets" -}}
{{- if .secrets }}
imagePullSecrets:
  {{- toYaml .secrets | nindent 2 }}
{{- end }}
{{- end }}
